from build import Build


class BuildRhel6CbaCom(Build):

    os = "rhel6"
    compiler = "native"
    repo = "com"
    target = "cbaptoff"
    name = "RHEL6 CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/rhel6/build"
    buildDir = "/build"
