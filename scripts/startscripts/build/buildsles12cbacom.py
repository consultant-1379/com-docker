from build import Build


class BuildSles12CbaCom(Build):

    os = "sles12"
    compiler = "native"
    repo = "com"
    target = "cba"
    name = "SLES12 CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
    buildDir = "/build"
