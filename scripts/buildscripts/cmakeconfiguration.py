#!/usr/bin/env python

import sys


class CMakeConfiguration:

    __booleans = ["1", "0", "on", "off", "true", "false", "yes", "no"]

    def __init__(self, config):
        self.__config = {}
        if config:
            self._parseConfiguration(config)

    def _parseConfiguration(self, config):
        print config
        retval = {}
        for item in config:
            key, value = item.split("=")
            retval[key] = value
        self.__config = retval

    def add(self, option, value):
        self.__config[option] = value

    def generate(self):
        cmakeList = []
        for key, value in self.__config.items():
            try:
                cmakeList.append(getattr(self, key)(value))
            except AttributeError:
                print "option: " + key + " does not exist"
                sys.exit(1)
        return cmakeList

    def booleanOption(self, option, value):
        if value.lower() in self.__booleans:
            return "-D" + option + "=" + value.lower()
        return ""

    def stringOption(self, option, value):
        return "-D" + option + "=" + value

    def pm(self, value):
        return self.booleanOption("PM", value)

    def comversion(self, value):
        return self.stringOption("COM_VERSION", value)

    def fmcoreversion(self, value):
        return self.stringOption("FM_CORE_VERSION", value)

    def cba(self, value):
        return self.stringOption("CBA_PACKAGING", value)

    def toolchain(self, value):
        return self.stringOption("CMAKE_TOOLCHAIN_FILE", value)

    def verifybuild(self, value):
        return self.booleanOption("VERIFY_BUILD", value)

    def lsb(self, value):
        return self.booleanOption("COMPILING_FOR_LSB", value)

    def astyle(self, value):
        return self.booleanOption("USE_ASTYLE", value)

    def secacs(self, value):
        return self.booleanOption("SECACS", value)

    def coverage(self, value):
        return self.booleanOption("USE_COVERAGE", value)

    def valgrind(self, value):
        return self.booleanOption("VALGRIND", value)

    def pt(self, value):
        return self.booleanOption("PT", value)

    def fm(self, value):
        return self.booleanOption("FM", value)

    def cli(self, value):
        return self.booleanOption("CLI", value)

    def nc(self, value):
        return self.booleanOption("NETCONF", value)

    def subshell(self, value):
        return self.booleanOption("SUBSHELL", value)

    def ns(self, value):
        return self.booleanOption("NOTIFICATIONSERVICE", value)

    def filem(self, value):
        return self.booleanOption("USEFILEM", value)

    def accessmgmt(self, value):
        return self.booleanOption("ACCESSMGMT", value)

    def tlsproxy(self, value):
        return self.booleanOption("TLSPROXY", value)

    def tlsd(self, value):
        return self.booleanOption("TLSD", value)

    def comdepsdir(self, value):
        return self.stringOption("COM_DEPS_DIR", value)

    def comdeveloper(self, value):
        return self.booleanOption("COM_DEVELOPER", value)

    def stripdebuginfo(self, value):
        return self.booleanOption("STRIP_DEBUGINFO", value)

    def buildtype(self, value):
        return self.stringOption("CMAKE_BUILD_TYPE", value)

    def heapmonitor(self, value):
        return self.booleanOption("HEAP_MONITOR", value)

    def functiontest(self, value):
        return self.booleanOption("FT", value)

    def unittest(self, value):
        return self.booleanOption("UT", value)

    def systemname(self, value):
        return self.stringOption("CMAKE_SYSTEM_NAME", value)

    def systemversion(self, value):
        return self.stringOption("CMAKE_SYSTEM_VERSION", value)

    def target(self, value):
        return self.stringOption("TARGET", value)

    def architecture(self, value):
        return self.stringOption("TARGET_ARCHITECTURE", value)

    def lsbversion(self, value):
        return self.stringOption("LSB_VERSION", value)

    def cflags(self, value):
        return self.stringOption("CMAKE_C_FLAGS", value)

    def cxxflags(self, value):
        return self.stringOption("CMAKE_CXX_FLAGS", value)

    def rootpath(self, value):
        return self.stringOption("CMAKE_FIND_ROOT_PATH", value)

    def opensslrootdir(self, value):
        return self.stringOption("OPENSSL_ROOT_DIR", value)

    def netsnmprootdir(self, value):
        return self.stringOption("NETSNMP_ROOT_DIR", value)

    def prebuilt(self, value):
        return self.booleanOption("USE_PREBUILT", value)

    def sysroot(self, value):
        return self.stringOption("SYSROOT", value)

    def cominstallprefix(self, value):
        return self.stringOption("COM_INSTALL_PREFIX", value)

    def rpm(self, value):
        return self.booleanOption("RPM", value)

    def sshdmanager(self, value):
        return self.booleanOption("COMSSHDMANAGER", value)

    def password(self, value):
        return self.booleanOption("PASSWD", value)

    def ft_psoinstallprefix(self, value):
        return self.stringOption("FT_PSO_INSTALL_PREFIX", value)

    def ft_startseparatesshd(self, value):
        return self.booleanOption("FT_START_SEPARATE_SSHD", value)

    def ft_sshdport(self, value):
        return self.stringOption("FT_REMOTE_HOST_SSH_PORT", value)

    def ft_startport(self, value):
        return self.stringOption("FT_START_PORT", value)

    def ft_endport(self, value):
        return self.stringOption("FT_END_PORT", value)

    def ft_numports(self, value):
        return self.stringOption("FT_NUM_PORTS", value)

    def ft_remoteinstalltype(self, value):
        return self.stringOption("FT_REMOTE_INSTALL_TYPE", value)

    def ft_comusername(self, value):
        return self.stringOption("FT_COM_USER_NAME", value)

    def ft_comuserpassword(self, value):
        return self.stringOption("FT_COM_USER_PASSWORD", value)

    def ft_rootusername(self, value):
        return self.stringOption("FT_ROOT_USER_NAME", value)

    def ft_rootuserpassword(self, value):
        return self.stringOption("FT_ROOT_USER_PASSWORD", value)

    def ft_netsnmpversion(self, value):
        return self.stringOption("FT_NETSNMP_VERSION", value)

    def ft_netsnmptlssupport(self, value):
        return self.booleanOption("FT_NETNSMP_HAS_DTLS_SUPPORT", value)

    def ft_ipversion(self, value):
        return self.stringOption("FT_IP_VERSION", value)

    def ft_checkarchitecture(self, value):
        return self.booleanOption("FT_CHECK_ARCHITECTURE", value)

    def fmcoredeveloper(self, value):
        return self.booleanOption("FM_CORE_DEVELOPER", value)

    def useastyle(self, value):
        return self.booleanOption("OPTION_USE_ASTYLE", value)

    def useretpoline(self, value):
        return self.booleanOption("USE_RETPOLINE", value)

    def useencryption(self, value):
        return self.booleanOption("USE_ENCRYPTION", value)

    def useauditshow(self, value):
        return self.booleanOption("USE_AUDIT_SHOW", value)

    def securitylogging(self, value):
        return self.booleanOption("SECURITY_LOGGING", value)

    def useauditlog(self, value):
        return self.booleanOption("USE_AUDIT_LOGGING", value)

    def usewrapping(self, value):
        return self.booleanOption("USE_ATTR_WRAPPING", value)
