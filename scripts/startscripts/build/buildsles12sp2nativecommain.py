from build import Build


class BuildSles12Sp2NativeComMain(Build):

    os = "sles12sp2"
    compiler = "native"
    repo = "com-main"
    target = "commain"
    name = "SLES12 SP2 Native"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
