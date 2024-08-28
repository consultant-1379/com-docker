#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`

BINPATH="/bin"

# install build script
ln -s "${SCRIPTPATH}/build" "${BINPATH}"

# install codechecker script
ln -s "${SCRIPTPATH}/buildwithcodechecker" "${BINPATH}"
