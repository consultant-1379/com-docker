from buildsles12scalability import BuildSles12Scalability


class BuildSles12ScalabilityNoAccessMgmt(BuildSles12Scalability):

    without = "accessmgmt"
    target = "comscalabilitynoaccessmgmt"
    wostr = "Access Management"
