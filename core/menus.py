#!/usr/share/env python 

# cloudPWN menus for interactive user options
import sys
import core.lib.ec2funky as ec2funky
import core.config
from fabric.colors import green, yellow, red

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

# Main Menu
def main_menu():
	print "Supported cloud services"
	print "1. Amazon AWS EC2"
	print "2. Linode (TODO)"
	print "3. Self Hosted External box (TODO)\n"
	print "Please select a cloud service to launch an attack from."
	userin = raw_input("Select a service (1/2/3): ")
	if int(userin.strip()) > 2:
		print red("Your selection is wrong, try again.")
		sys.exit(0)
	elif int(userin.strip()) == 1:
		aws = True
		linode = False
	elif int(userin.strip()) == 2:
		aws = False
		linode = True

	return aws, linode

# Instance Menu
def image_menu():
	config = core.config.get_config()
	conn = ec2funky.ec2connx(config['accesskey'], config['secretkey'])
	existing_instances = conn.get_all_instances()
	ami_images = ec2funky.get_images(conn, config["image_list"])
	ret_dic = {}
	count = 0

	# Lists exitsing EC2 AMI preconfigured images listed in config file
	print green("\nAvailable AWS AMI Images to Launch")
	for image in ami_images:
		print "%s. %s - %s - %s" % (str(count), image.name, image.description, image.id)
		ret_dic[str(count)] = [None, image.id]
		count += 1

	data = raw_input("\nEnter the image number to launch: ")
	if int(data) >= len(ret_dic):
		print red("Selection is out of range! Goodbye!")
		sys.exit(0)
	else:
		return ret_dic[data]

def instance_list():
	config = core.config.get_config()
	conn = ec2funky.ec2connx(config['accesskey'], config['secretkey'])
	existing_instances = conn.get_all_instances()
	ami_images = ec2funky.get_images(conn, config["image_list"])
	ret_dic = {}
	count = 0

	# Lists existing EC2 images for selection
	print green("\nAWS EC2 Launched Instances")
	for inst in existing_instances:
		print str(count) + ". " + str(inst.instances[0].tags.get("Name")) + " - " + str(inst.instances[0].id) + " : " + str(inst.instances[0].image_id) + " (%s)" % str(inst.instances[0].state)
		ret_dic[str(count)] = [inst.instances[0].id, inst.instances[0].image_id]
		count += 1

# Launch or start menu
def launch_start_menu():
	print "\nPlese select if you would like to launch a new instance from the instance selected or start the current instance selected"
	print "1. Launch a new instance"
	print "2. Start selected instance"
	userin = raw_input("Please select 1 or 2: ")
	if int(userin.strip()) > 2:
		print "Your selection is wrong"
		main_menu()
	elif int(userin.strip()) == 1:
		launch_new = True
		start = False
	elif int(userin.strip()) == 2:
		launch_new = False
		start = True

	return launch_new, start

# SET Web Attack Menu
def autoset_menu():
	print "\nSelect the SET attack you would like to launch"
	print "1. Java Applet (PyInjector)"
	print "2. Java Applet (Reverse Meterpreter x86)"
	print "3. Credential Harvester"
	userin = raw_input("Select and option: ")
	if int(userin.strip()) > 3:
		print "Try Harder!"
		autoset_menu()
	elif int(userin.strip()) == 1:
		java_app_pyi = True
		java_app = False
		charvest = False
	elif int(userin.strip()) == 2:
		java_app_pyi = False
		java_app = True
		charvest = False
	elif int(userin.strip()) == 3:
		java_app_pyi = False
		java_app = False
		charvest = True

	return java_app_pyi, java_app, charvest

# SET Automation file variable menu
def autoset_file_menu():
	print "\nPlease enter the following information."
	return raw_input("Website to clone: ")

# Interactive SSH shell menu
def inter_shell_menu():
	print "Interactive shell if you select no you will have to manually connect to the instance."
	userin = raw_input("\nWould you like to spawn an interactive shell? [Y/N] ")
	if userin == "Y" or userin == "y" or userin == "Yes" or userin == "yes":
		return True
	elif userin == "N" or userin == "n" or userin == "No" or userin == "no":
		return False

def cleanup_menu():
	print red("\nSelecting 'Yes' here will shutdown the attack, pull remote logs, and terminate the instance...")
	userin = raw_input(red("Is the attack done or are you still waiting for reverse connections? [Y/N] "))
	if userin == "Y" or userin == "y" or userin == "Yes" or userin == "yes":
		return True
	else:
		return False