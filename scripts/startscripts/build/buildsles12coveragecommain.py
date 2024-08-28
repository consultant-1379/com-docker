from build import Build

class BuildSles12CoverageComMain(Build):

    os = "sles12"
    compiler = "coverage"
    repo = "com-main"
    target = "commaincoverage"
    name = "SLES12 Coverage"
    image= "armdocker.rnd.ericsson.se/cba-com/sles12/build"
