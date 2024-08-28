from buildsles12sp5gcc10scalability import BuildSles12Sp5gcc10Scalability


class BuildSles12Sp5gcc10ScalabilityNoNC(BuildSles12Sp5gcc10Scalability):

    without = "nc"
    target = "comscalabilitynonc"
    wostr = "NC"
