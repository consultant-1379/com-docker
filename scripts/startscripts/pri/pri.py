import subprocess
import re
import sys

from cirpa.startbase import StartBase
from cirpa.utils.docker import Docker
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.hasharguments import Optional, RegExp


class Pri(StartBase):

    # always needs a commit passed in
    def __init__(self):
        # commit id e.g. commit hash, branch name, tag or gerrit reference to a patchset

        # name of the docker image to use
        self._imageName = "armdocker.rnd.ericsson.se/cba-com/pri-generator:latest"

        # running containers hash id
        self.__containerId = None

        self._mvnrepo = ["-v", "/repo/jenkins/maven-repository/:/root/.m2/:rw"]
        self._mirror = ["-v", "/repo/jenkins/local-mirrors/:/mirrors/:ro"]

        self.add_argument("version", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("base", Optional(""))
        self.add_argument("password", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))

    # this function should not be overriden unless a totally new way to spawn build is needed
    def _generatePri(self, params):
        returnValue = 0
        if self._imageName is not None:

            # check if image exists, if not try to pull the image from the repo
            # todo! we need a readonly user so that we can do pull safe

            try:
                extraRunParams = self._mirror + self._mvnrepo

                # add constraint to run only on build nodes
                extraRunParams += ["-e", "constraint:type==build"]

                if DockerSwarm.isConsulRunning():
                    docker = DockerSwarm()
                else:
                    docker = Docker()

                # pull the image
                docker.pull(self._imageName)

                # start the container
                self.__containerId = docker.run(self._imageName, extraRunParams, params)

                # temporary workaround to parse container id from return value
                temp = self.__containerId.splitlines()
                try:
                    self.__containerId = temp[0].strip()
                except IndexError:
                    raise Exception('No container id returned')

                print "id: " + self.__containerId

            except subprocess.CalledProcessError as e:
                print e.cmd
                print e.output
                returnValue = 1
            else:
                try:
                    # Follow the logs of the container and wait for it to complete
                    docker.logs(self.__containerId)

                    # Get the exit code of the container
                    returnValue = int(docker.getExitCode(self.__containerId).strip())

                except KeyboardInterrupt:
                    # this just catches the ctrl+c and so that our clean up will run.
                    print ""
                    print "we got a ctrl+c lets clean up and exit"
                    returnValue = 1

                # cleanup
                try:
                    print "cleaning up"
                    res = docker.rm(self.__containerId)
                    print "deleted: " + res

                except subprocess.CalledProcessError as e:
                    print e.cmd
                    print e.output

        # exit the generatePri with the return value from the generator
        return returnValue

    def execute(self, args):

        if args["base"] is None:

            sVer = args["version"].split("-")
            semVersion = sVer[0]
            relVersion = int(sVer[1])
            semVersionSplit = semVersion.split(".")
            semVersionPatch = int(semVersionSplit[2])

            url = "https://x-ci.rnd.ki.sw.ericsson.se/xci/md2/builds/com.ericsson.cba.com_x86_64/com_x86_64/latest?confidenceLevels=\\[componentRelease=SUCCESS\\]"
            urlForGreenTrack = url + "&track=GreenTrack"
            curlCommand = ['curl', '-s']
            runCurlCommand = False

            if semVersionPatch > 1:
                 curlCommand.append(urlForGreenTrack)
                 runCurlCommand = True
            elif relVersion == 1:
                 curlCommand.append(url)
                 runCurlCommand = True

            if runCurlCommand:
               try:
                   pipe_result = subprocess.Popen(curlCommand , stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
                   result = pipe_result.communicate()[0]
                   matcher = re.search(r'\"version\":\"([\w\.\-]+)\"',result)
                   if matcher:
                       self._baseversion = matcher.group(1)
                       print ("Base version {}".format(self._baseversion))
                   else:
                       print ("Unable to determine previous git tag. Please re-run with two parameters as: --version <actual tag> --base <last tag in the previous project>")
                       sys.exit(1)
               except Exception as e:
                   print ("Popen execution failed {}".format(e))
                   raise
            else:
                prevRelVersion = relVersion - 1
                self._baseversion = "%s-%d" % (semVersion, prevRelVersion)
        else:
            self._baseversion = args["base"]

        # TODO after CIRPA delivery rename the arguments, use correct ones
        print "Starting the PRI Generator"
        return self._generatePri(["generatepri",
                                  "--version", args["version"],
                                  "--prevVersion", self._baseversion,
                                  "--password", args["password"],
                                  ])

    def arguments(self, parser):
        parser.add_argument('--version', dest="version", type=RegExp)
        parser.add_argument('--base', dest="base", type=Optional)
        parser.add_argument('--password', dest="password", type=RegExp)
