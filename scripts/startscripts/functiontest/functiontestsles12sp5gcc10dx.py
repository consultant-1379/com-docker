from functiontest import FunctionTest


class FunctionTestSles12sp5gcc10Dx(FunctionTest):

    os = "sles12sp5gcc10dx"
    compiler = "native"

    def __init__(self):

        FunctionTest.__init__(self)
        self.set_path(self.compiler, self.os)
        self._teImageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"
        self._sutImageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/sut"
        self._filesToCopy = {
                              'te' : ["/build/com-build/gen"],
                              'sut': ["/var/log/messages"]
                            }

    def execute(self, args):
        print "Starting the SLES12 SP5 gcc10 DX function test"
        return self._run(["functiontest"], args)
