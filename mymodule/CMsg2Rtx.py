# -*- coding:UTF-8 -*-
"""CMsg2Rtx

CMsg2Rtx is a msg sender,sender msg to rtx

example:
    import CMsg2Rtx

    msgsender=CMsg2Rtx.getMsgSender('__TMP_TOOL_NAME')
    msgsender.setUrl(config.get('msg2rtx','weburl',''))
    msgsender.sendText('test')

config.ini:
    [msg2rtx]
    weburl=
    #weburl=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d4e8f3e5-7dc9-4513-9135-da5d1f36300c
"""

import requests
import logging

logger = logging.getLogger('__TMP_TOOL_NAME')

__all__=[
        "CMsg2Rtx",
        "getMsgSender",
        ]

class CMsg2Rtx:
    _msgsenderinstancelist={}
    def __init__(self):
        self._id=""
        self._url=""

    @staticmethod
    def getMsgSender(_id):
        if _id in _msgsenderinstancelist.keys():
            return _msgsenderinstancelist[_id]

        _msgsenderinstancelist[_id]=CMsg2Rtx()
        return _msgsenderinstancelist[_id]

    def setUrl(self,_url):
        self._url = _url

    def sendText(self,_msg="test",listRtx=[]):
        if len(self._url) == 0:
            logger.error(u"SendMsg Falied!!! Rtx Robot web url is empty!! {} {}".format(listRtx,_msg))
            return

        if len(listRtx) > 0:
            logger.debug(u"Rtx:{} Msg:{}".format(listRtx,_msg))
            requests.post(self._url, json = {'msgtype':'text','text':{"content":_msg,"mentioned_list":listRtx}})
        else:
            logger.debug(u"Msg:{}".format(_msg))
            requests.post(self._url, json = {'msgtype':'text','text':{"content":_msg}})

def getMsgSender(_id):
    '''
    get msg sender by id
    '''
    if _id in CMsg2Rtx._msgsenderinstancelist.keys():
        return CMsg2Rtx._msgsenderinstancelist[_id]

    CMsg2Rtx._msgsenderinstancelist[_id]=CMsg2Rtx()
    return CMsg2Rtx._msgsenderinstancelist[_id]

