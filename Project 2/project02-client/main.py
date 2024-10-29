#
# Client-side python app for photoapp, this time working with
# web service, which in turn uses AWS S3 and RDS to implement
# a simple photo application for photo storage and viewing.
#
# Authors:
#
#   <<<YOUR NAME>>>
#
#   Starter code: Prof. Joe Hummel
#   Northwestern University
#

import requests  # calling web service
import jsons  # relational-object mapping

import uuid
import pathlib
import logging
import sys
import os
import base64
import time

from configparser import ConfigParser

from config import *
from models import *
from helpers import prompt
from services import *


#########################################################################
# main
#
print("** Welcome to PhotoApp v2 **")
print()

# eliminate traceback so we just get error message:
sys.tracebacklimit = 0

#
# what config file should we use for this session?
#
# config_file = "photoapp-client-config.ini"
config_file = "ec2-client-config.ini"

print("What config file to use for this session?")
print("Press ENTER to use default (photoapp-client-config.ini),")
print("otherwise enter name of config file>")
s = input()

if s == "":  # use default
    pass  # already set
else:
    config_file = s

# baseurl, host = get_configs(config_file)
baseurl = get_configs(config_file)

#
# main processing loop:
#
cmd = prompt()

while cmd != 0:
    if cmd == 1:
        stats(baseurl)
    elif cmd == 2:
        users(baseurl)
    elif cmd == 3:
        assets(baseurl)
    elif cmd == 4:
        download(baseurl, display=True, host="localhost")
    elif cmd == 6:
        bucket_contents(baseurl)
    elif cmd == 7:
        add_user(baseurl)
    elif cmd == 8:
        upload(baseurl)
    else:
        print("** Unknown command, try again...")
    cmd = prompt()

#
# done
#
print()
print("** done **")
