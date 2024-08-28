from buildsles12sp5gcc10dxscalability import BuildSles12Sp5gcc10DxScalability


class BuildSles12Sp5gcc10DxScalabilityNoFM(BuildSles12Sp5gcc10DxScalability):

    without = "fm"
    target = "comscalabilitynofm"
    wostr = "FM"
