from buildsles12sp5gcc10scalability import BuildSles12Sp5gcc10Scalability


class BuildSles12Sp5gcc10ScalabilityNoFM(BuildSles12Sp5gcc10Scalability):

    without = "fm"
    target = "comscalabilitynofm"
    wostr = "FM"
