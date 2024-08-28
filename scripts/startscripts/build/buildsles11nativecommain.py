from build import Build


class BuildSles11NativeComMain(Build):

    os = "sles11"
    compiler = "native"
    repo = "com-main"
    target = "commain"
    name = "SLES11 Native"
    image = "armdocker.rnd.ericsson.se/cba-com/sles11sp3/build"
