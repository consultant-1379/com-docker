from build import Build


class BuildSles12Sp5gcc10CoverageComMain(Build):

    os = "sles12sp5gcc10"
    compiler = "coverage"
    repo = "com-main"
    target = "commaincoverage"
    name = "SLES12 SP5 gcc10 Coverage"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10/build"
