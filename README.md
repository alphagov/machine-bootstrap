# This repository is no longer maintained

The functionality in this repository is now provided by [Puppet].

[Puppet]: http://puppetlabs.com/puppet/puppet-open-source

# Overview

This repository contains fabric tasks for bootstrapping blank machines.

The only assumption it makes is that there exists a user called 'ubuntu'.

By default it use a password of 'ubuntu' for that user, however this can be
overridden by using the -I or --password arguments to Fabric.

```sh
$ fab -l
Available commands:

change_password   Change the password for the user [ubuntu] to a new random one
custom_script     Run a custom script on the machine (requires path to script)
default           Run the default set of actions
generate_gpg_key  Setup a GPG key for a user
generate_ssh_key  Generate and install an SSH key for the supplied user [ubuntu]
harden            Secure this machine (needs key-based login first)
help              Show extended help for a task (e.g. 'fab help:changepassword')
```

# Installation/setup

Once you have cloned the repository, install the necessary python
dependencies from requirements.txt:

    pip install -r requirements.txt

# Instructions for bootstrapping machines

In the following instructions, the IP `192.0.2.32` should be replaced by the IP
or hostname (asusming you have working DNS) of the VM you wish to bootstrap.

Running the default actions on a VM:

    fab -H 192.0.2.32 default

The `default` actions are:
 - generate_rsa_key
 - generate_gpg_key
 - change_password
 - harden
   - apt_upgrade
   - setup_ufw
   - setup_fail2ban
   - setup_ssh
   - reboot

Most complicated usage, specifying tasks manually and supplying options:

    fab -H 192.0.2.32 generate_ssh_key \
                      change_password \
                      generate_gpg_key:email="puppet@localhost.localdomain",name="Puppet Hiera Key" \
                      harden

Supplying an SSH public key where PUBLICKEY is the key WITHOUT the type (e.g. ssh-rsa) or the comment (e.g. user@hostname)

    fab -H 192.0.2.32 generate_rsa_key:PUBLICKEY

To view the list of tasks:

    $ fab -l

To view extended help on a task:

    $ fab help:change_password

# Instructions for development

## 1. Bring up a development VM.

Run the following commands:

```sh
    # spin up VM
    $ vagrant up
```

At this point you will have a local VM running, with the username
'ubuntu' and the password 'ubuntu' with SSH listening on a random
port (see output of vagrant) on `127.0.0.1`

## 2. Testing fabric against the VM

- You need to specify a `--port=PORT` argument, where `PORT` is
  the SSH port your VM is mapped to. It's usually `2222` by default,
  but it depends on how many Vagrant machines you are currently running.

- You should specify a `-H` argument of `127.0.0.1`


    $ fab --port=2222 -H 127.0.0.1 change_password

- If you mess up the password, you can reset it either by destroying and recreating the VM or:

```
    user@host$ vagrant up && vagrant ssh
    vagrant@vm$ sudo passwd ubuntu
```
