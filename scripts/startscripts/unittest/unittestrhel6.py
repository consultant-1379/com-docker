from comunittest import COMUnitTest

class UnitTestRhel6(COMUnitTest):

    def __init__(self):

        COMUnitTest.__init__(self)
        self.os = "rhel6"
        self.compiler = "native"
        self._imageName = "armdocker.rnd.ericsson.se/cba-com/rhel6/build"
        self._filesToCopy = ["report"]
        self._fileDestination = "."
        self.set_path(self.os, self.compiler)
