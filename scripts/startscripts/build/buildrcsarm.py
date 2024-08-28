from build import Build


class BuildRcsArm(Build):

    os = "sles12"
    compiler = "rcs-arm"
    repo = "com-main"
    target = "commainrcsarm"
    name = "RCS ARM"
    image = "armdocker.rnd.ericsson.se/cba-com/rcs/arm/build"
