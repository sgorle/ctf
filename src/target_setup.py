'''
Created on May 2, 2017

@author: sgorle
@summary: Target Setup
'''

from importlib import import_module

from ctf.src.configure import Configure as conf
from ctf.src.logfw import logger


class TargetSetup:
    """This sets up the target."""
    
    def __init__(self):
        """
        Default constructor. Sets up the given target in the config file.
        
        @return: None
        """
        logger.info( "Target setup initialization" )        
        self.target = conf.property("target", "null")
        tp = self.target + "_target"
        import_module("ctf.src.targets.{0}".format(tp))
        logger.info( "Target setup is done." )
