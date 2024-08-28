from buildsles12sp5scalability import BuildSles12Sp5Scalability


class BuildSles12Sp5ScalabilityNoAccessMgmt(BuildSles12Sp5Scalability):

    without = "accessmgmt"
    target = "comscalabilitynoaccessmgmt"
    wostr = "Access Management"
