from build import Build


class BuildSles12NativeComMain(Build):

    os = "sles12"
    compiler = "native"
    repo = "com-main"
    target = "commain"
    name = "SLES12 Native"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
