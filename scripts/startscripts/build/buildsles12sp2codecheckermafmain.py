from codechecker import CodeChecker


class BuildSles12Sp2CodeCheckerMafMain(CodeChecker):

    os = "sles12sp2"
    compiler = "native"
    repo = "maf-main"
    target = "mafmain"
    name = "SLES12 SP2 Native CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
    buildDir = "/build/maf-build"
