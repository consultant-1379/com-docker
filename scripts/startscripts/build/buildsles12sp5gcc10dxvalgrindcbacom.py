from build import Build

class BuildSles12Sp5gcc10DxValgrindCbaCom(Build):

    os = "sles12sp5gcc10dx"
    compiler = "valgrind"
    repo = "com"
    target = "cbavalgrind"
    name = "SLES12 SP5 gcc10 DX Valgrind CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"
    buildDir = "/build"
