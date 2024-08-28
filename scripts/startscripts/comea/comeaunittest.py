import subprocess, os

from cirpa.utils.docker import Docker
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.utils.dockerutility import save_container_id
from cirpa.startbase import StartBase
from cirpa.hasharguments import RegExp, Optional


class ComEaUnitTest(StartBase):

    def arguments(self, parser):
        parser.add_argument('--repo', dest="repo", type=RegExp)
        parser.add_argument('--commit', dest="commit", type=RegExp)
        parser.add_argument('--os', dest="os", type=RegExp)
        parser.add_argument('--com-version', dest="comVersion", type=Optional)
        parser.add_argument('--localsrc', dest="localsrc", type=Optional)
        parser.add_argument('--gerrit-project', dest="gerritProject", type=Optional)
        parser.add_argument('--gerrit-patchset', dest="patchset", type=Optional)
        parser.add_argument('--branch', dest="branch", type=Optional)
        parser.add_argument('--gerrit-trigger', action="store", dest="gerritTrigger", choices=['trigger', 'review', 'push'], type=Optional)
        parser.add_argument('--gerrit-branch', action="store", dest="gerritBranch", type=Optional)

    def __init__(self):

        self.add_argument("repo", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("commit", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("os", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("comVersion", Optional(""))
        self.add_argument("localsrc", Optional(""))
        self.add_argument("gerritProject", Optional(""))
        self.add_argument("patchset", Optional(""))
        self.add_argument("branch", Optional(""))
        self.add_argument("gerritTrigger", Optional(""))
        self.add_argument("gerritBranch", Optional(""))

        # name of the docker image to use
        self._imageName = None
        self._fileDestination = "."
        self._buildDir = "/build"
        self._filesToCopy = ["gen/comea/test-report"]
        # running containers hash id
        self.__containerId = None

        self._mvnrepo = ["-v", "/repo/jenkins/maven-repository/:/root/.m2/:rw"]
        self._mirror = ["-v", "/repo/jenkins/local-mirrors/:/mirrors/:ro"]

    # this function should not be overriden unless a totally new way to spawn build is needed
    def _runBuild(self, buildParams, args):
        _returnValue = 0

        if args["os"] in 'sles12sp2':
           self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
        elif args["os"] in 'sles12':
           self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
        elif args["os"] in 'sles12sp5':
           self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
        elif args["os"] in 'sles12sp5gcc10':
           self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
	elif args["os"] in 'sles12sp5gcc10dx':
           self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"

        if self._imageName is not None:

            # check if image exists, if not try to pull the image from the repo
            # todo! we need a readonly user so that we can do pull safe

            try:
                if args["localsrc"] is not None:
                    self._mirror = ["-v", args["localsrc"] + ":/localsrc/:ro"]
                    buildParams += ["--local-src", "/localsrc"]

                extraRunParams = self._mirror + self._mvnrepo

                if args["comVersion"] is not None:
                    buildParams += ["--com-version", args["comVersion"]]

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
        print "Starting the COMEA Unit Test"
        return self._runBuild(["comeaunittest",
                               "--commit", args["commit"],
                               "--repo", args["repo"],
                               "--mirror-path", "/mirrors",
                               ], args)
