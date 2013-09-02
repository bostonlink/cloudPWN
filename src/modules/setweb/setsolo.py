#!/usr/bin/env python
# Launch set with no automation

import sys
import src.core.config
import src.lib.fabfunky as fabfunky
import src.lib.ec2funky as ec2funky
from src.modules.setweb.fabsetweb import set_launch
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

def se_launch(idic, user, sshkey):
	
	# Parse the config file and unpack user options from autoset menu
	config = src.core.config.get_config()

	while True:
		try:
			sleep(2)
			print yellow("Attempting to establish a connection to %s" % idic["ip"])
			fabfunky.conn_est(idic["ip"], user, sshkey)
			break
		except Exception:
			print red("Instance is still initializing...")
			pass

	apache_status = apache_conf(config["set_config"])
		
	if apache_status == 'ON':

		if user == 'root':
			rfile = '/%s/set_config' % user
		else:
			rfile = '/home/%s/set_config' % user

		#uploads local SET config file
		fabfunky.file_upload(idic["ip"], user, config["set_config"], rfile, sshkey)
		fabfunky.move(idic["ip"], user, rfile, "/usr/share/set/config/", sshkey)
		print green("\nStarting Apache....")
		fabfunky.apache_start(idic["ip"], user, sshkey)
		print green("Apache Started...")

	else:
		pass

	interactive = menus.inter_shell_menu()
	
	if interactive == False:

		print green("\nLaunching SET...")
		set_launch(idic["ip"], user, sshkey)
		print green("\nSET Launched Credential Harvester..... browse to http://%s to test") % idic["ip"]

	elif interactive == True:
			
		print green("\nLaunching SET...")
		screen = set_launch(idic["ip"], user, sshkey)
		print green("\nSET Launched Credential Harvester..... browse to http://%s to test") % idic["ip"]

		screen = screen.strip().split()
		sleep(2)
		if '.SET' in screen[5]:
			print screen[5]
			cmd = 'sudo screen -r %s' % screen[5]
			print red("\nDropping into a SSH shell....")
			print green("SET Launched Java Applet (PyInjector)..... browse to http://%s to test") % idic["ip"]
			print yellow("\nRemember if you want to disconnect from the screen session hit CTRL+A+D to detatch and exit...\n")
			sleep(2)
			fabfunky.interactive_shell(idic["ip"], user, cmd, sshkey)
		else:
			cmd = None
			print red("\nDropping into a SSH shell....\n")
			print red("No screen session returned.")
			fabfunky.interactive_shell(idic["ip"], user, cmd, sshkey)