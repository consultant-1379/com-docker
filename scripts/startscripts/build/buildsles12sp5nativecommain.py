from build import Build


class BuildSles12Sp5NativeComMain(Build):

    os = "sles12sp5"
    compiler = "native"
    repo = "com-main"
    target = "commain"
    name = "SLES12 SP5 Native"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
