from buildsles12sp5gcc10dxscalability import BuildSles12Sp5gcc10DxScalability


class BuildSles12Sp5gcc10DxScalabilityNoAccessMgmt(BuildSles12Sp5gcc10DxScalability):

    without = "accessmgmt"
    target = "comscalabilitynoaccessmgmt"
    wostr = "Access Management"
