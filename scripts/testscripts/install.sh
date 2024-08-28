#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

BINPATH="/bin"

# make sure unittest is executable
chmod 755 "${SCRIPTPATH}/unittest"
chmod 755 "${SCRIPTPATH}/functiontest"
chmod 755 "${SCRIPTPATH}/comeaunittest"
chmod 755 "${SCRIPTPATH}/comsatest"
chmod 755 "${SCRIPTPATH}/integrationtest"
chmod 755 "${SCRIPTPATH}/mergedupgradetest"
chmod 755 "${SCRIPTPATH}/performancetest"
chmod 755 "${SCRIPTPATH}/maftest"

# install test scripts
ln -s "${SCRIPTPATH}/unittest" "${BINPATH}"
ln -s "${SCRIPTPATH}/functiontest" "${BINPATH}"
ln -s "${SCRIPTPATH}/comeaunittest" "${BINPATH}"
ln -s "${SCRIPTPATH}/comsatest" "${BINPATH}"
ln -s "${SCRIPTPATH}/integrationtest" "${BINPATH}"
ln -s "${SCRIPTPATH}/performancetest" "${BINPATH}"
ln -s "${SCRIPTPATH}/maftest" "${BINPATH}"
ln -s "${SCRIPTPATH}/mergedupgradetest" "${BINPATH}"
