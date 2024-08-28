from build import Build


class BuildRcsPpc(Build):

    os = "sles12"
    compiler = "rcs-ppc"
    repo = "com-main"
    target = "commainrcsppc"
    name = "RCS PowerPC"
    image = "armdocker.rnd.ericsson.se/cba-com/rcs/powerpc/build"
