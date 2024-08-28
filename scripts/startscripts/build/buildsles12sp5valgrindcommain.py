from build import Build


class BuildSles12Sp5ValgrindComMain(Build):

    os = "sles12sp5"
    compiler = "valgrind"
    repo = "com-main"
    target = "commainvalgrind"
    name = "SLES12 SP5 Valgrind"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
