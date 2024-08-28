from codechecker import CodeChecker


class BuildSles12Sp5gcc10CodeCheckerComMain(CodeChecker):

    os = "sles12sp5gcc10"
    compiler = "native"
    repo = "com-main"
    target = "commain"
    name = "SLES12 SP5 gcc10 Native CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
