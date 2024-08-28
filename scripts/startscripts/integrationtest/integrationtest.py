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

class IntegrationTest(StartBase):

    def arguments(self, parser):
        parser.add_argument('--suite', dest="suite", type=RegExp)
        parser.add_argument('--os', dest="os")
        parser.add_argument('--com-version', dest="comVersion", type=Optional)
        parser.add_argument('--sut-ip1', dest="sutIp1", default="10.0.2.15", type=Optional)
        parser.add_argument('--sut-ip2', dest="sutIp2", default="10.0.2.16", type=Optional)
        parser.add_argument('--copy-to', dest="copyTo", default="/results", type=RegExp)
        parser.add_argument('--version-file', dest="versionFile", type=Optional)
        parser.add_argument('--target', dest="target", choices=['legacy', 'csm', 'lda'])
        parser.add_argument('--base', dest="base", type=Optional)
        parser.add_argument('--cluster-size', dest="clusterSize", choices=['1+0', '1+1', '2+0', '2+2'], type=Optional)
        parser.add_argument('--brf-action', dest="brfAction", choices=['upgradebackup', 'restorebackup', 'upgrade', 'restore'], type=Optional, help="Mention the type of jeos brf required from the choices mentioned")

    def set_path(self, os, target):
        self.add_argument("suite", RegExp("^([a-z0-9]|_)+"))
        self.add_argument("os", os)
        self.add_argument("comVersion", Optional(""))
        self.add_argument("sutIp1", Optional(""))
        self.add_argument("sutIp2", Optional(""))
        self.add_argument("copyTo", RegExp("^.+"))
        self.add_argument("versionFile", Optional(""))
        self.add_argument("target", target)
        self.add_argument("base", Optional(""))
        self.add_argument("clusterSize", Optional(""))
        self.add_argument("brfAction", Optional(""))

    # constructor
    # the test option is used to filter out just some specific unit test binaries, e.g. test="pm"
    def __init__(self):

        # commit id e.g. commit hash, branch name, tag or gerrit reference to a patchset
        self._commit = None

        # name of the docker images to use
        self._teImageName = self._teImageName

        # this is a list of files e.g ["/dist", "/logs/build.log"]
        self._filesToCopy = ["/opt/dxtools/ait.log", "/messages", "/build/com-build/gen"]

        # running containers hash id
        self.__teContainerId = None

        self._workDir = "/workdir"

        self.set_path(self.os, self.target)

    def _checkIfExists(self, filename):
        if not os.path.isfile(filename):
            print("file: " + filename + " does not exist")
            sys.exit(1)  # just exit, no need for cleanup

    def execute(self, args):
        print "Starting the SLES12 integration test"
        return self._run(["integrationtest"], args)

    # this function should not be overriden unless a totally new way to spawn build is needed
    # TODO: Find a way to remove CXP numbers for COM packages
    def _run(self, params, args):
        returnValue = 0
        distDir = "dist/"
        if args["comVersion"]:
            comVersion = args["comVersion"]
        else:
            comVersion = getVersion(distDir)

        runtimePackageName = "com-" + comVersion + "-runtime.tar.gz"
        testPackageName = "com-" + comVersion + "-test.tar.gz"

        for files in os.listdir(distDir):
            if "COM-CXP" in files:
                runtimeSDPName = files
            elif "COM_DEBUGINFO" in files:
                debugSDPName = files

        deploymentPackageName = "com_x86_64-" + comVersion + "-deployment-sle-cxp9028492.tar.gz"
        deploymentPackageNameLegacy = "com-" + comVersion + "-deployment-sle-cxp9028492.tar.gz"
        sutIpAddress1 = args["sutIp1"]
        sutIpAddress2 = args["sutIp2"]
        versionFile = args["versionFile"]
        target = args["target"]

        if self._teImageName:

            try:
                # check if the package exists
                runtimePackage = os.path.join("dist", runtimePackageName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(runtimePackage)

                testPackage = os.path.join("dist", testPackageName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(testPackage)

                runtimeSDP = os.path.join("dist", runtimeSDPName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(runtimeSDP)

                debugSDP = os.path.join("dist", debugSDPName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(debugSDP)

                # This check is needed as there is different naming convention for deployment package in COM 7.0
                if os.path.isfile(os.path.join("dist", deploymentPackageNameLegacy)):
                    deploymentPackageName = deploymentPackageNameLegacy

                deploymentPackage = os.path.join("dist", deploymentPackageName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(deploymentPackage)

                # check if there is an active Consul for Docker Swarm
                isConsulRunning = DockerSwarm.isConsulRunning()
                if isConsulRunning:
                    docker = DockerSwarm()
                else:
                    docker = Docker()

                # adding support for using Fuse in the SUT
                teExtraDockerOptions = ["--cap-add", "SYS_ADMIN"]
                teExtraDockerOptions += ["--device", "/dev/fuse"]
                teExtraDockerOptions += ["--privileged"]
                teExtraDockerOptions += ["--security-opt", "apparmor:unconfined"]

                # setting up the TE options
                params += ["--runtime-package", runtimePackageName]
                params += ["--test-package", testPackageName]
                params += ["--runtime-sdp", runtimeSDPName]
                params += ["--debug-sdp", debugSDPName]
                params += ["--deployment-package", deploymentPackageName]
                params += ["--suite", args["suite"]]
                params += ["--sut-ip1", args["sutIp1"]]
                params += ["--sut-ip2", args["sutIp2"]]
                if args["versionFile"]:
                    params += ["--version-file", args["versionFile"]]
                if args["base"]:
                    params += ["--base", args["base"]]
                params += ["--target", args["target"]]
                params += ["--cluster-size", args["clusterSize"]]

                # TE extra docker options
                teExtraDockerOptions += ["-v", "/repo/jenkins/maven-repository/:/root/.m2/:rw"]

                # Add overlay network information if there is an active Consul
                if isConsulRunning:
                    teExtraDockerOptions += ["--network", "swarm_network"]

                # add constraint to run TE on integration nodes temporarily!!!
                # TODO: Update for FT and IT the constraint type
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

                print("te id: " + self.__teContainerId)

                # copy the runtime package to the correct location in the container
                dest = "/"
                docker.cp_to(self.__teContainerId, runtimePackage, dest)
                docker.cp_to(self.__teContainerId, testPackage, dest)
                docker.cp_to(self.__teContainerId, runtimeSDP, dest)
                docker.cp_to(self.__teContainerId, debugSDP, dest)
                docker.cp_to(self.__teContainerId, deploymentPackage, dest)
                if args["versionFile"]:
                    if os.path.isfile(versionFile) and os.access(versionFile, os.R_OK):
                        docker.cp_to(self.__teContainerId, versionFile, dest)

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
                print(e.cmd)
                print(e.output)
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
                    print("")
                    print("we got a ctrl+c lets clean up and exit")
                    returnValue = 1  # exit with error
                else:
                    # copy files from container
                    #
                    # follow the cp rules in the docker documents
                    # https://docs.docker.com/engine/reference/commandline/cp/
                    #
                    print("now copying files...")

                    dest = args["copyTo"]
                    try:
                        os.mkdir(dest)
                    except OSError:
                        print(dest + " already created!")

                    for src in self._filesToCopy:
                        # join workdir with src
                        src = os.path.join(self._workDir, src)

                        # copy files
                        retval = docker.cp_from(self.__teContainerId, src, dest)
                        if (retval > 0):
                            print("error when trying to copy: " + src + " to " + dest)
                            returnValue = retval

            # cleanup
            try:
                print("cleaning up")
                res = docker.rm(self.__teContainerId)
                print("deleted te: " + res)

            except subprocess.CalledProcessError as e:
                print(e.cmd)
                print(e.output)

        # exit the runBuild with the return value from the build
        return returnValue
