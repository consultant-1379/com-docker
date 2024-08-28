#!/bin/bash -e

#   The script will perform the following actions:
#       1.  Download the components from artifactory using Artifactory Manager
#       2.  Generates the AIT repo with downloaded components

if [ $# -ne 2 ]; then
    echo "PATH TO THE AIT REPOSITORY AND CBA VERSION FILE NAME NEEDS TO BE PROVIDED"
    exit 1
fi

REPO=$1
VERSION_FILE=$2

function cleanup {
    rm -rf $REPO/{SWP_File,swp}
}
trap cleanup EXIT

# Generate the AIT repository
set +e
set -o pipefail
# Maximum attemps to retry AM command due to connectivity issues
MAX_RETRY_ATTEMPTS=5
for ((retryLoop=1; retryLoop < $MAX_RETRY_ATTEMPTS; retryLoop++))
{
    artifact_manager -cr -i $VERSION_FILE -o $REPO |& tee /tmp/am_log.txt
    if [ $? -ne 0 ]; then
        if grep -q "No connectivity to Artifactory" /tmp/am_log.txt; then
            echo "Failed due to connectivity issue. Retrying again..."
        else
            echo "Error: Downloading of packages failed"
            break
        fi
    else
        break
    fi
}
set +o pipefail
set -e

(cd $REPO/swp ; cp DEPLOYMENT.working DEPLOYMENT.ready)
(cd $REPO ; ait-image-create swp swp)
chmod -R 755 $REPO
