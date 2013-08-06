#!/usr/bin/env python

# EC2 and boto python magic with the ec2funky functions for cloudSET

import boto.ec2
from time import sleep
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

def new_instance_launch(selection_id, connection, key_name, instance_type, sec_group):
	print green("creating instance from...... " + selection_id)
	connection.run_instances(selection_id,
		key_name = key_name,
		instance_type = instance_type,
		security_groups=[sec_group])
	res = connection.get_all_instances()
	for r in res:
		if r.instances[0].state == 'pending':
			new_id = r.instances[0].id
	
	while True:
		res = connection.get_all_instances(instance_ids=[new_id])
		if res[0].instances[0].state == 'pending':
			print yellow("%s's status is still %s. wait for the boot!" % (res[0].instances[0].id, res[0].instances[0].state))
			sleep(2)
		elif res[0].instances[0].state == 'running':
			print green("Instance started.... and its current state is %s" % res[0].instances[0].state) 
			print red("Ready to rock and roll, pwn them all!")
			break

	return new_id

def start_instance(instance_id, connection):
	res = connection.get_all_instances(instance_ids=[instance_id])
	print green("\nStarting %s instance" % res[0].instances[0].id)
	res[0].instances[0].start()
	while True:
		res = connection.get_all_instances(instance_ids=[instance_id])
		if res[0].instances[0].state == 'pending':
			print yellow("%s's status is still %s. wait for the it!" % (res[0].instances[0].id, res[0].instances[0].state))
			sleep(2)
		elif res[0].instances[0].state == 'running':
			print green("Instance started....")
			print "ssh into the instance using %s key" % res[0].instances[0].key_name
			print "cmd: ssh -i %s.pem ubuntu@%s" % (res[0].instances[0].key_name, res[0].instances[0].ip_address)
			print red("Ready to rock and roll, pwn them all!")
			break

def stop_instance(instance_id, connection):
	print "Stopping %s instance......" % instance_id
	connection.stop_instances(instance_ids=[instance_id])
	print "Instance %s stopped...." % instance_id

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