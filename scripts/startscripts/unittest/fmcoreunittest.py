import os
import subprocess
import sys

from cirpa.utils.docker import Docker
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.startbase import StartBase
from cirpa.hasharguments import RegExp, Optional
from comlib.version import getVersion


class FmCoreUnitTest(StartBase):

    def arguments(self, parser):
        parser.add_argument('--compiler', dest="compiler")
        parser.add_argument('--os', dest="os")
        parser.add_argument('--fmcore-version', dest="fmcoreVersion", type=Optional)
        parser.add_argument('--test-filter', dest="testFilter", type=Optional)

    def set_path(self, os, compiler):
        self.add_argument("fmcoreVersion", Optional(""))
        self.add_argument("testFilter", Optional(""))
        self.add_argument("os", os)
        self.add_argument("compiler", compiler)

    # constructor
    # the test option is used to filter out just some specific unit test binaries, e.g. test="fm"
    def __init__(self):

        # name of the docker image to use
        self._imageName = None

        # name of the os to use
        self.os = None

        # name of the compiler to use
        self.compiler = None

        # this is a list of files e.g ["/dist","/logs/build.log"]
        self._filesToCopy = None

        # destination where all the files should be copied
        self._fileDestination = None

        # running containers hash id
        self._containerId = None

        self._workDir = "/workdir"

    # this function should not be overriden unless a totally new way to spawn build is needed
    def _runUnitTest(self, utParams, args):
        returnValue = 0
        distDir = "dist"
        if args["fmcoreVersion"]:
            fmcoreVersion = args["fmcoreVersion"]
        else:
            fmcoreVersion =  getVersion(distDir)
        # init default runtime package name ( this can be overriden )
        runtimePackageName = "fmcore-" + fmcoreVersion + "-x86_64-unittest-runtime.tar.gz"
        if self._imageName is not None:

            try:
                # check if the unit test package exists
                src = os.path.join(distDir, runtimePackageName)  # we need to get the correct path maybe by using glob and search for the file
                if not os.path.isfile(src):
                    print ("Error: file: {} does not exist".format(src))
                    sys.exit(1)  # just exit, no need for cleanup

                # setting up the options for the unittest script
                utParams += ["--package", runtimePackageName]
                utParams += ["--work-dir", self._workDir]

                if args["testFilter"] is not None:
                    utParams += ["--test", args["testFilter"]]

                # settings for valgrind or coverage unit test
                # Note: Fm-core doesn't have support to run ut with valgrind
                if args["compiler"] == "valgrind" or args["compiler"] == "coverage":
                    flagValue = "--" + args["compiler"]
                    testPackageName = "fmcore-" + fmcoreVersion + "-test.tar.gz"
                    fmCoreTestSrc = os.path.join(distDir, testPackageName)
                    if not os.path.isfile(fmCoreTestSrc):
                        print ("Error: file: {} does not exist".format(fmCoreTestSrc))
                        sys.exit(1)  # just exit, no need for cleanup
                    utParams += [flagValue, testPackageName]

                # add constraint to run only on build nodes
                utExtraParams = ["-e", "constraint:type==build"]

                # enable ipv6 routing for the container
                utExtraParams += ["--sysctl", "net.ipv6.conf.all.disable_ipv6=0"]

                if DockerSwarm.isConsulRunning():
                    docker = DockerSwarm()
                else:
                    docker = Docker()

                # pull the image
                docker.pull(self._imageName)

                # create the container
                self.__containerId = docker.create(self._imageName, utExtraParams, utParams)

                # temporary workaround to parse container id from return value
                temp = self.__containerId.splitlines()
                try:
                    self.__containerId = temp[0].strip()
                except IndexError:
                    raise Exception('No container id returned')

                print ("id: {}".format(self.__containerId))

                # copy the unittest runtime package to the correct location in the container
                dest = "/"
                docker.cp_to(self.__containerId, src, dest)

                # copy test package which contains the valgrind suppression file
                if args["compiler"] == "valgrind" or args["compiler"] == "coverage":
                    docker.cp_to(self.__containerId, fmCoreTestSrc, dest)

                # start the container
                self.__containerId = docker.start(self.__containerId)

                # temporary workaround to parse container id from return value
                temp = self.__containerId.splitlines()
                try:
                    self.__containerId = temp[0].strip()
                except IndexError:
                    raise Exception('No container id returned')

            except subprocess.CalledProcessError as e:
                print ("{}".format(e.cmd))
                print ("{}".format(e.output))
                returnValue = 1
            else:
                # wait for the test to finish
                try:
                    # Follow the logs of the container and wait for it to complete
                    docker.logs(self.__containerId)

                    # Get the exit code of the container
                    returnValue = int(docker.getExitCode(self.__containerId).strip())

                except KeyboardInterrupt:
                    # this just catches the ctrl+c and so that our clean up will run.
                    print ("")
                    print ("we got a ctrl+c lets clean up and exit")
                    returnValue = 1  # exit with error
                else:
                    # copy files from container
                    #
                    # follow the cp rules in the docker documents
                    # https://docs.docker.com/engine/reference/commandline/cp/
                    #
                    print ("now copying files...")

                    dest = self._fileDestination
                    try:
                        os.mkdir(dest)
                    except OSError:
                        print ("{} already created!".format(dest))

                    for src in self._filesToCopy:
                        # join workdir with src
                        src = os.path.join(self._workDir, src)

                        # copy files
                        retval = docker.cp_from(self.__containerId, src, dest)
                        if (retval > 0):
                            print ("Error when trying to copy: {} to {}".format(src, dest))
                            returnValue = retval

            # cleanup
            try:
                print ("cleaning up")
                res = docker.rm(self.__containerId)
                print ("deleted: {}".format(res))

            except subprocess.CalledProcessError as e:
                print e.cmd
                print e.output

        # exit the runBuild with the return value from the build
        return returnValue

    # this function will start the unittest execution based on the derived class instance
    def execute(self, args):

        print ("Starting the  {} {} unittest".format(self.os.upper(), self.compiler.upper()))
        return self._runUnitTest(["unittest"], args)
