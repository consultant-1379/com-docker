from performancetest import PerformanceTest


class StabilitySles12Sp5(PerformanceTest):

    os = "sles12sp5"
    testType = "stability"

    def __init__(self):

        PerformanceTest.__init__(self)
        self.set_path(self.os, self.testType)
        self._teImageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
        self._sutImageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/sut"
        self._filesToCopy = ["/test/pt/doc"]

    def execute(self, args):
        print "Starting the SLES12 SP5 Stability test"
        return self._run(["performancetest",
                        "--test-duration", args["testDuration"]
                        ], args)
