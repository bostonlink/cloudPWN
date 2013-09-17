#!/usr/bin/env python
# Fucking around TODO

import random

__author__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__copyright__ = 'Copyright 2013, GuidePoint Security LLC'
__credits__ = ['GuidePoint Security LLC']
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'David Bressler (@bostonlink), GuidePoint Security LLC'
__email__ = 'david.bressler@guidepointsecurity.com'
__status__ = 'Development'


def randhead():
    head0 = """
       .__                   ._____________  __      _________ \r 
  ____ |  |   ____  __ __  __| _/\______   \/  \    /  \      \  \r
_/ ___\|  |  /  _ \|  |  \/ __ |  |     ___/\   \/\/   /   |   \ \r
\  \___|  |_(  <_> )  |  / /_/ |  |    |     \        /    |    \ \r
 \___  >____/\____/|____/\____ |  |____|      \__/\  /\____|__  /\r
     \/                       \/                   \/         \/\r
 """


    head1 = """
        __                ______ _       ___   __\r
  _____/ /___  __  ______/ / __ \ |     / / | / /\r
 / ___/ / __ \/ / / / __  / /_/ / | /| / /  |/ / \r
/ /__/ / /_/ / /_/ / /_/ / ____/| |/ |/ / /|  /  \r
\___/_/\____/\__,_/\__,_/_/     |__/|__/_/ |_/   \r
"""

    head2 = """
      _                 _______ _    _ _   _ \r
     | |               | | ___ \ |  | | \ | |\r
  ___| | ___  _   _  __| | |_/ / |  | |  \| |\r
 / __| |/ _ \| | | |/ _` |  __/| |/\| | . ` |\r
| (__| | (_) | |_| | (_| | |   \  /\  / |\  |\r
 \___|_|\___/ \__,_|\__,_\_|    \/  \/\_| \_/\r
 """

    head3 = """
            __                            __  _______   __       __  __    __ \r
          /  |                          /  |/       \ /  |  _  /  |/  \  /  |\r
  _______ $$ |  ______   __    __   ____$$ |$$$$$$$  |$$ | / \ $$ |$$  \ $$ |\r
 /       |$$ | /      \ /  |  /  | /    $$ |$$ |__$$ |$$ |/$  \$$ |$$$  \$$ |\r
/$$$$$$$/ $$ |/$$$$$$  |$$ |  $$ |/$$$$$$$ |$$    $$/ $$ /$$$  $$ |$$$$  $$ |\r
$$ |      $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$$$$$$/  $$ $$/$$ $$ |$$ $$ $$ |\r
$$ \_____ $$ |$$ \__$$ |$$ \__$$ |$$ \__$$ |$$ |      $$$$/  $$$$ |$$ |$$$$ |\r
$$       |$$ |$$    $$/ $$    $$/ $$    $$ |$$ |      $$$/    $$$ |$$ | $$$ |\r
 $$$$$$$/ $$/  $$$$$$/   $$$$$$/   $$$$$$$/ $$/       $$/      $$/ $$/   $$/ \r
                                                                            """

    head4 = """
                                    ######  #     # #     # \r
  ####  #       ####  #    # #####  #     # #  #  # ##    # \r
 #    # #      #    # #    # #    # #     # #  #  # # #   # \r
 #      #      #    # #    # #    # ######  #  #  # #  #  # \r
 #      #      #    # #    # #    # #       #  #  # #   # # \r
 #    # #      #    # #    # #    # #       #  #  # #    ## \r
  ####  ######  ####   ####  #####  #        ## ##  #     #\r
  """
    headlist = [head0, head1, head2, head3, head4]
    print headlist[random.randint(0, 4)]
    print '\nWelcome to cloudPWN the cloud attack automation toolkit'
    print 'Coded by: David Bressler (@bostonlink)'
    print 'Version: 0.1 (Development)\n'