from codechecker import CodeChecker


class BuildSles12Sp5CodeCheckerCbaCom(CodeChecker):

    os = "sles12sp5"
    compiler = "native"
    repo = "com"
    target = "cba"
    name = "SLES12 SP5 CBA CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
    buildDir = "/build"
