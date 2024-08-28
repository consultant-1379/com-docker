from codechecker import CodeChecker


class BuildSles12CodeCheckerComMain(CodeChecker):

    os = "sles12"
    compiler = "native"
    repo = "com-main"
    target = "commain"
    name = "SLES12 Native CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
