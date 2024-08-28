#!/bin/bash
# Usage:
# This is a helper file that copies component packages from artifactory to Eridoc
#

if [ $# -ne 5 ]
  then
    echo "This is a helper script that should not be called standalone unless you really know what you are doing"
    exit 0
fi

BUILD="$1"
DOCUMENT_TITLE="$2"
DOCUMENT_NUMBER="$3"
ARTIFACT_PATH="$4"
CXP_NUMBER="$5"

JSON_TEMPLATE="upload_template.json"

TEMP_FOLDER="$PWD/temp"
mkdir -p $TEMP_FOLDER

# Copy template to temp folder where we can manipulate the file
cp ${JSON_TEMPLATE} ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json

# Replace the tags from the template with the correct value. (some values have / in them so that can't be used in sed as separater)
sed -i "s#DOCUMENT_TITLE#${DOCUMENT_TITLE}#g" ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json
sed -i "s#DOCUMENT_NUMBER#${DOCUMENT_NUMBER}#g" ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json
sed -i "s#ARTIFACT_PATH#${ARTIFACT_PATH}#g" ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json
sed -i "s#CXP_NUMBER#${CXP_NUMBER}#g" ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json

#Actual storing to Eridoc
echo "Storing the packages to Eridoc"
if [[ $CXP_NUMBER == cxp9028492 || $CXP_NUMBER == cxp9028493 || $CXP_NUMBER == cxp9016946 || $CXP_NUMBER == cxp9017911 || $CXP_NUMBER == cxp9018540 ]]; then

echo "curl -s -u cbacomci:${Password} -X POST https://arm.sero.gic.ericsson.se/artifactory/api/plugins/execute/upload2eridoc?params=https://arm.rnd.ki.sw.ericsson.se/artifactory/proj-cba-dev-local/com/ericsson/cba/com_x86_64/com_x86_64/${BUILD}/${DOCUMENT_TITLE}.tar.gz -T ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json"

curl -s -u cbacomci:${Password} -X POST https://arm.sero.gic.ericsson.se/artifactory/api/plugins/execute/upload2eridoc?params=https://arm.rnd.ki.sw.ericsson.se/artifactory/proj-cba-dev-local/com/ericsson/cba/com_x86_64/com_x86_64/${BUILD}/${DOCUMENT_TITLE}.tar.gz -T ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json

elif [[ $CXP_NUMBER == cay901200 || $CXP_NUMBER == cay901201 ]]; then

curl -s -u cbacomci:${Password} -X POST https://arm.sero.gic.ericsson.se/artifactory/api/plugins/execute/upload2eridoc?params=https://arm.rnd.ki.sw.ericsson.se/artifactory/proj-cba-dev-local/com/ericsson/cba/com/com/${BUILD}/${DOCUMENT_TITLE}.tar.gz -T ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json

elif [[ $CXP_NUMBER == cay901203 || $CXP_NUMBER == cay901202 ]]; then

curl -s -u cbacomci:${Password} -X POST https://arm.sero.gic.ericsson.se/artifactory/api/plugins/execute/upload2eridoc?params=https://arm.rnd.ki.sw.ericsson.se/artifactory/proj-cba-dev-local/com/ericsson/cba/com/com-comsa/${BUILD}/${DOCUMENT_TITLE}.tar.gz -T ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json

elif [[ $CXP_NUMBER == cay901231 ]]; then

curl -s -u cbacomci:${Password} -X POST https://arm.sero.gic.ericsson.se/artifactory/api/plugins/execute/upload2eridoc?params=https://arm.rnd.ki.sw.ericsson.se/artifactory/proj-cba-dev-local/com/ericsson/cba/com/com-comea/${BUILD}/${DOCUMENT_TITLE}.tar.gz -T ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json

elif [[ $CXP_NUMBER == cay901233 ]]; then

curl -s -u cbacomci:${Password} -X POST https://arm.sero.gic.ericsson.se/artifactory/api/plugins/execute/upload2eridoc?params=https://arm.rnd.ki.sw.ericsson.se/artifactory/proj-cba-dev-local/com/ericsson/cba/com/com-vsftpd/${BUILD}/${DOCUMENT_TITLE}.tar.gz -T ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json

else

echo " Received an inappropriate cxp_number"

fi
