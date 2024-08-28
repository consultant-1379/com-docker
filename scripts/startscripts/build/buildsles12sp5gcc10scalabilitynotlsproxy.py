from buildsles12sp5gcc10scalability import BuildSles12Sp5gcc10Scalability

class BuildSles12Sp5gcc10ScalabilityNoTlsProxy(BuildSles12Sp5gcc10Scalability):

    without = "tlsproxy"
    target = "comscalabilitynotlsproxy"
    wostr = "TLS Proxy"
