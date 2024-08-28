from build import Build


class BuildRcsAarch64gcc10Dx(Build):

    os = "sles12sp5gcc10dx"
    compiler = "rcs-aarch64"
    repo = "com-main"
    target = "commainrcsaarch64"
    name = "RCS AARCH64"
    image = "armdocker.rnd.ericsson.se/cba-com/rcs/aarch64gcc10dx/build"

