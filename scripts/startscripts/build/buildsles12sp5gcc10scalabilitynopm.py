from buildsles12sp5gcc10scalability import BuildSles12Sp5gcc10Scalability


class BuildSles12Sp5gcc10ScalabilityNoPM(BuildSles12Sp5gcc10Scalability):

    without = "pm"
    target = "comscalabilitynopm"
    wostr = "PM"
