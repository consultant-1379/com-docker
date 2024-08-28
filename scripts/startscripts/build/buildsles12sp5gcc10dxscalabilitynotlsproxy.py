from buildsles12sp5gcc10dxscalability import BuildSles12Sp5gcc10DxScalability

class BuildSles12Sp5gcc10DxScalabilityNoTlsProxy(BuildSles12Sp5gcc10DxScalability):

    without = "tlsproxy"
    target = "comscalabilitynotlsproxy"
    wostr = "TLS Proxy"
