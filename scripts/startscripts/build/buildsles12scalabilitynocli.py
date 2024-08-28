from buildsles12scalability import BuildSles12Scalability


class BuildSles12ScalabilityNoCli(BuildSles12Scalability):

    without = "cli"
    target = "comscalabilitynocli"
    wostr = "CLI"
