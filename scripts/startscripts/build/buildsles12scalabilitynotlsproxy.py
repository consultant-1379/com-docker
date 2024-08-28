from buildsles12scalability import BuildSles12Scalability

class BuildSles12ScalabilityNoTlsProxy(BuildSles12Scalability):

    without = "tlsproxy"
    target = "comscalabilitynotlsproxy"
    wostr = "TLS Proxy"
