from build import Build


class BuildSles12Sp2Cpp11ComMain(Build):

    os = "sles12sp2"
    compiler = "cpp11"
    repo = "com-main"
    target = "commain"
    name = "SLES12 SP2 Cpp11"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/cpp11/build"
