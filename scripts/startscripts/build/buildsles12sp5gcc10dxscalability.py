import os
from build import Build


class BuildSles12Sp5gcc10DxScalability(Build):

    os = "sles12sp5gcc10dx"
    compiler = "native"
    repo = "com-main"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"

    def arguments(self, parser):
        Build.arguments(self, parser)
        parser.add_argument('--without', dest="without")

    def set_path(self, os, repo, compiler):
        Build.set_path(self, os, repo, compiler)
        self.add_argument("without", self.without)

    def __init__(self):
        Build.__init__(self)

        # Make sure the test packages have same folder structure, set build-dir to /build/com-build
        self.__builddir = "/build/com-build"

        self._imageName = self.image
        self._filesToCopy = [os.path.join(self.__builddir, "dist")]
        self._fileDestination = "."

    def execute(self, args):
        print ("Starting SLES 12 SP5 gcc10 DX Native build - without " + self.wostr)
        return self._runBuild(["build",
                               "--commit", args["commit"],
                               "--repo", self.repo,
                               "--build-type", self.target,
                               "--mirror-path", "/mirrors",
                               "--build-dir", self.__builddir,
                               ], args)
