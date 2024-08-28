from buildsles12sp5scalability import BuildSles12Sp5Scalability


class BuildSles12Sp5ScalabilityNoNC(BuildSles12Sp5Scalability):

    without = "nc"
    target = "comscalabilitynonc"
    wostr = "NC"
