from functiontest import FunctionTest


class FunctionTestSles11sp3Lsb(FunctionTest):

    os = "sles11"
    compiler = "lsb"

    def __init__(self):

        FunctionTest.__init__(self)
        self.set_path(self.compiler, self.os)
        self._teImageName = "armdocker.rnd.ericsson.se/cba-com/sles11sp3/lsb/build"
        self._sutImageName = "armdocker.rnd.ericsson.se/cba-com/sles11sp3/lsb/sut"
        self._filesToCopy = {
                              'te' : ["/build/com-build/gen"],
                              'sut': ["/var/log/messages"]
                            }

    def execute(self, args):
        print("Starting the SLES11 SP3 LSB function test")
        return self._run(["functiontest"], args)
