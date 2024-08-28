from buildsles12sp2scalability import BuildSles12Sp2Scalability

class BuildSles12Sp2ScalabilityNoTlsProxy(BuildSles12Sp2Scalability):

    without = "tlsproxy"
    target = "comscalabilitynotlsproxy"
    wostr = "TLS Proxy"
