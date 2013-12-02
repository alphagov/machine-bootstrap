from fabric.api import *

@task
def changepassword(username="ubuntu",password=""):
    """Change the password for username [default: ubuntu] (will create password if not supplied)"""
    # Prompt for a new password if it's not supplied on stdin
    # SSH to machine and change password
    # Test that password change works, if not bail
    print "unimplemented: changepassword"

@task
def gensshkey(username="ubuntu"):
    """Generate and install an SSH key for the supplied user [ubuntu]"""
    # Generate an RSA key
    # Print the public key
    # Print the private key
    # Copy the private key to the machine
    # Test that key auth works
    print "unimplemented: genrsakey"

@task
def harden():
    """Harden this machine using the config in the puppet dir"""
    # Copy puppet up to machine
    # Install necessary packages
    # Run librarian puppet
    # Run puppet
    print "unimplemented: harden"

@task
def customscript(script_path):
    """Run a custom script on the machine (requires path to script)"""
    # Copy script to machine
    # Run script under sudo
    # Report errors
    print "unimplemented: customscript"

@task
def gpgsetup(username="root",email="root@localhost.localdomain",name="GPG Key"):
    """Will setup a GPG key for the user [root] with email [root@localhost.localdomain] and name [GPG key] supplied"""
    # Create a new GPG key on the machine for the name and email
    # Export the GPG key
    print "unimplemented: gpgsetup"

@task
def default():
    changepassword()
    gensshkey()
    gpgsetup()
    harden()


