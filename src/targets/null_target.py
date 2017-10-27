'''
Created on Apr 27, 2017
 
@author: sgorle
'''
from ctf.src.device_factory import DeviceFactory
from ctf.src.logfw import logger as log
 
class NullTarget(object):
     
    """ ALl Null Target APIs are encapsulated in this class."""
     
    def __init__(self):
        """
        Default constructor for ScsTarget
        """
        log.info("__init__ method")
        raise NotImplementedError                  
    
DeviceFactory.type(NullTarget())
