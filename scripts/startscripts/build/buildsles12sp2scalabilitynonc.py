from buildsles12sp2scalability import BuildSles12Sp2Scalability


class BuildSles12Sp2ScalabilityNoNC(BuildSles12Sp2Scalability):

    without = "nc"
    target = "comscalabilitynonc"
    wostr = "NC"
