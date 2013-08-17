#!/usr/bin/env python

# cloudPWN source

import sys
import src.core.config
import src.lib.ec2funky as ec2funky
import src.lib.fabfunky as fabfunky
import src.core.menus as menus
import src.lib.selfy
from src.modules.setweb.charvest import charvest_launch
from src.modules.setweb.java_applet_default import java_applet
from src.modules.setweb.java_applet_pyinj import java_pyi
from src.modules.cleanup import cleanupz
from fabric.colors import red, yellow

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

# Parsing the config file
config = src.core.config.get_config()
accesskey = config["accesskey"]
secretkey = config["secretkey"]
securitykey = config["securitykey"]
security_group = config["security_group"]
instance_type = config["instance_type"]

# Select what service to launch and get the instance id
try:

	amazon, linode, self_hosted = menus.main_menu()
	
	if amazon == True and linode == False:
		
		conn = ec2funky.ec2connx(accesskey, secretkey)
		iid, aid = menus.image_menu()

		# launches new instance and sets the image id of the instance
		if iid == None:
			iid = ec2funky.new_instance_launch(aid, conn, securitykey, instance_type, security_group)

		# bulds instance information dictionary of the launched instance
		iinfo_dic = ec2funky.instance_info(iid, conn)

		# Launches SET Web Attacks
		java_app_pyi, java_app, charvest = menus.autoset_menu()
	
		if java_app_pyi == True:
			
			java_pyi(iinfo_dic, config['instance_user'], config['keypath'])
		
		elif java_app == True:

			java_applet(iinfo_dic, config['instance_user'], config['keypath'])

		elif charvest == True:

			charvest_launch(iinfo_dic, config['instance_user'], config['keypath'])

		# remote log pull and terminiation of instance
		cleanupz(iinfo_dic, config['instance_user'], config['keypath'])
	
		# Local temp file cleanup 
		fabfunky.clean_local()

	elif linode == True and amazon == False:
		print "Support for linode is coming soon.  Please use AWS for now."
		sys.exit(0)

	elif self_hosted == True:
		ip = raw_input("Please enter the IP address of the Self hosted attack box: ")
		self_dic = core.lib.selfy.self_info(ip)
		
		# Launches SET Web Attacks
		java_app_pyi, java_app, charvest = menus.autoset_menu()
	
		if java_app_pyi == True:
			
			java_pyi(self_dic, config['self_user'], config['self_key_path'])
		
		elif java_app == True:

			java_applet(self_dic, config['self_user'], config['self_key_path'])

		elif charvest == True:

			charvest_launch(self_dic, config['self_user'], config['self_key_path'])

		# remote log pull and terminiation of instance
		cleanupz(self_dic, config['self_user'], config['self_key_path'])
	
		# Local temp file cleanup 
		fabfunky.clean_local()

# Keyboard inturrupt exception
except KeyboardInterrupt:
	print yellow("\n\nExiting..... Come back soon!")