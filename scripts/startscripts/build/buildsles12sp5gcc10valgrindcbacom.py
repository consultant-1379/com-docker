from build import Build

class BuildSles12Sp5gcc10ValgrindCbaCom(Build):

    os = "sles12sp5gcc10"
    compiler = "valgrind"
    repo = "com"
    target = "cbavalgrind"
    name = "SLES12 SP5 gcc10 Valgrind CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
    buildDir = "/build"
