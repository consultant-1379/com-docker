#!/bin/bash
set -e

#   The script will perform the following actions:
#       1.  Generate the version.xml file for downloading components using
#           DX Tools Artifactory Manager tool

if [ "$ldews_Required" == 'true' ]; then
    declare -x ldews_PATH=${AM_WORKSPACE}/cache/ldews/$ldews
else
    declare -x ldews='cbaBaselineFunctionality'
    declare -x ldews_PATH=${AM_WORKSPACE}/cache/ldews/$ldews
fi

if [ "$coremw_x86_64_Required" == 'true' ]; then
    declare -x coremw_x86_64_PATH=${AM_WORKSPACE}/cache/coremw_x86_64/$coremw_x86_64
else
    declare -x coremw_x86_64='cbaBaselineFunctionality'
    declare -x coremw_x86_64_PATH=${AM_WORKSPACE}/cache/coremw_x86_64/$coremw_x86_64
fi

if [ "$ldews_brf_script_Required" == 'true' ]; then
    declare -x ldews_brf_script_PATH=${AM_WORKSPACE}/cache/ldews-brf_script/$ldews_brf_script
else
    declare -x ldews_brf_script=''
    declare -x ldews_brf_script_PATH=''
fi

if [ "$com_x86_64_Required" == 'true' ]; then
    declare -x com_x86_64_PATH=${AM_WORKSPACE}/cache/com_x86_64/$com_x86_64
else
    declare -x com_x86_64=''
    declare -x com_x86_64_PATH=''
fi

if [ "$trace_Required" == 'true' ]; then
    declare -x trace_PATH=${AM_WORKSPACE}/cache/trace/$trace
else
    declare -x trace=''
    declare -x trace_PATH=''
fi

if [ "$traceea_Required" == 'true' ]; then
    declare -x traceea_PATH=${AM_WORKSPACE}/cache/traceea/$traceea
else
    declare -x traceea=''
    declare -x traceea_PATH=''
fi

if [ "$coremw_x86_64_brf_c_Required" == 'true' ]; then
    declare -x coremw_x86_64_brf_c_PATH=${AM_WORKSPACE}/cache/coremw_x86_64-brf_c/$coremw_x86_64_brf_c
else
    declare -x coremw_x86_64_brf_c=''
    declare -x coremw_x86_64_brf_c_PATH=''
fi

if [ "$coremw_x86_64_brf_eia_Required" == 'true' ]; then
    declare -x coremw_x86_64_brf_eia_PATH=${AM_WORKSPACE}/cache/coremw_x86_64-brf_eia/$coremw_x86_64_brf_eia
else
    declare -x coremw_x86_64_brf_eia=''
    declare -x coremw_x86_64_brf_eia_PATH=''
fi

if [ "$coremw_x86_64_logm_Required" == 'true' ]; then
    declare -x coremw_x86_64_logm_PATH=${AM_WORKSPACE}/cache/coremw_x86_64-logm/$coremw_x86_64_logm
else
    declare -x coremw_x86_64_logm=''
    declare -x coremw_x86_64_logm_PATH=''
fi

if [ "$evip_Required" == 'true' ]; then
    declare -x evip_PATH=${AM_WORKSPACE}/cache/evip/$evip
else
    declare -x evip=''
    declare -x evip_PATH=''
fi

if [ "$lm_Required" == 'true' ]; then
    declare -x lm_PATH=${AM_WORKSPACE}/cache/lm/$lm
else
    declare -x lm=''
    declare -x lm_PATH=''
fi

if [ "$lmsa_Required" == 'true' ]; then
    declare -x lmsa_PATH=${AM_WORKSPACE}/cache/lmsa/$lmsa
else
    declare -x lmsa=''
    declare -x lmsa_PATH=''
fi

if [ "$evip_Required" == 'true' ]; then
    declare -x evip_PATH=${AM_WORKSPACE}/cache/sec-secm/$sec_secm
else
    declare -x evip=''
    declare -x evip_PATH=''
fi

if [ "$sec_secm_Required" == 'true' ]; then
    declare -x sec_secm_PATH=${AM_WORKSPACE}/cache/sec-secm/$sec_secm
else
    declare -x sec_secm=''
    declare -x sec_secm_PATH=''
fi

if [ "$sec_ldap_Required" == 'true' ]; then
    declare -x sec_ldap_PATH=${AM_WORKSPACE}/cache/sec-ldap/$sec_ldap
else
    declare -x sec_ldap=''
    declare -x sec_ldap_PATH=''
fi

if [ "$sec_cert_Required" == 'true' ]; then
    declare -x sec_cert_PATH=${AM_WORKSPACE}/cache/sec-cert/$sec_cert
else
    declare -x sec_cert=''
    declare -x sec_cert_PATH=''
fi

if [ "$sec_crypto_Required" == 'true' ]; then
    declare -x sec_crypto_PATH=${AM_WORKSPACE}/cache/sec-crypto/$sec_crypto
else
    declare -x sec_crypto=''
    declare -x sec_crypto_PATH=''
fi

if [ "$sec_acs_Required" == 'true' ]; then
    declare -x sec_acs_PATH=${AM_WORKSPACE}/cache/sec-acs/$sec_acs
else
    declare -x sec_acs=''
    declare -x sec_acs_PATH=''
fi

if [ "$sec_la_Required" == 'true' ]; then
    declare -x sec_la_PATH=${AM_WORKSPACE}/cache/sec-la/$sec_la
else
    declare -x sec_la=''
    declare -x sec_la_PATH=''
fi

if [ "$mmas_Required" == 'true' ]; then
    declare -x mmas_PATH=${AM_WORKSPACE}/cache/mmas/$mmas
else
    declare -x mmas=''
    declare -x mmas_PATH=''
fi

if [ "$mmas_jdk8_Required" == 'true' ]; then
    declare -x mmas_jdk8_PATH=${AM_WORKSPACE}/cache/mmas-jdk8/$mmas_jdk8
else
    declare -x mmas_jdk8=''
    declare -x mmas_jdk8_PATH=''
fi

if [ "$mmas_lite_Required" == 'true' ]; then
    declare -x mmas_lite_PATH=${AM_WORKSPACE}/cache/mmas-lite/$mmas_lite
else
    declare -x mmas_lite=''
    declare -x mmas_lite_PATH=''
fi

if [ "$mmas_tomcat_Required" == 'true' ]; then
    declare -x mmas_tomcat_PATH=${AM_WORKSPACE}/cache/mmas-tomcat/$mmas_tomcat
else
    declare -x mmas_tomcat=''
    declare -x mmas_tomcat_PATH=''
fi

if [ "$mmas_infinispan_Required" == 'true' ]; then
    declare -x mmas_infinispan_PATH=${AM_WORKSPACE}/cache/mmas-infinispan/$mmas_infinispan
else
    declare -x mmas_infinispan=''
    declare -x mmas_infinispan_PATH=''
fi

if [ "$mmas_sds_Required" == 'true' ]; then
    declare -x mmas_sds_PATH=${AM_WORKSPACE}/cache/mmas-sds/$mmas_sds
else
    declare -x mmas_sds=''
    declare -x mmas_sds_PATH=''
fi

if [ "$javaoam_Required" == 'true' ]; then
    declare -x javaoam_PATH=${AM_WORKSPACE}/cache/javaoam/$javaoam
else
    declare -x javaoam=''
    declare -x javaoam_PATH=''
fi

if [ "$javasip_Required" == 'true' ]; then
    declare -x javasip_PATH=${AM_WORKSPACE}/cache/javasip/$javasip
else
    declare -x javasip=''
    declare -x javasip_PATH=''
fi

if [ "$javasip_testapps_Required" == 'true' ]; then
    declare -x javasip_testapps_PATH=${AM_WORKSPACE}/cache/javasip_testapps/$javasip_testapps
else
    declare -x javasip_testapps=''
    declare -x javasip_testapps_PATH=''
fi

if [ "$ss7caf_Required" == 'true' ]; then
    declare -x ss7caf_PATH=${AM_WORKSPACE}/cache/ss7caf/$ss7caf
else
    declare -x ss7caf=''
    declare -x ss7caf_PATH=''
fi

if [ "$cdf_Required" == 'true' ]; then
    declare -x cdf_PATH=${AM_WORKSPACE}/cache/cdf/$cdf
else
    declare -x cdf=''
    declare -x cdf_PATH=''
fi

if [ "$dbs_Required" == 'true' ]; then
    declare -x dbs_PATH=${AM_WORKSPACE}/cache/dbs/$dbs
else
    declare -x dbs=''
    declare -x dbs_PATH=''
fi

if [ "$lem_Required" == 'true' ]; then
    declare -x lem_PATH=${AM_WORKSPACE}/cache/lem/$lem
else
    declare -x lem=''
    declare -x lem_PATH=''
fi

if [ "$cdiameter_Required" == 'true' ]; then
    declare -x cdiameter_PATH=${AM_WORKSPACE}/cache/cdiameter/$cdiameter
else
    declare -x cdiameter=''
    declare -x cdiameter_PATH=''
fi

if [ "$cdiametertestapp_Required" == 'true' ]; then
    declare -x cdiametertestapp_PATH=${AM_WORKSPACE}/cache/cdiametertestapp/$cdiametertestapp
else
    declare -x cdiametertestapp=''
    declare -x cdiametertestapp_PATH=''
fi

if [ "$vdicosee_Required" == 'true' ]; then
    declare -x vdicosee_PATH=${AM_WORKSPACE}/cache/vdicosee/$vdicosee
else
    declare -x vdicosee=''
    declare -x vdicosee_PATH=''
fi

if [ "$vdicoseetest_Required" == 'true' ]; then
    declare -x vdicoseetest_PATH=${AM_WORKSPACE}/cache/vdicoseetest/$vdicoseetest
else
    declare -x vdicoseetest=''
    declare -x vdicoseetest_PATH=''
fi

if [ "$vdicosrefappexternal_Required" == 'true' ]; then
    declare -x vdicosrefappexternal_PATH=${AM_WORKSPACE}/cache/vdicosrefappexternal/$vdicosrefappexternal
else
    declare -x vdicosrefappexternal=''
    declare -x vdicosrefappexternal_PATH=''
fi

AIT_FILE=versionFile

AIT_TEMPLATE=versions.xml.template
XSL=versions.xsl

function cleanup
{
    rm -f /tmp/${AIT_FILE}.xml{,.tmp}
}
trap cleanup EXIT

function set_file
{
    # This command fetches all patterns (something) and replaces it with the value of $something
    perl -wpi -e 's:\((\w+)\):$ENV{"$1"}:g' -- "$1"
}

# Set the ait_versions.xml file
cp ${AIT_TEMPLATE} /tmp/${AIT_FILE}.xml.tmp
set_file /tmp/${AIT_FILE}.xml.tmp

# applying xsl to both tmp xml to remove the unneeded components
xsltproc $XSL /tmp/${AIT_FILE}.xml.tmp > /${AIT_FILE}.xml

echo "AIT File"
cat /${AIT_FILE}.xml
