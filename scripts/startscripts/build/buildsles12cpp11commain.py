from build import Build


class BuildSles12Cpp11ComMain(Build):

    os = "sles12"
    compiler = "cpp11"
    repo = "com-main"
    target = "commain"
    name = "SLES12 Cpp11"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/cpp11/build"
