from buildsles12sp2scalability import BuildSles12Sp2Scalability


class BuildSles12Sp2ScalabilityNoFM(BuildSles12Sp2Scalability):

    without = "fm"
    target = "comscalabilitynofm"
    wostr = "FM"
