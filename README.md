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
    $ vagrant up # spin up VM
```

At this point you will have a local VM running, with the username 'ubuntu' and the password 'ubuntu'
with SSH listening on a random port (see output of vagrant).

## 2. Testing password changing against the VM

    ./bin/bootstrap -C -d -P2222 localhost

- If you mess up the password, you can reset it either by destroying and recreating the VM or:

```
    user@host$ vagrant up && vagrant ssh
    vagrant@vm$ sudo password ubuntu
```
