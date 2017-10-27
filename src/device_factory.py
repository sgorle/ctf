'''
Created on May 2, 2017

@author: sgorle
@summary: Singleton class to avoid the multiple instances of the device.
'''

class DeviceFactory(object):
    
    """
    Device factory class to get the device instance. This make sure to avoid the
    multiple instances of the device.
    """
    
    #############################################################################
    #
    # Used to store the runtime-type of the specialized FWK device to be
    # instantiated on this run. This should be set after the platform specific
    # FWK Device is defined.
    #
    #############################################################################
    device_type = None

    #############################################################################
    #
    # Module attribute to store the singleton FWK device once it has been
    # created.
    #
    #############################################################################
    default_device = None


    @classmethod
    def type ( cls, device_type ):
        """
        Set the type of FWK device to be instantiated by the first call to get_device().
        
        @param device_type: 
                [string] The type name of a specialization of the  FWK Interface.
        @return: None
        """
        cls.device_type = device_type

    @classmethod
    def get_device(cls):
        """
        Return a global FWK device according to the type set using type.
        The first time it is called it instantiates a FWK device and assigns
        it to the default_device attribute before returning the object.
        
        @return: A default, singleton, FWK device.
        """
        if cls.default_device is None :
            cls.default_device = cls.device_type
        return cls.default_device
