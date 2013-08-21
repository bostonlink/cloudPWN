#!/usr/bin/env python

# Fabric python magic with the fabfunky functions for cloudPwn

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

def nmap_syn_default(host, user, iplist, opts, sshkey):
	with settings(host_string = host, user = user, key_filename = sshkey, warn_only = True):
		f = open('data/temp/nmap.sh', 'w')
		f.write("mkdir nmap\n")
		f.write("cd nmap\n")
		f.write("sudo screen -A -m -d -L -S NMAP nmap -sS %s %s\n" % (iplist, opts))
		f.write("sudo screen -ls\n")
		f.close()
		file_upload(host, user, 'data/temp/nmap.sh', '/tmp/nmap.sh', sshkey)
		screen = run("bash /tmp/nmap.sh")
		local("rm -f data/temp/nmap.sh")
		return screen

def nmap_syn_full(host, user, iplist, opts, sshkey):
	with settings(host_string = host, user = user, key_filename = sshkey, warn_only = True):
		f = open('data/temp/nmap.sh', 'w')
		f.write("mkdir nmap\n")
		f.write("cd nmap\n")
		f.write("sudo screen -A -m -d -L -S NMAP nmap -sS -p 0- %s %s\n" % (iplist, opts))
		f.write("sudo screen -ls\n")
		f.close()
		file_upload(host, user, 'data/temp/nmap.sh', '/tmp/nmap.sh', sshkey)
		screen = run("bash /tmp/nmap.sh")
		local("rm -f data/temp/nmap.sh")
		return screen

def nmap_syn_targeted(host, user, iplist, portlst, opts, sshkey):
	with settings(host_string = host, user = user, key_filename = sshkey, warn_only = True):
		f = open('data/temp/nmap.sh', 'w')
		f.write("mkdir nmap\n")
		f.write("cd nmap\n")
		f.write("sudo screen -A -m -d -L -S NMAP nmap -sS -p %s %s %s\n" % (portlst, iplist, opts))
		f.write("sudo screen -ls\n")
		f.close()
		file_upload(host, user, 'data/temp/nmap.sh', '/tmp/nmap.sh', sshkey)
		screen = run("bash /tmp/nmap.sh")
		local("rm -f data/temp/nmap.sh")
		return screen

def nmap_tcp_default(host, user, iplist, opts, sshkey):
	with settings(host_string = host, user = user, key_filename = sshkey, warn_only = True):
		f = open('data/temp/nmap.sh', 'w')
		f.write("mkdir nmap\n")
		f.write("cd nmap\n")
		f.write("sudo screen -A -m -d -L -S NMAP nmap -sT %s %s\n" % (iplist, opts))
		f.write("sudo screen -ls\n")
		f.close()
		file_upload(host, user, 'data/temp/nmap.sh', '/tmp/nmap.sh', sshkey)
		screen = run("bash /tmp/nmap.sh")
		local("rm -f data/temp/nmap.sh")
		return screen

def nmap_tcp_targeted(host, user, iplist, portlst, opts, sshkey):
	with settings(host_string = host, user = user, key_filename = sshkey, warn_only = True):
		f = open('data/temp/nmap.sh', 'w')
		f.write("mkdir nmap\n")
		f.write("cd nmap\n")
		f.write("sudo screen -A -m -d -L -S NMAP nmap -sT -p %s %s %s\n" % (portlst, iplist, opts))
		f.write("sudo screen -ls\n")
		f.close()
		file_upload(host, user, 'data/temp/nmap.sh', '/tmp/nmap.sh', sshkey)
		screen = run("bash /tmp/nmap.sh")
		local("rm -f data/temp/nmap.sh")
		return screen