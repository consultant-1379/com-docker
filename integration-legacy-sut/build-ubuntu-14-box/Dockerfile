FROM armdockerhub.rnd.ericsson.se/ubuntu:14.04

ENV VAGRANTVERSION 1.9.1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y vim
RUN apt-get install -y qemu
RUN apt-get install -y qemu-kvm
RUN apt-get install -y libvirt-bin
RUN apt-get install -y ebtables
RUN apt-get install -y dnsmasq
RUN apt-get install -y libxslt-dev
RUN apt-get install -y libxml2-dev
RUN apt-get install -y libvirt-dev
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y ruby-dev
RUN apt-get install -y ssh
RUN apt-get install -y openssh-client
RUN apt-get install -y git
RUN apt-get install -y make
RUN apt-get install -y unzip

RUN cat /dev/zero | ssh-keygen -q -N ""

ENV DOWNLOADS /tmp/downloads

RUN mkdir -p $DOWNLOADS && \
    wget -P $DOWNLOADS https://releases.hashicorp.com/vagrant/${VAGRANTVERSION}/vagrant_${VAGRANTVERSION}_x86_64.deb && \
    dpkg -i $DOWNLOADS/vagrant_${VAGRANTVERSION}_x86_64.deb && \
    rm -rf $DOWNLOADS

RUN vagrant plugin install --plugin-version 0.0.35 vagrant-libvirt

# Install packager
ADD https://releases.hashicorp.com/packer/0.12.1/packer_0.12.1_linux_amd64.zip $DOWNLOADS/
RUN unzip $DOWNLOADS/packer_0.12.1_linux_amd64.zip -d /usr/local/bin && \
    rm -rf $DOWNLOADS

# Environment variables needed by the scripts
ENV VAGRANT_DIR /vagrant

# Add scripts
COPY scripts/start-libvirt /usr/local/bin
COPY scripts/start $VAGRANT_DIR/
COPY scripts/create-vagrant-box $VAGRANT_DIR/
RUN chmod 755 /usr/local/bin/start-libvirt
RUN chmod 755 $VAGRANT_DIR/start
RUN chmod 755 $VAGRANT_DIR/create-vagrant-box

# Add configuration files
COPY config/ $VAGRANT_DIR/

# Default start command
CMD ["bash","/vagrant/start"]
