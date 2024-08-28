#!/bin/bash

#   The script will perform the following actions:
#       1.  Store the version for downloading components

STACK_FILE=/versionStackFile

# Delete file if exists already
if [ -f /versionStackFile ]; then
    rm -rf $STACK_FILE
fi

echo "declare -x LDE_BASE_VERSION=$LDE_BASE_VERSION" > $STACK_FILE
echo "declare -x LDE_TO_VERSION=$LDE_TO_VERSION" >> $STACK_FILE
echo "declare -x COM_BASE_VERSION=$COM_BASE_VERSION" >> $STACK_FILE
echo "declare -x COM_TO_VERSION=$COM_TO_VERSION" >> $STACK_FILE
echo "declare -x CMW_BASE_VERSION=$CMW_BASE_VERSION" >> $STACK_FILE
echo "declare -x CMW_TO_VERSION=$CMW_TO_VERSION" >> $STACK_FILE
echo "declare -x SEC_BASE_VERSION=$SEC_BASE_VERSION" >> $STACK_FILE
echo "declare -x SEC_TO_VERSION=$SEC_TO_VERSION" >> $STACK_FILE

echo "Version Stack File"
cat ${STACK_FILE}
