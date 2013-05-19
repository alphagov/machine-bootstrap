Exec {
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
}

node default {
  class {'fail2ban':
    require => Exec['apt-get-update']
  }
  include ssh::server
  include ufw
  exec { 'apt-get-update':
    command => '/usr/bin/apt-get update || true',
  }
  ufw::allow { "allow-ssh-from-all":
    port => 22,
    ip   => 'any'
  }
}
