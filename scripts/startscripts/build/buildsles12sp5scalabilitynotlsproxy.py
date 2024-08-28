from buildsles12sp5scalability import BuildSles12Sp5Scalability

class BuildSles12Sp5ScalabilityNoTlsProxy(BuildSles12Sp5Scalability):

    without = "tlsproxy"
    target = "comscalabilitynotlsproxy"
    wostr = "TLS Proxy"
