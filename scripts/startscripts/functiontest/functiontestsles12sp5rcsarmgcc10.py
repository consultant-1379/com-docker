from functiontest import FunctionTest


class FunctionTestSles12sp5RcsArmgcc10(FunctionTest):

    os = "sles12sp5gcc10"
    compiler = "rcs-arm"

    def __init__(self):

        FunctionTest.__init__(self)
        self.set_path(self.compiler, self.os)
        self._teImageName = "armdocker.rnd.ericsson.se/cba-com/rcs/armgcc10/build"
        self._filesToCopy = {
                              'te' : ["/build/com-build/gen"]
                            }

    def execute(self, args):
        print "Starting the SLES12SP5 gcc10 RCS-ARM function test"
        return self._run(["functiontest"], args)
