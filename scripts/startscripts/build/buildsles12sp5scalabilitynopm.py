from buildsles12sp5scalability import BuildSles12Sp5Scalability


class BuildSles12Sp5ScalabilityNoPM(BuildSles12Sp5Scalability):

    without = "pm"
    target = "comscalabilitynopm"
    wostr = "PM"
