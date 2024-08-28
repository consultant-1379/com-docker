#!/bin/bash
# Usage:
# This is a helper file that copies component packages from artifactory to GASK
#

if [ $# -ne 4 ]
  then
    echo "This is a helper script that should not be called standalone unless you really know what you are doing"
    exit 0
fi

BUILD="$1"
DOCUMENT_TITLE="$2"
DOCUMENT_NUMBER="$3"
ARTIFACT_PATH="$4"
LAST_DOC_VERSION="Dummmy"
NEW_DOC_VERSION=""

timeout=300 # 5 mins
interval=10

echo "Getting latest revision number for document $DOCUMENT_NUMBER"
while true
do
    LAST_DOC_VERSION=$(pdi finddoc -dno ${DOCUMENT_NUMBER} -csv_hd_flds DocumentRevision -csv_noheader 2>/dev/null | head -1)
    if [ -z "$LAST_DOC_VERSION" ]; then
        echo "Previous revision not found. Setting revision to 'A'"
        echo "INFO: Check gasking is being done for new Product"
        NEW_DOC_VERSION='A'
        break
    elif [ "$LAST_DOC_VERSION" != "X" ] && [ ${#LAST_DOC_VERSION} -lt 3 ]; then
        echo "Latest revision is '$LAST_DOC_VERSION'"
        NEW_DOC_VERSION=`perl ${RELEASE2GASK_DIR}/../PDI/LZN9011398_3-R17A/utils/eriutl/Eridrev.pm -noverbose -rev ${LAST_DOC_VERSION} -next`
        break
    fi
    sleep $interval
    echo "Trying to get latest revision"
done


JSON_TEMPLATE="json_template/upload_template.json"

TEMP_FOLDER="$PWD/temp"
mkdir -p $TEMP_FOLDER

# Copy template to temp folder where we can manipulate the file
cp ${JSON_TEMPLATE} ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json

# Replace the tags from the template with the correct value. (some values have / in them so that can't be used in sed as separater)
sed -i "s#DOCUMENT_TITLE#${DOCUMENT_TITLE}#g" ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json
sed -i "s#DOCUMENT_NUMBER#${DOCUMENT_NUMBER}#g" ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json
sed -i "s#ARTIFACT_PATH#${ARTIFACT_PATH}#g" ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json
sed -i "s#NEW_DOC_VERSION#${NEW_DOC_VERSION}#g" ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json

# Populate the report.txt file
# Get MD5 sum from artifactory
DOCUMENT_MD5SUM=$(curl -u ${AUTHENTICATION_USER} -X GET https://arm.rnd.ki.sw.ericsson.se/artifactory/${ARTIFACT_PATH}.md5)

# Populate the report.txt file
echo -e "${DOCUMENT_TITLE}\t${DOCUMENT_NUMBER}\t${NEW_DOC_VERSION}\t\t${DOCUMENT_MD5SUM}" >> report.txt

# Do the actual storing to gask
curl -u ${AUTHENTICATION_USER} -X POST -T ${TEMP_FOLDER}/${DOCUMENT_TITLE}.json https://arm.rnd.ki.sw.ericsson.se/artifactory/api/plugins/execute/upload2gask

if ! [ $? -eq 0 ]; then
    echo "Error: Bad credentials..."
    exit 1
fi
while  [ $timeout -gt 0 ]
do
    CUR_VER=$(pdi finddoc -dno ${DOCUMENT_NUMBER} -csv_hd_flds DocumentRevision -csv_noheader 2>/dev/null | head -1 | grep ${NEW_DOC_VERSION})
    if [ $? -eq 0 ]; then
        echo "${DOCUMENT_TITLE} Uploaded"
        break
    else
        echo "Waiting for uploading ... ("$timeout"s left)"
    fi
    sleep $interval
    timeout=$(($timeout - $interval))
done
