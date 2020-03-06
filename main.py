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
import codecs
#__MYIMPORT

def run_cmds(cmds,cwd=os.getcwd(),ignored=False):
    try:
        output=subprocess.check_call(cmds,cwd=cwd)
        logger.debug("run cmds success! cmds:{} cwd:{} ignored={}".format(cmds,cwd,ignored))
    except subprocess.CalledProcessError as e:
        logger.error("run cmds failed!  cmds:{} cwd:{} ignored={}".format(cmds,cwd,ignored))
        if ignored:
            pass
        raise

def write_file(strName,strCon):
    with codecs.open(strName,'wc','utf-8') as fileObj:
        fileObj.write(strCon)
        fileObj.close()

def read_file(strFileName):
    strCon=''
    with open(strFileName,'r') as fileObj:
        strCon=fileObj.read()
        strCon=strCon.decode('utf-8')
        fileObj.close()
    return strCon

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
simpleformatter = logging.Formatter('%(message)s')
detailformatter = logging.Formatter('%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)
# create console handler with stdout output
stdout = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(stdout)

#log file
if args.enable_log_file or args.enable_debug_log:
    logfile=logging.FileHandler(logfilename)
    logfile.setFormatter(detailformatter)
    logger.addHandler(logfile)

if args.enable_debug_log:
    logger.setLevel(logging.DEBUG)
    stdout.setFormatter(detailformatter)
    logger.debug("if enable_debug_log, you will see this log")

logger.debug("helloworld")
logger.debug(args)
logger.error("error")

#__MYEXAMPLE

