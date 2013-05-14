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
}
