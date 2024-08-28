from build import Build


class BuildSles12Sp5CoverageComMain(Build):

    os = "sles12sp5"
    compiler = "coverage"
    repo = "com-main"
    target = "commaincoverage"
    name = "SLES12 SP5 Coverage"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
