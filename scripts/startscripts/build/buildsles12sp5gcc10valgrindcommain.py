from build import Build


class BuildSles12Sp5gcc10ValgrindComMain(Build):

    os = "sles12sp5gcc10"
    compiler = "valgrind"
    repo = "com-main"
    target = "commainvalgrind"
    name = "SLES12 SP5 gcc10 Valgrind"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
