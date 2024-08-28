#!/bin/sh

# Disable reverse lookup
echo "### added for vagrant" >> /etc/ssh/sshd_config
echo "UseDNS no" >> /etc/ssh/sshd_config

# Below line is recommended for drbd sync of controllers in SP2
touch /boot/.drbd-reinit-for-vii

# Below code will update the cluster.conf file with custom changes in SP2
if [ -f /cluster/etc/lde-config.xml ] && [ -f /boot/.cluster.conf ]; then
    cp /boot/.cluster.conf /cluster/etc/cluster.conf
    /opt/lde/lde-config/cluster2imm.py /boot/.cluster.conf /cluster/etc/lde-config.xml
    cluster config -r
fi

mkdir -p /cluster/nodes/2/etc/
cp /cluster/nodes/1/etc/rpm.conf /cluster/nodes/2/etc/rpm.conf
