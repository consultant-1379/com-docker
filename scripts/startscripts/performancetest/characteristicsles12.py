from performancetest import PerformanceTest


class CharacteristicSles12(PerformanceTest):

    os = "sles12"
    testType = "characteristics"

    def __init__(self):

        PerformanceTest.__init__(self)
        self.set_path(self.os, self.testType)
        self._teImageName = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
        self._filesToCopy = ["/test/pt/doc"]

    def execute(self, args):
        print "Starting the SLES12 Characteristic test"
        return self._run(["performancetest",
                        ], args)
