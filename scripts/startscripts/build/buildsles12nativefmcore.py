from build import Build


class BuildSles12NativeFmCore(Build):

    os = "sles12"
    compiler = "native"
    repo = "fm-core"
    target = "fmcore"
    name = "SLES12 Native"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
    buildDir = "/build/fmcore-build"
