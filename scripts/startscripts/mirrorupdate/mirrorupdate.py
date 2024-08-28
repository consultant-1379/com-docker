import subprocess

from cirpa.startbase import StartBase
from cirpa.utils.docker import Docker
from cirpa.utils.dockerswarm import DockerSwarm
from cirpa.hasharguments import RegExp


class MirrorUpdate(StartBase):

    def __init__(self):
        self._imageName = "armdocker.rnd.ericsson.se/cba-com/mirrors-ansible"

        self._containerId = None

        self._homeDir = "/root/"

        self._vaultPassword = None

        self.add_argument("hostsFileUrl", RegExp("[a-z]+://[a-z0-9.:]+/?([a-zA-Z0-9.?+#_=;\-]+/?)*"))
        self.add_argument('vaultPassword', RegExp("^.+"))

    def _runMirrorUpdate(self, params):
        returnValue = 0
        if self._imageName is not None:
            try:

                # Check if there is an active Consul for Docker Swarm
                if DockerSwarm.isConsulRunning():
                    docker = DockerSwarm()
                else:
                    docker = Docker()

                # Pull the ansible image
                docker.pull(self._imageName)

                # Add constraint to run container always on integration nodes temporarily!!!
                extraRunParams = ["-e", "constraint:type==integrationtest"]

                # Create the container
                self._containerId = docker.create(self._imageName, extraRunParams, params)

                # temporary workaround to parse container id from return value
                temp = self._containerId.splitlines()
                try:
                    self._containerId = temp[0].strip()
                except IndexError:
                    raise Exception('No container id returned')

                print "Container ID: " + self._containerId

                # Copy vault_pass to container
                docker.cp_to(self._containerId, self._vaultPassword, self._homeDir)

                # Start the container
                self._containerId = docker.start(self._containerId)

                # temporary workaround to parse container id from return value
                temp = self._containerId.splitlines()
                try:
                    self._containerId = temp[0].strip()
                except IndexError:
                    raise Exception('No container id returned')

            except subprocess.CalledProcessError as e:
                print e.cmd
                print e.output
                returnValue = 1
            else:
                try:
                    # Follow the logs of the container and wait for it to complete
                    docker.logs(self._containerId)

                    # Get the exit code of the container
                    returnValue = int(docker.getExitCode(self._containerId).strip())

                except KeyboardInterrupt:
                    # this just catches the ctrl+c and so that our clean up will run.
                    print ""
                    print "we got a ctrl+c lets clean up and exit"
                    returnValue = 1

                # cleanup
                try:
                    print "Cleaning up"
                    res = docker.rm(self._containerId)
                    print "Deleted container: " + res

                except subprocess.CalledProcessError as e:
                    print e.cmd
                    print e.output

        return returnValue

    def execute(self, args):

        self._vaultPassword = args["vaultPassword"]

        print "Starting the mirror update"
        return self._runMirrorUpdate(["update-mirrors.py",
                                     "--hosts-file-url", args["hostsFileUrl"]])

    def arguments(self, parser):
        parser.add_argument('--hosts-file-url', dest="hostsFileUrl", type=RegExp)
        parser.add_argument('--vault-password', dest="vaultPassword", type=RegExp)
