from build import Build


class BuildSles12Sp5gcc10DxNativeFmCore(Build):

    os = "sles12sp5gcc10dx"
    compiler = "native"
    repo = "fm-core"
    target = "fmcore"
    name = "SLES12 SP5 gcc10 DX Native"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"
    buildDir = "/build/fmcore-build"
