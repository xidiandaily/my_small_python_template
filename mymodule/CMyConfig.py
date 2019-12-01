# -*- coding: UTF-8 -*-
"""CMyConfig

CMyConfig is a ConfigParser warp

example:
    import CMyConfig

    config = CMyConfig.getMyConfig('__TMP_TOOL_NAME') #type:ConfigParser.ConfigParser
    config.read("config.ini")
    svn_username=config.get("svn","username")
    svn_passwd=config.get("svn","passwd")
    logger.debug("username:{}".format(svn_username))
    logger.debug("passwd:{}".format(svn_passwd))

config.ini:
    [svn]
    username=username
    passwd=passwd
"""
import ConfigParser

__all__ = [
        "CMyConfig",
        "getMyConfig"
        ]

class CMyConfig:
    _all_config_list={}

    def __init__(self):
        self._config = ConfigParser.ConfigParser()

def getMyConfig(_id):
    """
    Get a Config by input _id
    """
    if _id in CMyConfig._all_config_list:
        return CMyConfig._all_config_list[_id]._config

    config = CMyConfig()
    config._config = ConfigParser.ConfigParser()
    CMyConfig._all_config_list[_id] = config
    return CMyConfig._all_config_list[_id]._config

