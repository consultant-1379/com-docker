from build import Build


class BuildSles12Sp2ValgrindComMain(Build):

    os = "sles12sp2"
    compiler = "valgrind"
    repo = "com-main"
    target = "commainvalgrind"
    name = "SLES12 SP2 Valgrind"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
