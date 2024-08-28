from build import Build

class BuildSles12CoverageFmCore(Build):

    os = "sles12"
    compiler = "coverage"
    repo = "fm-core"
    target = "fmcorecoverage"
    name = "SLES12 Coverage"
    image= "armdocker.rnd.ericsson.se/cba-com/sles12/build"
    buildDir = "/build/fmcore-build"
