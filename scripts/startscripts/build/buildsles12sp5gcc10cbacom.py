from build import Build


class BuildSles12Sp5gcc10CbaCom(Build):

    os = "sles12sp5gcc10"
    compiler = "native"
    repo = "com"
    target = "cba"
    name = "SLES12 SP5 gcc10 CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
    buildDir = "/build"
