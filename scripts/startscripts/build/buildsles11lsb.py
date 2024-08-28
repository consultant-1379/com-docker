from build import Build


class BuildSles11LsbComMain(Build):

    os = "sles11"
    compiler = "lsb"
    repo = "com-main"
    target = "commainlsb"
    name = "SLES11 LSB"
    image = "armdocker.rnd.ericsson.se/cba-com/sles11sp3/lsb/build"
