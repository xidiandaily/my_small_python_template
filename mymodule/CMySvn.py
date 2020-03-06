# -*- coding:UTF-8 -*-
"""CMySvn

CMySvn is a svn helper, easy handler svn repo through python

example:
    import CMySvn

    mysvn=CMySvn.getMySvn('testsvn')
    mysvn.set_init('./code_repo_path/')
    filelist=mysvn.get_filelists()
    print(filelist)
    logitem=mysvn.get_logitem(10)
    print(logitem)
"""
import re
import pdb
import os
import subprocess
import logging
import time
import datetime
import pytz
from pytz import timezone
import xml.etree.ElementTree as ET

logger = logging.getLogger('sync_protocol')

__all__=[
        "CMySvn",
        "getMySvn",
        ]

class CMySvn:
    _mysvninstancelist = {}
    _cmd_need_args = ['--non-interactive','--trust-server-cert','--no-auth-cache']
    def __init__(self):
        self._id=""
        self._svnurl=''
        self._rootpath=''

    def run_cmds(self,cmds,cwd=None,xmloutput=True):
        for arg in self._cmd_need_args:
            if arg not in cmds:
                cmds.append(arg)

        if not cwd:
            cwd=self._rootpath

        if self._username:
            cmds.extend(['--username',self._username])
        if self._passwd:
            cmds.extend(['--password',self._passwd])

        if xmloutput:
            cmds.append('--xml')

        output=''
        try:
            output=subprocess.check_output(cmds,cwd=cwd,stderr=subprocess.STDOUT)
            logger.debug("run cmds success! cmds:{} cwd:{}".format(cmds,cwd))
        except subprocess.CalledProcessError as e:
            logger.error("run cmds failed!  cmds:{} cwd:{}. errMsg:{}".format(cmds,cwd,e.output))
            raise
        if  not xmloutput:
            return output
        root = ET.fromstring(output)
        return root

    def checkout(self,depth='infinity'):
        self.run_cmds(['svn','checkout',self._svnurl,'--depth',depth,self._rootpath],cwd='.',xmloutput=False)

    def update(self,subdirs=[],depth='infinity'):
        if not len(subdirs):
            self.run_cmds(['svn','up','--depth',depth],cwd=self._rootpath,xmloutput=False)
        else:
            for subdir in subdirs:
                self.run_cmds(['svn','up',subdir,'--depth',depth],cwd=self._rootpath,xmloutput=False)

    def get_repo_info(self):
        root = self.run_cmds(['svn','info'])

        info={}
        info['url']=root.find('entry').find('url').text
        return info

    def set_init(self,_rootpath,_svnurl=None,_username=None,_passwd=None):
        if not _svnurl and not os.path.exists(_rootpath):
            logger.error('repo rootpath:\'{}\' not exists!!'.format(_rootpath))
            raise Exception('inviable path')

        self._svnurl=_svnurl
        self._rootpath=_rootpath
        self._username=_username
        self._passwd=_passwd

        if not _svnurl:
            info = self.get_repo_info()
            self._svnurl=info['url']
        logger.debug('init set repo url:{} rootpath:{}'.format(_svnurl,_rootpath))

    def get_filelists(self,found_statuslists=None,subdir=None):
        '''get cur work copy directory file status
              get_filelists()  #get all files:
              get_filelists(['modified']) #get all modify files:
              get_filelists(['modified','unversioned ']) #get  unversioned files and modify files:
        '''
        if not subdir:
            root = self.run_cmds(['svn','status'])
        else:
            root = self.run_cmds(['svn','status',subdir])

        result={}
        for entry_tag in root.find('target').findall('entry'):
            curstatus = entry_tag.find('wc-status').get('item')
            if not found_statuslists or curstatus in found_statuslists:
                if curstatus in result.keys():
                    result[curstatus].append(entry_tag.get('path'))
                else:
                    result[curstatus]= [entry_tag.get('path')]
        return result

    def get_logitem(self,limit=1,subdir=None):
        '''get cur work copy directory file status
        '''
        if not subdir:
            root = self.run_cmds(['svn','log','-v','-l','{}'.format(limit)])
        else:
            root = self.run_cmds(['svn','log',subdir,'-v','-l','{}'.format(limit)])
        items=[]
        for logentry in root.findall('logentry'):
            logitem = {}
            logitem['revision'] = int(logentry.get('revision'))
            logitem['author']   = logentry.find('author').text
            logitem['date']     = logentry.find('date').text
            logitem['msg']      = logentry.find('msg').text
            if not logitem['msg']:
                logitem['msg']   = ''

            logitem['filelist']  = {}

            strDate=re.sub("\..*","",logitem['date'])
            logitem['timestamp'] = int(time.mktime(datetime.datetime.strptime(strDate,"%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone('UTC')).astimezone(tz=pytz.timezone('Asia/Shanghai')).timetuple()))
            logitem['utc8date']  = datetime.datetime.strptime(strDate,"%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone('UTC')).astimezone(tz=pytz.timezone('Asia/Shanghai')).isoformat()

            for pathentry in logentry.find('paths').findall('path'):
                if pathentry.get('kind') != 'file':
                    continue

                action=pathentry.get('action')
                if action in logitem['filelist'].keys():
                    logitem['filelist'][action].append(pathentry.text)
                else:
                    logitem['filelist'][action]=[pathentry.text]
            items.append(logitem)
        return items

def getMySvn(_id):
    '''
    get mysvn by id
    '''
    if _id in CMySvn._mysvninstancelist.keys():
        return CMySvn._mysvninstancelist[_id]

    CMySvn._mysvninstancelist[_id]=CMySvn()
    return CMySvn._mysvninstancelist[_id]

