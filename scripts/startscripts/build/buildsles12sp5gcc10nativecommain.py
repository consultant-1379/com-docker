from build import Build


class BuildSles12Sp5gcc10NativeComMain(Build):

    os = "sles12sp5gcc10"
    compiler = "native"
    repo = "com-main"
    target = "commain"
    name = "SLES12 SP5 gcc10 Native"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
