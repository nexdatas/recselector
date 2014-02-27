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
        attr.set_value(self.stg.state["Components"])


#------------------------------------------------------------------
#    Write Components attribute
#------------------------------------------------------------------
    def write_Components(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_Components()"
        self.stg.state["Components"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["Components"]

#------------------------------------------------------------------
#    Read AutomaticComponents attribute
#------------------------------------------------------------------
    def read_AutomaticComponents(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_AutomaticComponents()"
        attr.set_value(self.stg.state["AutomaticComponents"])


#------------------------------------------------------------------
#    Write ComponentGroup attribute
#------------------------------------------------------------------
    def write_AutomaticComponents(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_AutomaticComponents()"
        self.stg.state["AutomaticComponents"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["AutomaticComponents"]



#------------------------------------------------------------------
#    Read ConfigDevice attribute
#------------------------------------------------------------------
    def read_ConfigDevice(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ConfigDevice()"
        attr.set_value(self.stg.configDevice)


#------------------------------------------------------------------
#    Write ConfigDevice attribute
#------------------------------------------------------------------
    def write_ConfigDevice(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ConfigDevice()"
        self.stg.configDevice = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.configDevice


#------------------------------------------------------------------
#    Read WriterDevice attribute
#------------------------------------------------------------------
    def read_WriterDevice(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_WriterDevice()"
        attr.set_value(self.stg.writerDevice)


#------------------------------------------------------------------
#    Write WriterDevice attribute
#------------------------------------------------------------------
    def write_WriterDevice(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_WriterDevice()"
        self.stg.writerDevice = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.writerDevice

#------------------------------------------------------------------
#    Read DataRecord attribute
#------------------------------------------------------------------
    def read_DataRecord(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DataRecord()"
        attr.set_value(self.stg.state["DataRecord"])


#------------------------------------------------------------------
#    Write DataRecord attribute
#------------------------------------------------------------------
    def write_DataRecord(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DataRecord()"
        self.stg.state["DataRecord"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["DataRecord"]



#------------------------------------------------------------------
#    Read LabelPaths attribute
#------------------------------------------------------------------
    def read_LabelPaths(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_LabelPaths()"
        attr.set_value(self.stg.state["LabelPaths"])


#------------------------------------------------------------------
#    Write LabelPaths attribute
#------------------------------------------------------------------
    def write_LabelPaths(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_LabelPaths()"
        self.stg.state["LabelPaths"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["LabelPaths"]




#------------------------------------------------------------------
#    Read DataSourceLabels attribute
#------------------------------------------------------------------
    def read_DataSourceLabels(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DataSourceLabels()"
        attr.set_value(self.stg.state["DataSourceLabels"])


#------------------------------------------------------------------
#    Write DataSourceLabels attribute
#------------------------------------------------------------------
    def write_DataSourceLabels(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DataSourceLabels()"
        self.stg.state["DataSourceLabels"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["DataSourceLabels"]


#------------------------------------------------------------------
#    Read DataSources attribute
#------------------------------------------------------------------
    def read_DataSources(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DataSources()"
        attr.set_value(self.stg.state["DataSources"])


#------------------------------------------------------------------
#    Write DataSources attribute
#------------------------------------------------------------------
    def write_DataSources(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DataSources()"
        self.stg.state["DataSources"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["DataSources"]


#------------------------------------------------------------------
#    Read AppendEntry attribute
#------------------------------------------------------------------
    def read_AppendEntry(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_AppendEntry()"
        attr.set_value(self.stg.state["AppendEntry"])


#------------------------------------------------------------------
#    Write AppendEntry attribute
#------------------------------------------------------------------
    def write_AppendEntry(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_AppendEntry()"
        self.stg.state["AppendEntry"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["AppendEntry"]
        

#------------------------------------------------------------------
#    Read ComponentsFromMntGrp attribute
#------------------------------------------------------------------
    def read_ComponentsFromMntGrp(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ComponentsFromMntGrp()"
        attr.set_value(self.stg.state["ComponentsFromMntGrp"])


#------------------------------------------------------------------
#    Write ComponentsFromMntGrp attribute
#------------------------------------------------------------------
    def write_ComponentsFromMntGrp(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ComponentsFromMntGrp()"
        self.stg.state["ComponentsFromMntGrp"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["ComponentsFromMntGrp"]


#------------------------------------------------------------------
#    Read DynamicComponents attribute
#------------------------------------------------------------------
    def read_DynamicComponents(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DynamicComponents()"
        attr.set_value(self.stg.state["DynamicComponents"])


#------------------------------------------------------------------
#    Write DynamicComponents attribute
#------------------------------------------------------------------
    def write_DynamicComponents(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DynamicComponents()"
        self.stg.state["DynamicComponents"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["DynamicComponents"]


#------------------------------------------------------------------
#    Read DynamicLinks attribute
#------------------------------------------------------------------
    def read_DynamicLinks(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DynamicLinks()"
        attr.set_value(self.stg.state["DynamicLinks"])

#------------------------------------------------------------------
#    Write DynamicLinks attribute
#------------------------------------------------------------------
    def write_DynamicLinks(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DynamicLinks()"
        self.stg.state["DynamicLinks"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["DynamicLinks"]


#------------------------------------------------------------------
#    Read DynamicPath attribute
#------------------------------------------------------------------
    def read_DynamicPath(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_DynamicPath()"
        attr.set_value(self.stg.state["DynamicPath"])


#------------------------------------------------------------------
#    Write DynamicPath attribute
#------------------------------------------------------------------
    def write_DynamicPath(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_DynamicPath()"
        self.stg.state["DynamicPath"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["DynamicPath"]


#------------------------------------------------------------------
#    Read ConfigVariables attribute
#------------------------------------------------------------------
    def read_ConfigVariables(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ConfigVariables()"
        attr.set_value(self.stg.state["ConfigVariables"])


#------------------------------------------------------------------
#    Write ConfigVariables attribute
#------------------------------------------------------------------
    def write_ConfigVariables(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ConfigVariables()"
        self.stg.state["ConfigVariables"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["ConfigVariables"]


#------------------------------------------------------------------
#    Read ConfigFile attribute
#------------------------------------------------------------------
    def read_ConfigFile(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_ConfigFile()"
        attr.set_value(self.stg.configFile)


#------------------------------------------------------------------
#    Write ConfigFile attribute
#------------------------------------------------------------------
    def write_ConfigFile(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_ConfigFile()"
        self.stg.configFile = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.configFile


#    Read TimeZone attribute
#------------------------------------------------------------------
    def read_TimeZone(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::read_TimeZone()"
        attr.set_value(self.stg.state["TimeZone"])


#------------------------------------------------------------------
#    Write TimeZone attribute
#------------------------------------------------------------------
    def write_TimeZone(self, attr):
        print >> self.log_info, "In ", self.get_name(), "::write_TimeZone()"
        self.stg.state["TimeZone"] = attr.get_write_value()
        print >> self.log_info, "Attribute value = %s" % self.stg.state["TimeZone"]




#==================================================================
#
#    NXSRecSettings command methods
#
#==================================================================

#------------------------------------------------------------------
#    LoadConfiguration command:
#
#    Description: Load server configuration
#                
#------------------------------------------------------------------
    def LoadConfiguration(self):
        print >> self.log_info, "In ", self.get_name(), \
            "::LoadConfiguration()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            self.stg.loadConfiguration()
            
            ## updating memorized attributes
            dp = PyTango.DeviceProxy(str(self.get_name()))
            for var in self.stg.state.keys():
                if hasattr(dp, var):
                    if isinstance(self.stg.state[var], unicode):
                        dp.write_attribute(str(var), str(self.stg.state[var]))
                    else:
                        dp.write_attribute(str(var), self.stg.state[var])

            self.set_state(PyTango.DevState.ON)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.ON)
        


#---- LoadConfiguration command State Machine -----------------
    def is_LoadConfiguration_allowed(self):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            return False
        return True



#------------------------------------------------------------------
#    LoadConfiguration command:
#
#    Description: Save server configuration
#                
#------------------------------------------------------------------
    def SaveConfiguration(self):
        print >> self.log_info, "In ", self.get_name(), \
            "::SaveConfiguration()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            self.stg.saveConfiguration()
            self.set_state(PyTango.DevState.ON)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.ON)
        


#---- SaveConfiguration command State Machine -----------------
    def is_SaveConfiguration_allowed(self):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            return False
        return True



#------------------------------------------------------------------
#    DataSourcePath command:
#
#    Description: Returns a NeXus path of a given datasource
#                
#    argout: DevString    datasource name
#    argout: DevString    NeXus path
#------------------------------------------------------------------
    def DataSourcePath(self, argin):
        print >> self.log_info, "In ", self.get_name(), \
            "::DataSourcePath()"
        try:
            self.set_state(PyTango.DevState.RUNNING)
            argout = str(self.stg.dataSourcePath(argin))
            self.set_state(PyTango.DevState.ON)
        finally:
            if self.get_state() == PyTango.DevState.RUNNING:
                self.set_state(PyTango.DevState.ON)
        
        return argout


#---- AvailableComponents command State Machine -----------------
    def is_DataSourcePath_allowed(self):
        if self.get_state() in [PyTango.DevState.RUNNING]:
            return False
        return True


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
        'DataSourcePath':
            [[PyTango.DevString, "datasource name"],
            [PyTango.DevString, "NeXus Path"]],
        'LoadConfiguration':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVoid, ""]],
        'SaveConfiguration':
            [[PyTango.DevVoid, ""],
            [PyTango.DevVoid, ""]],
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
                'description':"JSON list of Selected Components",
                'Memorized':"true",
                'Display level':PyTango.DispLevel.EXPERT,
            } ],
        'AutomaticComponents':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Automatic Components",
                'description':"JSON list of components available for automatic selection",
                'Memorized':"true",
                'Display level':PyTango.DispLevel.EXPERT,
            } ],
        'ConfigDevice':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Configuration Device",
                'description':"Configuration device",
                'Memorized':"true",
            } ],
        'WriterDevice':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Writer Device",
                'description':"Writer device",
                'Memorized':"true",
            } ],
        'DataRecord':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Client Data Record",
                'description':"JSON dictionary with Client Data Record",
                'Memorized':"true",
                'Display level':PyTango.DispLevel.EXPERT,
            } ],
        'LabelPaths':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"NeXus Paths for DataSource Labels",
                'description':"JSON dictionary with NeXus Paths for Datasource Labels",
                'Memorized':"true",
                'Display level':PyTango.DispLevel.EXPERT,
            } ],
        'DataSourceLabels':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"DataSource Labels",
                'description':"JSON dictionary with Datasource Labels",
                'Memorized':"true",
                'Display level':PyTango.DispLevel.EXPERT,
            } ],
        'DataSources':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Selected Datasources",
                'description':"JSON list of Selected Datasources",
                'Memorized':"true",
                'Display level':PyTango.DispLevel.EXPERT,
            } ],
        'AppendEntry':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Append Entry",
                'description':"flag for entry  appending ",
                'Memorized':"true",
            } ],
        'ComponentsFromMntGrp':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Select Components from MntGrp",
                'description':"select components from mntgrp",
                'Memorized':"true",
            } ],
        'DynamicComponents':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Dynamic Components",
                'description':"create dynamic components",
                'Memorized':"true",
            } ],
        'DynamicLinks':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Links for Dynamic Components",
                'description':"create links for dynamic components",
                'Memorized':"true",
            } ],
        'DynamicPath':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Path for Dynamic Components",
                'description':"path for dynamic components",
                'Memorized':"true",
            } ],
        'ConfigVariables':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Configuration Variables",
                'description':"JSON dictionary with configuration variables for templated components",
                'Memorized':"true",
                'Display level':PyTango.DispLevel.EXPERT,
            } ],
        'ConfigFile':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Config File with its Path",
                'description':"config file with its full path",
                'Memorized':"true",
            } ],
        'TimeZone':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'label':"Time Zone",
                'description':"timezone",
                'Memorized':"true",
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
