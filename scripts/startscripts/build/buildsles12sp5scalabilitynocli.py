from buildsles12sp5scalability import BuildSles12Sp5Scalability


class BuildSles12Sp5ScalabilityNoCli(BuildSles12Sp5Scalability):

    without = "cli"
    target = "comscalabilitynocli"
    wostr = "CLI"
