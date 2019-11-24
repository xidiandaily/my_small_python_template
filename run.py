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
import fileinput

# create logger with 'run'
logger = logging.getLogger('run')
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
parser.add_argument('-n',dest="toolname",action='store',help='tool name')
args=parser.parse_args()
logger.debug(args)


if args.enable_debug_log:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    logfile.setLevel(logging.DEBUG)
    logger.debug("if enable_debug_log, you will see this log")

if not args.toolname:
    parser.print_help()
    sys.exit()

# global name
outputdir="output"
toolscriptname = os.path.join(outputdir,"{}.py".format(args.toolname))

if not os.path.exists("main.py"):
    logger.error("Failed!! not found template file main.py")
    sys.exit()

if os.path.exists(toolscriptname):
    choice=raw_input("tool ('{}') script is exit,re generate? [Yy/Nn](default:N)")
    if choice != 'Y' or choice != 'y':
        sys.exit()

if not os.path.exists(outputdir):
    os.mkdir(outputdir)

with open(toolscriptname,'w') as fileObj:
    for line in fileinput.FileInput('main.py'):
        while True:
            if re.search("^#",line):
                break
            if re.search("__TMP_TOOL_NAME",line):
                line = re.sub(r"__TMP_TOOL_NAME",args.toolname,line)
            break
        fileObj.write(line)
    fileObj.close()
    print("{} is generate success ".format(toolscriptname))

