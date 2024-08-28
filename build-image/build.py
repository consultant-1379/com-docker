#!/usr/bin/python

import argparse
import sys
import os
import docker
import git
import getpass
import urlparse
from pwd import getpwnam
from cirpa.utils.imageconf import ImageConf


parser = argparse.ArgumentParser(description='Build images')

arguments = parser.add_argument_group('')

arguments.add_argument('-f', '--dockerfile', action="store", dest="dockerfile", default=False, required=True,
                       help="Name of Dockerfile to build")

arguments.add_argument('-t', '--tag', action="store", dest="tag", default=False, required=False,
                       help="The tag of the image, default is the HEAD's commit hash of the current git branch")

arguments.add_argument('-u', '--user', action="store", dest="user", default=False, required=True,
                       help="The username for creating the local image and to login to the remote registry")

arguments.add_argument('-a', '--apikey', action="store", dest="apiKey", default=None, required=False,
                       help="The generated apikey for the registry supplied by Artifactory")

arguments.add_argument('--push', const='default', dest="registry", nargs='?', required=False,
                       help="The registry URL including the registry name, default is armdocker.rnd.ericsson.se/cba-com")

arguments.add_argument('--nocache', action="store_true", dest="nocache", default=False,
                       required=False, help="Rebuild the image not using any cache")

arguments.add_argument('--imageconf', action="store", dest="config",
                       required=False, help="image config path")

arguments.add_argument('--imageid', action="store", dest="imageid",
                       required=False, help="image id to use when accessing the image config in the start scripts")

arguments.add_argument('--build-args', dest="buildArgs", nargs='*', required=False,
                       help="Set build-time variables to be used in dockerfile")

args = parser.parse_args()

registryUrl = None

if args.registry == 'default':
    registryUrl = "armdocker.rnd.ericsson.se/cba-com"
elif args.registry is not None:
    registryUrl = args.registry.strip()

args.dockerfile = args.dockerfile.strip()

args.user = args.user.strip()

# get commit hash and repository remote url
workdir = os.getcwd()
repo = git.Repo(path=workdir)

repository = repo.remote().urls
for u in repository:
    repository = urlparse.urlparse(u)
    if repository.scheme.startswith('ssh'):
        repository = repository.scheme + '://' + repository.netloc.split('@')[-1] + repository.path
    else:
        repository = 'ssh://' + repository.netloc.split('@')[-1] + ':29418/' + '/'.join(repository.path.split('/')[2::])
    break

# get current commit hash
head = repo.head.commit
commit = head.hexsha[:8]

# set tag to commit if not supplied by argument --tag
if not args.tag:
    args.tag = commit
else:
    args.tag = args.tag.strip()

# set docker filename and file path  supplied by argument --dockerfile
# docker file path should be relative to the repository name(e.g: com-docker)
if args.dockerfile.find("/") == -1:
    fullPath = os.getcwd()
    fileName = args.dockerfile
else:
    data = args.dockerfile.rsplit('/', 1)
    fullPath = os.getcwd() + "/" + data[0]
    fileName = data[1]

#
# construct image name
#

# remove "Dockerfile." and replace all "~" with "/"
imageName = fileName.replace("Dockerfile.", "").replace("~", "/")

# replace the first "." from the right with "/"
imageName = "/".join(imageName.rsplit(".", 1))

#
# construct the staging name
#
stagingName = args.user + "/" + imageName + ":" + args.tag

#
# handling the Image conf
#
imageConfig = None
if args.config:
    if args.imageid:
        id = args.imageid

        imageConfig = ImageConf(args.config)

        url = None
        if registryUrl:
            url = registryUrl
        else:
            url = args.user

        imageConfig.add_image(id, name=imageName, tag=args.tag, registry=url)
    else:
        print("Error, the argument '--imageid' is needed when using '--imageconf'")
        sys.exit(1)

else:
    print("no image config will be generated")

#
# pull image without build
#
if args.tag == "stable":
    with docker.APIClient(base_url='unix://var/run/docker.sock', version="auto") as cli:
     for line in cli.pull(
            registryUrl + "/" + imageName,
            tag="latest",
            stream=True
     ):
        # printing build stream log
        def printDict(d):
            if type(d) == dict:
                for k, v in d.items():
                    printDict(v)
            else:
                try:
                    sys.stdout.write(str(d))
                except:
                    pass  # we need to take care of the non printable strings somehow

        printDict(line)

else:
    # build image
    print("building image: {}".format(stagingName))
    # use APIClient only for building images
    with docker.APIClient(base_url='unix://var/run/docker.sock', version="auto") as cli:
        for line in cli.build(
                decode=True,
                pull=True,
                nocache=args.nocache,
                tag=stagingName,
                dockerfile=fileName,
                path=fullPath,
                buildargs={"COMMIT": commit, "REPOSITORY": repository,
                           "ci_user": args.user, "ci_password": args.apiKey,
                           "admin_user": args.buildArgs[0], "admin_password": args.buildArgs[1]}
        ):
            # printing build stream log
            def printDict(d):
                if type(d) == dict:
                    for k, v in d.items():
                        printDict(v)
                else:
                    try:
                        sys.stdout.write(str(d))
                    except:
                        pass  # we need to take care of the non printable strings somehow

            printDict(line)

# getting the image info
client = docker.from_env(version="auto")
if args.tag == "stable":
    image = client.images.get(registryUrl + "/" + imageName)
else:
    image = client.images.get(stagingName)
print registryUrl

# pushing the image
if registryUrl:
    print "pushing image to " + registryUrl

    image.tag(registryUrl + "/" + imageName, tag=args.tag)

    username = args.user.strip()
    print "username: " + username
    if args.apiKey:
        password = args.apiKey
    else:
        password = getpass.getpass()

    result = client.login(registry=registryUrl, username=username, password=password)

    if "Succeeded" in result['Status']:
        print "Pushing image: " + registryUrl + "/" + imageName + ":" + args.tag
        for output in client.images.push(registryUrl + "/" + imageName, tag=args.tag, stream=True):
            sys.stdout.write('.')
            sys.stdout.flush()
        print "Done"
    else:
        print "Error when logging in"
        sys.exit(1)

else:
    print stagingName


# save the image config to disk with the supplied users user id and group id
if args.imageid:
    uid = getpwnam(args.user).pw_uid
    gid = getpwnam(args.user).pw_gid

    # set the uid and gid to args.user
    os.setegid(gid)
    os.seteuid(uid)

    imageConfig.save()

    # set the uid and gid back to root
    os.setegid(0)
    os.seteuid(0)
