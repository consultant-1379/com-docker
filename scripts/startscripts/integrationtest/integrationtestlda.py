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

class IntegrationTestLda(StartBase):

    def arguments(self, parser):
        parser.add_argument('--suite', dest="suite", type=RegExp)
        parser.add_argument('--os', dest="os")
        parser.add_argument('--target', dest="target", choices=['legacy', 'csm', 'lda'])
        parser.add_argument('--com-version', dest="comVersion", type=Optional)
        parser.add_argument('--sut-ip1', dest="sutIp1", default="10.0.2.15", type=Optional)
        parser.add_argument('--sut-ip2', dest="sutIp2", default="10.0.2.16", type=Optional)
        parser.add_argument('--copy-to', dest="copyTo", default="/results", type=RegExp)
        parser.add_argument('--version-file', dest="versionFile", type=Optional)
        parser.add_argument('--base', dest="base", type=Optional)
        parser.add_argument('--cluster-size', dest="clusterSize", choices=['1+0', '1+1', '2+0', '2+2'], type=Optional)
        parser.add_argument('--brf-action', dest="brfAction", choices=['upgradebackup', 'restorebackup', 'upgrade', 'restore'], type=Optional, help="Mention the type of jeos brf required from the choices mentioned")
        parser.add_argument('--external-fs', dest="externalFs", type=Optional, help="To enable external-fs in the cluster")
        parser.add_argument('--disablekernelmodule', dest="disablekernelmodule", type=Optional)
        parser.add_argument('--ldesugar', dest="ldesugar", type=Optional)

    def set_path(self, os, target):
        self.add_argument("suite", RegExp("^([a-z0-9]|_)+"))
        self.add_argument("os", os)
        self.add_argument("target", target)
        self.add_argument("comVersion", Optional(""))
        self.add_argument("sutIp1", Optional(""))
        self.add_argument("sutIp2", Optional(""))
        self.add_argument("copyTo", RegExp("^.+"))
        self.add_argument("versionFile", Optional(""))
        self.add_argument("base", Optional(""))
        self.add_argument("clusterSize", Optional(""))
        self.add_argument("brfAction", Optional(""))
        self.add_argument("externalFs", Optional(""))
        self.add_argument("disablekernelmodule", Optional(""))
        self.add_argument("ldesugar", Optional(""))

    # constructor
    # the test option is used to filter out just some specific unit test binaries, e.g. test="pm"
    def __init__(self):

        # commit id e.g. commit hash, branch name, tag or gerrit reference to a patchset
        self._commit = None

        # name of the docker images to use
        self._teImageName = self._teImageName
        self._sutImageName = self._sutImageName

        # this is a list of files e.g ["/dist", "/logs/build.log"]
        self._teFilesToCopy = ["/messages", "/build/com-build/gen"]
        self._sutFilesToCopy = ["/var/log/dmesg"]
        self._filesToRemove = ["/ovf-env.xml", "/lda.box"]

        # running containers hash id
        self.__teContainerId = None
        self.__sutContainerId = None

        self._workDir = "/workdir"

        self.set_path(self.os, self.target)

    def _checkIfExists(self, filename):
        if not os.path.isfile(filename):
            print("file: " + filename + " does not exist")
            sys.exit(1)  # just exit, no need for cleanup

    def execute(self, args):
        print "Starting the SLES12 lda integration test"
        returnValue = self._runSutImage(["integrationtest"], args)
        if returnValue == 0:
            returnValue = self._runTeImage(["integrationtest"], args)
        self._cleanup()
        # exit the test with the return value from the sut or te images run process
        return returnValue

    # this function should not be overriden unless a totally new way to spawn build is needed
    # TODO: Find a way to remove CXP numbers for COM packages
    def _runSutImage(self, params, args):
        returnValue = 0
        distDir = "dist/"
        if args["comVersion"]:
            comVersion = args["comVersion"]
        else:
            comVersion = getVersion(distDir)
        runtimePackageName = "com_x86_64-" + comVersion + "-runtime-sle-cxp9028493.tar.gz"
        deploymentPackageName = "com_x86_64-" + comVersion + "-deployment-sle-cxp9028492.tar.gz"

        if self._sutImageName:
            try:
                # check if the package exists
                runtimePackage = os.path.join("dist", runtimePackageName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(runtimePackage)

                deploymentPackage = os.path.join("dist", deploymentPackageName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(deploymentPackage)

                # check if there is an active Consul for Docker Swarm
                isConsulRunning = DockerSwarm.isConsulRunning()
                if isConsulRunning:
                    docker = DockerSwarm()
                else:
                    docker = Docker()

                # adding support for using Fuse in the SUT
                tsExtraDockerOptions = ["--cap-add", "SYS_ADMIN"]
                tsExtraDockerOptions += ["--device", "/dev/kvm:/dev/kvm:rw"]
                tsExtraDockerOptions += ["--privileged"]
                tsExtraDockerOptions += ["--security-opt", "apparmor:unconfined"]

                # Add overlay network information if there is an active Consul
                if isConsulRunning:
                    tsExtraDockerOptions += ["--network", "swarm_network"]

                parameter = ["/start"]
                parameter += [args["clusterSize"]]
                externalFs = args["externalFs"]
                if externalFs:
                    parameter += [externalFs]
                versionFile = args["versionFile"]
                if versionFile:
                    self._checkIfExists(versionFile)
                    parameter += [versionFile]
                else:
                    if args["suite"] == "integration_bfu_csm":
                        parameter += ["/root/.csm/config/versionsBfu.xml"]
                    else:
                        parameter += ["/root/.csm/config/versions.xml"]

                if args["disablekernelmodule"]:
                    parameter += [args["disablekernelmodule"]]
                if args["ldesugar"]:
                    parameter += [args["ldesugar"]]

                # pull the SUT image
                docker.pull(self._sutImageName)
                # create the SUT container
                self.__sutContainerId = docker.create(self._sutImageName, tsExtraDockerOptions, parameter)

                if args["brfAction"] != "upgradebackup":
                    # copy the deployment package to the correct location in the container
                    dest = "/root/.csm/registry"
                    docker.cp_to(self.__sutContainerId, deploymentPackage, dest)
                    docker.cp_to(self.__sutContainerId, runtimePackage, dest)
                    # copy the runtime package to the correct location in the container
                    dest = "/local_repo"
                    docker.cp_to(self.__sutContainerId, runtimePackage, dest)
                    docker.cp_to(self.__sutContainerId, deploymentPackage, dest)
                # copy the versionFile to the correct location in the container
                if versionFile:
                    dest = "/"
                    docker.cp_to(self.__sutContainerId, versionFile, dest)

                # start the container
                self.__sutContainerId = docker.start(self.__sutContainerId)
                save_container_id(self.__sutContainerId)

            except subprocess.CalledProcessError as e:
                print(e.cmd)
                print(e.output)
                returnValue = 1
            else:
                # wait for the test to finish
                try:
                    # Follow the logs of the container and wait for it to complete
                    docker.logs(self.__sutContainerId)
                    docker.cp_from(self.__sutContainerId, "/lda.box", "/")
                    docker.cp_from(self.__sutContainerId, "/ovf-env.xml", "/")

                    # Get the exit code of the container
                    returnValue = int(docker.getExitCode(self.__sutContainerId).strip())

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

                    for src in self._sutFilesToCopy:
                        # join workdir with src
                        src = os.path.join(self._workDir, src)

                        # copy files
                        retval = docker.cp_from(self.__sutContainerId, src, dest)
                        if (retval > 0):
                            print("error when trying to copy: " + src + " to " + dest)
                            returnValue = retval
        return returnValue

    def _runTeImage(self, params, args):

        returnValue = 0
        esmBoxName = "lda.box"
        configDriveName = "ovf-env.xml"
        distDir = "dist/"

        if args["comVersion"]:
            comVersion = args["comVersion"]
        else:
            comVersion = getVersion(distDir)

        runtimePackageName = "com_x86_64-" + comVersion + "-runtime-sle-cxp9028493.tar.gz"
        deploymentPackageName = "com_x86_64-" + comVersion + "-deployment-sle-cxp9028492.tar.gz"
        testPackageName = "com-" + comVersion + "-test.tar.gz"

        for files in os.listdir(distDir):
            if "COM_DEBUGINFO" in files:
                debugSDPName = files

        # start the Cluster
        if self._teImageName:

            try:
                # check if the package exists
                testPackage = os.path.join("dist", testPackageName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(testPackage)

                runtimePackage = os.path.join("dist", runtimePackageName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(runtimePackage)

                deploymentPackage = os.path.join("dist", deploymentPackageName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(deploymentPackage)

                esmBox = os.path.join("/", esmBoxName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(esmBox)

                configDrive = os.path.join("/", configDriveName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(configDrive)

                debugSDP = os.path.join("dist", debugSDPName)  # we need to get the correct path maybe by using glob and search for the file
                self._checkIfExists(debugSDP)

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
                params += ["--test-package", testPackageName]
                params += ["--debug-sdp", debugSDPName]
                params += ["--suite", args["suite"]]
                params += ["--sut-ip1", args["sutIp1"]]
                params += ["--sut-ip2", args["sutIp2"]]
                params += ["--target", args["target"]]
                params += ["--cluster-size", args["clusterSize"]]
                if args["base"]:
                    params += ["--base", args["base"]]
                    params += ["--runtime-package", runtimePackageName]
                    params += ["--deployment-package", deploymentPackageName]
                if args["brfAction"]:
                    params += ["--brf-action", args["brfAction"]]
                if args["externalFs"]:
                    params += ["--external-fs", args["externalFs"]]

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
                save_container_id(self.__teContainerId)

                # copy the runtime package to the correct location in the container
                dest = "/"
                docker.cp_to(self.__teContainerId, esmBox, dest)
                docker.cp_to(self.__teContainerId, testPackage, dest)
                docker.cp_to(self.__teContainerId, debugSDP, dest)

                if args["base"]:
                    docker.cp_to(self.__teContainerId, runtimePackage, dest)
                    docker.cp_to(self.__teContainerId, deploymentPackage, dest)

                if args["brfAction"] == "upgrade" or args["brfAction"] == "restore":
                    configBackup = "configBackup.tar.gz"
                    self._checkIfExists(configBackup)
                    print("Copying backup file: {}".format(configBackup))
                    docker.cp_to(self.__teContainerId, configBackup, dest)

                # start the container
                self.__teContainerId = docker.start(self.__teContainerId)

                # temporary workaround to parse container id from return value
                temp = self.__teContainerId.splitlines()
                try:
                    self.__teContainerId = temp[0].strip()
                except IndexError:
                    raise Exception('No container id returned')

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

                    for src in self._teFilesToCopy:
                        # join workdir with src
                        src = os.path.join(self._workDir, src)

                        # copy files
                        retval = docker.cp_from(self.__teContainerId, src, dest)
                        if (retval > 0):
                            print("error when trying to copy: " + src + " to " + dest)
                            returnValue = retval
        return returnValue

    def _cleanup(self):
        # cleanup
        # check if there is an active Consul for Docker Swarm
        isConsulRunning = DockerSwarm.isConsulRunning()
        if isConsulRunning:
            docker = DockerSwarm()
        else:
            docker = Docker()
        try:
            print "cleaning up"
            if self.__teContainerId is not None:
                res = docker.rm(self.__teContainerId)
                print "deleted te: " + res

            if self.__sutContainerId is not None:
                res = docker.rm(self.__sutContainerId)
                print "deleted sut: " + res

            # remove files copied to slave
            for files in self._filesToRemove:
                if os.path.isfile(files):
                    os.remove(files)
        except subprocess.CalledProcessError as e:
            print e.cmd
            print e.output
