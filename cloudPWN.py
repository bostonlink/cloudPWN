#!/usr/bin/env python

# CloudPWN source

import sys
import core.config
import core.lib.ec2funky as ec2funky
import core.lib.fabfunky as fabfunky
import core.modules.setweb as setweb
import core.menus as menus
import core.lib.selfy
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
config = core.config.get_config()
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

		# Launched new instance from user selection
		if iid == None:
			iid = ec2funky.new_instance_launch(aid, conn, securitykey, instance_type, security_group)

		# bulds instance information dictionary of the launched instance
		iinfo_dic = ec2funky.instance_info(iid, conn)

		# Launch SET Web Attacks
		setweb.set_web_attacks(iinfo_dic)
	
		# Local Cleanup 
		fabfunky.clean_local()

	elif linode == True and amazon == False:
		print "Support for linode is coming soon.  Please use AWS for now."
		sys.exit(0)

	elif self_hosted == True:
		ip = raw_input("Please enter the IP address of the Self hosted attack box: ")
		self_dic = core.lib.selfy.self_info(ip)
		print self_dic

# Keyboard inturrupt exception
except KeyboardInterrupt:
	print yellow("\n\nExiting..... Come back soon!")