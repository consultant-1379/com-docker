from codechecker import CodeChecker


class BuildSles12Sp2CodeCheckerComMain(CodeChecker):

    os = "sles12sp2"
    compiler = "native"
    repo = "com-main"
    target = "commain"
    name = "SLES12 SP2 Native CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
