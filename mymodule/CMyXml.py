# -*- coding:UTF-8 -*-
"""CMyXml

CMyXml is a xml helper, easy handler xml through python

example:
    import CMyXml

    myxml=CMyXml.getMyXml('__TMP_TOOL_NAME')
    myxml.set_init('xmlinputfile_utf8')
    partylists=myxml.get_elementlists_by_tag(myxml.getroot(),'Party',True)
    endpoint=myxml.get_elementlists_with_attrib(partylists[0],'schemeID',"0088",True)[0]
    logger.error(endpoint.get('schemeID'))
    logger.error(endpoint.text)
"""
import re
import pdb
import os
import subprocess
import logging
import xml.etree.ElementTree as ET
from collections import defaultdict

logger = logging.getLogger('__TMP_TOOL_NAME')

__all__=[
        "CMyXml",
        "getMyXml",
        ]

class CMyXml:
    _myxmlinstancelist = {}
    def __init__(self):
        self._xml=None
        self._xmlfilepath=None

    def set_init(self,_xmlpath=None,_xmlstring=None):
        '''
        example xmlpath: ./mymodule/base-example.xml
        set_init("./mymodule/base-example.xml")
        '''

        if not _xmlpath and not _xmlstring:
            logger.error('xmlpath({}) not found!'.format(_xmlpath))
            raise Exception('inviable path')
        if _xmlpath:
            try:
                self._xml = ET.parse(_xmlpath)
            except Exception as e:
                logger.error(e)
                raise e

            self._xmlfilepath=_xmlpath
            logger.debug(u"parse xmlfile success:{}".format(_xmlpath))
        elif _xmlstring:
            try:
                self._xml = ET.fromstring(_xmlstring)
            except Exception as e:
                logger.error(e)
                raise e
            logger.debug(u"parse xmlstring success")

    @staticmethod
    def etree_to_dict(_t):
        '''
        example: https://newbedev.com/converting-xml-to-dictionary-using-elementtree

        '''
        if isinstance(_t,ET.ElementTree):
            t=_t.getroot()
        elif isinstance(_t,ET.Element):
            t=_t
        else:
            raise Exception("unknown type:{}".format(type(_t)))

        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(CMyXml.etree_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {t.tag: {k: v[0] if len(v) == 1 else v
                         for k, v in dd.items()}}
        if t.attrib:
            d[t.tag].update(('@' + k, v)
                            for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d

    @staticmethod
    def get_elementlists_by_tag(el,_tag=None,is_recursive=False):
        '''
        sub return: []
        recursive return: [<Element 'CityName' at 0x105c38e50>, <Element 'CityName' at 0x105c40450>]
        '''
        if not _tag:
            return []
        if is_recursive:
            return el.findall(u".//{}".format(_tag))
        else:
            return el.findall(u"./{}".format(_tag))

    @staticmethod
    def get_elementlists_with_attrib(el,_attrib=None,_val=None,is_recursive=False):
        '''
        sub return: []
        recursive return: [<Element 'CityName' at 0x105c38e50>, <Element 'CityName' at 0x105c40450>]
        '''
        if not _attrib:
            return []
        if is_recursive:
            if not _val:
                return el.findall(u".//*[@{}]".format(_attrib))
            else:
                return el.findall(u".//*[@{}='{}']".format(_attrib,_val))
        else:
            if not _val:
                return el.findall(u"./*[@{}]".format(_attrib))
            else:
                return el.findall(u"./*[@{}='{}']".format(_attrib,_val))

    def getroot(self):
        '''
        root = ET.fromstring(countrydata)

        # Top-level elements
        root.findall(".")

        # All 'neighbor' grand-children of 'country' children of the top-level
        # elements
        root.findall("./country/neighbor")

        # Nodes with name='Singapore' that have a 'year' child
        root.findall(".//year/..[@name='Singapore']")

        # 'year' nodes that are children of nodes with name='Singapore'
        root.findall(".//*[@name='Singapore']/year")

        # All 'neighbor' nodes that are the second child of their parent
        root.findall(".//neighbor[2]")
        '''
        return self._xml

def getMyXml(_id):
    '''
    get myxml by id
    '''
    if _id in CMyXml._myxmlinstancelist.keys():
        return CMyXml._myxmlinstancelist[_id]

    CMyXml._myxmlinstancelist[_id]=CMyXml()
    return CMyXml._myxmlinstancelist[_id]

