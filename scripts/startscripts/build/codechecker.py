import os
import subprocess

from cirpa.utils.docker import Docker
from cirpa.utils.dockerutility import save_container_id
from cirpa.utils.stringutils import StringUtils
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.startbase import StartBase
from cirpa.hasharguments import RegExp, Optional


class CodeChecker(StartBase):

    buildDir="/build/com-build"

    def arguments(self, parser):
        parser.add_argument('--repo', dest="repo")
        parser.add_argument('--compiler', dest="compiler")
        parser.add_argument('--os', dest="os")
        parser.add_argument('--commit', dest="commit", type=RegExp)
        parser.add_argument('--com-version', dest="comVersion", type=Optional)
        parser.add_argument('--localsrc', dest="localSrc", type=Optional)
        parser.add_argument('--gerrit-project', dest="gerritProject", type=Optional)
        parser.add_argument('--gerrit-patchset', dest="patchset", type=Optional)
        parser.add_argument('--branch', dest="branch", type=Optional)
        parser.add_argument('--gerrit-trigger', action="store", dest="gerritTrigger", choices=['trigger', 'review', 'push'], type=Optional)
        parser.add_argument('--gerrit-branch', action="store", dest="gerritBranch", type=Optional)
        parser.add_argument('--com-branch', action="store", dest="comBranch", type=Optional)
        parser.add_argument('--vault-pass', action="store", dest="vaultPass", type=Optional)
        parser.add_argument('--base-code', action="store", dest="baseCode", type=Optional)
        parser.add_argument('--username', action="store", dest="username", type=RegExp)
        parser.add_argument('--password', action="store", dest="password", type=RegExp)
        parser.add_argument('--maf-latest', action="store", dest="mafLatest",
                            choices=['yes', 'true', 't', 'y', '1', 'no', 'false', 'f', 'n', '0'], type=Optional, help="Accepts Boolean values")

    def set_path(self, os, repo, compiler):
        self.add_argument("repo", repo)
        self.add_argument("os", os)
        self.add_argument("compiler", compiler)
        self.add_argument("commit", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("comVersion", Optional(""))
        self.add_argument("localSrc", Optional(""))
        self.add_argument("gerritProject", Optional(""))
        self.add_argument("patchset", Optional(""))
        self.add_argument("branch", Optional(""))
        self.add_argument("gerritTrigger", Optional(""))
        self.add_argument("gerritBranch", Optional(""))
        self.add_argument("comBranch", Optional(""))
        self.add_argument('vaultPass', Optional(""))
        self.add_argument('baseCode', Optional(""))
        self.add_argument('username', RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument('password', RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument('mafLatest', Optional(""))

    # always needs a commit passed in
    def __init__(self):

        # to make sure the test package have the same folder structure we need to set the build-dir to /build/com-build
        self.__builddir = self.buildDir

        # name of the docker image to use
        self._imageName = self.image

        # this is a list of files e.g ["/dist", "/logs/build.log"]
        self._filesToCopy = ["/reports"]

        # destination where all the files should be copied
        self._fileDestination = "."

        # running containers hash id
        self.__containerId = None

        self._mvnrepo = ["-v", "/repo/jenkins/maven-repository/:/root/.m2/:rw"]
        self._mirror = ["-v", "/repo/jenkins/local-mirrors/:/mirrors/:ro"]

        self.__cmakeConfig = []

        self.set_path(self.os, self.repo, self.compiler)

    # this function should not be overriden unless a totally new way to spawn build is needed
    def _runBuild(self, buildParams, args):
        returnValue = 0
        if self._imageName is not None:

            # check if image exists, if not try to pull the image from the repo
            # todo! we need a readonly user so that we can do pull safe

            try:
                if args["localSrc"] is not None:
                    self._mirror = ["-v", args["localSrc"] + ":/localsrc/:ro"]
                    buildParams += ["--local-src", "/localsrc"]

                extraRunParams = self._mirror + self._mvnrepo

                if args["comVersion"] is not None:
                    buildParams += ["--com-version", args["comVersion"]]

                if args["baseCode"] is not None:
                    buildParams += ["--base-code", args["baseCode"]]

                if args["gerritProject"] is not None:
                    buildParams += ["--gerrit-project", args["gerritProject"]]

                if args["patchset"] is not None:
                    buildParams += ["--gerrit-patchset", args["patchset"]]

                if args["branch"] is not None:
                    buildParams += ["--branch", args["branch"]]

                if args["gerritTrigger"] is not None:
                    buildParams += ["--gerrit-trigger", args["gerritTrigger"]]

                if args["gerritBranch"] is not None:
                    buildParams += ["--gerrit-branch", args["gerritBranch"]]

                if args["comBranch"] is not None:
                    buildParams += ["--com-branch", args["comBranch"]]

                if args["mafLatest"] is not None:
                    stringutils = StringUtils()
                    if stringutils.str2bool(args["mafLatest"]) is True:
                        buildParams += ["--maf-latest"]

                # add volume for vault password
                if args["vaultPass"] is not None:
                    mountVaultPass = ["-v", "/home/cbacomci/.vault_pass:/root/.vault_pass"]
                    extraRunParams += mountVaultPass
                    buildParams += ["--vault-pass", args["vaultPass"]]

                # add constraint to run only on build nodes
                extraRunParams += ["-e", "constraint:type==build"]

                if DockerSwarm.isConsulRunning():
                    docker = DockerSwarm()
                else:
                    docker = Docker()

                # pull the image
                docker.pull(self._imageName)

                # start the container
                self.__containerId = docker.run(self._imageName, extraRunParams, buildParams)

                # temporary workaround to parse container id from return value
                temp = self.__containerId.splitlines()
                try:
                    self.__containerId = temp[0].strip()
                except IndexError:
                    raise Exception('No container id returned')

                print ("id: {}".format(self.__containerId))
                save_container_id(self.__containerId)

            except subprocess.CalledProcessError as e:
                print ("".format(e.cmd))
                print ("".format(e.output))
                returnValue = 1
            else:
                try:
                    # Follow the logs of the container and wait for it to complete
                    docker.logs(self.__containerId)

                    # Get the exit code of the container
                    returnValue = int(docker.getExitCode(self.__containerId).strip())

                except KeyboardInterrupt:
                    # this just catches the ctrl+c and so that our clean up will run.
                    print ("")
                    print ("we got a ctrl+c lets clean up and exit")
                    returnValue = 1
                else:
                    # copy files from container
                    #
                    # follow the cp rules in the docker documents
                    # https://docs.docker.com/engine/reference/commandline/cp/
                    #
                    print ("successfully built, now copying files...")
                    dest = self._fileDestination
                    try:
                        os.mkdir(dest)
                    except OSError:
                        print ("{} aleady created".format(dest))

                    for src in self._filesToCopy:
                        copyReturnValue = docker.cp_from(self.__containerId, src, dest)
                        if (copyReturnValue > 0):
                            print ("error when trying to copy: {0} to {1}".format(src, dest))
                            returnValue = copyReturnValue
                        # Remove the files in reports directory, that are irrelavant
                        else:
                            reportsPath = os.path.join(os.getcwd(), "reports")
                            filelist = [files for files in os.listdir(reportsPath) if not files.endswith(".txt")]
                            for files in filelist:
                                filesPath = os.path.join(reportsPath, files)
                                if os.path.isfile(filesPath):
                                    os.remove(filesPath)
                # cleanup
                try:
                    print ("cleaning up")
                    res = docker.rm(self.__containerId)
                    print ("deleted: {}".format(res))

                except subprocess.CalledProcessError as e:
                    print ("{}".format(e.cmd))
                    print ("{}".format(e.output))

        # exit the runBuild with the return value from the build
        return returnValue

    def execute(self, args):
        print ("Starting the {} Build".format(self.name))
        return self._runBuild(["buildwithcodechecker",
                        "--commit", args["commit"],
                        "--repo", args["repo"],
                        "--build-type", self.target,
                        "--mirror-path", "/mirrors",
                        "--build-dir", self.__builddir,
                        "--username", args["username"],
                        "--password", args["password"],
                        ], args)
