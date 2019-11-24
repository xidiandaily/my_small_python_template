#!/usr/local/bin/python
# -*- coding:UTF-8 -*-
import subprocess
import os
import sys
import logging
import argparse
import re
import datetime
import ConfigParser

# create logger with '__TMP_TOOL_NAME'
logger = logging.getLogger('__TMP_TOOL_NAME')
logger.setLevel(logging.ERROR)
# create file handler which logs even debug messages
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)

#log file
logfile=logging.FileHandler(os.path.splitext(sys.argv[0])[0]+".log")
logfile.setLevel(logging.ERROR)
logfile.setFormatter(formatter)
logger.addHandler(logfile)

parser=argparse.ArgumentParser(description="tool description",version="version 1.0,release by lawrencechi(at)tencent.com")
parser.add_argument('-l',dest="enable_debug_log",action='store_true',help='enable debug log')
# parser.add_argument('-a','--a1',dest='test',action='store',help='store ')
# parser.add_argument('-b',const='if_argument_is_set_set_this_value',action='store_const',help='store_const')
# parser.add_argument('-c',action='store_true',help='store_true')
# parser.add_argument('-d',action='store_false',help='store_false')
# parser.add_argument('-e',action='append',help='append')
# parser.add_argument('-f',const="if_argument_is_set_set_this_value",action='append_const',help='append_const')
# parser.add_argument('-g',action='count',help='count')
args=parser.parse_args()
logger.debug(args)
parser.print_help()

if args.enable_debug_log:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    logfile.setLevel(logging.DEBUG)
    logger.debug("if enable_debug_log, you will see this log")

# # read config
# config=ConfigParser.ConfigParser()
# config.read("config.ini")
# svn_username=config.get("svn","username")
# svn_passwd=config.get("svn","passwd")
# logger.debug("username:{}".format(svn_username))
# logger.debug("passwd:{}".format(svn_passwd))

