from buildsles12sp5gcc10dxscalability import BuildSles12Sp5gcc10DxScalability


class BuildSles12Sp5gcc10DxScalabilityNoPM(BuildSles12Sp5gcc10DxScalability):

    without = "pm"
    target = "comscalabilitynopm"
    wostr = "PM"
