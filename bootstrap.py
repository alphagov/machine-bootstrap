from fabric import state
from fabric.api import *
from fabric.colors import *
from fabric.task_utils import crawl
from fabric.utils import puts, fastprint

# For password generation
from passlib.hash import sha512_crypt
import random
import string

# For ssh key generation
from Crypto.PublicKey import RSA

# For gpg key generation
from StringIO import StringIO

# For help function
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

def warn(message):
    puts(red(message))

# Helper functions for password management

def _choose_random_chars(alphabet,length):
    """From an alphabet, choose a number of random characters"""
    chars = []
    for i in range(length):
        chars.append(random.choice(alphabet))
    return "".join(chars)


def _generate_salt(length):
    """Generate a random string of length to be used as a SHAS512 salt"""
    salt_alphabet = string.digits + string.ascii_letters + "./"
    salt = _choose_random_chars(salt_alphabet,length)
    return salt


def _generate_password(length):
    """Generate a random string of length to be used as a password"""
    password_alphabet = string.digits + string.ascii_letters
    password = _choose_random_chars(password_alphabet,length)
    return password


def _encrypt_password(password):
    """Generate the salted password hash using SHA512 with the same options as Ubuntu 12.04"""
    return sha512_crypt.encrypt(password,salt=_generate_salt(8),rounds=5000)


def _new_password(length, user):
    """Output {password => "PLAINTEXT", shadow => "Shadow entry"} dict for later use"""
    output = {}
    output['password'] = _generate_password(length)
    output['shadow'] = "%s:%s:::::::" % (user, _encrypt_password(output['password']))
    return output


# Helper functions for ssh key management

def _generate_rsa_key(username):
    key = RSA.generate(2048)
    key_info = {}
    key_info['private'] = key.exportKey('PEM')
    key_info['public']  = key.exportKey('OpenSSH') + " %s@%s" % (username,env.host)
    return key_info


def _setup_key_auth(username="ubuntu",ssh_publickey=None):
    if ssh_publickey is None:
        key = _generate_rsa_key(username)
        warn('New SSH private key for %s@%s' % (username, env.host))
        print('')
        fastprint(key['private'])
        print('')
        print('')
        publickey = key['public']
    else:
        info('Using supplied public key for SSH')
        publickey = "ssh-rsa " + ssh_publickey + " %s@%s" % (username,env.host)
    sudo('test -d ~%s/.ssh || mkdir ~%s/.ssh && chmod 700 ~%s/.ssh' % (username,username,username))
    sudo('echo "%s" >> ~%s/.ssh/authorized_keys && chmod 600 ~%s/.ssh/authorized_keys' % (publickey,username,username))


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
def change_password(my_user="ubuntu"):
    """
    Change the password for the user [ubuntu] to a new random one
    """
    info("Changing password for %s user" % my_user)
    new_pass = _new_password(10,my_user)
    command = "sed -i 's;" + my_user + ":.*;" + new_pass['shadow'] + ";g' /etc/shadow"
    sudo(command)
    old_pass = env.password
    env.password = new_pass['password']
    try:
        with hide('stdout'):
            run('uname -a')
        warn("New password for %s is %s" % (my_user,new_pass['password']))
    except:
        warn("Password change failed, try logging in manually with old password")
        env.password = old_pass

@task
def generate_ssh_key(username="ubuntu",ssh_publickey=None):
    """
    Generate and install an SSH key for the supplied user [ubuntu]

    This will generate a unique SSH key on your machine and add the
    public key to the /home/${username}/.ssh/authorized_keys file.

    You can set a particular public key by supplying the correct
    argument (ssh_publickey=path/to/public/key) to the task.
    """
    info("Setting up SSH key-auth for %s" % username)
    _setup_key_auth(username,ssh_publickey)


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
    info("Running script: %s" % script_path)
    put(local_path=script_path,remote_path="/root/.bootstrap-script",use_sudo=True)
    sudo('chmod 755 /root/.bootstrap-script && /root/.bootstrap-script')


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
    info('Creating a GPG key for %s' % username)
    info('    Name:  %s' % name)
    info('    Email: %s' % email)
    with hide('stdout'):
        info(' - Installing gnupg2 and haveged')
        sudo('apt-get install -y gnupg2 haveged')
        options = """
                  Key-Type: RSA
                  Key-Length: 4096
                  Subkey-Type: default
                  Name-Real: %s
                  Name-Email: %s
                  Expire-Date: 0
                  %%commit
                  """ % (name,email)
        real_options = textwrap.dedent(options).strip()
        info(' - Creating GPG key')
        sudo('echo "%s" | gpg2 --batch --gen-key -' % real_options,user=username)
    warn('New GPG public key - please use wisely')
    my_output = StringIO()
    sudo('gpg2 --armor --export "%s" > /tmp/gpg_key' % name,user=username)
    get('/tmp/gpg_key',my_output)
    print('')
    fastprint(my_output.getvalue())
    print('')
    my_output.close()
    sudo('rm -f /tmp/gpg_key')

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

