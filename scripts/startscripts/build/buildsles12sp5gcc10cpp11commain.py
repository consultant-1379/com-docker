from build import Build


class BuildSles12Sp5gcc10Cpp11ComMain(Build):

    os = "sles12sp5gcc10"
    compiler = "cpp11"
    repo = "com-main"
    target = "commain"
    name = "SLES12 SP5 gcc10 Cpp11"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/cpp11/build"
