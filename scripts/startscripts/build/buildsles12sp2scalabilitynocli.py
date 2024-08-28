from buildsles12sp2scalability import BuildSles12Sp2Scalability


class BuildSles12Sp2ScalabilityNoCli(BuildSles12Sp2Scalability):

    without = "cli"
    target = "comscalabilitynocli"
    wostr = "CLI"
