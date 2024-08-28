from build import Build


class BuildSles12Sp5gcc10DxCoverageComMain(Build):

    os = "sles12sp5gcc10dx"
    compiler = "coverage"
    repo = "com-main"
    target = "commaincoverage"
    name = "SLES12 SP5 gcc10 DX Coverage"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"
