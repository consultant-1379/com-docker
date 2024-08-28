from codechecker import CodeChecker


class BuildSles12Sp5CodeCheckerMafMain(CodeChecker):

    os = "sles12sp5"
    compiler = "native"
    repo = "maf-main"
    target = "mafmain"
    name = "SLES12 SP5 Native CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
    buildDir = "/build/maf-build"
