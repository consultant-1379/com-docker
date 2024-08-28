import subprocess
from cirpa.utils.docker import Docker
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.startbase import StartBase
from cirpa.hasharguments import RegExp, Optional


class BuildLdeBox(StartBase):

    def arguments(self, parser):
        parser.add_argument('--lde-version', dest="ldeVersion", type=RegExp)
        parser.add_argument('--cluster-size', action="store", dest="clusterSize", choices=['2+0', '2+2'], type=RegExp)

    def set_path(self):
        self.add_argument("ldeVersion", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("clusterSize", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))

    def __init__(self):

        # setting paths for cirpa to validate hex values
        self.set_path()

        # name of the docker image to use
        self._imageName = "armdocker.rnd.ericsson.se/cba-com/vagrantbuild/ldebox"

        # this is a list of files e.g ["/dist", "/logs/build.log"]
        self._filesToCopy = None

        # running containers hash id
        self.__containerId = None

        self.__builddir = "/"

    def execute(self, args):
        print ("Starting the vagrant build image process")
        return self._runBuild(["/packer/create-vagrant-box", args["ldeVersion"], args["clusterSize"]])

    # this function should not be overriden unless a totally new way to spawn build is needed
    def _runBuild(self, buildParams):
        returnValue = 0
        if self._imageName is not None:

            # check if image exists, if not try to pull the image from the repo
            # TODO: we need a readonly user so that we can do pull safe

            try:

                # add constraint to run only on build nodes
                extraRunParams = ["-e", "constraint:type==build"]
                extraRunParams += ["--privileged"]
                extraRunParams += ["--cap-add=ALL"]

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

                print ("id: " + self.__containerId)

            except subprocess.CalledProcessError as e:
                print (e.cmd)
                print (e.output)
                returnValue = 1
            else:
                try:
                    # Follow the logs of the container and wait for it to complete
                    docker.logs(self.__containerId)

                    # Get the exit code of the container
                    returnValue = int(docker.getExitCode(self.__containerId).strip())

                except KeyboardInterrupt:
                    # this just catches the ctrl+c and so that our clean up will run.
                    print ("we got a ctrl+c lets clean up and exit")
                    returnValue = 1

                # cleanup
                try:
                    print ("cleaning up")
                    res = docker.rm(self.__containerId)
                    print ("deleted: " + res)

                except subprocess.CalledProcessError as e:
                    print (e.cmd)
                    print (e.output)

        # exit the runBuild with the return value from the build
        return returnValue
