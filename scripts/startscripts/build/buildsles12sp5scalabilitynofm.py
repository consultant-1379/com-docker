from buildsles12sp5scalability import BuildSles12Sp5Scalability


class BuildSles12Sp5ScalabilityNoFM(BuildSles12Sp5Scalability):

    without = "fm"
    target = "comscalabilitynofm"
    wostr = "FM"
