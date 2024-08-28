from build import Build


class BuildSles12Sp5Cpp11ComMain(Build):

    os = "sles12sp5"
    compiler = "cpp11"
    repo = "com-main"
    target = "commain"
    name = "SLES12 SP5 Cpp11"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/cpp11/build"
