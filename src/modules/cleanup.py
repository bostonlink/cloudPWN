#!/usr/bin/env python
# Defines general remote log pulls and cleanup tasks for all attacks

import sys
import src.core.config
import src.lib.fabfunky as fabfunky
import src.lib.ec2funky as ec2funky
import src.modules.setweb.autoset as autoset
import src.core.menus as menus
from fabric.colors import green, yellow, red
from src.modules.setweb.set_conf import apache_conf
from time import sleep

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

def cleanupz(idic, user, sshkey):
	
	# Parse the config file and unpack user options from autoset menu
	config = core.config.get_config()

	if idic["ip"] == idic["iid"]:
				
		print "Self Hosted Attack box detected... Pulling logs"
		print "Please clean system independently..."
		fabfunky.get_logz(idic["ip"], user, sshkey)
		fabfunky.disconnect_all()
		pass
			
	else:
				
		cleanup = menus.cleanup_menu()

		if cleanup == True:

			conn = ec2funky.ec2connx(config["accesskey"], config["secretkey"])
			print red("Cleaning up %s - %s instance" % (idic["tags"], idic["iid"]))
			fabfunky.get_logz(idic["ip"], user, sshkey)
			fabfunky.disconnect_all()
			ec2funky.terminate_instance(idic["iid"], conn)

		else:

			fabfunky.disconnect_all()
			print red("SSH: ssh -i %s.pem %s@%s") % (idic["key"], user,idic["ip"])
			print "Be sure to run 'python cloudPWNclean.py' after the attack to pull logs and terminate the instance."