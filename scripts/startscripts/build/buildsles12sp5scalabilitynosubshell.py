from buildsles12sp5scalability import BuildSles12Sp5Scalability


class BuildSles12Sp5ScalabilityNoSubshell(BuildSles12Sp5Scalability):

    without = "subshell"
    target = "comscalabilitynosubshell"
    wostr = "Subshell"
