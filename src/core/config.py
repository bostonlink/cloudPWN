#!/usr/bin/env python

# cloudPWN config functions

import hashlib

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

# Parses the cloudPWN config file and returns a dictionary of config options


def get_config():
    config_file = "config/cloudPWN.conf"
    config = {}
    execfile(config_file, config)
    return config

# Checks the hash of the set_conf file to the set_conf.orig
#and if different uploaded the set_conf file to the remote instance


def check_setconf():
    setorig = 'config/autoset/set_config.orig'
    sof = open(setorig, 'r')
    setmod = 'config/autoset/set_config'
    smf = open(setmod, 'r')

    orighash = hashlib.md5(sof.read())
    modhash = hashlib.md5(smf.read())

    sof.close()
    smf.close()

    if orighash.hexdigest() != modhash.hexdigest():
        return True
    else:
        return False
