from build import Build


class BuildSles12Sp2CoverageComMain(Build):

    os = "sles12sp2"
    compiler = "coverage"
    repo = "com-main"
    target = "commaincoverage"
    name = "SLES12 SP2 Coverage"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp2/build"
