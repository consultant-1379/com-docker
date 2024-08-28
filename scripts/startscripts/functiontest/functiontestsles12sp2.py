from functiontest import FunctionTest


class FunctionTestSles12sp2(FunctionTest):

    os = "sles12sp2"
    compiler = "native"

    def __init__(self):

        FunctionTest.__init__(self)
        self.set_path(self.compiler, self.os)
        self._teImageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
        self._sutImageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/sut"
        self._filesToCopy = {
                              'te' : ["/build/com-build/gen"],
                              'sut': ["/var/log/messages"]
                            }

    def execute(self, args):
        print "Starting the SLES12 SP2 function test"
        return self._run(["functiontest"], args)
