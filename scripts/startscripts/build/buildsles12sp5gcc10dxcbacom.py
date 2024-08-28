from build import Build


class BuildSles12Sp5gcc10DxCbaCom(Build):

    os = "sles12sp5gcc10dx"
    compiler = "native"
    repo = "com"
    target = "cba"
    name = "SLES12 SP5 gcc10 DX CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"
    buildDir = "/build"
