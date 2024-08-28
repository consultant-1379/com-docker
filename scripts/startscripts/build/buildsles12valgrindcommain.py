from build import Build


class BuildSles12ValgrindComMain(Build):

    os = "sles12"
    compiler = "valgrind"
    repo = "com-main"
    target = "commainvalgrind"
    name = "SLES12 Valgrind"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
