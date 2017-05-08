#    "$Name:  $";
#    "$Header:  $";
#=============================================================================
#
# file :        TestConfigServer.py
#
# description : Python source for the TestConfigServer and its commands.
#                The class is derived from Device. It represents the
#                CORBA servant object which will be accessed from the
#                network. All commands which can be executed on the
#                TestConfigServer are implemented in this file.
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
import numpy
import struct
import pickle
import json
import re

#==================================================================
#   TestConfigServer Class Description:
#
#         My Simple Server
#
#==================================================================
#     Device States Description:
#
#   DevState.ON :  Server On
#==================================================================


class NXSConfigServer(PyTango.Device_4Impl):

    #--------- Add you global variables here --------------------------

    #------------------------------------------------------------------
    #    Device constructor
    #------------------------------------------------------------------
    def __init__(self, cl, name):
        PyTango.Device_4Impl.__init__(self, cl, name)

        self.attr_value = ""
        NXSConfigServer.init_device(self)

    #------------------------------------------------------------------
    #    Device destructor
    #------------------------------------------------------------------
    def delete_device(self):
        """ """
        # print "[Device delete_device method] for device", self.get_name()

    #------------------------------------------------------------------
    #    Device initialization
    #------------------------------------------------------------------
    def init_device(self):
        # print "In ", self.get_name(), "::init_device()"
        self.set_state(PyTango.DevState.ON)

        self.attr_XMLString = ""
        self.attr_Version = "2.0.0"
        self.attr_Selection = ""
        self.attr_JSONSettings = ""
        self.attr_STEPDataSources = ""
        self.attr_LinkDataSources = ""
        self.attr_Variables = "{}"

        self.cmd = {}
        self.cmd["CPDICT"] = {}
        self.cmd["DSDICT"] = {}
        self.cmd["SELDICT"] = {}
        self.cmd["VARS"] = []
        self.cmd["COMMANDS"] = []
        self.cmd["MCPLIST"] = []
        self.cmd["VALUE"] = None
        self.cmd["CHECKVARIABLES"] = "{}"

        self.get_device_properties(self.get_device_class())

    #------------------------------------------------------------------
    #    Always excuted hook method
    #------------------------------------------------------------------
    def always_executed_hook(self):
        pass
    #        print "In ", self.get_name(), "::always_excuted_hook()"

    #------------------------------------------------------------------
    #    Read Version attribute
    #------------------------------------------------------------------
    def read_Version(self, attr):
        # print >> self.log_info, "In ", self.get_name(), "::read_Version"
        attr.set_value(self.attr_Version)

    #------------------------------------------------------------------
    #    Read XMLString attribute
    #------------------------------------------------------------------
    def read_XMLString(self, attr):
        # print >> self.log_info, "In ", self.get_name(), "::read_XMLString()"
        attr.set_value(self.attr_XMLString)

    #------------------------------------------------------------------
    #    Write XMLString attribute
    #------------------------------------------------------------------
    def write_XMLString(self, attr):
        # print >> self.log_info, "In ", self.get_name(), "::write_XMLString()"
        self.attr_XMLString = attr.get_write_value()

    #------------------------------------------------------------------
    #    Read Selection attribute
    #------------------------------------------------------------------
    def read_Selection(self, attr):
        # print >> self.log_info, "In ", self.get_name(), "::read_Selection()"
        attr.set_value(self.attr_Selection)

    #------------------------------------------------------------------
    #    Write Selection attribute
    #------------------------------------------------------------------
    def write_Selection(self, attr):
        # print >> self.log_info, "In ", self.get_name(), "::write_Selection()"
        self.attr_Selection = attr.get_write_value()

    #------------------------------------------------------------------
    #    Read JSONSettings attribute
    #------------------------------------------------------------------
    def read_JSONSettings(self, attr):
        # print >> self.log_info, "In ", self.get_name(), "::read_JSONSettings()"
        attr.set_value(self.attr_JSONSettings)

    #------------------------------------------------------------------
    #    Write JSONSettings attribute
    #------------------------------------------------------------------
    def write_JSONSettings(self, attr):
        # print >> self.log_info, "In ", self.get_name(), \
            "::write_JSONSettings()"
        self.attr_JSONSettings = attr.get_write_value()

    #------------------------------------------------------------------
    #    Read STEPDataSources attribute
    #------------------------------------------------------------------
    def read_STEPDataSources(self, attr):
        # print >> self.log_info, "In ", self.get_name(), \
            "::read_STEPDataSources()"
        attr.set_value(self.attr_STEPDataSources)

    #------------------------------------------------------------------
    #    Write STEPDataSources attribute
    #------------------------------------------------------------------
    def write_STEPDataSources(self, attr):
        # print >> self.log_info, "In ", self.get_name(), \
            "::write_STEPDataSources()"
        self.attr_STEPDataSources = attr.get_write_value()

    #------------------------------------------------------------------
    #    Read LinkDataSources attribute
    #------------------------------------------------------------------
    def read_LinkDataSources(self, attr):
        # print >> self.log_info, "In ", self.get_name(), \
            "::read_LinkDataSources()"
        attr.set_value(self.attr_LinkDataSources)

    #------------------------------------------------------------------
    #    Write LinkDataSources attribute
    #------------------------------------------------------------------
    def write_LinkDataSources(self, attr):
        # print >> self.log_info, "In ", self.get_name(), \
            "::write_LinkDataSources()"
        self.attr_LinkDataSources = attr.get_write_value()

    #------------------------------------------------------------------
    def read_Variables(self, attr):
        # print >> self.log_info, "In ", self.get_name(), "::read_Variables()"
        attr.set_value(self.attr_Variables)

    #------------------------------------------------------------------
    #    Write Variables attribute
    #------------------------------------------------------------------
    def write_Variables(self, attr):
        # print >> self.log_info, "In ", self.get_name(), "::write_Variables()"
        self.attr_Variables = attr.get_write_value()

    #
    #==================================================================
    #
    #    NXSConfigServer command methods
    #
    #==================================================================
    #
    #------------------------------------------------------------------
    #    Open command:
    #
    #    Description: Opens connection to the database
    #
    #------------------------------------------------------------------
    def Open(self):
        # print >> self.log_info, "In ", self.get_name(), "::Open()"\
        """ """

    #------------------------------------------------------------------
    #    Close command:
    #
    #    Description: Closes connection into the database
    #
    #------------------------------------------------------------------
    def Close(self):
        """ """
        # print >> self.log_info, "In ", self.get_name(), "::Close()"
 
    #------------------------------------------------------------------
    #    Components command:
    #
    #    Description: Returns a list of required components
    #
    #    argin:  DevVarStringArray    list of component names
    #    argout: DevVarStringArray    list of required components
    #------------------------------------------------------------------
    def Components(self, names):
        # print >> self.log_info, "In ", self.get_name(), "::Components()"
        self.cmd["VARS"].append(names)
        self.cmd["COMMANDS"].append("Components")
        return [self.cmd["CPDICT"][nm] for nm in names
                if nm in self.cmd["CPDICT"].keys()]

    #------------------------------------------------------------------
    #    ComponentVariables command:
    #
    #    Description: Returns a list of required componentVariables
    #
    #    argin:  DevString    list of component names
    #    argout: DevVarStringArray    list of required componentVariables
    #------------------------------------------------------------------
    def ComponentVariables(self, name):
        # print >> self.log_info, "In ", self.get_name(), \
            "::ComponentVariables()"
        self.cmd["VARS"].append(name)
        self.cmd["COMMANDS"].append("ComponentVariables")
        cp = self.cmd["CPDICT"][name]
        return self.__findText(cp, "$var.")

    def __findText(self, text, label):
        variables = []
        index = text.find(label)
        while index != -1:
            try:
                subc = re.finditer(
                    r"[\w]+",
                    text[(index + len(label)):]
                ).next().group(0)
            except Exception as e:
                print("Error: %s" % str(e))
                subc = ""
            name = subc.strip() if subc else ""
            if name:
                variables.append(name)
            index = text.find(label, index + 1)
        return variables

    def DependentComponents(self, argin):
        """ DependentComponents command

        :brief: returns a list of dependent component names
            for a given components

        :param argin:  DevVarStringArray    component names
        :type argin: :obj:`list` <:obj:`str`>
        :returns: DevVarStringArray    list of component names
        :rtype: :obj:`list` <:obj:`str`>
        """
        self.debug_stream("In DependentComponents()")
        self.cmd["VARS"].append(argin)
        self.cmd["COMMANDS"].append("DependentComponents")
        res = []
        for name in argin:
            res.append(name)
            cp = self.cmd["CPDICT"][name]
            res.extend(self.__findText(cp, "$components."))
        return res

    
    #------------------------------------------------------------------
    #    Selections command:
    #
    #    Description: Returns a list of required selections
    #
    #    argin:  DevVarStringArray    list of selection names
    #    argout: DevVarStringArray    list of required selections
    #------------------------------------------------------------------
    def Selections(self, names):
        # print >> self.log_info, "In ", self.get_name(), "::Selections()"
        self.cmd["VARS"].append(names)
        self.cmd["COMMANDS"].append("Selections")
        return [self.cmd["SELDICT"][nm] for nm in names
                if nm in self.cmd["SELDICT"].keys()]

    #------------------------------------------------------------------
    #    InstantiatedComponents command:
    #
    #    Description: Returns a list of required components
    #
    #    argin:  DevVarStringArray    list of component names
    #    argout: DevVarStringArray    list of instantiated components
    #------------------------------------------------------------------
    def InstantiatedComponents(self, names):
        # print >> self.log_info, "In ", self.get_name(), \
            "::InstantiateComponents()"
        if self.cmd["CHECKVARIABLES"] != self.attr_Variables:
            # print "CMD", self.cmd["CHECKVARIABLES"]
            # print self.attr_Variables
            raise Exception("Variables not set")
        self.cmd["VARS"].append(names)
        self.cmd["COMMANDS"].append("InstantiatedComponents")
        return [self.cmd["CPDICT"][nm] for nm in names
                if nm in self.cmd["CPDICT"].keys()]

    #------------------------------------------------------------------
    #    DataSources command:
    #
    #    Description: Return a list of required DataSources
    #
    #    argin:  DevVarStringArray    list of DataSource names
    #    argout: DevVarStringArray    list of required DataSources
    #------------------------------------------------------------------
    def DataSources(self, names):
        # print >> self.log_info, "In ", self.get_name(), "::DataSources()"
        self.cmd["VARS"].append(names)
        self.cmd["COMMANDS"].append("DataSources")
        return [self.cmd["DSDICT"][nm] for nm in names
                if nm in self.cmd["DSDICT"].keys()]

    #------------------------------------------------------------------
    #    AvailableComponents command:
    #
    #    Description: Returns a list of available component names
    #
    #    argout: DevVarStringArray    list of available component names
    #------------------------------------------------------------------
    def AvailableComponents(self):
        # print >> self.log_info, "In ", self.get_name(), \
            "::AvailableComponents()"
        self.cmd["VARS"].append(None)
        self.cmd["COMMANDS"].append("AvailableComponents")
        return list(self.cmd["CPDICT"].keys())

    #------------------------------------------------------------------
    #    AvailableSelections command:
    #
    #    Description: Returns a list of available selection names
    #
    #    argout: DevVarStringArray    list of available selection names
    #------------------------------------------------------------------
    def AvailableSelections(self):
        # print >> self.log_info, "In ", self.get_name(), \
            "::AvailableSelections()"
        self.cmd["VARS"].append(None)
        self.cmd["COMMANDS"].append("AvailableSelections")
        return list(self.cmd["SELDICT"].keys())

    #------------------------------------------------------------------
    #    AvailableDataSources command:
    #
    #    Description: Returns a list of available DataSource names
    #
    #    argout: DevVarStringArray    list of available DataSource names
    #------------------------------------------------------------------
    def AvailableDataSources(self):
        # print >> self.log_info, "In ", self.get_name(), \
            "::AvailableDataSources()"
        self.cmd["VARS"].append(None)
        self.cmd["COMMANDS"].append("AvailableDataSources")
        return list(self.cmd["DSDICT"].keys())

    #------------------------------------------------------------------
    #    MandatoryComponents command:
    #
    #    Description: Sets the mandatory components
    #
    #    argout: DevVarStringArray    component names
    #------------------------------------------------------------------
    def MandatoryComponents(self):
        # print >> self.log_info, "In ", self.get_name(), \
            "::MandatoryComponents()"
        #    Add your own code here

        self.cmd["VARS"].append(None)
        self.cmd["COMMANDS"].append("MandatoryComponents")
        return list(self.cmd["MCPLIST"])

    #------------------------------------------------------------------
    #    StoreSelection command:
    #
    #    Description: Stores the selection from XMLString
    #
    #    argin:  DevString    selection name
    #------------------------------------------------------------------
    def StoreSelection(self, argin):
        # print >> self.log_info, "In ", self.get_name(), "::StoreSelection()"
        self.cmd["VARS"].append(argin)
        self.cmd["COMMANDS"].append("StoreSelection")
        self.cmd["SELDICT"][str(argin)] = self.attr_Selection

    #------------------------------------------------------------------
    #    StoreDataSource command:
    #
    #    Description: Stores the selection from XMLString
    #
    #    argin:  DevString    selection name
    #------------------------------------------------------------------
    def StoreDataSource(self, argin):
        # print >> self.log_info, "In ", self.get_name(), "::StoreDataSource()"
        self.cmd["VARS"].append(argin)
        self.cmd["COMMANDS"].append("StoreDataSource")
        self.cmd["DSDICT"][str(argin)] = self.attr_XMLString

    #------------------------------------------------------------------
    #    StoreComponent command:
    #
    #    Description: Stores the component from XMLString
    #
    #    argin:  DevString    component name
    #------------------------------------------------------------------
    def StoreComponent(self, argin):
        # print >> self.log_info, "In ", self.get_name(), "::StoreComponent()"
        self.cmd["VARS"].append(argin)
        self.cmd["COMMANDS"].append("StoreComponent")
        self.cmd["CPDICT"][str(argin)] = self.attr_XMLString

    #------------------------------------------------------------------
    #    DeleteComponent command:
    #
    #    Description: Deletes the component from XMLString
    #
    #    argin:  DevString    component name
    #------------------------------------------------------------------
    def DeleteComponent(self, argin):
        # print >> self.log_info, "In ", self.get_name(), "::DeleteComponent()"
        self.cmd["VARS"].append(argin)
        self.cmd["COMMANDS"].append("DeleteComponent")
        self.cmd["CPDICT"].pop(str(argin))

    #------------------------------------------------------------------
    #    DeleteSelection command:
    #
    #    Description: Deletes the selection from XMLString
    #
    #    argin:  DevString    selection name
    #------------------------------------------------------------------
    def DeleteSelection(self, argin):
        # print >> self.log_info, "In ", self.get_name(), "::DeleteSelection()"
        self.cmd["VARS"].append(argin)
        self.cmd["COMMANDS"].append("DeleteSelection")
        self.cmd["SELDICT"].pop(str(argin))

    #------------------------------------------------------------------
    #    DeleteDataSource command:
    #
    #    Description: Deletes the datasource from XMLString
    #
    #    argin:  DevString    datasource name
    #------------------------------------------------------------------
    def DeleteDataSource(self, argin):
        # print >> self.log_info, "In ", self.get_name(), "::DeleteDataSource()"
        self.cmd["VARS"].append(argin)
        self.cmd["COMMANDS"].append("DeleteDataSource")
        self.cmd["DSDICT"].pop(str(argin))

    #------------------------------------------------------------------
    #    CreateConfiguration command:
    #
    #    Description: Creates the NDTS configuration script from the
    #                 given components. The result is strored in XMLString
    #
    #    argin:  DevVarStringArray    list of component names
    #------------------------------------------------------------------
    def CreateConfiguration(self, argin):
        # print >> self.log_info, "In ", self.get_name(), \
            "::CreateConfiguration()"
        self.cmd["VARS"].append(argin)
        self.cmd["COMMANDS"].append("CreateConfiguration")

    #------------------------------------------------------------------
    #    SetState command:
    #
    #    Description: Set state of tango device
    #
    #    argin: DevString     tango state
    #------------------------------------------------------------------
    def SetState(self, state):
        # print "In ", self.get_name(), "::SetState()"
        if state == "RUNNING":
            self.set_state(PyTango.DevState.RUNNING)
        elif state == "FAULT":
            self.set_state(PyTango.DevState.FAULT)
        elif state == "ALARM":
            self.set_state(PyTango.DevState.ALARM)
        else:
            self.set_state(PyTango.DevState.ON)

    #------------------------------------------------------------------
    #    GetCommandVariable command:
    #
    #    Description: Get command variable
    #
    #    argin: DevString     variable
    #------------------------------------------------------------------
    def GetCommandVariable(self, variable):
        return json.dumps(self.cmd[variable])

    #------------------------------------------------------------------
    #    SetCommandVariable command:
    #
    #    Description: Set command variable
    #
    #    argin: DevVarStringArray     variable
    #------------------------------------------------------------------
    def SetCommandVariable(self, record):
        self.cmd[record[0]] = json.loads(record[1])


#==================================================================
#
#    NXSConfigServerClass class definition
#
#==================================================================
class NXSConfigServerClass(PyTango.DeviceClass):

    #    Class Properties
    class_property_list = {
    }

    #    Device Properties
    device_property_list = {
    }

    #    Command definitions
    cmd_list = {
        'SetState':
            [[PyTango.DevString, "ScalarString"],
             [PyTango.DevVoid, ""]],
        'Open':
            [[PyTango.DevVoid, ""],
             [PyTango.DevVoid, ""]],
        'Close':
            [[PyTango.DevVoid, ""],
             [PyTango.DevVoid, ""]],
        'Components':
            [[PyTango.DevVarStringArray, "list of component names"],
             [PyTango.DevVarStringArray, "list of required components"]],
        'Selections':
            [[PyTango.DevVarStringArray, "list of selection names"],
             [PyTango.DevVarStringArray, "list of required selections"]],
        'InstantiatedComponents':
            [[PyTango.DevVarStringArray, "list of component names"],
             [PyTango.DevVarStringArray, "list of instantiated components"]],
        'DataSources':
            [[PyTango.DevVarStringArray, "list of DataSource names"],
             [PyTango.DevVarStringArray, "list of required DataSources"]],
        'AvailableComponents':
            [[PyTango.DevVoid, ""],
             [PyTango.DevVarStringArray, "list of available component names"]],
        'AvailableSelections':
            [[PyTango.DevVoid, ""],
             [PyTango.DevVarStringArray, "list of available selection names"]],
        'AvailableDataSources':
            [[PyTango.DevVoid, ""],
             [PyTango.DevVarStringArray,
              "list of available DataSource names"]],
        'StoreSelection':
            [[PyTango.DevString, "selection name"],
             [PyTango.DevVoid, ""]],
        'CreateConfiguration':
            [[PyTango.DevVarStringArray, "list of component names"],
             [PyTango.DevVoid, ""]],
        'MandatoryComponents':
            [[PyTango.DevVoid, ""],
             [PyTango.DevVarStringArray, "component names"]],
        'StoreComponent':
            [[PyTango.DevString, "component name"],
             [PyTango.DevVoid, ""]],
        'StoreDataSource':
            [[PyTango.DevString, "datasource name"],
             [PyTango.DevVoid, ""]],
        'DeleteComponent':
            [[PyTango.DevString, "component name"],
             [PyTango.DevVoid, ""]],
        'DeleteSelection':
            [[PyTango.DevString, "selection name"],
             [PyTango.DevVoid, ""]],
        'DeleteDataSource':
            [[PyTango.DevString, "datasource name"],
             [PyTango.DevVoid, ""]],
        'SetCommandVariable':
            [[PyTango.DevVarStringArray, "(name,jsonstring)"],
             [PyTango.DevVoid, ""]],
        'GetCommandVariable':
            [[PyTango.DevString, "name"],
             [PyTango.DevString, "jsonstring"]],
        'ComponentVariables':
            [[PyTango.DevString, "component name"],
             [PyTango.DevVarStringArray, "list of variable names"]],
        'DependentComponents':
            [[PyTango.DevVarStringArray, "component names"],
             [PyTango.DevVarStringArray, "list of component names"]],
    }

    #    Attribute definitions
    attr_list = {
        'XMLString':
            [[PyTango.DevString,
              PyTango.SCALAR,
              PyTango.READ_WRITE],
             {
                 'label': "XML configuration",
                 'description':
                 "It allows to pass XML strings into database during "
                 "performing StoreComponent and StoreDataSource."
                 "\nMoreover, after performing CreateConfiguration "
                 "it contains the resulting XML configuration.",
                 'Display level': PyTango.DispLevel.EXPERT,
            }],
        'Selection':
            [[PyTango.DevString,
              PyTango.SCALAR,
              PyTango.READ_WRITE],
             {
                 'label': "Selected Component",
                 'description':
                 "It allows to pass JSON strings into database during "
                 "performing StoreSelection.",
                 'Display level': PyTango.DispLevel.EXPERT,
            }],
        'JSONSettings':
            [[PyTango.DevString,
              PyTango.SCALAR,
              PyTango.READ_WRITE],
             {
                 'label': "Arguments of MySQLdb.connect(...)",
                 'description': "The JSON string with parameters of "
                 "MySQLdb.connect(...).",
                 'Memorized': "true",
                 'Display level': PyTango.DispLevel.EXPERT,
            }],
        'Variables':
            [[PyTango.DevString,
              PyTango.SCALAR,
              PyTango.READ_WRITE],
             {
                 'label': "XML configuration variables",
                 'description': "The JSON string with "
                 "XML configuration variables",
            }],
        'STEPDataSources':
            [[PyTango.DevString,
              PyTango.SCALAR,
              PyTango.READ_WRITE],
             {
                 'label': "datasources to be switched into STEP mode",
                 'description': "datasources to be switched "
                 "into STEP mode during creating configuration process",
            }],
        'LinkDataSources':
            [[PyTango.DevString,
              PyTango.SCALAR,
              PyTango.READ_WRITE],
             {
                 'label': "datasources to be switched into Link mode",
                 'description': "datasources to be switched "
                 "into Link mode during creating configuration process",
            }],
        'Version':
            [[PyTango.DevString,
              PyTango.SCALAR,
              PyTango.READ],
             {
                 'label': "Configuration Version",
                 'description': "Configuration version",
            }],
    }

#------------------------------------------------------------------
#    NXSConfigServerClass Constructor
#------------------------------------------------------------------
    def __init__(self, name):
        PyTango.DeviceClass.__init__(self, name)
        self.set_type(name)
        # print "In TestConfigServerClass  constructor"

#==================================================================
#
#    NXSConfigServer class main method
#
#==================================================================
if __name__ == '__main__':
    try:
        argv = list(sys.argv)
        argv[0] = "NXSConfigServer"
        py = PyTango.Util(argv)
        py.add_class(NXSConfigServerClass, NXSConfigServer)

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed, e:
        print '-------> Received a DevFailed exception:', e
    except Exception, e:
        print '-------> An unforeseen exception occured....', e
