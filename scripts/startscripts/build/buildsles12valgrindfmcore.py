from build import Build


class BuildSles12ValgrindFmCore(Build):

    os = "sles12"
    compiler = "valgrind"
    repo = "fm-core"
    target = "fmcorevalgrind"
    name = "SLES12 Valgrind"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
    buildDir = "/build/fmcore-build"
