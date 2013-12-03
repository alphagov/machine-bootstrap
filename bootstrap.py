from fabric import state
from fabric.api import *
from fabric.colors import *
from fabric.task_utils import crawl
from fabric.utils import puts, fastprint
import textwrap


# This is an opinionated module that assumes that the ubuntu user exists
env.user="ubuntu"


# Unless we pass a password on the command-line via -I or --password we assume it is ubuntu
if env.password == None:
    env.password="ubuntu"


# By default we want to manage our own output
state.output.status=False
state.output.running=False


# General helper functions and tasks

@task
def help(name=""):
    """
    Show extended help for a task (e.g. 'fab help:changepassword')

    These fabric tasks are designed to take a vanilla Ubuntu 12.04
    machine with default passwords/setup and then apply various
    security tasks to make it suitable to place this machine on the
    internet awaiting further setup.
    """
    task = crawl(name, state.commands)
    if name is "":
        help("help")
    elif task is None:
        abort("%r is not a valid task name" % task)
    else:
        puts(textwrap.dedent(task.__doc__).strip())


def info(message):
    puts(blue(message))


# Helper functions for password management

# Helper functions for gpg key management

# Helper functions to be used in other tasks

def _apt_update():
    """
    Run 'apt-get update' on this machine.

    Update all the package indexes. This should be run prior
    to installing any packages.
    """
    info('Running apt-get update')
    with hide('running','stdout'):
        sudo('/usr/bin/apt-get update -qq >>/root/machine-bootstrap.log')


def _apt_upgrade():
    """
    Run 'apt-get upgrade' on this machine.

    This will update all packages to the latest version
    supplied by the OS vendor.
    """
    info('Running apt-get upgrade')
    with hide('running','stdout'):
        sudo('DEBIAN_FRONTEND=noninteractive /usr/bin/apt-get upgrade -qq -y >>/root/machine-bootstrap.log')


def _reboot():
    """
    Reboot the machine.

    Reboot machine, to be used after all configuration is completed.
    """
    info('Rebooting machine immediately')
    with hide('running','stdout'):
        sudo('shutdown -r now')


def _setup_ufw():
    """Enable UFW with port 22 open"""
    info('Enabling UFW with allow for 22/tcp')
    with hide('running','stdout'):
        sudo('/usr/bin/apt-get install -y ufw')
        sudo('/usr/sbin/ufw allow 22/tcp')
        sudo('yes | ufw enable')


def _setup_fail2ban():
    """Install fail2ban package"""
    info('Installing and starting fail2ban')
    with hide('running','stdout'):
        sudo('/usr/bin/apt-get install -y fail2ban >>/root/machine-bootstrap.log')
        sudo('/usr/sbin/service fail2ban start >>/root/machine-bootstrap.log')


def _setup_ssh():
    """Disable password logins to SSH"""
    info('Disabling password logins to SSH')
    with hide('running','stdout'):
        sudo('/bin/sed -i \'s/PasswordAuthentication yes/PasswordAuthentication no/g\' /etc/ssh/sshd_config >>/root/machine-bootstrap.log')
        sudo('/sbin/restart ssh >>/root/machine-bootstrap.log')


# Public fabric tasks

@task
def change_password(username="ubuntu",password=""):
    """
    Change the password for username [default: ubuntu]

    You can supply optional username and password arguments if you wish
    to set a particular password or change the password for a different
    user than the default [ubuntu]
    """
    # Prompt for a new password if it's not supplied on stdin
    # SSH to machine and change password
    # Test that password change works, if not bail
    print "unimplemented: change_password"


@task
def generate_ssh_key(username="ubuntu",ssh_publickey=""):
    """
    Generate and install an SSH key for the supplied user [ubuntu]

    This will generate a unique SSH key on your machine and add the
    public key to the /home/${username}/.ssh/authorized_keys file.

    You can set a particular public key by supplying the correct
    argument (ssh_publickey=path/to/public/key) to the task.
    """
    # Generate an RSA key
    # Print the public key
    # Print the private key
    # Copy the private key to the machine
    # Test that key auth works
    print "unimplemented: generate_rsa_key"


@task
def harden():
    """
    Secure this machine (needs key-based login first)

    This will:
        - Disable password logins to SSH
        - Enable UFW with port 22 open
        - Install Fail2ban with the default config
    """
    info('Running hardening tasks')
    with hide('running'):
        _apt_upgrade()
        _setup_ufw()
        _setup_fail2ban()
        _setup_ssh()


@task
def custom_script(script_path):
    """
    Run a custom script on the machine (requires path to script)

    The argument to this script should be an executable script that
    will run as root on the destination machine.
    """
    # Copy script to machine
    # Run script under sudo
    # Report errors
    print "unimplemented: customscript"


@task
def generate_gpg_key(username="root",email="root@localhost.localdomain",name="GPG Key"):
    """
    Setup a GPG key for a user

    Create a GPG key for the user specified [root] with:
        - email: [root@localhost.localdomain]
        - name: [GPG key]

    The output will be the Public GPG key with the private key
    stored only on the machine. The intention is that this can
    then be used to encrypt files for decryption only by this
    machine.
    """
    # Create a new GPG key on the machine for the name and email
    # Export the GPG key
    print "unimplemented: gpgsetup"


@task
def default():
    """
    Run the default set of actions

    These are:
        - apt_update
        - generate_rsa_key
        - generate_gpg_key
        - change_password
        - harden
            - apt_upgrade
            - setup_ufw
            - setup_fail2ban
            - setup_ssh
        - reboot
    """
    _apt_update()
    generate_ssh_key()
    generate_gpg_key()
    change_password()
    harden()
    _reboot()

