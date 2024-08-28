from codechecker import CodeChecker


class BuildSles12CodeCheckerCbaCom(CodeChecker):

    os = "sles12"
    compiler = "native"
    repo = "com"
    target = "cba"
    name = "SLES12 CBA CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
    buildDir = "/build"
