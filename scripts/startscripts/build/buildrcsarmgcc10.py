from build import Build


class BuildRcsArmgcc10(Build):

    os = "sles12sp5gcc10"
    compiler = "rcs-arm"
    repo = "com-main"
    target = "commainrcsarm"
    name = "RCS ARM"
    image = "armdocker.rnd.ericsson.se/cba-com/rcs/armgcc10/build"
