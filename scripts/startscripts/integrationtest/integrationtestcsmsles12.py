import sys
from integrationtestcsm import IntegrationTestCsm


class IntegrationTestCsmSles12(IntegrationTestCsm):

    os = "sles12"
    name = "SLES12 Integration Test"
    target = "csm"
    if "comsa-" not in str(sys.argv):
        _teImageName = "armdocker.rnd.ericsson.se/cba-com/vagrant/cluster"
        _sutImageName = "armdocker.rnd.ericsson.se/cba-com/vagrantbuild/esmbox"
    else:
        _teImageName = "armdocker.rnd.ericsson.se/cba-com/comsavagrant/cluster"
        _sutImageName = "armdocker.rnd.ericsson.se/cba-com/comsavagrantbuild/esmbox"
