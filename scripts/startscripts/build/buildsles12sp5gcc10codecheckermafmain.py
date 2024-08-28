from codechecker import CodeChecker


class BuildSles12Sp5gcc10CodeCheckerMafMain(CodeChecker):

    os = "sles12sp5gcc10"
    compiler = "native"
    repo = "maf-main"
    target = "mafmain"
    name = "SLES12 SP5 gcc10 Native CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
    buildDir = "/build/maf-build"
