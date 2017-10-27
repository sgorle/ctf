'''
Created on Apr 27, 2017

Encapsulation of Sound Clear Studio (SCS) APIs
 
@author: sgorle
@summary: ALl Sound Clear Studio APIs are encapsulated in this class.
'''
import os

from ctf.src.configure import Configure as Conf
from ctf.src.device_factory import DeviceFactory
from ctf.src.logfw import logger

from studiolink.StudioLink import StudioLink
from studiolink.enums.ConnectionStatus import ConnectionStatus
from studiolink.exceptions.StudioLinkException import StudioLinkException
 
 
class ScsTarget(object):
     
    """ ALl Sound Clear Studio APIs are encapsulated in this class."""
     
    SystemName = Conf.property("Target_SystemName", "Simulated System")
    SystemFile = Conf.property("SystemFile", "cdb42l42.xml")
    DeviceName = Conf.property("Device_Name", "cs42l42")
    SimulatedSystem = Conf.property("Simulated_System", False)
    linkPath = Conf.property("linkPath", r"C:\Program Files\Cirrus Logic\SoundClearStudio_1.2\link\bin")
    CoreIndex = Conf.property("Core_Index", 3)
    ScsPkgName = Conf.property("ScsPkgName", r"")
     
    def __init__(self):
        """
        Default constructor for ScsTarget
        
        @return: None
        """
        self.link = None
        self.system = None
        self.device = None
        self.core_firmware = None
        self.core = None
        
        self._start_studio_link()
                  
    def connect(self):
        """
        Starts Studio Link, loads given scs package and connect to given device on given system.
        
        @return: None
        """   
#         self._start_studio_link()
        if self.ScsPkgName != "":
            self.load_scs_pkg(self.ScsPkgName)
        if self.SimulatedSystem is True:
            self._create_and_connect_to_simulated_system_and_device(self.SystemName, self.SystemFile, self.DeviceName)
        else:
            self._connect_to_system_and_device(self.SystemName, self.DeviceName)
            
    def get_system(self, system_name):
        """
        Gets the current System
        @param system_name: 
                [string] System name to get
        @return: [CLSystem] the connected CLSystem
        """
        system = None  # @UnusedVariable
        system = self.link.getCLSystem(system_name)
        if system.getName() == "Unknown":
            system = None
        return system
            
    def get_device(self, system_name, device_name):
        """
        Gets the current device
        @param system_name: 
                [string] System name to get
        @param device_name: 
                [string] Device name to get.
        @return: [Device] the connected device.
        """
        device = None
        system = self.link.getCLSystem(system_name)
        if system is not None:
            device = system.getDevice(device_name)
        return device   
        
    def _start_studio_link(self):
        """
        Starts the Studio Link server.
        
        @return: None
        @throws [\ref exceptions.StudioLinkException.StudioLinkException "StudioLinkException"]  
                if unable to communicate with %StudioLink
        """
        if os.path.exists(self.linkPath) is False:
            raise Exception("{} path not exists.".format(self.linkPath) + \
                            str(logger.error("{} path not exists.".format(self.linkPath))))
        try:           
            self.link = StudioLink(self.linkPath)
            self.link.start()    
            logger.info("Studio Link started")
            version = self.link.getStudioLinkVersion()
            logger.info("Studio Link version number is: {0}".format(version))  
        except StudioLinkException, e:
            raise Exception("Studio link not started. " + 
                            str(logger.error(str(e) + " - Error Code: " + str(e.getErrorCode()))))
           
    def _connect_to_system_and_device(self, systemName, deviceName):
        """
        Connects the given System and Device.
        
        @param systemName: 
                    [string] Name of the system to be connected.
        @param deviceName: 
                    [string] Name of the device to be connected.
        @return: None
        """
        self.system = self.link.getCLSystem(systemName)
        if self.system is None:              
            raise Exception("Could not get system {}".format(systemName) + 
                             str(logger.error("Could not get system {}".format(systemName))))
        logger.info("Connected to {0}".format(systemName))
        self.device = self.system.getDevice(deviceName)
        if self.device is None:
            raise Exception("Could not get device {0} from system {1}".format(deviceName, systemName) + 
                            str(logger.error("Could not get device {0} from system {1}".format(deviceName, systemName))))         
        logger.info("Connected to {0}".format(deviceName))
        
    def _create_and_connect_to_simulated_system_and_device(self, system_name, system_file, device_name):
        """
        Creates a simulated system and connects to given device on simulated system
        
        @param simSysName: 
                    [string] Simulated System Name
        @param deviceName: 
                    [string] Name of the device to be connected.
        @return: None
        """
        self._add_system_manually(system_name, system_file)
        self._connect_to_system_and_device(system_name, device_name)
        
    def _add_system_manually(self, system_name, system_file):
        """ Add System manually. Or Create a simulated System.
        
        @param system_name: System name to be created
        @param system_file: System file (.xml file)
        @return: None
        """
        try:           
            self.link.addCLSystemManually(system_name, system_file)
            logger.info("System " + system_name + " added")
        except StudioLinkException as sle:
            if "A system already exists with the given name" not in str(sle):
                raise Exception("Connection problem with StudioLink" + 
                                str(logger.error(str(sle) + " - Error Code: " + str(sle.getErrorCode()))))
            else:                
                raise Exception("System already exists with the given name " + 
                                str(logger.error("System already exists with the given name")))
            
    def disconnect_system(self):
        """
        Disconnected CL System from Studio Link
        
        @return: None
        """
        self.link.disconnectCLSystem(self.SystemName)
        
    def remove_system(self, system_name):
        """
        Removes the CL System from Studio Link
        
        @param system_name: 
                [string] System to remove.
        @return: None
        """
        self.link.removeCLSystemManually(system_name)
               
    def end(self):
        """
        Stops link connection and quit.
        
        @return: None
        """
        if (self.system is not None and self.system.getConnectionStatus() == ConnectionStatus.CONNECTED):
            self.link.disconnectCLSystem(self.SystemName)
            self.link.stop()
            quit()
         
    def load_scs_pkg(self, pkgName):
        """
        Loads the given scs package.
        
        @param pkgName: 
                [string] scs package name to be loaded.
        @return: None
        """
        raise NotImplementedError
    
     
    def load_firmware(self, firmwareFilePath, coreIndex, blocking=False):
        """
        Load the given firmware on a given core index.
        
        @param firmwareFilePath: 
                    [string] path to firmware file to laod.
        @param coreIndex: 
                    [Number] An integer number which is the index of the core on which firmware has to be loaded.
        @param blocking: 
                    [boolean] This is optional. whether to download without blocking
        @return: None
        """
        logger.info("Loading firmware ...")
        cores = self.device.getCores()
        logger.info("No of Cores: {}".format(len(cores)))
        if cores == []:
            raise Exception("Device {0} has No cores".format(self.device.getName()) + 
                            str(logger.error("Device {0} has No cores".format(self.device.getName()))))
        try:
            self.core = cores[coreIndex]
            self.core.loadFirmware(firmwareFilePath, blocking)
            self.is_firmware_loaded()
        except Exception, e:            
            raise Exception(str(e) + str(logger.error(str(e))))
               
    def is_firmware_loaded(self):
        """
        Get the Loaded Firmware.
        
        @return: [coreFirmware] loaded firmware.
        """
        self.core_firmware = self.device.getLoadedFirmware()
        if self.core_firmware is None:
            raise Exception("Device {0} has no firmware loaded".format(self.device) + 
                            str(logger.error("Device {0} has no firmware loaded".format(self.device))))
        logger.info("Firmware {0} has been successfully loaded on to the Device {1} Core {2}"
                    .format(self.core_firmware.getName(), self.device, self.core_firmware.getCore().getName()))
        return self.core_firmware
     
    def is_firmware_valid(self):
        """
        Get whether the firmware image is valid.
        
        @return: [bool] true if the firmware is valid.
        """
        return self.core_firmware.isValid()
     
    def get_algo_list_in_firmware(self):
        """
        Get the algorithms in the firmware.
        
        @return: [CoreAlgorithm] list of algorithms in the firmware.
        """
        return self.core_firmware.getAlgorithms()
     
    def get_memory_regions(self):
        """
        Get the types of memory regions in the firmware.
        
        @return: [MemoryRegionType] list of types of memory regions in the firmware.
        """
        return self.core_firmware.getMemoryRegions()
     
    def get_memory_region_size(self, typeOfMemoryRegion):
        """
        Get the size of the given memory region in the firmware.
        
        @param type: 
                [MemoryRegionType] type of memory region to get size of.
        @return: [int] size of the memory region in words.
        """
        return self.core_firmware.getMemoryRegionSize(typeOfMemoryRegion)
     
         
    def start_core(self):
        """
        Start the firmware running on the core.
        
        @return: None
        """
        self.core.startCore()
         
    def stop_core(self):
        """
        Stop the firmware running on the core.
        
        @return: None
        """
        self.core.stopCore()  
              
        
    def read_register(self, reg, page=None):
        """
        Read from given Register.
        
        @param reg: 
                [str|hex|long|int] Register can be Register Name or Register Address.
                (Address accepts the following types: hex, long, int)
        @param page: 
                [hex|long|int] Page of the Register.
        @return: Register value in Long or Integer
        """
        regValue = None
        
        if page is None:
            if isinstance(reg, str):
                regValue = self.device.readRegisterByName(reg)
            elif isinstance(reg, int) or isinstance(reg, long):
                regValue = self.device.readRegisterByAddress(reg)
            else:
                raise Exception("Argument reg type is incorrect. Only string, int, long will be accepted" + 
                                str(logger.error("Argument reg type is incorrect. Only string, int," + 
                                                 " long will be accepted")))
        else:
            if isinstance(page, int) or isinstance(page, long):
                if isinstance(reg, int) or isinstance(reg, long):
                    regValue = self.device.readRegisterByPageAndAddress(reg, page)
                else:
                    raise Exception("Argument reg type is incorrect. Only int, long will be accepted" + 
                                    str(logger.error("Argument reg type is incorrect. Only int, long will be accepted")))
            else:
                raise Exception("Argument page type is incorrect. Only int, long will be accepted" + 
                                str(logger.error("Argument page type is incorrect. Only int, long will be accepted")))
            
        return regValue
    
    def write_register(self, reg, value, page=None):
        """
        Write to given Register.
         
        @param reg: 
                [String|HEX|Long|Integer] Register can be Register Name or Register Address.
                (Address accepts the following types: HEX, Long, Integer)
        @param value: 
                [hex|long|int] Value to write in to the given register.
        @param page: 
                [hex|long|int] Page of the Register.
        @return: None
        """
        
        if page is None:
            if isinstance(reg, str):
                self.device.writeRegisterByName(reg, value)
            elif isinstance(reg, int) or isinstance(reg, long):
                self.device.writeRegisterByAddress(reg, value)
            else:
                raise Exception("Argument reg type is incorrect. Only string, int, long will be accepted" + 
                                str(logger.error("Argument reg type is incorrect. Only string, int, " + 
                                                 "long will be accepted")))
        else:
            if isinstance(page, int) or isinstance(page, long):
                if isinstance(reg, int) or isinstance(reg, long):
                    self.device.writeRegisterByPageAndAddress(reg, page, value)
                else:
                    raise Exception("Argument reg type is incorrect. Only int, long will be accepted" + 
                                    str(logger.error("Argument reg type is incorrect. Only int, long will be accepted")))
            else:
                raise Exception("Argument page type is incorrect. Only int, long will be accepted" + 
                                str(logger.error("Argument page type is incorrect. Only int, long will be accepted")))
            
    
    def read_block_data_from_regsister(self, reg, count, page=None):
        """
        Read block of data from given Register.
        
        @param reg: 
                [str|hex|long|int] Register can be Register Name or Register Address.
                (Address accepts the following types: hex, long, int)
        @param count: 
                [long|Integer] count of registers to read.
        @param page: 
                [hex|long|int] Page of the Register.
        @return: list of [long] register values, one for each register read.
        """
        regBlockData = None
        
        if page is None:
            if isinstance(reg, str):
                regBlockData = self.device.blockReadRegisterByName(reg, count)
            else:
                raise Exception("Argument reg type is incorrect. Only string will be accepted" + 
                                str(logger.error("Argument reg type is incorrect. Only string will be accepted")))
        else:
            if isinstance(page, int) or isinstance(page, long):
                if isinstance(reg, int) or isinstance(reg, long):
                    regBlockData = self.device.blockReadRegisterByAddress(reg, page, count)
                else:
                    raise Exception("Argument reg type is incorrect. Only int, long will be accepted" + 
                                    str(logger.error("Argument reg type is incorrect. Only int, long will be accepted")))
            else:
                raise Exception("Argument page type is incorrect. Only int, long will be accepted" + 
                                str(logger.error("Argument page type is incorrect. Only int, long will be accepted")))
            
        return regBlockData
    
    
    def write_block_data_to_regsister(self, reg, count, values, page=None):
        """
        Write given block of data to given Register.
         
        @param reg: 
                [string|hex|long|int] Register can be Register Name or Register Address.
                (Address accepts the following types: hex, long, int)
        @param count: 
                [long|int] count of registers to read.
        @param values: 
                [long] list of values to write.
        @param page: 
                [hex|long|int] Page of the Register.
        @return: None
        """
       
        if page is None:
            if isinstance(reg, str):
                self.device.blockWriteRegisterByName(reg, count, values)
            else:
                raise Exception("Argument reg type is incorrect. Only string will be accepted" + 
                                str(logger.error("Argument reg type is incorrect. Only string will be accepted")))
        else:
            if isinstance(page, int) or isinstance(page, long):
                if isinstance(reg, int) or isinstance(reg, long):
                    self.device.blockWriteRegisterByAddress(reg, page, count, values)
                else:
                    raise Exception("Argument reg type is incorrect. Only int, long will be accepted" + 
                                    str(logger.error("Argument reg type is incorrect. Only int, long will be accepted")))
            else:
                raise Exception("Argument page type is incorrect. Only int, long will be accepted" + 
                                str(logger.error("Argument page type is incorrect. Only int, long will be accepted")))
                    
    def reset_device(self):
        """
        Performs a software reset of the device.
        
        @return: None
        """
        self.device.resetDevice()
        
    def stop_link(self):
        """ 
        Stop studio link.
        
        @return: None
        """
        try:
            if self.link is not None:
                self.link.stop()
        except StudioLinkException, e:
            logger.error("Disconnection problem with Studio Link")
            raise Exception(str(e) + str(logger.error(str(e))))
        
    def device_id(self):
        """
        Returns the Hardware Device ID read from register 0h
        
        @return: [HEX value|nil] Returns the Hardware Device ID
        """
        if self.device is not None:
            sw_rst_dev_id = self.read_register('SW_RST_DEV_ID')
            return hex(sw_rst_dev_id)
        else:
            return None
        
    def hw_revision(self):
        """
        Returns the Hardware Revision read from register 1h
        
        @return: [HEX value|nil] Returns the Hardware Revision
        """
        if self.device is not None:
            hw_rev = self.read_register('HW_REVISION')
            return hex(hw_rev)
        else:
            return None
        
    def read_dsp_sampling_freq_reg_value(self, index):
        """
        It is used to get the sampling frequency value from the corresponding register.
        
        @param index: 
                [Integer] index It is used to select specific DSP.
        @return: [HEX value] The value which comes from the DSP register.
        """
        value = self.read_register('DSP[{0}]_RATE'.format(index))
        
        choices = {0 : self.read_register('SAMPLE_RATE_1'),
                   1 : self.read_register('SAMPLE_RATE_2'),
                   2: self.read_register('SAMPLE_RATE_3')}
        result = choices.get(int(value), None)
        return hex(result)
    
    def read_dsp_sample_rate_value(self, index):
        """
        This method is used for reading Sample Rate Value for a DSP.
        It is obtained by converting Sample Rate Register value to sampling rate
        
        @param index: 
                [Integer] index It is used to select specific DSP.
        @return: [Integer] Sampling rate
        """
        actual_freq = None
        actual_value = self.read_dsp_sampling_freq_reg_value(index)
        freq_value = Conf.property('DSPSamplingFrequencies' , {})
        sample_freq_value = Conf.property('DSPSamplingFreqRegvalues' , {})
        for number in xrange(1, len(freq_value)):
            sample_value = sample_freq_value[ "value{0}".format(number) ]
            if (sample_value == actual_value):
                actual_freq = freq_value[ "actualFreq{0}".format(number) ]
        return actual_freq
    
    def check_core_within_range(self, dsp_core_index):
        """
        Check that a given DSP core index lies within the range of cores available on the connected device.
        Cores are indexed from zero, i.e. 'DSP1' has index 0.
        
        @param dsp_core_index: 
                [Integer] dsp_core_index DSP Core integer index (e.g. 1 for 'DSP2').
        @return: None
        @raise exception: [Exception] If requested core is out of range of the cores available on the device.
        """
        n_cores = len(self.device.getCores())
        core_range = range(0, n_cores)

        # raise an exception if the core index is out of range.
        if dsp_core_index not in core_range:
            raise Exception("Requested DSP core index {0} out of range (there are {1} cores available). "
                            .format(dsp_core_index, n_cores) + 
                            str(logger.error("Requested DSP core index {0} out of range (there are {1} cores available)."
                            .format(dsp_core_index, n_cores)))
                            )
            
    def refresh_dvice(self):
        """
        Refresh the device.
        
        @return: None
        """
        self.device.refreshDevice()
        # TBD - For the completion status of the refresh, listen for a notification on the "AsyncRequest" topic.
        
    def get_default_value_of_register(self, reg, page=None):
        """
        Get the Register default value as specified in the device description file.
        
        @param reg: 
                [String|Integer|Long] Register can be either Register name or Address 
                (address can be in hex format or Long or Integer)
        @param page: 
                [None|Integer|Long] Page can be None or Integert or Hex or Long format.
                When page is not None, then reg param cannot be string.
        @raise exception: 
                Exception Incorrect argument type.
        @return: [Long] Register default value. 
        """
        regInfo = None
        
        if page is None:
            if isinstance(reg, str):
                regInfo = self.device.getRegisterInfoByName(reg)
            elif isinstance(reg, int) or isinstance(reg, long):
                regInfo = self.device.getRegisterInfoByAddress(reg)
            else:
                raise Exception("Argument reg type is incorrect. Only string, int, long will be accepted" + 
                                str(logger.error("Argument reg type is incorrect. Only string, int, " + 
                                                 "long will be accepted")))
        else:
            if isinstance(page, int) or isinstance(page, long):
                if isinstance(reg, int) or isinstance(reg, long):
                    regInfo = self.device.getRegisterInfoByAddressAndPage(reg, page)
                else:
                    raise Exception("Argument reg type is incorrect. Only int, long will be accepted" + 
                                    str(logger.error("Argument reg type is incorrect. Only int, long will be accepted")))
            else:
                raise Exception("Argument page type is incorrect. Only int, long will be accepted" + 
                                str(logger.error("Argument page type is incorrect. Only int, long will be accepted")))
            
        return regInfo.getDefaultValue()
    
    def list_devices(self):
        """
        Debug method for displaying the connected devices and protocols to the console.
        
        @return: None
        """
        
        devices = self.system.getDeviceList()
        for dev in devices:
            printed_name = dev.getName()
            if printed_name == "" or printed_name is None:
                printed_name = 'Unknown Device'
            logger.debug("'{0}' using control interface {1}".format(printed_name, dev.getCurrentControlInterface()))
        
    def find_device_by_name_with_comm_interface(self, device_name, comm_interface):
        """
        Finds a given device using the requested communication Interface if one exists on
        the current system.
        
        @param device_name: 
                [str]  device_name Name of the device to find (e.g. WM5110).
        @param comm_interface: 
                [str] Communication interface
        @return: [Device] device
        """
        device = None
        devices = self.system.getDeviceList()
        for dev in devices:
            if dev.getName() == device_name and dev.getCurrentControlInterface == comm_interface:
                device = dev
        return device
    
    def get_required_device(self, device_name):
        """
        get the required device and checks for existence of the device.
        
        @param device_name: 
                [str] Name of the device
        @return: [Device] device
        """
        return self.system.getDevice(device_name)
    
    def lochnagar_soft_reset(self, lochnager_name):
        """
        This Function will Soft Reset the lochnagar.
        
        @param lochnager_name: 
                [str] Lochnagar to be reset. Eg: 'WM0050' for Lochnagar1 and 'LN2 FPGA' for Lochnagar2.
        @return: None
        """
        import time 
        
        device = self.get_required_device(lochnager_name)
        device.writeField('SW_RST_DEV_ID', 0)
        # Time required to reset the Lochnagar
        time.sleep(10)
 
        
DeviceFactory.type(ScsTarget())
