#!/usr/local/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
import logging
import re
import datetime
import ConfigParser
import subprocess
import argparse
import tarfile
import pdb
import shutil
import pickle

class DBInfo:

    def __init__(self):
        self._pc_time=0
        self._mac_time=0

def save_datebase(dbinfo):
    with open('data.db','wb') as fileObj:
        pickle.dump(dbinfo,fileObj)
        fileObj.close()

def load_database():
    if os.path.exists('data.db'):
        with open('data.db','rb') as fileObj:
            dbinfo=pickle.load(fileObj)
            fileObj.close()
            return dbinfo
    return DBInfo()

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

# import my module
sys.path.append("./mymodule")
import CMyConfig

# create logger with '__TMP_TOOL_NAME'
logger = logging.getLogger('rsyncmybase_pc2mac')
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
parser.add_argument('-q',dest="enable_scilence_log",action='store_true',help='if this argument has been set,stop output any log to stdout')
args=parser.parse_args()
logger.debug(args)

if args.enable_scilence_log:
    logger.removeHandler(ch)

if args.enable_debug_log:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    logfile.setLevel(logging.DEBUG)
    logger.debug("if enable_debug_log, you will see this log")

#global var
dbinfo=load_database()

# module:CMyConfig example:
config = CMyConfig.getMyConfig('rsyncmybase_pc2mac') #type:ConfigParser.ConfigParser
config.read("config.ini")

# check mybase is running or not
output=subprocess.check_output(["tasklist"])
for line in output.splitlines():
    if re.search(r"^myBase.exe\s",line):
        logger.error("myBase.exe is on running now,quit rsync")
        sys.exit()

# # get remote file
# filename = "from_mac_to_svr.tar.gz"
# os.remove(filename)
# host=config.get('remote','host')
# subprocess.call(["scp","{}:/home/ubuntu/temp/from_mac_to_svr.tar.gz".format(host),"./"])
# if not os.path.exists(filename):
#     logger.error("download file:{} from host:{} failed!".format(filename,host))

# # backup my file
# 
# 
# # backup
# if os.path

# tar new file
files=[
        "D:/myBaseData/StudyOnWin.myBase.nyf",
        "D:/myBaseData/workOnWin.myBase.nyf"
        ]

time_new = 0
for filename in files:
    stat = os.stat(filename)
    if time_new < stat.st_mtime:
        time_new = stat.st_mtime

if dbinfo._pc_time == time_new:
    logger.debug("mybase is not change")
    sys.exit()

dbinfo._pc_time=time_new

tarfilename="from_pc_to_mac.tar.gz"
delete_file(tarfilename)
tar=tarfile.open(tarfilename,"w")

time_new=0
for filename in files:
    stat = os.stat(filename)
    if time_new < stat.st_mtime:
        time_new = stat.st_mtime
    shutil.copy(filename,os.path.basename(filename))
    tar.add(os.path.basename(filename))
    delete_file(os.path.basename(filename))

tempfile=datetime.datetime.fromtimestamp(time_new).strftime("time_%Y_%m_%d_%H_%M_%S")
with open(tempfile,'w') as fileObj:
    fileObj.write(tempfile)
    fileObj.close()
    tar.add(tempfile)
    delete_file(tempfile)
tar.close()

if not os.path.exists(tarfilename):
    logger.error("tar files failed!")
else:
    logger.debug("{} generate success".format(tarfilename))

# zip compress with passwd
zipfilename="from_pc_to_mac.zip"
delete_file(zipfilename)
subprocess.call(["zip","-e","-P",config.get("remote","passwd"),zipfilename,tarfilename])
if not os.path.exists(zipfilename):
    logger.error("zip files failed!")
else:
    logger.debug("{} generate success".format(zipfilename))

# upload file
host=config.get('remote','host')
subprocess.call(["scp",zipfilename,"{}:/home/ubuntu/temp/{}".format(host,zipfilename)])

# save db
save_datebase(dbinfo)

