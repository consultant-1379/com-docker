from codechecker import CodeChecker


class BuildSles12Sp5gcc10CodeCheckerCbaCom(CodeChecker):

    os = "sles12sp5gcc10"
    compiler = "native"
    repo = "com"
    target = "cba"
    name = "SLES12 SP5 gcc10 CBA CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
    buildDir = "/build"
