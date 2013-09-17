#!/usr/bin/env python

# Fabric python magic for distributed nmap scanning

from time import sleep
from fabric.api import *
from src.lib.fabfunky import file_upload

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

# Funtion to automate set web attacks


def set_auto(host, user, autofile, sshkey):
    with settings(host_string = host, user = user, key_filename = sshkey, warn_only = True):
        uploaddir = "/tmp/autoset.txt"
        file_upload(host, user, autofile, uploaddir, sshkey)
        f = open("data/temp/setweb.sh", "w")
        f.write("cd /usr/share/set/\n")
        f.write('sudo screen -A -m -d -L -S SET "/usr/share/set/set-automate" "/tmp/autoset.txt"\n')
        f.write("sudo screen -ls")
        f.close()
        file_upload(host, user, "data/temp/setweb.sh", "/tmp/setweb.sh", sshkey)
        screen = run("bash /tmp/setweb.sh")
        sleep(1)
        return screen

# Function to launch set with no automation


def set_launch(host, user, sshkey):
    with settings(host_string = host, user = user, key_filename = sshkey, warn_only = True):
        f = open("data/temp/setweb.sh", "w")
        f.write("cd /usr/share/set/\n")
        f.write('sudo screen -A -m -d -L -S SET /usr/share/set/setoolkit\n')
        f.write("sudo screen -ls")
        f.close()
        file_upload(host, user, "data/temp/setweb.sh", "/tmp/setweb.sh", sshkey)
        screen = run("bash /tmp/setweb.sh")
        sleep(1)
        return screen
