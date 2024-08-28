from build import Build


class BuildRcsAarch64gcc10(Build):

    os = "sles12sp5gcc10"
    compiler = "rcs-aarch64"
    repo = "com-main"
    target = "commainrcsaarch64"
    name = "RCS AARCH64"
    image = "armdocker.rnd.ericsson.se/cba-com/rcs/aarch64gcc10/build"

