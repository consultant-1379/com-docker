import sys
sys.path.append("/usr/src/scripts/startscripts/build/")
from build import Build

class UpdateSubModuleCbaCom(Build):

    os = "sles12"
    compiler = "native"
    repo = "com"
    target = "updatesubmodule"
    name = "SLES12 CBA COM Sub Module"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12/build"
    buildDir = "/build"
