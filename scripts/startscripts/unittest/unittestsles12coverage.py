from comunittest import COMUnitTest

class UnitTestSles12Coverage(COMUnitTest):

    def __init__(self):
        COMUnitTest.__init__(self)
        self.os = "sles12"
        self.compiler = "coverage"
        self._imageName = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
        self._filesToCopy = ["report"]
        self._fileDestination = "."
        self.set_path(self.os, self.compiler)
