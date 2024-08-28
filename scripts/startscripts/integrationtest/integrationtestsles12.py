from integrationtest import IntegrationTest


class IntegrationTestSles12(IntegrationTest):

    os = "sles12"
    target = "legacy"
    name = "SLES12 Integration Test"
    _teImageName = "armdocker.rnd.ericsson.se/cba-com/vagrant/cluster"
