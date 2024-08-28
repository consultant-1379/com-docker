#!/bin/bash
# Usage:
# Environment file required to valdiate the PDI and set paths required
# to run gask automatic upload

RELEASE2GASK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Making sure PDI is configured
pdi -help > /dev/null 2>&1
if [ $? -eq 0 ]
then
  echo "PDI is already configured"
else
  if [ -f $RELEASE2GASK_DIR/../PDI/config/sourceme.source ]; then
    source $RELEASE2GASK_DIR/../PDI/config/sourceme.source
   echo "PDI has been sourced and are now working"
  else
    echo "PDI is not configured, please do that before continue"
    exit 1
  fi
fi

# Adding the executable to PATH environment variable
PATH=$RELEASE2GASK_DIR/bin:$PATH

export RELEASE2GASK_DIR