'''
Created on Sep 19, 2017

@author: sgorle
'''
from ctf.src.device_factory import DeviceFactory
from ctf.src.logfw import logger as log

class RemoteTarget(object):
    
    """ ALl Remote Target APIs are encapsulated in this class."""

    def __init__(self):
        """
        Default constructor
        """
        log.info("__init__ method")
        raise NotImplementedError

    
DeviceFactory.type(RemoteTarget())