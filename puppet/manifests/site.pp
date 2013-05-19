Exec {
  path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
}

node default {
  include ufw
  exec { 'apt-get-update':
    command => '/usr/bin/apt-get update || true',
  }
  ufw::allow { "allow-ssh-from-all":
    port => 22,
    ip   => 'any'
  }
}
