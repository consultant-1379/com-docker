from build import Build


class BuildSles12Sp5Gcc10DxAuditLogCbaCom(Build):

    os = "sles12sp5gcc10dxauditlog"
    compiler = "native"
    repo = "com"
    target = "commainrcsaudit"
    name = "SLES12 SP5 GCC10 DX CBA WITH AUDIT AND WRAPPING"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5gcc10dx/build"
    buildDir = "/build"

