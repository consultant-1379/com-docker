import os
import subprocess
import sys
import time

from cirpa.utils.docker import Docker
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.utils.dockerutility import save_container_id
from cirpa.startbase import StartBase
from cirpa.hasharguments import RegExp, Optional
from comlib.version import getVersion
from cirpa.utils.shellhelper import execute

class FunctionTest(StartBase):

    def arguments(self, parser):
        parser.add_argument('--suite', dest="suite", type=RegExp)
        parser.add_argument('--os', dest="os")
        parser.add_argument('--compiler', dest="compiler")
        parser.add_argument('--com-version', dest="comVersion", type=Optional)
        parser.add_argument('--openssl-version', dest="opensslVersion", choices=['1.0.1e'], type=Optional)
        parser.add_argument('--sut-ip', dest="sut-ip", type=Optional)
        parser.add_argument('--copy-to', dest="copy-to", default="/results", type=RegExp)

    def set_path(self, compiler, os):
        self.add_argument("suite", RegExp("^([a-z0-9]|_)+"))
        self.add_argument("os", os)
        self.add_argument("compiler", compiler)
        self.add_argument("comVersion", Optional(""))
        self.add_argument("sut-ip", Optional(""))
        self.add_argument("opensslVersion", Optional(""))
        self.add_argument("copy-to", RegExp("^.+"))

    # constructor
    # the test option is used to filter out just some specific unit test binaries, e.g. test="pm"
    def __init__(self):

        # commit id e.g. commit hash, branch name, tag or gerrit reference to a patchset
        self._commit = None

        # name of the docker images to use
        self._teImageName = None
        self._sutImageName = None

        # this is a list of files e.g ["/dist","/logs/build.log"]
        self._filesToCopy = None

        # running containers hash id
        self.__teContainerId = None
        self.__sutContainerId = None

        self._workDir = "/workdir"

    def _checkIfExists(self, filename):
        if not os.path.isfile(filename):
            print "file: " + filename + " does not exist"
            sys.exit(1)  # just exit, no need for cleanup

    # this function should not be overriden unless a totally new way to spawn build is needed
    def _run(self, params, args):
        returnValue = 0
        distDir = "dist/"

        if args["comVersion"]:
            comVersion = args["comVersion"]
        else:
            comVersion =  getVersion(distDir)

        runtimePackageName = "com-" + comVersion + "-runtime.tar.gz"
        testPackageName = "com-" + comVersion + "-test.tar.gz"
        sutIpAddress = args["sut-ip"]

        if self._teImageName:

            # openssl version check
            if args["opensslVersion"] == "1.0.1e":
                self._teImageName = "armdocker.rnd.ericsson.se/cba-com/sles11sp3/lsbopenssl/1.0.1e/build"

            try:
                # check if the package exists
                runtimePackage = os.path.join("dist", runtimePackageName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(runtimePackage)

                testPackage = os.path.join("dist", testPackageName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(testPackage)

                # check if there is an active Consul for Docker Swarm
                isConsulRunning = DockerSwarm.isConsulRunning()
                if isConsulRunning:
                    docker = DockerSwarm()
                else:
                    docker = Docker()

                if sutIpAddress is None and self._sutImageName:
                    print "No SUT is available, starting a new SUT container."

                    # adding support for using Fuse in the SUT
                    extraOptions = ["--cap-add", "SYS_ADMIN"]
                    extraOptions += ["--device", "/dev/fuse"]
                    extraOptions += ["--security-opt", "apparmor:unconfined"]

                    # add constraint to run SUT on functiontest nodes
                    extraOptions += ["-e", "constraint:type==functiontest"]

                    # add hostname 'sut' for SUT container
                    extraOptions += ["-h", "sut"]

                    if isConsulRunning:
                        # Add an overlay network
                        extraOptions += ["--network", "swarm_network"]

                    # pull the SUT image
                    docker.pull(self._sutImageName)

                    # create the SUT container
                    self.__sutContainerId = docker.run(self._sutImageName, extraOptions, [])

                    # temporary workaround to parse container id from return value
                    temp = self.__sutContainerId.splitlines()
                    try:
                        self.__sutContainerId = temp[0].strip()
                    except IndexError:
                        raise Exception('No container id returned')

                    print "sut id: " + self.__sutContainerId
                    save_container_id(self.__sutContainerId)

                    # Get the IP address of the SUT and add in /etc/hosts of TE
                    sutIpAddress = docker.getIPAddress(self.__sutContainerId)
                else:
                    # we are about to run FT's on a hardware. Reboot node first.
                    rebootCommand = "/usr/src/scripts/utils/reboot_node"
                    print(execute([rebootCommand, sutIpAddress, "root", "root"]))


                # setting up the TE options
                params += ["--runtime-package", runtimePackageName]
                params += ["--test-package", testPackageName]
                params += ["--suite", args["suite"]]
                if args["compiler"] == "valgrind":
                   params += ["--valgrind"]

                # TE extra docker options
                teExtraDockerOptions = ["-v", "/repo/jenkins/maven-repository/:/root/.m2/:rw"]
                teExtraDockerOptions += ["--add-host", "sut:%s" % sutIpAddress.strip()]

                # Add overlay network information if there is an active Consul
                if isConsulRunning:
                    teExtraDockerOptions += ["--network", "swarm_network"]

                # add constraint to run TE on integration nodes temporarily!!!
                teExtraDockerOptions += ["-e", "constraint:type==integrationtest"]

                # pull the TE image
                docker.pull(self._teImageName)

                # create the test executor container
                self.__teContainerId = docker.create(self._teImageName, teExtraDockerOptions, params)

                # temporary workaround to parse container id from return value
                temp = self.__teContainerId.splitlines()
                try:
                    self.__teContainerId = temp[0].strip()
                except IndexError:
                    raise Exception('No container id returned')

                print "te id: " + self.__teContainerId
                save_container_id(self.__teContainerId)

                # copy the runtime package to the correct location in the container
                dest = "/"
                docker.cp_to(self.__teContainerId, runtimePackage, dest)
                docker.cp_to(self.__teContainerId, testPackage, dest)

                # start the container
                self.__teContainerId = docker.start(self.__teContainerId)

                # temporary workaround to parse container id from return value
                temp = self.__teContainerId.splitlines()
                try:
                    self.__teContainerId = temp[0].strip()
                except IndexError:
                    raise Exception('No container id returned')

            except subprocess.CalledProcessError as e:
                print e.cmd
                print e.output
                returnValue = 1
            else:
                # wait for the test to finish
                try:
                    # Follow the logs of the container and wait for it to complete
                    docker.logs(self.__teContainerId)

                    # Get the exit code of the container
                    returnValue = int(docker.getExitCode(self.__teContainerId).strip())

                except KeyboardInterrupt:
                    # this just catches the ctrl+c and so that our clean up will run.
                    print ""
                    print "we got a ctrl+c lets clean up and exit"
                    returnValue = 1  # exit with error
                else:
                    # copy files from container
                    #
                    # follow the cp rules in the docker documents
                    # https://docs.docker.com/engine/reference/commandline/cp/
                    #
                    print "now copying files..."

                    dest = args["copy-to"]
                    try:
                        os.mkdir(dest)
                    except OSError:
                        print dest + " already created!"

                    containerId = None
                    for key in self._filesToCopy.keys():
                        for file in self._filesToCopy[key]:
                            src = file
                            if key == 'te':
                                containerId = self.__teContainerId
                            elif key == 'sut':
                                containerId = self.__sutContainerId

                            retval = docker.cp_from(containerId, src , dest)
                            if (retval > 0):
                                print("Error: copy failed ({}): {} to {}".format(key, src, dest))
                                returnValue = retval

            # cleanup
            try:
                print "cleaning up"
                res = docker.rm(self.__teContainerId)
                print "deleted te: " + res

                if self.__sutContainerId is not None:
                    res = docker.rm(self.__sutContainerId)
                    print "deleted sut: " + res

            except subprocess.CalledProcessError as e:
                print e.cmd
                print e.output

        # exit the runBuild with the return value from the build
        return returnValue
