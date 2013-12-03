# -*- mode: ruby -*-
# vi: set ft=ruby:

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.ssh.forward_agent = true
  config.vm.box            = 'ubuntu-precise-cloud-image'
  config.vm.box_url        = 'http://cloud-images.ubuntu.com/precise/current/precise-server-cloudimg-vagrant-amd64-disk1.box'
  config.vm.provider :virtualbox do |vb|
    vb.customize        ["modifyvm", :id, "--rtcuseutc", "on"]
    vb.customize        ['modifyvm', :id, '--memory', 256]
    vb.customize        ['modifyvm', :id, '--cpus', 1]
    vb.customize        ['modifyvm', :id, '--name', 'ubuntu-1204-bootstrap-dev']
  end
  config.vm.host_name      = 'vm.bootstrap.dev'
  config.vm.provision :shell do |shell|
      # Set the password for the ubuntu user to 'ubuntu'
      shell.inline = "sudo su - root /bin/bash -c 'echo \"ubuntu:ubuntu\" | chpasswd -c SHA512'"
  end
end
