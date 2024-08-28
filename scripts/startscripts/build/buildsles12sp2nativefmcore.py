from build import Build


class BuildSles12Sp2NativeFmCore(Build):

    os = "sles12sp2"
    compiler = "native"
    repo = "fm-core"
    target = "fmcore"
    name = "SLES12 SP2 Native"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
    buildDir = "/build/fmcore-build"
