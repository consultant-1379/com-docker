from buildsles12sp2scalability import BuildSles12Sp2Scalability


class BuildSles12Sp2ScalabilityNoAccessMgmt(BuildSles12Sp2Scalability):

    without = "accessmgmt"
    target = "comscalabilitynoaccessmgmt"
    wostr = "Access Management"
