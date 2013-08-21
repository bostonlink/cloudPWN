#!/usr/bin/env python

# cloudPWN config functions

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