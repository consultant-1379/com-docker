#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)

BINPATH="/bin"

# install build script
ln -s "${SCRIPTPATH}/gaskupload" "${BINPATH}"
