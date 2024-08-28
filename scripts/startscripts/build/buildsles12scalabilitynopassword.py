from buildsles12scalability import BuildSles12Scalability


class BuildSles12ScalabilityNoPassword(BuildSles12Scalability):

    without = "password"
    target = "comscalabilitynopassword"
    wostr = "Password"
