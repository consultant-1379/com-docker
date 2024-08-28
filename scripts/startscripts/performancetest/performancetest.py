import os
import subprocess
import sys
import glob

from cirpa.utils.docker import Docker
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.utils.dockerutility import save_container_id
from cirpa.startbase import StartBase
from cirpa.hasharguments import RegExp, Optional
from cirpa.utils.shellhelper import execute
from comlib.version import getVersion

class PerformanceTest(StartBase):

    def arguments(self, parser):
        parser.add_argument('--suite', dest="suite", type=RegExp)
        parser.add_argument('--os', dest="os")
        parser.add_argument('--test-type', dest="testType")
        parser.add_argument('--sut-ip', dest="sutIp", type=Optional)
        parser.add_argument('--com-version', dest="comVersion", type=Optional)
        parser.add_argument('--copy-to', dest="copyTo", default="/results", type=RegExp)
        parser.add_argument('--test-duration', dest="testDuration", default="60", type=RegExp)
        parser.add_argument('--cpuload', dest="cpuLoad", default="0", type=RegExp)
        parser.add_argument('--memoryload', dest="memoryLoad", default="0", type=RegExp)
        parser.add_argument('--execution-type', dest="testExecution", choices=['characteristicstest', 'characteristicsshorttest', 'stabilitytest', 'loadtest'], help='type of testexecution', type=RegExp)

    def set_path(self, os, testType):
        self.add_argument("suite", RegExp("^([a-z0-9]|_)+"))
        self.add_argument("os", os)
        self.add_argument("testType", testType)
        self.add_argument("sutIp", Optional(""))
        self.add_argument("comVersion", Optional(""))
        self.add_argument("copyTo", RegExp("^.+"))
        self.add_argument("testDuration", RegExp("^[0-9]+"))
        self.add_argument("cpuLoad", RegExp("^[0-9]+"))
        self.add_argument("memoryLoad", RegExp("^[0-9]+"))
        self.add_argument("testExecution", RegExp("^([a-z0-9]|_)+"))

    # constructor
    def __init__(self):

        # name of the docker images to use
        self._teImageName = None

        # this is a list of files e.g ["/dist","/logs/build.log"]
        self._filesToCopy = None

        # running containers hash id
        self.__teContainerId = None
        self.__sutContainerId = None


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
            comVersion = getVersion(distDir)

        ptPackageName = "com-pt-test-*.noarch.rpm"
        files = glob.glob(os.path.join("dist", ptPackageName))
        for src in files:
            head, tail = os.path.split(src)
            ptPackageName = tail
        runtimePackageName = "com-" + comVersion + "-runtime.tar.gz"
        testPackageName = "com-" + comVersion + "-test.tar.gz"
        sutIpAddress = args["sutIp"]

        if self._teImageName:

            try:
                # check if the package exists
                ptPackage = os.path.join("dist", ptPackageName)
                self._checkIfExists(ptPackage)
                runtimePackage = os.path.join("dist", runtimePackageName)
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
                    print("No SUT is available, starting a new SUT container.")

                    # adding support for using Fuse in the SUT
                    extraOptions = ["--cap-add", "SYS_ADMIN"]
                    extraOptions += ["--device", "/dev/fuse"]
                    extraOptions += ["--security-opt", "apparmor:unconfined"]

                    # enable ipv6 on the container
                    extraOptions += ["--sysctl", "net.ipv6.conf.all.disable_ipv6=0"]

                    # add constraint to run SUT on functiontest nodes
                    extraOptions += ["-e", "constraint:type==performancetest"]

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

                    print("sut id: " + self.__sutContainerId)

                    # Get the IP address of the SUT and add in /etc/hosts of TE
                    sutIpAddress = docker.getIPAddress(self.__sutContainerId)

                # setting up the TE options
                params += ["--pt-package", ptPackageName]
                params += ["--runtime-package", runtimePackageName]
                params += ["--test-package", testPackageName]
                params += ["--execution-type", args["testExecution"]]
                params += ["--suite", args["suite"]]
                params += ["--sut-ip", sutIpAddress.strip()]
                params += ["--cpuload", args["cpuLoad"]]
                params += ["--memoryload", args["memoryLoad"]]

                # TE extra docker options
                teExtraDockerOptions = ["-v", "/repo/jenkins/maven-repository/:/root/.m2/:rw"]
                teExtraDockerOptions += ["--add-host", "sut:%s" % sutIpAddress.strip()]

                # Add overlay network information if there is an active Consul
                if isConsulRunning:
                    teExtraDockerOptions += ["--network", "swarm_network"]

                # add constraint to run TE on integration nodes temporarily!!!
                teExtraDockerOptions += ["-e", "constraint:type==performancetest"]

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

                # copy the test package to the correct location in the container
                dest = "/"
                docker.cp_to(self.__teContainerId, ptPackage, dest)
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
                save_container_id(self.__teContainerId)

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

                    dest = args["copyTo"]
                    try:
                        os.mkdir(dest)
                    except OSError:
                        print dest + " already created!"

                    # untar com testpackage to find the path of com-main.
                    execute(["tar", "xf", testPackage, "-C", "/"])
                    repoSrc = None
                    for root, dir, files in os.walk('/src'):
                        if 'com-main' in dir:
                            repoSrc = root + '/com-main'
                            break

                    self._filesToCopy = [repoSrc + ele for ele in self._filesToCopy]

                    for src in self._filesToCopy:
                        # copy files
                        retval = docker.cp_from(self.__teContainerId, src, dest)
                        if (retval > 0):
                            print "error when trying to copy: " + src + " to " + dest
                            returnValue = retval
                    # remove the content extracted from testPackage
                    execute(["rm", "-rf", "/src", "/build"])

            # cleanup
            try:
                print "cleaning up"
                res = docker.rm(self.__teContainerId)
                print "deleted te: " + res
                if self.__sutContainerId is not None:
                    res = docker.rm(self.__sutContainerId)
                    print ("deleted sut: {}".format(self.__sutContainerId))

            except subprocess.CalledProcessError as e:
                print e.cmd
                print e.output

        # exit the runBuild with the return value from the build
        return returnValue
