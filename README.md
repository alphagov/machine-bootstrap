# Overview

This repository contains methods for bootstrapping blank machines.

It currently contains a single script `bin/bootstrap` which can:
- Connect to a machine via SSH and set a random password
- Connect to a machine via SSH and apply the puppet manifest in the `puppet` directory
- Run an optional bootstrap script (any lang available on destination) after initial puppet run
- A vagrant environment where `bootstrap` can be tested

# Instructions for hardening machines

Generating a new SSH key automatically and hardening for a machine at
IP address 192.0.2.32:

    ./bin/bootstrap 192.0.2.32

Supplying an SSH public key:

    ./bin/bootstrap -k 'ssh-rsa LONGKEY comment' 192.0.2.32

To list other options, view the builtin help:

    ./bin/bootstrap -h

# Instructions for development

## 1. Bring up a development VM.

Within the checked out copy of this repository, run the `rake` command. This will:

1. Install the relevant Ruby Gems using bundler.
2. Create Vagrantfile.local which will set a random IP for your VM.
3. Download an Ubuntu Image and create a VM (This will include running Puppet).

At this point you will have a local VM running, with the username 'ubuntu' and the password 'ubuntu'
with SSH listening on a random port (see output of vagrant).

## 2. Modify the VM using puppet

The intention of this Repo is to provide a development platform where you can customise the VM using
Puppet. This puppet code to configure a server can then be applied to remote servers.

### 2.1 Including External Puppet Modules

Where possible, you should aim not to re-invent the wheel. [Puppet Forge](https://forge.puppetlabs.com/)
contains a large number of externally developed modules (of varying quality), that you can use to help
configure your environment. The find out more about how to include external dependencies, please see the
[README for Librarian Puppet](https://github.com/rodjek/librarian-puppet)

### 2.2 Writing your own modules

Puppet modules cannot be contained in this repository. All puppet code must live in manifests/site.pp and
refer only to external modules if extended functionality is required. If you need to extend this repo and
an external module does not exist, you must write one.

### 2.3 Applying puppet changes to your VM

`manifests/site.pp` includes a single node called **default** - adding puppet resources (via includes,
classes or [native puppet types](http://docs.puppetlabs.com/references/latest/type.html)) to this node
definition will make them available to your VM.

To apply changed puppet code to your VM, from within this repository you can use the `bin/bootstrap`
command to connect to your local VM and apply changes. By default the VM password is ubuntu:ubuntu and
SSH will listen on a random port on localhost (as set by Vagrant).

    ./bin/bootstrap -H -d -P2222 localhost

## Testing password changing against the VM

    ./bin/bootstrap -C -d -P2222 localhost

- If you mess up the password, you can reset it either by destroying and recreating the VM or:

    MAC> vagrant up %% vagrant ssh
    VM>  sudo password ubuntu

# Full list of Rake commands

```
rake config            # Create Vagrantfile.local
```
From within the repository, you can also use vagrant commands such as `vagrant up`, `vagrant halt`
and `vagrant provision` if you wish.
