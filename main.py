#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
import logging
import re
import datetime
import ConfigParser
import subprocess
import argparse
import pdb
#__MYIMPORT

def run_cmds(cmds,cwd=os.getcwd(),ignored=False):
    try:
        output=subprocess.check_call(cmds,cwd=cwd)
        logger.debug("run cmds success! cmds:{} cwd:{} ignored={}".format(cmds,cwd,ignored))
    except subprocess.CalledProcessError as e:
        logger.error("run cmds failed!  cmds:{} cwd:{} ignored={}".format(cmds,cwd,ignored))
        if ignored:
            pass

logfilename=os.path.splitext(sys.argv[0])[0]+".log"

parser=argparse.ArgumentParser(description="tool description",version="version 1.0,release by lawrencechi(at)tencent.com")
parser.add_argument('-l',dest="enable_debug_log",action='store_true',help='enable debug log')
parser.add_argument('-f',dest="enable_log_file",action='store_true',help='if this argument has been set,output log to logfile:{}'.format(logfilename))
# parser.add_argument('-a','--a1',dest='test',action='store',help='store ')
# parser.add_argument('-b',const='if_argument_is_set_set_this_value',action='store_const',help='store_const')
# parser.add_argument('-c',action='store_true',help='store_true')
# parser.add_argument('-d',action='store_false',help='store_false')
# parser.add_argument('-e',action='append',help='append')
# parser.add_argument('-f',const="if_argument_is_set_set_this_value",action='append_const',help='append_const')
# parser.add_argument('-g',action='count',help='count')
args=parser.parse_args()
parser.print_help()

# create logger with '__TMP_TOOL_NAME'
logger = logging.getLogger('__TMP_TOOL_NAME')
logger.setLevel(logging.ERROR)
# create file handler which logs even debug messages
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)

#log file
if args.enable_log_file or args.enable_debug_log:
    formatter = logging.Formatter('%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    logfile=logging.FileHandler(logfilename)
    logfile.setLevel(logging.ERROR)
    logfile.setFormatter(formatter)
    logger.addHandler(logfile)

if args.enable_debug_log:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logfile.setLevel(logging.DEBUG)
    logger.debug("if enable_debug_log, you will see this log")

logger.debug("helloworld")
logger.debug(args)
logger.error("error")

#__MYEXAMPLE

