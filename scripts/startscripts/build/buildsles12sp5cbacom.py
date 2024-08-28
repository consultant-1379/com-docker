from build import Build


class BuildSles12Sp5CbaCom(Build):

    os = "sles12sp5"
    compiler = "native"
    repo = "com"
    target = "cba"
    name = "SLES12 SP5 CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
    buildDir = "/build"
