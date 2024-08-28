from fmcoreunittest import FmCoreUnitTest

class UnitTestSles12FmCore(FmCoreUnitTest):

    def __init__(self):

        FmCoreUnitTest.__init__(self)
        self.os = "sles12"
        self.compiler = "native"
        self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
        self._filesToCopy = ["report"]
        self._fileDestination = "."
        self.set_path(self.os, self.compiler)
