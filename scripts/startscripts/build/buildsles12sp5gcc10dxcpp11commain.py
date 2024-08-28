from build import Build


class BuildSles12Sp5gcc10DxCpp11ComMain(Build):

    os = "sles12sp5gcc10dx"
    compiler = "cpp11"
    repo = "com-main"
    target = "commain"
    name = "SLES12 SP5 gcc10 DX Cpp11"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/cpp11/build"
