from codechecker import CodeChecker


class BuildSles12Sp5gcc10DxCodeCheckerCbaCom(CodeChecker):

    os = "sles12sp5gcc10dx"
    compiler = "native"
    repo = "com"
    target = "cba"
    name = "SLES12 SP5 gcc10 DX CBA CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"
    buildDir = "/build"
