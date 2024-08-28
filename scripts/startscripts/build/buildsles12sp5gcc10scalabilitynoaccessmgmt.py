from buildsles12sp5gcc10scalability import BuildSles12Sp5gcc10Scalability


class BuildSles12Sp5gcc10ScalabilityNoAccessMgmt(BuildSles12Sp5gcc10Scalability):

    without = "accessmgmt"
    target = "comscalabilitynoaccessmgmt"
    wostr = "Access Management"
