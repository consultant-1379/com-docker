import subprocess, os

from cirpa.utils.docker import Docker
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.utils.dockerutility import save_container_id
from cirpa.startbase import StartBase
from cirpa.hasharguments import RegExp, Optional


class MafTest(StartBase):

    def arguments(self, parser):
        parser.add_argument('--os', dest="os", type=RegExp)
        parser.add_argument('--repo', dest="repo", type=RegExp)
        parser.add_argument('--buildtype', dest="buildType", type=RegExp)
        parser.add_argument('--maf-version', dest="mafVersion", type=Optional)
        parser.add_argument('--local-src', dest="localSrc", type=Optional)
        parser.add_argument('--valgrind', dest="valgrind", type=Optional)
        parser.add_argument('--commit', dest="commit", type=RegExp )

    def __init__(self):
        self.add_argument("commit", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("os", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("mafVersion", Optional(""))
        self.add_argument("buildType",  RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("repo", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("valgrind", Optional(""))
        self.add_argument("localSrc", Optional(""))

        # name of the docker image to use
        self._imageName = None
        self._fileDestination = "."
        self._buildDir = "/src/maf-main/build"
        self._filesToCopy = ["/src/maf-main/gen/"]
        # running containers hash id
        self.__containerId = None

        self._mirror = ["-v", "/repo/jenkins/local-mirrors/:/mirrors/:ro"]

    # this function should not be overriden unless a totally new way to spawn build is needed
    def _runBuild(self, buildParams, args):
        _returnValue = 0
        extraRunParams = []
        if args["os"] == 'sles12sp2':
           self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
        elif args["os"] == 'sles12':
           self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
        if args["os"] == 'sles12sp5':
           self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
        if args["os"] == 'sles12sp5gcc10':
           self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
        if args["os"] == 'sles12sp5gcc10dx':
           self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"

        if self._imageName is not None:

            # check if image exists, if not try to pull the image from the repo
            # todo! we need a readonly user so that we can do pull safe

            try:
                if args["localSrc"]:
                    self._mirror = ["-v", args["localSrc"] + ":/localsrc/:ro"]
                    buildParams += ["--local-src", "/localsrc"]

                extraRunParams = self._mirror

                if args["mafVersion"]:
                    buildParams += ["--maf-version", args["mafVersion"]]

                if args["valgrind"]:
                    buildParams += ["--valgrind", args["valgrind"]]

                # add constraint
                if args["buildType"] == "functiontest":
                   extraRunParams += ["-e", "constraint:type==integrationtest"]
                else:
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

                print "id: " + self.__containerId
                save_container_id(self.__containerId)

            except subprocess.CalledProcessError as e:
                print e.cmd
                print e.output
                _returnValue = 1
            else:
                try:
                    # Follow the logs of the container and wait for it to complete
                    docker.logs(self.__containerId)

                    # Get the exit code of the container
                    _returnValue = int(docker.getExitCode(self.__containerId).strip())

                except KeyboardInterrupt:
                    # this just catches the ctrl+c and so that our clean up will run.
                    print ""
                    print "we got a ctrl+c lets clean up and exit"
                    _returnValue = 1
                else:
                    print "succesfully built"
                    # copy files from container
                    #
                    # follow the cp rules in the docker documents
                    # https://docs.docker.com/engine/reference/commandline/cp/
                    #
                    print "now copying files..."

                    try:
                       os.mkdir(self._fileDestination)
                    except OSError:
                        print self._fileDestination + " already created!"

                    for src in self._filesToCopy:
                        # join workdir with src
                        src = os.path.join(self._buildDir, src)

                        # copy files
                        retval = docker.cp_from(self.__containerId, src, self._fileDestination)
                        if (retval > 0):
                            print "error when trying to copy: " + src + " to " + self._fileDestination
                            _returnValue = retval

                # cleanup
                try:
                    print "cleaning up"
                    res = docker.rm(self.__containerId)
                    print "deleted: " + res

                except subprocess.CalledProcessError as e:
                    print e.cmd
                    print e.output

        # exit the runBuild with the return value from the build
        return _returnValue

    def execute(self, args):
        print "Starting the MAF Test"
        return self._runBuild(["maftest",
                               "--build-type", args["buildType"],
                               "--commit", args["commit"],
                               "--repo", args["repo"],
                               "--mirror-path", "/mirrors",
                               ], args)
