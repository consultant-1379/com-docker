#!/usr/bin/env python3

from jproperties import Properties

'''
This class is used for reading and writing to the com_test.properties file
'''


class ComTestProperties:

    _propertyObject = Properties()

    def load(self, filename):
        self._fileObject = open(filename, "rb")
        self._propertyObject.load(self._fileObject, "utf-8")

    def store(self, filename):
        self._propertyObject.store(open(filename, "wb"), encoding="utf-8")

    def _set(self, name, value):
        self._propertyObject[name] = value

    def _get(self, name):
        value = self._propertyObject[name]
        return value.data

    def setComRemoteHost(self, value):
        self._set("com_remote_host", value)

    def setFmCoreRemoteHost(self, value):
        self._set("fm_core_remote_host", value)

    def setStartport(self, value):
        self._set("start_port", value)

    def setEndPort(self, value):
        self._set("end_port", value)

    def setPorts(self, value):
        self._set("ports", value)

    def setComRemoteHostInstallationType(self, value):
        self._set("com_remote_host_installation_type", value)

    def setComUser(self, value):
        self._set("com_user", value)

    def setComUserPassword(self, value):
        self._set("com_user_password", value)

    def setRootUser(self, value):
        self._set("root_user", value)

    def setRootUserPassword(self, value):
        self._set("root_user_password", value)

    def setUseFilem(self, value):
        self._set("use_filem", value)

    def setNetSnmpMajorVersion(self, value):
        self._set("FT_NetSNMPMajorVersion", value)

    def setComCmwSystemSC2Address(self, value):
        self._set("com_cmw_system_SC2_address", value)

    def setSecCertPackageDir(self, value):
        self._set("sec_cert_package_dir", value)

    def setSecLaPackageDir(self, value):
        self._set("sec_la_package_dir", value)

    def setSecAcsPackageDir(self, value):
        self._set("sec_acs_package_dir", value)

    def setSecSecMPackageDir(self, value):
        self._set("sec_secm_package_dir", value)

    def setSecLdapPackageDir(self, value):
        self._set("sec_ldap_package_dir", value)

    def setSecCryptoPackageDir(self, value):
        self._set("sec_crypto_package_dir", value)

    def setLdewSSdpPackageDir(self, value):
        self._set("ldews_sdp_package_dir", value)

    def setPmProducerSdp(self, value):
        self._set("pmproducer_app", value)

    def setPmProducerCampaign(self, value):
        self._set("pmproducer_campaign", value)

    def setComDeploymentTemplate(self, value):
        self._set("com_deployment_template", value)

    def setComBundleSdp(self, value):
        self._set("com_bundle_sdp", value)

    def setComDebugSdp(self, value):
        self._set("com_debug_sdp", value)

    def setUpPackageDir(self, value):
        self._set("up_file_location", value)

    def setResourcesDir(self, value):
        self._set("com_resources_dir", value)

    def setComSdpPnr(self, value):
        self._set("COM_SDP_PNR", value)

    def setBfuFromVersion(self, value):
        self._set("bfu_from_version", value)

    def setUpgradeBundlesDir(self, value):
        self._set("upgrade_bundles_dir", value)

    def setComRuntimePackageRepo(self, value):
        self._set("com_runtime_package_repository", value)

    def set(self, value):
        self._set("", value)

    def setValgrind(self, value):
        self._set("valgrind", value)

    def setValgrindPath(self, value):
        self._set("valgrind_log_parser", value)

    def setComsaTestDir(self, value):
        self._set("comsa_test_dir", value)

    def setComsaNtfSend(self, value):
        self._set("comsa_ntfsend_file", value)

    def setComUbuntuAddress(self, value):
        self._set("com_ubuntu_address", value)

    def setComVsftpdRpm(self, value):
        self._set("com_vsftpd_rpm", value)

    def setDeploymentType(self, value):
        self._set("deployment_type", value)

    def setClusterSize(self, value):
        self._set("cluster_size", value)
