from codechecker import CodeChecker


class BuildSles12CodeCheckerMafMain(CodeChecker):

    os = "sles12"
    compiler = "native"
    repo = "maf-main"
    target = "mafmain"
    name = "SLES12 Native CodeChecker"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
    buildDir = "/build/maf-build"
