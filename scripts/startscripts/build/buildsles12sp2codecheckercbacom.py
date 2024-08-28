from codechecker import CodeChecker


class BuildSles12Sp2CodeCheckerCbaCom(CodeChecker):

    os = "sles12sp2"
    compiler = "native"
    repo = "com"
    target = "cba"
    name = "SLES12 SP2 CBA CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
    buildDir = "/build"
