#!/usr/bin/env python

# SET Config File Parse for options

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'

# Parses the APACHE_SERVER flag within the local SET file


def apache_conf(conf):
    f = open(conf, 'r')
    conf = f.readlines()
    f.close()

    for l in conf:
        if 'APACHE_SERVER' in l:
            switch = l.strip().split('=')
            return switch[1]


def ps_ports(conf):
    f = open(conf, 'r')
    conf = f.readlines()
    f.close()

    for l in conf:
        if 'POWERSHELL_MULTI_PORTS' in l:
            ports = l.strip().split('=')
            return ports[1].split(',')
