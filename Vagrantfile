# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  ENV['LC_ALL']="en_US.UTF-8"

  config.vm.provision "shell", inline: <<-SHELL
    apt-get -qqy update

    apt-get -qqy install make zip unzip postgresql

    apt-get -qqy install python3 python3-pip
    pip3 install --upgrade pip

    apt-get -qqy install python python-pip
    pip2 install --upgrade pip

    su postgres -c 'createuser -dRS vagrant'
    su vagrant -c 'createdb'
    su vagrant -c 'createdb news'

    vagrantTip="[35m[1mThe shared directory is located at /vagrant\\nTo access your shared files: cd /vagrant[m"
    echo -e $vagrantTip > /etc/motd

    echo "Done installing your virtual machine!"
  SHELL
end
