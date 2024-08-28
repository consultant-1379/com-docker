from build import Build


class BuildSles12Sp5gcc10DxValgrindComMain(Build):

    os = "sles12sp5gcc10dx"
    compiler = "valgrind"
    repo = "com-main"
    target = "commainvalgrind"
    name = "SLES12 SP5 gcc10 DX Valgrind"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"
