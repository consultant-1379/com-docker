from build import Build


class BuildSles12Sp5AuditLogCbaCom(Build):

    os = "sles12sp5auditlog"
    compiler = "native"
    repo = "com"
    target = "commainrcsaudit"
    name = "SLES12 SP5 CBA"
    image = "armdocker.rnd.ericsson.se/cba-com/sles12sp5/build"
    buildDir = "/build"

