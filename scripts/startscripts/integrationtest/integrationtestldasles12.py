from integrationtestlda import IntegrationTestLda


class IntegrationTestLdaSles12(IntegrationTestLda):

    os = "sles12"
    name = "SLES12 lda Integration Test"
    target = "lda"
    _teImageName = "armdocker.rnd.ericsson.se/cba-com/vagrant/lda/cluster"
    _sutImageName = "armdocker.rnd.ericsson.se/cba-com/vagrant/com/lda/box"
