#!/bin/sh

# updating you.linux.ericsson.se in http address with 10.35.28.4 to resolve the dns and also for
# connecting to node without long wait time
# we need to update this IP in future if it changes
#
# download and install zypper and its dependencies
for i in \
    zypper-1.11.14-1.2.x86_64.rpm \
    libzypp-14.29.4-1.10.x86_64.rpm \
    libaugeas0-1.2.0-1.5.x86_64.rpm \
    libsolv-tools-0.6.5-1.7.x86_64.rpm \
    gpg2-2.0.24-1.5.x86_64.rpm \
    libproxy1-0.4.11-11.2.x86_64.rpm \
    libmodman1-2.0.1-15.75.x86_64.rpm \
    ;
do
    python -c "import urllib; urllib.urlretrieve('https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLES12-Pool/x86_64/%s' % \"$i\", '/cluster/rpms/%s' % \"$i\")"
    cluster rpm --add $i --node 1
    cluster rpm --add $i --node 2
done

cluster rpm --activate --node 1
cluster rpm --activate --node 2


# Ericsson YOU/SMT repos
#   see https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/config/

if [[ $(lsb_release -d) == *SP2* ]]; then
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLES12-SP2-Pool/ 12-Pool-you
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLES12-SP2-Updates/ 12-Updates-you
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLE12-SP2-SDK-Pool/ 12-SDK-Pool-you
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLE12-SP2-SDK-Updates/ 12-SDK-Updates-you
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLES12-SP2-Debuginfo-Pool/ SLES12-Debuginfo-Pool-you
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLES12-SP2-Debuginfo-Updates/ SLES12-Debuginfo-Updates-you
else
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLES12-Pool/ 12-Pool-you
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLES12-Updates/ 12-Updates-you
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLE12-SDK-Pool/ 12-SDK-Pool-you
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLE12-SDK-Updates/ 12-SDK-Updates-you
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLES12-Debuginfo-Pool/ SLES12-Debuginfo-Pool-you
    zypper ar -f https://arm.sero.gic.ericsson.se/artifactory/proj-suse-repos-rpm-local/SLE12/SLES12-Debuginfo-Updates/ SLES12-Debuginfo-Updates-you
fi
