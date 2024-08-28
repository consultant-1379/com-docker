from build import Build

class BuildRcsX64gcc10(Build):

    os = "sles12sp5gcc10"
    compiler = "rcs-x64"
    repo = "com-main"
    target = "commainrcsx64"
    name = "RCS X64"
    image = "armdocker.rnd.ericsson.se/cba-com/rcs/x64gcc10/build"
