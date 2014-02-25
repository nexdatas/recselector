#    "$Name:  $";
#    "$Header:  $";
#=============================================================================
#
# file :        NXSRecSettings.py
#
# description : Python source for the NXSRecSettings and its commands. 
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                NXSRecSettings are implemented in this file.
#
# project :     TANGO Device Server
#
# $Author:  $
#
# $Revision:  $
#
# $Log:  $
#
# copyleft :    European Synchrotron Radiation Facility
#               BP 220, Grenoble 38043
#               FRANCE
#
#=============================================================================
#          This file is generated by POGO
#    (Program Obviously used to Generate tango Object)
#
#         (c) - Software Engineering Group - ESRF
#=============================================================================
#


import PyTango
import sys


#==================================================================
#   NXSRecSettings Class Description:
#
#         Tango Server for Nexus Sardana Recorder Settings
#
#==================================================================
#     Device States Description:
#
#   DevState.ON :   Server is ON
#   DevState.RUNNING : Performing a query
#==================================================================


from Settings import Settings as STG

class NXSRecSettings(PyTango.Device_4Impl):

#--------- Add you global variables here --------------------------

#------------------------------------------------------------------
#    Device constructor
#------------------------------------------------------------------
    def __init__(self,cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        ## Recorder Settings
        self.stg = STG(self)
        NXSRecSettings.init_device(self)

#------------------------------------------------------------------
#    Device destructor
#------------------------------------------------------------------
    def delete_device(self):
        print >> self.log_info, "[Device delete_device method] for device",self.get_name()
        if hasattr(self, 'stg') and  self.stg :
            del self.stg
            self.stg = None
        self.set_state(PyTango.DevState.OFF)

#------------------------------------------------------------------
#    Device initialization
#------------------------------------------------------------------
    def init_device(self):
        print >> self.log_info, "In ", self.get_name(), "::init_device()"
        if hasattr(self, 'stg') and  self.stg :
            del self.stg
            self.stg = None
        self.stg = STG(self)
        self.set_state(PyTango.DevState.ON)
        self.get_device_properties(self.get_device_class())

#------------------------------------------------------------------
#    Always excuted hook method
#------------------------------------------------------------------
    def always_executed_hook(self):
        print >> self.log_info, "In ", self.get_name(), "::always_excuted_hook()"

#==================================================================
#
#    NXSRecSettings read/write attribute methods
#
#==================================================================
#------------------------------------------------------------------
#    Read Attribute Hardware
#------------------------------------------------------------------
    def read_attr_hardware(self,data):
        print >> self.log_info, "In ", self.get_name(), "::read_attr_hardware()"



#------------------------------------------------------------------
#    Read Components attribute
#------------------------------------------------------------------
    def read_Components(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_Components()"
        attr.set_value(self.stg.components)


#------------------------------------------------------------------
#    Write Components attribute
#------------------------------------------------------------------
    def write_Components(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_Components()"
        self.stg.components = get_write_value()
        print >> self.log_info, "Attribute value = ", self.stg.components 

        #    Add your own code here


#------------------------------------------------------------------
#    Read ConfigDevice attribute
#------------------------------------------------------------------
    def read_ConfigDevice(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ConfigDevice()"
        
        #    Add your own code here
        
        attr_ConfigDevice_read = "Hello Tango world"
        attr.set_value(attr_ConfigDevice_read)


#------------------------------------------------------------------
#    Write ConfigDevice attribute
#------------------------------------------------------------------
    def write_ConfigDevice(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ConfigDevice()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read WriterDevice attribute
#------------------------------------------------------------------
    def read_WriterDevice(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_WriterDevice()"
        
        #    Add your own code here
        
        attr_WriterDevice_read = "Hello Tango world"
        attr.set_value(attr_WriterDevice_read)


#------------------------------------------------------------------
#    Write WriterDevice attribute
#------------------------------------------------------------------
    def write_WriterDevice(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_WriterDevice()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read DataRecord attribute
#------------------------------------------------------------------
    def read_DataRecord(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DataRecord()"
        
        #    Add your own code here
        
        attr_DataRecord_read = "Hello Tango world"
        attr.set_value(attr_DataRecord_read)


#------------------------------------------------------------------
#    Write DataRecord attribute
#------------------------------------------------------------------
    def write_DataRecord(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DataRecord()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read DataSources attribute
#------------------------------------------------------------------
    def read_DataSources(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DataSources()"
        
        #    Add your own code here
        
        attr_DataSources_read = "Hello Tango world"
        attr.set_value(attr_DataSources_read)


#------------------------------------------------------------------
#    Write DataSources attribute
#------------------------------------------------------------------
    def write_DataSources(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DataSources()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read AppendEntry attribute
#------------------------------------------------------------------
    def read_AppendEntry(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_AppendEntry()"
        
        #    Add your own code here
        
        attr_AppendEntry_read = 1
        attr.set_value(attr_AppendEntry_read)


#------------------------------------------------------------------
#    Write AppendEntry attribute
#------------------------------------------------------------------
    def write_AppendEntry(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_AppendEntry()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read ComponentsFromMntGrp attribute
#------------------------------------------------------------------
    def read_ComponentsFromMntGrp(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ComponentsFromMntGrp()"
        
        #    Add your own code here
        
        attr_ComponentsFromMntGrp_read = 1
        attr.set_value(attr_ComponentsFromMntGrp_read)


#------------------------------------------------------------------
#    Write ComponentsFromMntGrp attribute
#------------------------------------------------------------------
    def write_ComponentsFromMntGrp(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ComponentsFromMntGrp()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read DynamicComponents attribute
#------------------------------------------------------------------
    def read_DynamicComponents(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DynamicComponents()"
        
        #    Add your own code here
        
        attr_DynamicComponents_read = 1
        attr.set_value(attr_DynamicComponents_read)


#------------------------------------------------------------------
#    Write DynamicComponents attribute
#------------------------------------------------------------------
    def write_DynamicComponents(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DynamicComponents()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read DynamicLinks attribute
#------------------------------------------------------------------
    def read_DynamicLinks(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DynamicLinks()"
        
        #    Add your own code here
        
        attr_DynamicLinks_read = 1
        attr.set_value(attr_DynamicLinks_read)


#------------------------------------------------------------------
#    Write DynamicLinks attribute
#------------------------------------------------------------------
    def write_DynamicLinks(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DynamicLinks()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read DynamicPath attribute
#------------------------------------------------------------------
    def read_DynamicPath(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DynamicPath()"
        
        #    Add your own code here
        
        attr_DynamicPath_read = "Hello Tango world"
        attr.set_value(attr_DynamicPath_read)


#------------------------------------------------------------------
#    Write DynamicPath attribute
#------------------------------------------------------------------
    def write_DynamicPath(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DynamicPath()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read ConfigVariables attribute
#------------------------------------------------------------------
    def read_ConfigVariables(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ConfigVariables()"
        
        #    Add your own code here
        
        attr_ConfigVariables_read = "Hello Tango world"
        attr.set_value(attr_ConfigVariables_read)


#------------------------------------------------------------------
#    Write ConfigVariables attribute
#------------------------------------------------------------------
    def write_ConfigVariables(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ConfigVariables()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read ScanFile attribute
#------------------------------------------------------------------
    def read_ScanFile(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ScanFile()"
        
        #    Add your own code here
        
        attr_ScanFile_read = "Hello Tango world"
        attr.set_value(attr_ScanFile_read)


#------------------------------------------------------------------
#    Write ScanFile attribute
#------------------------------------------------------------------
    def write_ScanFile(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ScanFile()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read ScanDir attribute
#------------------------------------------------------------------
    def read_ScanDir(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ScanDir()"
        
        #    Add your own code here
        
        attr_ScanDir_read = "Hello Tango world"
        attr.set_value(attr_ScanDir_read)


#------------------------------------------------------------------
#    Write ScanDir attribute
#------------------------------------------------------------------
    def write_ScanDir(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ScanDir()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read ScanID attribute
#------------------------------------------------------------------
    def read_ScanID(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ScanID()"
        
        #    Add your own code here
        
        attr_ScanID_read = 1
        attr.set_value(attr_ScanID_read)


#------------------------------------------------------------------
#    Write ScanID attribute
#------------------------------------------------------------------
    def write_ScanID(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ScanID()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read ActiveMntGrp attribute
#------------------------------------------------------------------
    def read_ActiveMntGrp(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ActiveMntGrp()"
        
        #    Add your own code here
        
        attr_ActiveMntGrp_read = "Hello Tango world"
        attr.set_value(attr_ActiveMntGrp_read)


#------------------------------------------------------------------
#    Write ActiveMntGrp attribute
#------------------------------------------------------------------
    def write_ActiveMntGrp(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ActiveMntGrp()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here


#------------------------------------------------------------------
#    Read TimeZone attribute
#------------------------------------------------------------------
    def read_TimeZone(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_TimeZone()"
        
        #    Add your own code here
        
        attr_TimeZone_read = "Hello Tango world"
        attr.set_value(attr_TimeZone_read)


#------------------------------------------------------------------
#    Write TimeZone attribute
#------------------------------------------------------------------
    def write_TimeZone(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_TimeZone()"
        data=[]
        attr.get_write_value(data)
        print >> self.log_info, "Attribute value = ", data

        #    Add your own code here




#==================================================================
#
#    NXSRecSettings command methods
#
#==================================================================

#------------------------------------------------------------------
#    AvailableComponents command:
#
#    Description: Returns a list of available component names
#                
#    argout: DevVarStringArray    list of available component names
#------------------------------------------------------------------
    def AvailableComponents(self):
        print >> self.log_info, "In ", self.get_name(), \
            "::AvailableComponents()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.stg.availableComponents()
            self.set_state(PyTango.DevState.ON)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.ON)
        
        return argout


#---- AvailableComponents command State Machine -----------------
    def is_AvailableComponents_allowed(self):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            return False
        return True


#------------------------------------------------------------------
#    AvailableDataSources command:
#
#    Description: Returns a list of available DataSource names
#                
#    argout: DevVarStringArray    list of available DataSource names
#------------------------------------------------------------------
    def AvailableDataSources(self):
        print >> self.log_info, "In ", self.get_name(), \
            "::AvailableDataSources()"
        #    Add your own code here
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.stg.availableDataSources()
            self.set_state(PyTango.DevState.ON)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.ON)
        
        return argout


#---- AvailableDataSources command State Machine -----------------
    def is_AvailableDataSources_allowed(self):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            return False
        return True



#------------------------------------------------------------------
#    MandatoryComponents command:
#
#    Description: Sets the mandatory components
#                
#    argout: DevVarStringArray    component names
#------------------------------------------------------------------
    def MandatoryComponents(self):
        print >> self.log_info, "In ", self.get_name(), \
            "::MandatoryComponents()"
        #    Add your own code here
        
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = self.stg.mandatoryComponents()
            self.set_state(PyTango.DevState.ON)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.ON)
        return argout


#---- MandatoryComponents command State Machine -----------------
    def is_MandatoryComponents_allowed(self):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            return False
        return True



#==================================================================
#
#    NXSRecSettingsClass class definition
#
#==================================================================
class NXSRecSettingsClass(PyTango.DeviceClass):

    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        'AvailableComponents':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVarStringArray, "list of available component names"]],
        'AvailableDataSources':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVarStringArray, "list of available DataSource names"]],
        'MandatoryComponents':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVarStringArray, "component names"]],
        }


    #    Attribute definitions
    attr_list = {
        'Components':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Selected Components",
                'description':"Selected Components",
                'Memorized':"true_without_hard_applied",
            } ],
        'ConfigDevice':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Configuration device",
                'description':"Configuration device",
                'Memorized':"true_without_hard_applied",
            } ],
        'WriterDevice':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Writer device",
                'description':"Writer device",
                'Memorized':"true_without_hard_applied",
            } ],
        'DataRecord':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"JSON with Client Data Record",
                'description':"JSON with Client Data Record",
                'Memorized':"true_without_hard_applied",
            } ],
        'DataSources':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Selected Datasources",
                'description':"Selected Datasources",
                'Memorized':"true_without_hard_applied",
            } ],
        'AppendEntry':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"flag for entry  appending ",
                'description':"flag for entry  appending ",
                'Memorized':"true_without_hard_applied",
            } ],
        'ComponentsFromMntGrp':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"select components from mntgrp",
                'description':"select components from mntgrp",
                'Memorized':"true_without_hard_applied",
            } ],
        'DynamicComponents':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"create dynamic components",
                'Memorized':"true_without_hard_applied",
            } ],
        'DynamicLinks':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"create links for dynamic components",
                'description':"create links for dynamic components",
                'Memorized':"true_without_hard_applied",
            } ],
        'DynamicPath':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"path for dynamic components",
                'description':"path for dynamic components",
                'Memorized':"true_without_hard_applied",
            } ],
        'ConfigVariables':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true_without_hard_applied",
            } ],
        'ScanFile':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"scan file",
                'description':"scan file",
                'Memorized':"true_without_hard_applied",
            } ],
        'ScanDir':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"scan directory",
                'description':"scan directory",
                'Memorized':"true_without_hard_applied",
            } ],
        'ScanID':
            [[PyTango.DevLong64,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true_without_hard_applied",
            } ],
        'ActiveMntGrp':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true_without_hard_applied",
            } ],
        'TimeZone':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true_without_hard_applied",
            } ],
        }


#------------------------------------------------------------------
#    NXSRecSettingsClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name);
        print "In NXSRecSettingsClass  constructor"

#==================================================================
#
#    NXSRecSettings class main method
#
#==================================================================
if __name__ == '__main__':
    pass
