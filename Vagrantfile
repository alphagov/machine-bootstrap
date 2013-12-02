# -*- mode: ruby -*-
# vi: set ft=ruby:

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.dns.tld           = 'bootstrap.dev'
  config.dns.patterns      = [/^.*bootstrap.dev$/]
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
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path  = "puppet/manifests"
    puppet.manifest_file   = "vagrant.pp"
    puppet.module_path     = "puppet/vendor/modules"
  end
end
