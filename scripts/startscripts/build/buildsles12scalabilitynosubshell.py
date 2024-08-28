from buildsles12scalability import BuildSles12Scalability


class BuildSles12ScalabilityNoSubshell(BuildSles12Scalability):

    without = "subshell"
    target = "comscalabilitynosubshell"
    wostr = "Subshell"
