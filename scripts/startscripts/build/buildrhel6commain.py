from build import Build


class BuildRhel6ComMain(Build):

    os = "rhel6"
    compiler = "native"
    repo = "com-main"
    target = "commain"
    name = "RHEL6 Native"
    image = "armdocker.rnd.ericsson.se/cba-com/rhel6/build"
