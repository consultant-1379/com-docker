from buildsles12scalability import BuildSles12Scalability


class BuildSles12ScalabilityNoNC(BuildSles12Scalability):

    without = "nc"
    target = "comscalabilitynonc"
    wostr = "NC"
