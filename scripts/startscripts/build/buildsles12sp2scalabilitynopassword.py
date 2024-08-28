from buildsles12sp2scalability import BuildSles12Sp2Scalability


class BuildSles12Sp2ScalabilityNoPassword(BuildSles12Sp2Scalability):

    without = "password"
    target = "comscalabilitynopassword"
    wostr = "Password"
