from build import Build


class BuildSles12Sp5NativeFmCore(Build):

    os = "sles12sp5"
    compiler = "native"
    repo = "fm-core"
    target = "fmcore"
    name = "SLES12 SP5 Native"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
    buildDir = "/build/fmcore-build"
