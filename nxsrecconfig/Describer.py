#!/usr/bin/env python
#   This file is part of nxsrecconfig - NeXus Sardana Recorder Settings
#
#    Copyright (C) 2014 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
## \file Describer.py
# component describer

"""  Component Describer """

import re
import xml.dom.minidom
from .Utils import Utils

## NeXus Sardana Recorder settings
class Describer(object):
    """ Lists datasources, strategy and dstype of given component """

    def __init__(self, configserver):
        self.__result = [{}, {}]
        self.__server = configserver
        self.__nexusconfig_device = None

    def run(self, components=None, strategy='', dstype=''):

        if self.__server:
            self.__nexusconfig_device = Utils.openProxy(self.__server)
            self.__nexusconfig_device.Open()
            if components is not None:
                cpp = self.__nexusconfig_device.AvailableComponents()  
                cps = [cp for cp in components if cp in cpp]
            else:
                cps = self.__nexusconfig_device.AvailableComponents()  
            if components is None:
                mand = self.__nexusconfig_device.MandatoryComponents()
                cps = list(set(cps)- set(mand))

            if components is None:
                for cp in mand:
                    dss = self.__getDataSourceAttributes(cp)  
                    tr = {}
                    for ds in dss.keys():
                        for vds in dss[ds]:
                            if (not strategy or vds[0] == strategy) and \
                                    (not dstype or vds[1] == dstype):
                                if ds not in tr:
                                    tr[ds] = []
                                tr[ds].append(vds)
                    self.__result[0][cp] = tr

            for cp in cps:
                dss = self.__getDataSourceAttributes(cp)  
                tr = {}
                for ds in dss.keys():
                    for vds in dss[ds]:
                        if (not strategy or vds[0] == strategy) and \
                                (not dstype or vds[1] == dstype):
                            if ds not in tr:
                                tr[ds] = []
                            tr[ds].append(vds)
                self.__result[1][cp] = tr
        return self.__result

    def __getRecord(self, node):
        res = ''
        host = None
        port = None
        dname = None
        rname = None
        device = node.getElementsByTagName("device")
        if device and len(device)>0:
            if device[0].hasAttribute("host"):
                host = device[0].attributes["host"].value
            if device[0].hasAttribute("port"):
                port = device[0].attributes["port"].value
            if device[0].hasAttribute("name"):
                dname = device[0].attributes["name"].value

        record = node.getElementsByTagName("record")
        if record and len(record)>0:
            if record[0].hasAttribute("name"):
                rname = record[0].attributes["name"].value
                if dname:
                    if host:
                        if not port:
                            port = '10000'
                        res = '%s:%s/%s/%s' % (host, port, dname, rname)
                    else:
                        res = '%s/%s' % (dname, rname)
                else:
                    res = rname
        return res

    def __checkNode(self, node):
        label = 'datasources'
        dstype = None
        name = None
        record = None
        if node.nodeName == 'datasource':
            if node.hasAttribute("type"):
                dstype  = node.attributes["type"].value
            if node.hasAttribute("name"):
                name = node.attributes["name"].value
            record = self.__getRecord(node)     
        elif node.nodeType == node.TEXT_NODE:
            dstxt = node.data
            index = dstxt.find("$%s." % label)
            while index != -1 and not dstype:
                try:
                    subc = re.finditer(
                        r"[\w]+", 
                        dstxt[(index+len(label)+2):]).next().group(0)
                except Exception:
                    subc = ''
                name = subc.strip() if subc else ""
                try:
                    dsource = self.__nexusconfig_device.DataSources([str(name)])
                except:
                    dsource = []
                if len(dsource)>0:
                    indom = xml.dom.minidom.parseString(dsource[0])
                    dss = indom.getElementsByTagName("datasource")
                    for ds in dss:
                        if ds.nodeName == 'datasource':
                            if ds.hasAttribute("type"):
                                dstype  = ds.attributes["type"].value
                            if ds.hasAttribute("name"):
                                name = ds.attributes["name"].value
                            record = self.__getRecord(ds)    
                index = dstxt.find("$%s." % label, index+1)
        return name, dstype, record
                

    def __appendNode(self, node, dss, mode, counter): 
        prefix = '__unnamed__'
        name, dstype, record = self.__checkNode(node)
        if name:
            if name not in dss:
                dss[name] = [] 
            dss[name].append((str(mode), str(dstype) if dstype else None,
                              str(record) if record else None))
        elif node.nodeName == 'datasource':
            name = prefix + str(counter) 
            while name in dss.keys():
                name = prefix + str(counter) 
                counter = counter + 1
            dss[name] = [] 
            dss[name].append((str(mode), str(dstype) if dstype else None,
                              str(record) if record else None))
        
        counter = counter +1
        return (name, counter)

    def __getDataSourceAttributes(self, cp):         
        dss = {}
        xmlc = self.__nexusconfig_device.Components([cp])
        names = []
        if not len(xmlc)>0:
            return names
        indom = xml.dom.minidom.parseString(xmlc[0])
        strategy = indom.getElementsByTagName("strategy")
        counter = 1

        for sg in strategy:
            if sg.hasAttribute("mode"):
                mode = sg.attributes["mode"].value
                name = None
                nxt = sg.nextSibling
                while nxt and not name:
                    name, counter = self.__appendNode(nxt, dss, mode, counter)
                    nxt = nxt.nextSibling    

                prev = sg.previousSibling
                while prev and not name:
                    name, counter = self.__appendNode(prev, dss, mode, counter)
                    prev = prev.previousSibling  
        return dss


     
