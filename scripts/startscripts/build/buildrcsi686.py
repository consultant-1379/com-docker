from build import Build


class BuildRcsI686(Build):

    os = "sles12"
    compiler = "rcs-i686"
    repo = "com-main"
    target = "commainrcsi686"
    name = "RCS i686"
    image = "armdocker.rnd.ericsson.se/cba-com/rcs/i686/build"
