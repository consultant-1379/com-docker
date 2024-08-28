from comunittest import COMUnitTest

class UnitTestSles12Sp5(COMUnitTest):

    def __init__(self):

        COMUnitTest.__init__(self)
        self.os = "sles12sp5"
        self.compiler = "native"
        self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
        self._filesToCopy = ["report"]
        self._fileDestination = "."
        self.set_path(self.os, self.compiler)
