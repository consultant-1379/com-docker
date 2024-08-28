from buildsles12sp2scalability import BuildSles12Sp2Scalability


class BuildSles12Sp2ScalabilityNoPM(BuildSles12Sp2Scalability):

    without = "pm"
    target = "comscalabilitynopm"
    wostr = "PM"
