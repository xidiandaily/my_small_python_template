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
import shutil

class CMyModule:
    def __init__(self):
        self._modulename=''
        self._example=''
        self._files=[]
        self._inicontent=''

    def __str__(self):
        return "\nmodulename:{}\nexample:\n{}".format(self._modulename,self._example)

def get_module_by_name(_modulename):
    filename=os.path.join("mymodule","{}.py".format(name))
    if not os.path.exists(filename):
        return None

    # example
    _regex_import=re.compile(r"(\s*)import\s*{}".format(_modulename))
    strExample=""
    _prefix=''
    for line in fileinput.FileInput(filename):
        if len(_prefix) > 0 and len(line) > len(_prefix):
            if _prefix != line[0:len(_prefix)]:
                break
            strExample += line[len(_prefix):]

        result = _regex_import.search(line)
        if result:
            _prefix = result.group(1)

    #config
    _regex_ini=re.compile(r"^\s*config\.ini")
    strIniContent=''
    _prefix=''
    bFoundIni=0
    for line in fileinput.FileInput(filename):
        if len(line)==0:
            continue
        
        if bFoundIni == 1:
            if len(_prefix) == 0:
                _prefix=re.search(r"(\s*)\w*",line).group(1)
                logger.debug("prefix:{},len:{}".format(_prefix,len(_prefix)))

            if len(line) > len(_prefix):
                if _prefix != line[0:len(_prefix)]:
                    break
                strIniContent += line[len(_prefix):]
        if bFoundIni == 0 and _regex_ini.search(line):
            bFoundIni=1


    mymodule = CMyModule()
    mymodule._modulename = _modulename
    mymodule._example = strExample
    mymodule._files.append(filename)
    mymodule._inicontent=strIniContent
    logger.debug(strIniContent)
    return mymodule
    
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

mysupportmodules=[]
for root,paths,files in os.walk("mymodule"):
    for filename in files:
        if re.search(r"\.py$",filename):
            mysupportmodules.append(os.path.basename(filename).replace(".py",''))

if len(mysupportmodules):
    parser.add_argument('-m',dest="modules",action='store',help='add module what you warn,support modules:{}'.format(','.join(mysupportmodules)))

args=parser.parse_args()
logger.debug(args)

if args.enable_debug_log:
    logger.setLevel(logging.DEBUG)
    ch.setLevel(logging.DEBUG)
    logfile.setLevel(logging.DEBUG)
    logger.debug("if enable_debug_log, you will see this log")

logger.debug(mysupportmodules)

if not args.toolname:
    parser.print_help()
    sys.exit()

enablemodules=[]
if args.modules:
    names=args.modules.split(',')
    newnames=[]
    # if has config,generate it first
    if 'CMyConfig' in names:
        newnames.append('CMyConfig')

    for name in names:
        if 'CMyConfig' != name:
            newnames.append(name)
    for name in newnames:
        module = get_module_by_name(name)
        if isinstance(module,CMyModule):
            enablemodules.append(module)
            logger.debug("enable module:{}".format(module))

# global name
outputdir="output"
if not os.path.exists(outputdir):
    os.mkdir(outputdir)

if len(enablemodules) > 0:
    outputdir=os.path.join(outputdir,args.toolname)
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)

toolscriptname = os.path.join(outputdir,"{}.py".format(args.toolname))

if not os.path.exists("main.py"):
    logger.error("Failed!! not found template file main.py")
    sys.exit()

if os.path.exists(toolscriptname):
    choice=raw_input("tool ('{}') script is exit,re generate? [Yy/Nn](default:N)".format(toolscriptname))
    logger.debug("choice:{} len:{}".format(choice,len(choice)))
    if choice != 'Y' and choice != 'y':
        logger.debug("no do anythin,quit")
        sys.exit()

strModuleImport=''
strModuleExample=''
strIniContent=''
if len(enablemodules):
    strModuleImport='''
# import my module
sys.path.append("./mymodule")
'''
    for module in enablemodules:
        strModuleImport+="import {}\n".format(module._modulename)
        strModuleExample+="\n# module:{} example:\n{}".format(module._modulename,module._example)
        strIniContent+="\n# module:{} ini config:\n{}".format(module._modulename,module._inicontent)
        for filename in module._files:
            mymoduledir=os.path.join(outputdir,"mymodule")
            if not os.path.exists(mymoduledir):
                os.mkdir(mymoduledir)

            strModule=''
            with open(filename,'r') as fileObj:
                strModule=fileObj.read()
                fileObj.close()

            strModule=strModule.replace('__TMP_TOOL_NAME',args.toolname)
            with open(os.path.join(mymoduledir,os.path.basename(filename)),'w') as fileObj:
                fileObj.write(strModule)
                fileObj.close()
        print("copy module:{} success".format(module._modulename))

strContent=''
with open('main.py','r') as fileObj:
    strContent=fileObj.read()
    fileObj.close()

strContent=re.sub(r"#__MYIMPORT",strModuleImport,strContent,re.S)
strContent=re.sub(r"#__MYEXAMPLE",strModuleExample,strContent,re.S)
with open(toolscriptname,'w') as fileObj:
    for line in strContent.splitlines():
        while True:
            if re.search("^#",line):
                break
            if re.search("__TMP_TOOL_NAME",line):
                line = re.sub(r"__TMP_TOOL_NAME",args.toolname,line)
            break
        fileObj.write(line+"\n")
    fileObj.close()
    print("{} is generate success ".format(toolscriptname))

# write ini config
if len(strIniContent):
    strIniContent=strIniContent.replace("\r\n","\n")
    inifilename=os.path.join(outputdir,"config.ini")
    with open(inifilename,'w') as fileObj:
        fileObj.write(strIniContent)
        fileObj.close()
    print("{} is generate success".format(inifilename))

