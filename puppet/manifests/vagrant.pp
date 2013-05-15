# This manifest is solely for inital provisioning in Vagrant. Real changes should be in site.pp
node default {
  file { '/home/vagrant/.hushlogin':
    owner   => 'vagrant',
    group   => 'vagrant',
    content => '',
  }
  exec { 'apt-get-update':
    command => '/usr/bin/apt-get update || true',
  }
  package { 'language-pack-en': 
    ensure  => installed,
    require => Exec['apt-get-update']
  }
  user { 'ubuntu':
    ensure   => present,
    # This password is 'ubuntu'
    password => '$6$7iug.VMI$BS0neei8prD1vl13zJMZCNn0D9bfErgGz3ozB80fEXTe15eAeSxdt0yQYN1XHztEsKxeXOzZeIPida5q0TIcm.',
  }
}
