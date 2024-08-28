from functiontest import FunctionTest


class FunctionTestSles12RcsPpc(FunctionTest):

    os = "sles12"
    compiler = "rcs-ppc"

    def __init__(self):

        FunctionTest.__init__(self)
        self.set_path(self.compiler, self.os)
        self._teImageName = "armdocker.rnd.ericsson.se/cba-com/rcs/powerpc/build"
        self._filesToCopy = {
                              'te' : ["/build/com-build/gen"]
                            }

    def execute(self, args):
        print "Starting the SLES12 RCS-PPC function test"
        return self._run(["functiontest"], args)
