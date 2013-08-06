#!/usr/bin/env python

# cloudPWN source cleanup script when done attacking

import core.lib.ec2funky as ec2funky
import core.lib.fabfunky as fabfunky
import sys
import core.config
from fabric.colors import green, red

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

try:
	# Parsing the config file
	config = core.config.get_config()

	accesskey = config["accesskey"]
	secretkey = config["secretkey"]
	securitykey = config["securitykey"]
	security_group = config["security_group"]
	instance_type = config["instance_type"]

	# Establishing EC2 connection
	conn = ec2funky.ec2connx(accesskey, secretkey)
	instances = conn.get_all_instances()
	ret_dic = {}
	count = 1

	# Lists running instances need to fix up logic so it does not repeat (Quickfix)
	for inst in instances:
		print green("\nAWS EC2 Running Instances")
		for inst in instances:
			if inst.instances[0].state == "running":
				print str(count) + ". " + str(inst.instances[0].tags.get("Name")) + " - " + str(inst.instances[0].id) + " : " + str(inst.instances[0].image_id) + " (%s)" % str(inst.instances[0].state)
				ret_dic[str(count)] = [inst.instances[0].id, inst.instances[0].image_id]
				count += 1
			else:
				pass

	# User input which instance to terminate
	data = raw_input("\nEnter the instance number: ")
	if int(data) > len(ret_dic):
		print red("Selection is out of range! Goodbye!")
		sys.exit(0)
	else:
		choice = ret_dic[data]
		iinfo_dic = ec2funky.instance_info(choice[0], conn)

	# Pull remote logs and terminate instance
	print "You are about to clean and terminate %s - %s instance" % (iinfo_dic["tags"], iinfo_dic["iid"])
	userin = raw_input("Proceed with cleaning? [Y/N]: ")
	if userin == 'Y' or userin == 'y' or userin == 'yes' or userin == 'Yes':
		print red("Cleaning up %s - %s instance" % (iinfo_dic["tags"], iinfo_dic["iid"]))
		fabfunky.get_logz(iinfo_dic["ip"], config["instance_user"])
		ec2funky.terminate_instance(iinfo_dic["iid"], conn)

	fabfunky.disconnect_all()

# Keyboard inturrupt exception
except KeyboardInterrupt:
	print yellow("\n\nExiting..... Come back soon!")