#!/bin/sh

echo ">>> cleaning up"

# cleanup log files
find /var/log -type f | while read f; do echo -ne '' > $f; done;

# Remove bash history
unset HISTFILE
rm -f /root/.bash_history
rm -f /home/vagrant/.bash_history

# clean up partitions for better compression
for i in / /boot/ /var/log/; do
    echo "Zeroing out filesystem: $i"
    dd bs=1M if=/dev/zero of=${i}whitespace 2>/dev/null
    rm -f ${i}whitespace
done

if [ -d /cluster/storage/no-backup ]; then
    rm -fr /cluster/storage/no-backup/* 2>/dev/null || true
fi

rm -f /cluster/dumps/*

#echo "Zeroing swap"
#swappart=`cat /proc/swaps | tail -n1 | awk -F ' ' '{print $1}'`
#swapoff $swappart;
#dd if=/dev/zero of=$swappart;
#mkswap $swappart;
#swapon $swappart;
