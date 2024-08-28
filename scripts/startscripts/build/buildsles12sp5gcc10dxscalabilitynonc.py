from buildsles12sp5gcc10dxscalability import BuildSles12Sp5gcc10DxScalability


class BuildSles12Sp5gcc10DxScalabilityNoNC(BuildSles12Sp5gcc10DxScalability):

    without = "nc"
    target = "comscalabilitynonc"
    wostr = "NC"
