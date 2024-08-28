import os
import subprocess
import sys

from cirpa.utils.docker import Docker
from cirpa.utils.dockerutility import save_container_id
from cirpa.utils.stringutils import StringUtils
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.startbase import StartBase
from cirpa.hasharguments import RegExp, Optional


class Build(StartBase):

    buildDir="/build/com-build"

    def arguments(self, parser):
        parser.add_argument('--repo', dest="repo")
        parser.add_argument('--compiler', dest="compiler")
        parser.add_argument('--os', dest="os")
        parser.add_argument('--commit', dest="commit", type=RegExp)
        parser.add_argument('--com-version', dest="comVersion", type=Optional)
        parser.add_argument('--fmcore-version', dest="fmcoreVersion", type=Optional)
        parser.add_argument('--openssl-version', dest="opensslVersion", type=Optional, choices=['1.0.1e'])
        parser.add_argument('--localsrc', dest="localsrc", type=Optional)
        parser.add_argument('--gerrit-project', dest="gerritProject", type=Optional)
        parser.add_argument('--gerrit-patchset', dest="patchset", type=Optional)
        parser.add_argument('--branch', dest="branch", type=Optional)
        parser.add_argument('--gerrit-trigger', action="store", dest="gerritTrigger", choices=['trigger', 'review', 'push'], type=Optional)
        parser.add_argument('--gerrit-branch', action="store", dest="gerritBranch", type=Optional)
        parser.add_argument('--com-branch', action="store", dest="comBranch", type=Optional)
        parser.add_argument('--vault-pass', action="store", dest="vaultPass", type=Optional)
        parser.add_argument('--use-verbose', action="store", dest="useVerbose",
                            choices=['yes', 'true', 't', 'y', '1', 'no', 'false', 'f', 'n', '0'], type=Optional, help="make with verbose enabled")
        parser.add_argument('--maf-latest', action="store", dest="mafLatest",
                            choices=['yes', 'true', 't', 'y', '1', 'no', 'false', 'f', 'n', '0'], type=Optional, help="Accepts Boolean values")
        parser.add_argument('--test', action="store", dest="comsaTest", type=Optional)

    def set_path(self, os, repo, compiler):
        self.add_argument("repo", repo)
        self.add_argument("os", os)
        self.add_argument("compiler", compiler)
        self.add_argument("commit", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("comVersion", Optional(""))
        self.add_argument("fmcoreVersion", Optional(""))
        self.add_argument("opensslVersion", Optional(""))
        self.add_argument("localsrc", Optional(""))
        self.add_argument("gerritProject", Optional(""))
        self.add_argument("patchset", Optional(""))
        self.add_argument("branch", Optional(""))
        self.add_argument("gerritTrigger", Optional(""))
        self.add_argument("gerritBranch", Optional(""))
        self.add_argument("comBranch", Optional(""))
        self.add_argument('vaultPass', Optional(""))
        self.add_argument('useVerbose', Optional(""))
        self.add_argument('mafLatest', Optional(""))
        self.add_argument("test", Optional(""))

    # always needs a commit passed in
    def __init__(self):

        # to make sure the test package have the same folder structure we need to set the build-dir to /build/com-build
        self.__builddir = self.buildDir

        # name of the docker image to use
        self._imageName = self.image

        # this is a list of files e.g ["/dist", "/logs/build.log"]
        self._filesToCopy = [os.path.join(self.__builddir, "dist")]

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

            # openssl version check
            if args["opensslVersion"] is not None and args["compiler"] == "lsb":
                self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles11sp3/lsbopenssl/1.0.1e/build"

            # check if image exists, if not try to pull the image from the repo
            # todo! we need a readonly user so that we can do pull safe

            try:
                if args["localsrc"] is not None:
                    self._mirror = ["-v", args["localsrc"] + ":/localsrc/:ro"]
                    buildParams += ["--local-src", "/localsrc"]

                extraRunParams = self._mirror + self._mvnrepo

                if args["comVersion"] is not None:
                    buildParams += ["--com-version", args["comVersion"]]

                if args["fmcoreVersion"] is not None:
                    buildParams += ["--fmcore-version", args["fmcoreVersion"]]

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

                if args["useVerbose"] is not None:
                    stringutils = StringUtils()
                    if stringutils.str2bool(args["useVerbose"]) is True:
                        buildParams += ["--use-verbose"]

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

                print "id: " + self.__containerId
                save_container_id(self.__containerId)

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
                else:
                    # copy files from container
                    #
                    # follow the cp rules in the docker documents
                    # https://docs.docker.com/engine/reference/commandline/cp/
                    #
                    if args["gerritTrigger"] == "review" or args["gerritTrigger"] == "push":
                        print "Nothing to copy as this is a submodule update"
                    else:
                        print "successfully built, now copying files..."

                        dest = self._fileDestination
                        try:
                            os.mkdir(dest)
                        except OSError:
                            print dest + " already created!"

                        for src in self._filesToCopy:
                            copyReturnValue = docker.cp_from(self.__containerId, src, dest)
                            if (copyReturnValue > 0):
                                print "error when trying to copy: " + src + " to " + dest
                                returnValue = copyReturnValue

                # cleanup
                try:
                    print "cleaning up"
                    res = docker.rm(self.__containerId)
                    print "deleted: " + res

                except subprocess.CalledProcessError as e:
                    print e.cmd
                    print e.output

        # exit the runBuild with the return value from the build
        return returnValue

    # if comsa testing pass --test argument as a parameter to build script
    if "--test" in str(sys.argv):
        def execute(self, args):
            print ("Starting the "+self.name+" Build")
            return self._runBuild(["build",
                            "--commit", args["commit"],
                            "--repo", args["repo"],
                            "--build-type", self.target,
                            "--mirror-path", "/mirrors",
                            "--build-dir", self.__builddir,
                            "--test", args["comsaTest"],
                            ], args)
    else:
        def execute(self, args):
            print ("Starting the "+self.name+" Build")
            return self._runBuild(["build",
                            "--commit", args["commit"],
                            "--repo", args["repo"],
                            "--build-type", self.target,
                            "--mirror-path", "/mirrors",
                            "--build-dir", self.__builddir,
                            ], args)
