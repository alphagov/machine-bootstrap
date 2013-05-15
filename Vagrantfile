# -*- mode: ruby -*-
# vi: set ft=ruby:

Vagrant::Config.run do |config|
  config.dns.tld           = 'harden.dev'
  config.dns.patterns      = [/^.*harden.dev$/]
  config.ssh.forward_agent = true
  config.vm.box            = 'ubuntu-precise-cloud-image'
  config.vm.box_url        = 'http://cloud-images.ubuntu.com/precise/current/precise-server-cloudimg-vagrant-amd64-disk1.box'
  config.vm.customize        ["modifyvm", :id, "--rtcuseutc", "on"]
  config.vm.customize        ['modifyvm', :id, '--memory', 256]
  config.vm.customize        ['modifyvm', :id, '--cpus', 1]
  config.vm.customize        ['modifyvm', :id, '--name', 'ubuntu-1204-dev']
  config.vm.host_name      = 'vm.harden.dev'
  if File.exist? 'Vagrantfile.local'
    instance_eval File.read('Vagrantfile.local'), 'Vagrantfile.local'
  end
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path  = "puppet/manifests"
    puppet.manifest_file   = "site.pp"
    puppet.module_path     = "puppet/vendor/modules"
  end
end
