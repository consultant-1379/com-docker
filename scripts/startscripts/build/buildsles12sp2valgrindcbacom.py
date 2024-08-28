from build import Build

class BuildSles12Sp2ValgrindCbaCom(Build):

    os = "sles12sp2"
    compiler = "valgrind"
    repo = "com"
    target = "cbavalgrind"
    name = "SLES12 SP2 Valgrind CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
    buildDir = "/build"
