from build import Build


class BuildRcsArmgcc10Dx(Build):

    os = "sles12sp5gcc10dx"
    compiler = "rcs-arm"
    repo = "com-main"
    target = "commainrcsarm"
    name = "RCS ARM"
    image = "armdocker.rnd.ericsson.se/cba-com/rcs/armgcc10dx/build"
