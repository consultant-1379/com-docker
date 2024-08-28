from build import Build

class BuildSles12ValgrindCbaCom(Build):

    os = "sles12"
    compiler = "valgrind"
    repo = "com"
    target = "cbavalgrind"
    name = "SLES12 Valgrind CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
    buildDir = "/build"
