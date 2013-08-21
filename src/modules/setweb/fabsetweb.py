#!/usr/bin/env python

# Fabric python magic for distributed nmap scanning

from fabric.api import *
from fabric.colors import green, yellow, red
from fabric.state import connections

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

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