#!/bin/bash
set -e

#   The script will perform the following actions:
#       1.  Generate the version.xml file for downloading components using
#           DX Tools Artifactory Manager tool
if ! [ "$lde_base_Required" == 'true' ]; then
    declare -x lde_base=''
fi

if ! [ "$lde_cba_if_Required" == 'true' ]; then
    declare -x lde_cba_if=''
fi

if ! [ "$lde_agents_Required" == 'true' ]; then
    declare -x lde_agents=''
fi

if ! [ "$sles_base_Required" == 'true' ]; then
    declare -x sles_base=''
fi

if ! [ "$lde_reference_os_Required" == 'true' ]; then
    declare -x lde_reference_os=''
fi

if ! [ "$lde_services_Required" == 'true' ]; then
    declare -x lde_services=''
fi

if ! [ "$coremw_x86_64_core_Required" == 'true' ]; then
    declare -x coremw_x86_64_core=''
fi

if ! [ "$coremw_x86_64_swm_Required" == 'true' ]; then
    declare -x coremw_x86_64_swm=''
fi

if ! [ "$coremw_x86_64_pmrm_Required" == 'true' ]; then
    declare -x coremw_x86_64_pmrm=''
fi

if ! [ "$coremw_x86_64_clmnodedetect_Required" == 'true' ]; then
    declare -x coremw_x86_64_clmnodedetect=''
fi

if ! [ "$coremw_x86_64_cr_Required" == 'true' ]; then
    declare -x coremw_x86_64_cr=''
fi

if ! [ "$coremw_x86_64_logm_Required" == 'true' ]; then
    declare -x coremw_x86_64_logm=''
fi

if ! [ "$coremw_x86_64_isp_Required" == 'true' ]; then
    declare -x coremw_x86_64_isp=''
fi

if ! [ "$coremw_x86_64_cbrfeia_Required" == 'true' ]; then
    declare -x coremw_x86_64_cbrfeia=''
fi

if ! [ "$coremw_x86_64_cbrfcmwa_Required" == 'true' ]; then
    declare -x coremw_x86_64_cbrfcmwa=''
fi

if ! [ "$coremw_x86_64_cbrfc_Required" == 'true' ]; then
    declare -x coremw_x86_64_cbrfc=''
fi

if ! [ "$sec_secm_Required" == 'true' ]; then
    declare -x sec_secm=''
fi

if ! [ "$sec_ldap_Required" == 'true' ]; then
    declare -x sec_ldap=''
fi

if ! [ "$sec_cert_Required" == 'true' ]; then
    declare -x sec_cert=''
fi

if ! [ "$sec_crypto_Required" == 'true' ]; then
    declare -x sec_crypto=''
fi

if ! [ "$sec_acs_Required" == 'true' ]; then
    declare -x sec_acs=''
fi

if ! [ "$sec_la_Required" == 'true' ]; then
    declare -x sec_la=''
fi

if ! [ "$com_x86_64_Required" == 'true' ]; then
    declare -x com_x86_64=''
fi

if ! [ "$trace_Required" == 'true' ]; then
    declare -x trace=''
fi

if ! [ "$traceea_Required" == 'true' ]; then
    declare -x traceea=''
fi

if ! [ "$cbas_pmtestapp_Required" == 'true' ]; then
    declare -x cbas_pmtestapp=''
fi

if ! [ "$lm_Required" == 'true' ]; then
    declare -x lm=''
fi

if ! [ "$lmsa_Required" == 'true' ]; then
    declare -x lmsa=''
fi

if ! [ "$evip_Required" == 'true' ]; then
    declare -x evip=''
fi

if ! [ "$mmas_Required" == 'true' ]; then
    declare -x mmas=''
fi

if ! [ "$mmas_jdk8_Required" == 'true' ]; then
    declare -x mmas_jdk8=''
fi

if ! [ "$mmas_lite_Required" == 'true' ]; then
    declare -x mmas_lite=''
fi

if ! [ "$mmas_tomcat_Required" == 'true' ]; then
    declare -x mmas_tomcat=''
fi

if ! [ "$mmas_infinispan_Required" == 'true' ]; then
    declare -x mmas_infinispan=''
fi

if ! [ "$mmas_sds_Required" == 'true' ]; then
    declare -x mmas_sds=''
fi

if ! [ "$javaoam_Required" == 'true' ]; then
    declare -x javaoam=''
fi

if ! [ "$javasip_Required" == 'true' ]; then
    declare -x javasip=''
fi

if ! [ "$javasip_testapps_Required" == 'true' ]; then
    declare -x javasip_testapps=''
fi

if ! [ "$ss7caf_Required" == 'true' ]; then
    declare -x ss7caf=''
fi

if ! [ "$cdf_Required" == 'true' ]; then
    declare -x cdf=''
fi

if ! [ "$dbs_Required" == 'true' ]; then
    declare -x dbs=''
fi

if ! [ "$lem_Required" == 'true' ]; then
    declare -x lem=''
fi

if ! [ "$cdiameter_Required" == 'true' ]; then
    declare -x cdiameter=''
fi

if ! [ "$cdiametertestapp_Required" == 'true' ]; then
    declare -x cdiametertestapp=''
fi

if ! [ "$vdicosee_Required" == 'true' ]; then
    declare -x vdicosee=''
fi

if ! [ "$vdicoseetest_Required" == 'true' ]; then
    declare -x vdicoseetest=''
fi

if ! [ "$vdicosrefappexternal_Required" == 'true' ]; then
    declare -x vdicosrefappexternal=''
fi

VERSION_FILE=versionFile

VERSION_TEMPLATE=versions_lda.xml.template
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

# Set the versions.xml file
cp ${VERSION_TEMPLATE} /tmp/${VERSION_FILE}.xml.tmp
set_file /tmp/${VERSION_FILE}.xml.tmp

# applying xsl to both tmp xml to remove the unneeded components
xsltproc $XSL /tmp/${VERSION_FILE}.xml.tmp > /${VERSION_FILE}.xml

echo "Version File"
cat /${VERSION_FILE}.xml
