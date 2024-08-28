from build import Build


class BuildSles12Sp5gcc10NativeFmCore(Build):

    os = "sles12sp5gcc10"
    compiler = "native"
    repo = "fm-core"
    target = "fmcore"
    name = "SLES12 SP5 gcc10 Native"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
    buildDir = "/build/fmcore-build"
