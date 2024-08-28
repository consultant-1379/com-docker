import subprocess
import sys
import os

from cirpa.startbase import StartBase
from cirpa.utils.docker import Docker
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.hasharguments import RegExp


class Eridoc(StartBase):

    # always needs a commit passed in
    def __init__(self):
        # commit id e.g. commit hash, branch name, tag or gerrit reference to a patchset

        # name of the docker image to use
        self._imageName = "armdocker.rnd.ericsson.se/cba-com/eridoc-upload:latest"

        # running containers hash id
        self.__containerId = None

        self.add_argument("username", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("password", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))
        self.add_argument("comVersion", RegExp("^([a-zA-Z0-9]|/|_|-|\.)+"))

    # this function should not be overriden unless a totally new way to spawn build is needed
    def _eridocUpload(self, params):
        returnValue = 0
        if self._imageName is not None:

            # check if image exists, if not try to pull the image from the repo
            # todo! we need a readonly user so that we can do pull safe

            try:
                # add constraint to run only on eridoc nodes
                extraRunParams = ["-e", "constraint:type==functiontest"]
                try:
                    eridocComponentList = os.environ['componentList']
                    if eridocComponentList is not None:
                        extraRunParams += ["-e", "componentList="+eridocComponentList.lstrip()]
                except KeyError:
                    raise Exception('Error: Component list to perform eridoc uupload is not set')

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

                print("id: " + self.__containerId)

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
                    print("we got a ctrl+c lets clean up and exit")
                    returnValue = 1

                # cleanup
                try:
                    print("cleaning up")
                    res = docker.rm(self.__containerId)
                    print("deleted: " + res)

                except subprocess.CalledProcessError as e:
                    print e.cmd
                    print e.output

        # exit the generatePri with the return value from the generator
        return returnValue

    def execute(self, args):

        # TODO after CIRPA delivery rename the arguments, use correct ones
        print("Starting the Eridoc upload")
        return self._eridocUpload(["eridocupload",
                                  args["username"],
                                  args["password"],
                                  args["comVersion"],
                                  ])

    def arguments(self, parser):
        parser.add_argument('--username', dest="username", type=RegExp)
        parser.add_argument('--password', dest="password", type=RegExp)
        parser.add_argument('--com-version', dest="comVersion", type=RegExp)
