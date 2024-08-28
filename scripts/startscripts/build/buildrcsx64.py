from build import Build

class BuildRcsX64(Build):

    os = "sles12"
    compiler = "rcs-x64"
    repo = "com-main"
    target = "commainrcsx64"
    name = "RCS X64"
    image = "armdocker.rnd.ericsson.se/cba-com/rcs/x64/build"
