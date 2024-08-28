from build import Build


class BuildSles12Sp2CbaCom(Build):

    os = "sles12sp2"
    compiler = "native"
    repo = "com"
    target = "cba"
    name = "SLES12 SP2 CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
    buildDir = "/build"
