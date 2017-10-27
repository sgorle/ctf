'''
Created on May 26, 2017

@author: sgorle
@summary: This class loads the given yaml config file and can read and update the keys or values.
'''
import yaml

class Configure(object):
    
    """
    This class loads the given yaml config file and can read and update the keys or values.
    """
    
    file_name = r'ctf\configs\default_config.yaml'
    open_config = None
    dict = {}
        
    @classmethod
    def init(cls):
        """
        This loads the given config file.
        
        @return: None
        """
        with open(cls.file_name, "r") as f:
            cls.dict = yaml.load(f)
             
    @classmethod
    def set_source(cls, filename):
        """
        This sets the config file.
        
        @param filename: 
                [string] config file name with path.
        @return: None
        """
        cls.file_name = filename
        cls.open_config = None
         
    @classmethod     
    def property(cls, key, default_value):
        """
        This retrieves the value of a given key. if value is none assigns default value.
        
        @param key: 
                [string] key to be fetched.
        @param default_value:
                [string] default value if the value of given key not present.
        @return: [string] value of the key.
        """
        if cls.open_config is None:
            cls.init()
            cls.open_config = ""
        key = str(key)
        value = cls.dict.get(key)
        if value is None:
            cls.dict[key] = default_value
            value = default_value
        return value
    
    @classmethod     
    def update_key(cls, key, value):
        """
        Update the value of a key, if key not presents adds the key.
        
        @param key: 
                [string] key to be updated
        @param value: 
                [string] value to be updated for the given key.
        @return: None
        """
        if cls.open_config is None:
            cls.init()
            cls.open_config = ""
        key = str(key)
        cls.dict[key] = value
        
        with open(cls.file_name, "w") as f:
            yaml.dump(cls.dict, f)

