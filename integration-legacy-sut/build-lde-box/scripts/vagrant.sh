#!/bin/sh

#
# Since mkpasswd is not available in all systems, here are some
# hashes for password "vagrant".  DES based hash is most compatible
# with old systems.
#
# $ mkpasswd -m des vagrant
pwhash='3hsUgsrz5T102'
# $ mkpasswd -m sha-256 vagrant
#pwhash='$5$OlGE.iFVlyR$RJhQ77X6A9BEPnwAdQGr.0nEXQNakrIIOPsvLFB7a75'
# $ mkpasswd -m sha-512 vagrant
# pwhash='$6$CI2cBRtTM3i2Nhg$uMUlDFLAbkhAPz3ac6ds2gDnoYH.yn7IJzmM6WdwosPSK.yFqv4EwJzDpGvuT/yIfhmkAVEr9SxIg2.01qzAv.'

# Create user, set passwords
groupadd vagrant
useradd -m vagrant -g vagrant -p $pwhash

# Add vagrant as global user in cluster
lde-global-user -u vagrant

# Set the default ssh key for vagrant user
mkdir -m 700 /home/vagrant/.ssh
cat > /home/vagrant/.ssh/authorized_keys <<EOF
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key
EOF
chmod 600 /home/vagrant/.ssh/authorized_keys
chown -R vagrant:vagrant /home/vagrant

# Allow passwordless sudo
cat >> /etc/sudoers.d/vagrant <<EOF
vagrant ALL=(ALL) NOPASSWD:ALL
Defaults:vagrant !requiretty
EOF

# Allow passwordless sudo for payloads
echo "vagrant ALL=(ALL) NOPASSWD:ALL" >> /cluster/etc/sudoers
echo "Defaults:vagrant !requiretty" >> /cluster/etc/sudoers

# Problem:
#    No /sbin in PATH in SLE
#    https://github.com/mitchellh/vagrant/issues/2775
#
# Workaround:
echo "export PATH=\$PATH:/sbin/:/usr/sbin" >> /home/vagrant/.bashrc

# enable core dumps for vagrant user
echo "ulimit -c unlimited" >> /home/vagrant/.bashrc
