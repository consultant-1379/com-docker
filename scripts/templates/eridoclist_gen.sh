!/bin/bash
set -e

# This script will prepare the list of COM packages that need
# to be uploaded to eridoc

declare -x componentList

if [ "$com_x86_64_Deployment_Required" == 'true' ]; then
    componentList="$componentList com_x86_64_Deployment"
fi

if [ "$com_x86_64_Runtime_Required" == 'true' ]; then
    componentList="$componentList com_x86_64_Runtime"
fi

if [ "$com_x86_64_Spi_Required" == 'true' ]; then
    componentList="$componentList com_x86_64_Spi"
fi

if [ "$com_x86_64_Api_Required" == 'true' ]; then
    componentList="$componentList com_x86_64_Api"
fi

if [ "$com_x86_64_oammodels_Required" == 'true' ]; then
    componentList="$componentList com_x86_64_oammodels"
fi

if [ "$com_src_Required" == 'true' ]; then
    componentList="$componentList com_src"
fi

if [ "$com_yocto_Required" == 'true' ]; then
    componentList="$componentList com_yocto"
fi

if [ "$comsa_src_Required" == 'true' ]; then
    componentList="$componentList comsa_src"
fi

if [ "$comsa_yocto_Required" == 'true' ]; then
    componentList="$componentList comsa_yocto"
fi

if [ "$comea_src_Required" == 'true' ]; then
    componentList="$componentList comea_src"
fi

if [ "$comvsftpd_src_Required" == 'true' ]; then
    componentList="$componentList comvsftpd_src"
fi

echo $componentList
