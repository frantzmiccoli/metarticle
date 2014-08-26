# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "hashicorp/precise64"
  
  script = <<-eos
    sudo apt-get update
    sudo apt-get -y install python-pip python-dev libxml2-dev libxslt1-dev python-yaml rake curl
    cd /vagrant/src/
    sudo pip install -r requirements.txt
    sudo python -m nltk.downloader all
    cd ..
    rake data
    rake crunch
eos

  config.vm.provision "shell", inline: script

end
