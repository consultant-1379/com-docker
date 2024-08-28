from build import Build

class BuildSles12Sp5ValgrindCbaCom(Build):

    os = "sles12sp5"
    compiler = "valgrind"
    repo = "com"
    target = "cbavalgrind"
    name = "SLES12 SP5 Valgrind CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
    buildDir = "/build"
