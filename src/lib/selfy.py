#!/usr/bin/env python

# Self hosted functions

import src.core.config

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

def self_info(ip):
	config = src.core.config.get_config()
	return {'iid' : ip,
			'key' : config['self_key_path'],
			'ip' : ip,
			'tags' : 'Self Hosted system at %s' % ip}