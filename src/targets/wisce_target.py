'''
Created on Sep 19, 2017

@author: sgorle
@summary: ALl WISCE Target APIs are encapsulated in this class.
'''
from ctf.src.device_factory import DeviceFactory
from ctf.src.logfw import logger as log


class WisceTarget(object):
    
    """ ALl WISCE Target APIs are encapsulated in this class."""

    def __init__(self):
        """
        Default constructor
        
        @return: None
        """
        log.info("__init__ method")
        raise NotImplementedError

    
DeviceFactory.type(WisceTarget())