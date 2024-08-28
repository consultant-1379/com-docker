#!/bin/sh

set -ex

echo "######################### Adding Payload rpms #################################"
cd /cluster/rpms
cluster rpm -a ldews-payload*.rpm -n 3
cluster rpm -a ldews-payload*.rpm -n 4
cluster config -r
echo "###############################################################################"
