#!/usr/bin/env python

# EC2 and boto python magic with the ec2funky functions for cloudSET

import boto.ec2
from time import sleep, strftime
from datetime import datetime
from fabric.colors import green, yellow, red

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

def ec2connx(accesskey, secretkey):
	return boto.ec2.connect_to_region("us-east-1", aws_access_key_id=accesskey, aws_secret_access_key=secretkey)

def get_images(conn, imagelst):
	return conn.get_all_images(image_ids=imagelst)

def new_instance_launch(image_id, connection, key_name, instance_type, sec_group):
	print green("creating instance from...... " + image_id)
	ress = connection.run_instances(image_id,
		key_name = key_name,
		instance_type = instance_type,
		security_groups=[sec_group])
	
	while True:
		res = connection.get_all_instances(instance_ids=[ress.instances[0].id])
		if res[0].instances[0].state == 'pending':
			print yellow("%s's status is still %s. wait for the boot!" % (res[0].instances[0].id, res[0].instances[0].state))
			sleep(2)
		elif res[0].instances[0].state == 'running':
			res[0].instances[0].add_tag("Name", "SET Attack - %s" % strftime("%m-%d-%Y %H:%M:%S"))
			print green("Instance started.... and its current state is %s" % res[0].instances[0].state) 
			print red("Ready to rock and roll, pwn them all!")
			break

	return ress.instances[0].id

def multi_instance_launch(image_id, connection, min_count, max_count, key_name, instance_type, sec_group):
	print green("creating %s instances from...... %s" % (str(max_count), image_id))
	ress = connection.run_instances(image_id,
		min_count = min_count,
		max_count = max_count,
		key_name = key_name,
		instance_type = instance_type,
		security_groups=[sec_group])
	
	count = 1
	iid_list = []
	for instance in ress.instances:
		instance.add_tag("Name", "Instance %s - %s" % (count, strftime("%m-%d-%Y %H:%M:%S")))
		iid_list.append(instance)
		count += 1

	for instance in ress.instances:
		while True:
			if instance.state == 'pending':
				instance.update()
				print yellow("%s's status is still %s. wait for the boot!" % (instance.id, instance.state))
				sleep(2)
			elif instance.state == 'running':
				print green("Instance %s started.... and its current state is %s" % (instance.id, instance.state))
				break
		
	print red("Ready to rock and roll, pwn them all!")
	return iid_list


def terminate_instance(instance_id, connection):
	print "Terminating %s instance....." % instance_id
	userin = raw_input("Are you sure you want to terminate the instance? [Y/N] ")
	if userin == 'Y' or userin == 'y' or userin == 'Yes' or userin == 'yes':
		connection.terminate_instances(instance_ids=[instance_id])
		print red("Instance %s terminated! No turning back now!" % instance_id)
	elif userin == 'N' or userin == 'n' or userin == 'no' or userin == 'No':
		print yellow("cancelling termination of %s" % instance_id)
		pass

def instance_info(instance_id, connection):
	res = connection.get_all_instances(instance_ids=[instance_id])
	return {'iid' : instance_id,
			'itype' : res[0].instances[0].instance_type, 
			'aid' : res[0].instances[0].image_id, 
			'placement' : res[0].instances[0].placement,
			'state' : res[0].instances[0].state,
			'key' : res[0].instances[0].key_name,
			'ltime' : res[0].instances[0].launch_time,
			'pip' : res[0].instances[0].private_ip_address,
			'ip' : res[0].instances[0].ip_address,
			'groups' : res[0].instances[0].groups,
			'kernel' : res[0].instances[0].kernel,
			'ramdisk' : res[0].instances[0].ramdisk,
			'arch' : res[0].instances[0].architecture,
			'platform' : res[0].instances[0].platform,
			'tags' : res[0].instances[0].tags.get("Name")}