#!/usr/share/env python

# cloudPWN menus for interactive user options
import sys
import src.lib.ec2funky as ec2funky
import src.core.config
from fabric.colors import green, red

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
    count = 0
    print "Supported cloud services:"
    count += 1
    print "%s. Amazon AWS EC2" % str(count)
    count += 1
    print "%s. Linode (TODO)" % str(count)
    count += 1
    print "%s. Self Hosted External box\n" % str(count)
    userin = raw_input("Select a service (1/2/3): ")
    if int(userin.strip()) > count:
        print red("Your selection is wrong, try again.")
        sys.exit(0)
    elif int(userin.strip()) == 1:
        aws = True
        linode = False
        self_hosted = False
    elif int(userin.strip()) == 2:
        aws = False
        linode = True
        self_hosted = False
    elif int(userin.strip()) == 3:
        aws = False
        linode = False
        self_hosted = True

    return aws, linode, self_hosted

# Instance Menu


def image_menu():
    config = src.core.config.get_config()
    conn = ec2funky.ec2connx(config['accesskey'], config['secretkey'])
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
    config = src.core.config.get_config()
    conn = ec2funky.ec2connx(config['accesskey'], config['secretkey'])
    existing_instances = conn.get_all_instances()
    ret_dic = {}
    count = 0

    # Lists existing EC2 images for selection
    print green("\nAWS EC2 Launched Instances")
    for inst in existing_instances:
        print str(count) + ". " + str(inst.instances[0].tags.get("Name")) + " - " + str(inst.instances[0].id) + " : " + str(inst.instances[0].image_id) + " (%s)" % str(inst.instances[0].state)
        ret_dic[str(count)] = [inst.instances[0].id, inst.instances[0].image_id]
        count += 1

# SET Web Attack Menu


def autoset_menu():
    count = 0
    print "\nSelect the SET attack you would like to launch:"
    count += 1
    print "%s. Java Applet (PyInjector)" % str(count)
    count += 1
    print "%s. Java Applet (Reverse Meterpreter x86)" % str(count)
    count += 1
    print "%s. Credential Harvester" % str(count)
    count += 1
    print "%s. Launch SET with No Automation\n"
    userin = raw_input("Select and option: ")
    if int(userin.strip()) > count:
        print "Try Harder!"
        autoset_menu()
    elif int(userin.strip()) == 1:
        java_app_pyi = True
        java_app = False
        charvest = False
        setsolo = False
    elif int(userin.strip()) == 2:
        java_app_pyi = False
        java_app = True
        charvest = False
        setsolo = False
    elif int(userin.strip()) == 3:
        java_app_pyi = False
        java_app = False
        charvest = True
        setsolo = False
    elif int(userin.strip()) == 4:
        java_app_pyi = False
        java_app = False
        charvest = False
        setsolo = True

    return java_app_pyi, java_app, charvest, setsolo

# SET Automation file variable menu


def autoset_file_menu():
    print "\nPlease enter the following information."
    return raw_input("Website to clone: ")

# Interactive SSH shell menu


def inter_shell_menu():
    print "Interactive SSH session if you select 'NO' you will have to manually connect to the instance."
    userin = raw_input("\nWould you like to spawn an interactive SSH session? [Y/N] ")
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
