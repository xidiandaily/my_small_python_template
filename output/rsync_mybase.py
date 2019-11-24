#!/usr/local/bin/python
# -*- coding:UTF-8 -*-
import os
import tarfile
import sys
import logging
import re
import datetime
import ConfigParser
import subprocess
import argparse

# create logger with '__TMP_TOOL_NAME'
logger = logging.getLogger('rsync_mybase')
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

parser=argparse.ArgumentParser(description="rsync mybase files between mac and pc",version="version 1.0,release by lawrencechi(at)tencent.com")
parser.add_argument('-m',dest='from_mac_to_pc',action='store_true',help='rsync files from mac to pc')
parser.add_argument('-p',dest='from_pc_to_mac',action='store_true',help='rsync files from pc to mac')
parser.add_argument('-l',dest="enable_debug_log",action='store_true',help='enable debug log')
args=parser.parse_args()
logger.debug(args)

if args.enable_debug_log:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    logfile.setLevel(logging.DEBUG)
    logger.debug("if enable_debug_log, you will see this log")

if not args.from_mac_to_pc and not args.from_pc_to_mac:
    logger.error("please run the tool with argument -m or -p")
    parser.print_help()
    sys.exit()

# read config
config=ConfigParser.ConfigParser()
config.read("config.ini")
rsync_cmd=config.get("remote","rsync_cmd")
logger.debug("rsync_cmd:{}".format(rsync_cmd))

if len(rsync_cmd) <= 0:
    logger.error("rsync_cmd is empty,please set")
    sys.exit()

compress_pwd=config.get("compress","passwd")
logger.debug("passwd:{}".format(compress_pwd))

if len(compress_pwd) <= 0:
    logger.error("compress passwd is too short ,please set")
    sys.exit()

filenum = int(config.get("compress","filenum"))

files=[]
for idx in range(0,filenum):
    filename=config.get("compress","filename{}".format(idx+1))
    if not os.path.exists(filename):
        logger.error("file:{} not found!",filename)
    else:
        files.append(filename)

if len(files) == 0:
    logger.error("rsync files empty")
    sys.exit()

# tar new file
compress_filename="from_mac_to_pc.tar.gz"
if args.from_pc_to_mac:
    compress_filename = "from_pc_to_mac.tar.gz"

tarfilename=compress_filename
tarfilename=os.path.abspath(tarfilename)
tar=tarfile.open(tarfilename,"w")
for r in files:
    tar.add(r,arcname=os.path.relpath(r,os.path.dirname(r)))
tar.close()

# compress with passw
subprocess.call(["zip","-e","-P",compress_pwd,re.sub(r".tar.gz",".zip",compress_filename),compress_filename])

# rsync upload
cmds=rsync_cmd.replace('"','').split(' ')
print(cmds)
subprocess.call(cmds)

