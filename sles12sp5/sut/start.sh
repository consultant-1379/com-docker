#!/bin/bash

# TODO: is this really needed? Should COM take care of it?
# create directory necessary for PM jobs
mkdir -p /var/filem/internal_root

# start rsyslog
/usr/sbin/rsyslogd

# start the snmp deamon
mkdir -p /run/slapd
/usr/lib/openldap/start

# generate the hostkeys
/usr/bin/ssh-keygen -A

# start the sshd deamon
/usr/sbin/sshd -D -f /etc/ssh/sshd_config
