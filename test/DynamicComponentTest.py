#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2014 DESY, Jan Kotanski <jkotan@mail.desy.de>
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
## \package test nexdatas
## \file DynamicComponentTest.py
# unittests for TangoDsItemTest running Tango Server
#
import unittest
import os
import sys
import subprocess
import random
import struct
import threading
import binascii
import Queue
import PyTango
import json
import pickle
import string
import time

import logging
logger = logging.getLogger()

import TestMacroServerSetUp
import TestPoolSetUp
import TestServerSetUp
import TestConfigServerSetUp
import TestWriterSetUp


from nxsrecconfig.MacroServerPools import MacroServerPools
from nxsrecconfig.DynamicComponent import DynamicComponent
from nxsrecconfig.Utils import TangoUtils, MSUtils
from nxsconfigserver.XMLConfigurator import XMLConfigurator

## if 64-bit machione
IS64BIT = (struct.calcsize("P") == 8)

## list of available databases
DB_AVAILABLE = []

try:
    import MySQLdb
    ## connection arguments to MYSQL DB
    mydb = MySQLdb.connect({})
    mydb.close()
    DB_AVAILABLE.append("MYSQL")
except:
    try:
        import MySQLdb
    ## connection arguments to MYSQL DB
        args = {'host': u'localhost', 'db': u'nxsconfig',
                'read_default_file': u'/etc/my.cnf', 'use_unicode': True}
    ## inscance of MySQLdb
        mydb = MySQLdb.connect(**args)
        mydb.close()
        DB_AVAILABLE.append("MYSQL")
    except:
        try:
            import MySQLdb
            from os.path import expanduser
            home = expanduser("~")
        ## connection arguments to MYSQL DB
            args2 = {'host': u'localhost', 'db': u'nxsconfig',
                     'read_default_file': u'%s/.my.cnf' % home,
                     'use_unicode': True}
        ## inscance of MySQLdb
            mydb = MySQLdb.connect(**args2)
            mydb.close()
            DB_AVAILABLE.append("MYSQL")

        except ImportError, e:
            print "MYSQL not available: %s" % e
        except Exception, e:
            print "MYSQL not available: %s" % e
        except:
            print "MYSQL not available"


## test fixture
class DynamicComponentTest(unittest.TestCase):

    ## constructor
    # \param methodName name of the test method
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

        self._bint = "int64" if IS64BIT else "int32"
        self._buint = "uint64" if IS64BIT else "uint32"
        self._bfloat = "float64" if IS64BIT else "float32"

#        self._ms = TestMacroServerSetUp.TestMacroServerSetUp()
        self._cf = TestConfigServerSetUp.TestConfigServerSetUp()
#        self._wr = TestWriterSetUp.TestWriterSetUp()
#        self._pool = TestPoolSetUp.TestPoolSetUp()
        self._simps = TestServerSetUp.TestServerSetUp()

        try:
            self.__seed = long(binascii.hexlify(os.urandom(16)), 16)
        except NotImplementedError:
            self.__seed = long(time.time() * 256)

        self.__rnd = random.Random(self.__seed)

        self.__dump = {}

        self.__npTn = {"float32": "NX_FLOAT32", "float64": "NX_FLOAT64",
                       "float": "NX_FLOAT32", "double": "NX_FLOAT64",
                       "int": "NX_INT", "int64": "NX_INT64",
                       "int32": "NX_INT32", "int16": "NX_INT16",
                       "int8": "NX_INT8", "uint64": "NX_UINT64",
                       "uint32": "NX_UINT32", "uint16": "NX_UINT16",
                       "uint8": "NX_UINT8", "uint": "NX_UINT64",
                       "string": "NX_CHAR", "bool": "NX_BOOLEAN"}
        ## default zone
        self.__defaultzone = 'Europe/Berlin'
        ## default mntgrp
        self.__defaultmntgrp = 'nxsmntgrp'
        ## default path
        self.__defaultpath = \
            '/entry$var.serialno:NXentry/NXinstrument/collection'

        self._keys = [
            ("Timer", '[]'),
            ("OrderedChannels", '[]'),
            ("ComponentGroup", '{}'),
            ("AutomaticComponentGroup", '{}'),
            ("AutomaticDataSources", '[]'),
            ("DataSourceGroup", '{}'),
            ("InitDataSources", '[]'),
            ("OptionalComponents", '[]'),
            ("AppendEntry", False),
            ("ComponentsFromMntGrp", False),
            ("ConfigVariables", '{}'),
            ("DataRecord", '{}'),
            ("Labels", '{}'),
            ("LabelPaths", '{}'),
            ("LabelLinks", '{}'),
            ("HiddenElements", '[]'),
            ("LabelTypes", '{}'),
            ("LabelShapes", '{}'),
            ("DynamicComponents", True),
            ("DynamicLinks", True),
            ("DynamicPath", self.__defaultpath),
            ("TimeZone", self.__defaultzone),
            ("ConfigDevice", ''),
            ("WriterDevice", ''),
            ("Door", ''),
            ("MntGrp", '')
            ]

        self.mysel = {
            'mysl': (
                '{}'),
            'mysl2': (
                json.dumps({key: value for (key, value) in self._keys})),
            }

        self.mycps = {
            'mycp': (
                '<?xml version=\'1.0\'?>'
                '<definition>'
                '<group type="NXcollection" name="dddd"/>'
                '</definition>'),
            'mycp2': (
                '<definition><group type="NXcollection" name="dddd">'
                '<field><datasource type="TANGO" name="ann" /></field>'
                '</group></definition>'),
            'mycp3': (
                '<definition><group type="NXcollection" name="dddd">'
                '<field><datasource type="TANGO" name="ann" />'
                '<strategy mode="STEP" />'
                '</field></group></definition>'),
            'exp_t01': (
                '<?xml version=\'1.0\'?>'
                '<definition>'
                '<group type="NXentry" name="entry1">'
                '<group type="NXinstrument" name="instrument">'
                '<group type="NXdetector" name="detector">'
                '<field units="s" type="NX_FLOAT" name="exp_t01">'
                '<strategy mode="STEP"/>'
                '<datasource type="CLIENT" name="exp_t01">'
                '<record name="haso228k:10000/expchan/dgg2_exp_01/1"/>'
                '</datasource></field></group></group>'
                '</group></definition>'),
            'dim1': (
                '<definition><group type="NXentry">'
                '<field type="NX_INT8" name="field1">'
                '<datasource type="TANGO" name="tann1c">'
                '<record name="myattr2"/>'
                '<device member="attribute" name="dsf/sd/we"/>'
                '</datasource>'
                '<strategy mode="INIT"/>'
                '<dimensions rank="1">'
                '<dim index="1" value="34">'
                '</dim></dimensions>'
                '</field></group>'
                '</definition>'),
            'dim2': (
                '<definition><group type="NXentry">'
                '<field type="NX_INT8" name="field1">'
                '<datasource type="TANGO" name="tann1c">'
                '<record name="myattr2"/>'
                '<device member="attribute" name="dsf/sd/we"/>'
                '</datasource>'
                '<strategy mode="INIT"/>'
                '<dimensions rank="1">'
                '<dim index="1" value="$datasource.ann">'
                '</dim></dimensions>'
                '</field></group>'
                '</definition>'),
            'dim3': (
                '<definition><group type="NXentry">'
                '<field type="NX_INT8" name="field1">'
                '<datasource type="TANGO" name="tann1c">'
                '<record name="myattr2"/>'
                '<device member="attribute" name="dsf/sd/we"/>'
                '</datasource>'
                '<strategy mode="INIT"/>'
                '<dimensions rank="1">'
                '<dim index="1">1234'
                '</dim></dimensions>'
                '</field></group>'
                '</definition>'),
            'dim4': (
                '<definition><group type="NXentry">'
                '<field type="NX_INT8" name="field1">'
                '<datasource type="TANGO" name="tann1c">'
                '<record name="myattr2"/>'
                '<device member="attribute" name="dsf/sd/we"/>'
                '</datasource>'
                '<strategy mode="INIT"/>'
                '<dimensions rank="1">'
                '<dim index="1">$datasource.ann2<strategy mode="CONFIG" />'
                '</dim></dimensions>'
                '</field></group>'
                '</definition>'),
            'dim5': (
                '<definition><group type="NXentry">'
                '<field type="NX_INT8" name="field1">'
                '<datasource type="TANGO" name="tann1c">'
                '<record name="myattr2"/>'
                '<device member="attribute" name="dsf/sd/we"/>'
                '</datasource>'
                '<strategy mode="INIT"/>'
                '<dimensions rank="1">'
                '<dim index="1"><strategy mode="CONFIG" />'
                '<datasource type="TANGO" name="ann" />'
                '</dim></dimensions>'
                '</field></group>'
                '</definition>'),
            'dim6': (
                '<definition><group type="NXentry">'
                '<field type="NX_INT8" name="field1">'
                '<datasource type="TANGO" name="tann1c">'
                '<record name="myattr2"/>'
                '<device member="attribute" name="dsf/sd/we"/>'
                '</datasource>'
                '<strategy mode="INIT"/>'
                '<dimensions rank="2">'
                '<dim index="1" value="$datasource.ann" />'
                '<dim index="2" value="123" />'
                '</dimensions>'
                '</field></group>'
                '</definition>'),
            'dim7': (
                '<definition><group type="NXentry">'
                '<field type="NX_INT8" name="field1">'
                '<datasource type="TANGO" name="tann1c">'
                '<record name="myattr2"/>'
                '<device member="attribute" name="dsf/sd/we"/>'
                '</datasource>'
                '<strategy mode="INIT"/>'
                '<dimensions rank="2" />'
                '</field></group>'
                '</definition>'),
            'dim8': (
                '<definition><group type="NXentry">'
                '<field type="NX_INT8" name="field1">'
                '<datasource type="TANGO" name="tann1c">'
                '<record name="myattr2"/>'
                '<device member="attribute" name="dsf/sd/we"/>'
                '</datasource>'
                '<strategy mode="INIT"/>'
                '<dimensions rank="2">'
                '<dim index="2" value="123" />'
                '</dimensions>'
                '</field></group>'
                '</definition>'),
            'scan': (
                '<definition><group type="NXentry" name="entry1">'
                '<group type="NXinstrument" name="instrument">'
                '<group type="NXdetector" name="detector">'
                '<field units="m" type="NX_FLOAT" name="counter1">'
                '<strategy mode="STEP"/>'
                '<datasource type="CLIENT"><record name="exp_c01"/>'
                '</datasource></field>'
                '<field units="s" type="NX_FLOAT" name="counter2">'
                '<strategy mode="STEP"/><datasource type="CLIENT">'
                '<record name="exp_c02"/></datasource></field>'
                '<field units="" type="NX_FLOAT" name="mca">'
                '<dimensions rank="1"><dim value="2048" index="1"/>'
                '</dimensions><strategy mode="STEP"/>'
                '<datasource type="CLIENT"><record name="p09/mca/exp.02"/>'
                '</datasource></field></group></group></group></definition>'
                ),

            'scan2': (
                '<definition><group type="NXentry" name="entry1">'
                '<group type="NXinstrument" name="instrument">'
                '<group type="NXdetector" name="detector">'
                '<field units="m" type="NX_FLOAT" name="counter1">'
                '<strategy mode="STEP"/>'
                '<datasource name="c01" type="CLIENT">'
                '<record name="exp_c01"/></datasource></field>'
                '<field units="s" type="NX_FLOAT" name="counter2">'
                '<strategy mode="STEP"/>'
                '<datasource type="CLIENT" name="c02">'
                '<record name="exp_c02"/></datasource></field>'
                '<field units="" type="NX_FLOAT" name="mca">'
                '<dimensions rank="1"><dim value="2048" index="1"/>'
                '</dimensions><strategy mode="STEP"/>'
                '<datasource type="CLIENT"  name="mca">'
                '<record name="p09/mca/exp.02"/>'
                '</datasource></field></group></group></group></definition>'
                ),
            'scan3': (
                '<definition><group type="NXentry" name="entry1">'
                '<group type="NXinstrument" name="instrument">'
                '<group type="NXdetector" name="detector">'
                '<field units="m" type="NX_FLOAT" name="counter1">'
                '<strategy mode="STEP"/>'
                '<datasource name="c01" type="CLIENT">'
                '<record name="exp_c01"/></datasource></field>'
                '<field units="s" type="NX_FLOAT" name="counter2">'
                '<strategy mode="INIT"/>'
                '<datasource type="CLIENT" name="c01">'
                '<record name="exp_c01"/></datasource></field>'
                '<field units="" type="NX_FLOAT" name="mca">'
                '<dimensions rank="1"><dim value="2048" index="1"/>'
                '</dimensions><strategy mode="STEP"/>'
                '<datasource type="CLIENT"  name="mca">'
                '<record name="p09/mca/exp.02"/>'
                '</datasource></field></group></group></group></definition>'
                ),

            }

        self.smycps = {
            'smycp': (
                '<definition><group type="NXcollection" name="dddd">'
                '<field name="long">'
                '$datasources.scalar_long<strategy mode="STEP"/></field>'
                '<field name="short">'
                '$datasources.scalar_short<strategy mode="STEP"/></field>'
                '</group></definition>'),
            'smycp2': (
                '<definition><group type="NXcollection" name="dddd">'
                '<field name="long">'
                '$datasources.spectrum_long<strategy mode="INIT"/></field>'
                '<field name="short">'
                '$datasources.spectrum_short<strategy mode="STEP"/></field>'
                '</group></definition>'),
            'smycp3': (
                '<definition><group type="NXcollection" name="dddd">'
                '<field name="long">'
                '$datasources.image_long<strategy mode="FINAL"/></field>'
                '<field name="short">'
                '$datasources.image_short<strategy mode="STEP"/></field>'
                '</group></definition>'),
            'smycpnt1': (
                '<definition><group type="NXcollection" name="ddddnt">'
                '<field name="long">'
                '$datasources.client_long<strategy mode="FINAL"/></field>'
                '<field name="short">'
                '$datasources.client_short<strategy mode="STEP"/></field>'
                '</group></definition>'),
            }

        self.smycps2 = {
            's2mycp': (
                '<definition><group type="NXcollection" name="dddd2">'
                '<field name="long">'
                '$datasources.scalar2_long<strategy mode="STEP"/></field>'
                '<field name="short">'
                '$datasources.scalar2_short<strategy mode="STEP"/></field>'
                '</group></definition>'),
            's2mycp2': (
                '<definition><group type="NXcollection" name="dddd2">'
                '<field name="long">'
                '$datasources.spectrum2_long<strategy mode="STEP"/></field>'
                '<field name="short">'
                '$datasources.spectrum2_short<strategy mode="FINAL"/></field>'
                '</group></definition>'),
            's2mycp3': (
                '<definition><group type="NXcollection" name="dddd2">'
                '<field name="long">'
                '$datasources.image2_long<strategy mode="STEP"/></field>'
                '<field name="short">'
                '$datasources.image2_short<strategy mode="INIT"/></field>'
                '</group></definition>'),
            's2mycpnt1': (
                '<definition><group type="NXcollection" name="dddd2nt">'
                '<field name="long">'
                '$datasources.client2_long<strategy mode="FINAL"/></field>'
                '<field name="short">'
                '$datasources.client2_short<strategy mode="STEP"/></field>'
                '</group></definition>'),
            }

        self.smydss = {
            'scalar_long': (
                '<definition><datasource type="TANGO" name="scalar_long">'
                '<record name="ScalarLong"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_bool': (
                '<definition><datasource type="TANGO" name="scalar_bool">'
                '<record name="ScalarBoolean"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_short': (
                '<definition><datasource type="TANGO" name="scalar_short">'
                '<record name="ScalarShort"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_ushort': (
                '<definition><datasource type="TANGO" name="scalar_ushort">'
                '<record name="ScalarUShort"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_ulong': (
                '<definition><datasource type="TANGO" name="scalar_ulong">'
                '<record name="ScalarULong"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_long64': (
                '<definition><datasource type="TANGO" name="scalar_long64">'
                '<record name="ScalarLong64"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_ulong64': (
                '<definition><datasource type="TANGO" name="scalar_ulong64">'
                '<record name="ScalarULong64"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_float': (
                '<definition><datasource type="TANGO" name="scalar_float">'
                '<record name="ScalarFloat"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_double': (
                '<definition><datasource type="TANGO" name="scalar_double">'
                '<record name="ScalarDouble"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_string': (
                '<definition><datasource type="TANGO" name="scalar_string">'
                '<record name="ScalarString"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_Encoded': (
                '<definition><datasource type="TANGO" name="scalar_encoded">'
                '<record name="ScalarEncoded"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'scalar_uchar': (
                '<definition><datasource type="TANGO" name="scalar_uchar">'
                '<record name="ScalarUChar"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_long': (
                '<definition><datasource type="TANGO" name="spectrum_long">'
                '<record name="SpectrumLong"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_bool': (
                '<definition><datasource type="TANGO" name="spectrum_bool">'
                '<record name="SpectrumBoolean"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_short': (
                '<definition><datasource type="TANGO" name="spectrum_short">'
                '<record name="SpectrumShort"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_ushort': (
                '<definition><datasource type="TANGO" name="spectrum_ushort">'
                '<record name="SpectrumUShort"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_ulong': (
                '<definition><datasource type="TANGO" name="spectrum_ulong">'
                '<record name="SpectrumULong"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_long64': (
                '<definition><datasource type="TANGO" name="spectrum_long64">'
                '<record name="SpectrumLong64"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_ulong64': (
                '<definition><datasource type="TANGO" name="spectrum_ulong64">'
                '<record name="SpectrumULong64"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_float': (
                '<definition><datasource type="TANGO" name="spectrum_float">'
                '<record name="SpectrumFloat"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_double': (
                '<definition><datasource type="TANGO" name="spectrum_double">'
                '<record name="SpectrumDouble"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_string': (
                '<definition><datasource type="TANGO" name="spectrum_string">'
                '<record name="SpectrumString"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_Encoded': (
                '<definition><datasource type="TANGO" name="spectrum_encoded">'
                '<record name="SpectrumEncoded"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'spectrum_uchar': (
                '<definition><datasource type="TANGO" name="spectrum_uchar">'
                '<record name="SpectrumUChar"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'image_long': (
                '<definition><datasource type="TANGO" name="image_long">'
                '<record name="ImageLong"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'image_bool': (
                '<definition><datasource type="TANGO" name="image_bool">'
                '<record name="ImageBoolean"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'image_short': (
                '<definition><datasource type="TANGO" name="image_short">'
                '<record name="ImageShort"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'image_ushort': (
                '<definition><datasource type="TANGO" name="image_ushort">'
                '<record name="ImageUShort"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'image_ulong': (
                '<definition><datasource type="TANGO" name="image_ulong">'
                '<record name="ImageULong"/>'
                '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                '</datasource></definition>'),
            'image_long64':
                ('<definition><datasource type="TANGO" name="image_long64">'
                 '<record name="ImageLong64"/>'
                 '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                 '</datasource></definition>'),
            'image_ulong64':
                ('<definition><datasource type="TANGO" name="image_ulong64">'
                 '<record name="ImageULong64"/>'
                 '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                 '</datasource></definition>'),
            'image_float':
                ('<definition><datasource type="TANGO" name="image_float">'
                 '<record name="ImageFloat"/>'
                 '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                 '</datasource></definition>'),
            'image_double':
                ('<definition><datasource type="TANGO" name="image_double">'
                 '<record name="ImageDouble"/>'
                 '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                 '</datasource></definition>'),
            'image_string':
                ('<definition><datasource type="TANGO" name="image_string">'
                 '<record name="ImageString"/>'
                 '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                 '</datasource></definition>'),
            'image_Encoded':
                ('<definition><datasource type="TANGO" name="image_encoded">'
                 '<record name="ImageEncoded"/>'
                 '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                 '</datasource></definition>'),
            'image_uchar':
                ('<definition><datasource type="TANGO" name="image_uchar">'
                 '<record name="ImageUChar"/>'
                 '<device member="attribute" name="ttestp09/testts/t1r228"/>'
                 '</datasource></definition>'),
            'client_long':
                ('<definition><datasource type="CLIENT" name="client_long">'
                 '<record name="ClientLong"/>'
                 '</datasource></definition>'),
            'client_short':
                ('<definition><datasource type="CLIENT" name="client_short">'
                 '<record name="ClientShort"/>'
                 '</datasource></definition>'),
            }

        self.smydss2 = {
            'scalar2_long':
                ('<definition><datasource type="TANGO" name="scalar2_long">'
                 '<record name="ScalarLong"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_bool':
                ('<definition><datasource type="TANGO" name="scalar2_bool">'
                 '<record name="ScalarBoolean"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_short':
                ('<definition><datasource type="TANGO" name="scalar2_short">'
                 '<record name="ScalarShort"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_ushort':
                ('<definition><datasource type="TANGO" name="scalar2_ushort">'
                 '<record name="ScalarUShort"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_ulong':
                ('<definition><datasource type="TANGO" name="scalar2_ulong">'
                 '<record name="ScalarULong"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_long64':
                ('<definition><datasource type="TANGO" name="scalar2_long64">'
                 '<record name="ScalarLong64"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_ulong64':
                ('<definition><datasource type="TANGO" name="scalar2_ulong64">'
                 '<record name="ScalarULong64"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_float':
                ('<definition><datasource type="TANGO" name="scalar2_float">'
                 '<record name="ScalarFloat"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_double':
                ('<definition><datasource type="TANGO" name="scalar2_double">'
                 '<record name="ScalarDouble"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_string':
                ('<definition><datasource type="TANGO" name="scalar2_string">'
                 '<record name="ScalarString"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_Encoded':
                ('<definition><datasource type="TANGO" name="scalar2_encoded">'
                 '<record name="ScalarEncoded"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'scalar2_uchar':
                ('<definition><datasource type="TANGO" name="scalar2_uchar">'
                 '<record name="ScalarUChar"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_long':
                ('<definition><datasource type="TANGO" name="spectrum2_long">'
                 '<record name="SpectrumLong"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_bool':
                ('<definition><datasource type="TANGO" name="spectrum2_bool">'
                 '<record name="SpectrumBoolean"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_short':
                ('<definition>'
                 '<datasource type="TANGO" name="spectrum2_short">'
                 '<record name="SpectrumShort"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_ushort':
                ('<definition>'
                 '<datasource type="TANGO" name="spectrum2_ushort">'
                 '<record name="SpectrumUShort"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_ulong':
                ('<definition>'
                 '<datasource type="TANGO" name="spectrum2_ulong">'
                 '<record name="SpectrumULong"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_long64':
                ('<definition>'
                 '<datasource type="TANGO" name="spectrum2_long64">'
                 '<record name="SpectrumLong64"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_ulong64':
                ('<definition>'
                 '<datasource type="TANGO" name="spectrum2_ulong64">'
                 '<record name="SpectrumULong64"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_float':
                ('<definition><datasource type="TANGO" name="spectrum2_float">'
                 '<record name="SpectrumFloat"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_double':
                ('<definition>'
                 '<datasource type="TANGO" name="spectrum2_double">'
                 '<record name="SpectrumDouble"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_string':
                ('<definition>'
                 '<datasource type="TANGO" name="spectrum2_string">'
                 '<record name="SpectrumString"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_Encoded':
                ('<definition>'
                 '<datasource type="TANGO" name="spectrum2_encoded">'
                 '<record name="SpectrumEncoded"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'spectrum2_uchar':
                ('<definition><datasource type="TANGO" name="spectrum2_uchar">'
                 '<record name="SpectrumUChar"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_long':
                ('<definition><datasource type="TANGO" name="image2_long">'
                 '<record name="ImageLong"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_bool':
                ('<definition><datasource type="TANGO" name="image2_bool">'
                 '<record name="ImageBoolean"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_short':
                ('<definition><datasource type="TANGO" name="image2_short">'
                 '<record name="ImageShort"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_ushort':
                ('<definition><datasource type="TANGO" name="image2_ushort">'
                 '<record name="ImageUShort"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_ulong':
                ('<definition><datasource type="TANGO" name="image2_ulong">'
                 '<record name="ImageULong"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_long64':
                ('<definition><datasource type="TANGO" name="image2_long64">'
                 '<record name="ImageLong64"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_ulong64':
                ('<definition><datasource type="TANGO" name="image2_ulong64">'
                 '<record name="ImageULong64"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_float':
                ('<definition><datasource type="TANGO" name="image2_float">'
                 '<record name="ImageFloat"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_double':
                ('<definition><datasource type="TANGO" name="image2_double">'
                 '<record name="ImageDouble"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_string':
                ('<definition><datasource type="TANGO" name="image2_string">'
                 '<record name="ImageString"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_Encoded':
                ('<definition><datasource type="TANGO" name="image2_encoded">'
                 '<record name="ImageEncoded"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'image2_uchar':
                ('<definition><datasource type="TANGO" name="image2_uchar">'
                 '<record name="ImageUChar"/>'
                 '<device member="attribute" name="ttestp09/testts/t2r228"/>'
                 '</datasource></definition>'),
            'client2_long':
                ('<definition><datasource type="CLIENT" name="client2_long">'
                 '<record name="Client2Long"/>'
                 '</datasource></definition>'),
            'client2_short':
                ('<definition><datasource type="CLIENT" name="client2_short">'
                 '<record name="Client2Short"/>'
                 '</datasource></definition>'),
            }

        self.mydss = {
            'nn':
            ('<?xml version=\'1.0\'?><definition><datasource type="TANGO">'
             '</datasource></definition>'),
            'nn2': ('<definition><datasource type="TANGO" name="">'
                    '</datasource></definition>'),
            'ann': ('<definition><datasource type="TANGO" name="ann">'
                    '</datasource></definition>'),
            'ann2': ('<definition><datasource type="CLIENT" name="ann2">'
                     '</datasource></definition>'),
            'ann3': ('<definition><datasource type="DB" name="ann3">'
                     '</datasource></definition>'),
            'ann4': ('<definition><datasource type="PYEVAL" name="ann4">'
                     '</datasource></definition>'),
            'ann5': ('<definition><datasource type="NEW" name="ann5">'
                     '</datasource></definition>'),
            'tann0': ('<definition><datasource type="TANGO" name="tann0">'
                     '<record name="myattr"/>'
                     '<device port="12345" encoding="sfd" hostname="sf" '
                     'member="attribute" name="dsff"/>'
                     '</datasource></definition>'),
            'tann1': ('<definition><datasource type="TANGO" name="tann1">'
                     '<record name="myattr2"/>'
                     '<device port="10000" encoding="sfd" hostname="sfa" '
                     'member="attribute" name="dsf"/>'
                     '</datasource></definition>'),
            'tann1b': ('<definition><datasource type="TANGO" name="tann1b">'
                     '<record name="myattr2"/>'
                     '<device member="attribute" name="dsf"/>'
                     '</datasource></definition>'),
            'tann1c': ('<definition><datasource type="TANGO" name="tann1c">'
                     '<record name="myattr2"/>'
                     '<device member="attribute" name="dsf/sd/we"/>'
                     '</datasource></definition>'),
            'P1M_postrun': (
                '<definition>'
                '<datasource type="PYEVAL" name="P1M_postrun">'
                '<result name="result">'
                'ds.result = "" + ds.P1M_fileDir + "/" + ds.P1M_filePrefix + '
                '"%03i" + ds.P1M_filePostfix + ":1:" + '
                ' str(ds.P1M_fileStartNum)</result>'
                ' $datasources.P1M_fileStartNum'
                ' $datasources.P1M_fileDir'
                ' $datasources.P1M_filePostfix'
                ' $datasources.P1M_filePrefix</datasource>'
                '</definition>'),
            'dbtest': (
                '<definition>'
                '<datasource type="DB" name="dbtest">'
                '<database dbtype="MYSQL"/>'
                '<query format="SPECTRUM">select name for device;</query>'
                '</datasource>'
                '</definition>'),
            'dbds': (
                '<definition>'
                '<datasource type="DB">'
                '<database dbtype="MYSQL">complicated DSN string</database>'
                '<query format="IMAGE">select * from device</query>'
                '<doc>test database datasource</doc>'
                '</datasource>'
                '</definition>'),
            'slt1vgap': (
                '<definition>'
                '<datasource type="CLIENT" name="slt1vgap">'
                '<record name="p02/slt/exp.07"/>'
                '</datasource>'
                '</definition>'
                ),
            }

    ## test starter
    # \brief Common set up
    def setUp(self):
        print "SEED =", self.__seed
#        self._wr.setUp()
#        self._ms.setUp()
        self._cf.setUp()
#        self._pool.setUp()
        self._simps.setUp()
        print "\nsetting up..."

    ## test closer
    # \brief Common tear down
    def tearDown(self):
        print "tearing down ..."
        self._simps.tearDown()
#        self._pool.tearDown()
        self._cf.tearDown()
#        self._ms.tearDown()
#        self._wr.tearDown()

    def getRandomName(self, maxsize):
        letters = string.lowercase + string.uppercase + string.digits
        size = self.__rnd.randint(1, maxsize)
        return ''.join(self.__rnd.choice(letters) for _ in range(size))

    ## Exception tester
    # \param exception expected exception
    # \param method called method
    # \param args list with method arguments
    # \param kwargs dictionary with method arguments
    def myAssertRaise(self, exception, method, *args, **kwargs):
        err = None
        try:
            error = False
            method(*args, **kwargs)
        except exception, e:
            error = True
            err = e
        self.assertEqual(error, True)
        return err

    def myAssertDict(self, dct, dct2):
        logger.debug('dict %s' % type(dct))
        logger.debug("\n%s\n%s" % (dct, dct2))
        self.assertTrue(isinstance(dct, dict))
        self.assertTrue(isinstance(dct2, dict))
        logger.debug("%s %s" % (len(dct.keys()), len(dct2.keys())))
        self.assertEqual(len(dct.keys()), len(dct2.keys()))
        for k, v in dct.items():
            logger.debug("%s  in %s" % (str(k), str(dct2.keys())))
            self.assertTrue(k in dct2.keys())
            if isinstance(v, dict):
                self.myAssertDict(v, dct2[k])
            else:
                logger.debug("%s , %s" % (str(v), str(dct2[k])))
                self.assertEqual(v, dct2[k])

    ## constructor test
    # \brief It tests default settings
    def ttest_create_remove(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)
        cps = {"empty":
                   '<?xml version="1.0" ?>\n<definition/>\n'}
        dname = "__dynamic_component__"
        dc = DynamicComponent(None)
        dc = DynamicComponent(self._cf.dp)

        cpname = dc.create()
        self.assertEqual(cpname, dname)
        self._cf.dp.Components([cpname])
        self.assertEqual(cps["empty"], self._cf.dp.Components([cpname])[0])

        cpname = dc.create()
        self.assertEqual(cpname, dname + "x")
        self._cf.dp.Components([cpname])
        self.assertEqual(cps["empty"], self._cf.dp.Components([cpname])[0])

        cpname = dc.create()
        self.assertEqual(cpname, dname + "xx")
        self._cf.dp.Components([cpname])
        self.assertEqual(cps["empty"], self._cf.dp.Components([cpname])[0])

        cpname = dc.create()
        self.assertEqual(cpname, dname + "xxx")
        self._cf.dp.Components([cpname])
        self.assertEqual(cps["empty"], self._cf.dp.Components([cpname])[0])

        dc.remove(dname + "xx")
        self.assertEqual(self._cf.dp.Components([dname + "xx"]), [])

        cpname = dc.create()
        self.assertEqual(cpname, dname + "xx")
        self._cf.dp.Components([cpname])
        self.assertEqual(cps["empty"], self._cf.dp.Components([cpname])[0])

        dc.remove(dname + "x")
        self.assertEqual(self._cf.dp.Components([dname + "x"]), [])

        dc.remove(dname + "xxx")
        self.assertEqual(self._cf.dp.Components([dname + "xxx"]), [])

        dc.remove(dname + "xx")
        self.assertEqual(self._cf.dp.Components([dname + "xx"]), [])

        dc.remove(dname + "xx")
        self.assertEqual(self._cf.dp.Components([dname + "xx"]), [])

        dc.remove(dname)
        self.assertEqual(self._cf.dp.Components([dname]), [])

        self.myAssertRaise(Exception, dc.remove, "sdfsdf")

    ## constructor test
    # \brief It tests default settings
    def ttest_create_dict(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)
        cps = {
            "empty":
                '<?xml version="1.0" ?>\n<definition/>\n',
            "one":
                '<?xml version="1.0" ?>\n<definition>\n'
            '<group name="entry$var.serialno" type="NXentry">\n'
            '<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="onename" type="NX_CHAR">\n<strategy mode="STEP"/>\n'
            '<datasource name="onename" type="CLIENT">\n'
            '<record name="onename"/>\n</datasource>\n</field>\n'
            '</group>\n</group>\n<group name="data" type="NXdata">\n'
            '<link name="onename" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/onename"/>\n'
            '</group>\n</group>\n</definition>\n',
            "two":
                '<?xml version="1.0" ?>\n<definition>\n'
            '<group name="entry$var.serialno" type="NXentry">\n'
            '<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="ds1" type="NX_CHAR">\n<strategy mode="STEP"/>\n'
            '<datasource name="ds1" type="CLIENT">\n<record name="ds1"/>\n'
            '</datasource>\n</field>\n</group>\n</group>\n'
            '<group name="data" type="NXdata">\n'
            '<link name="ds1" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/ds1"/>\n</group>\n</group>\n'
            '<group name="entry$var.serialno" type="NXentry">'
            '\n<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="ds2" type="NX_CHAR">\n<strategy mode="STEP"/>\n'
            '<datasource name="ds2" type="CLIENT">\n<record name="ds2"/>\n'
            '</datasource>\n</field>\n</group>\n</group>\n'
            '<group name="data" type="NXdata">\n'
            '<link name="ds2" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/ds2"/>\n</group>\n'
            '</group>\n</definition>\n',
            "three":
                '<?xml version="1.0" ?>\n<definition>\n'
            '<group name="entry$var.serialno" type="NXentry">\n'
            '<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="ds1" type="NX_CHAR">\n<strategy mode="STEP"/>\n'
            '<datasource name="ds1" type="CLIENT">\n<record name="ds1"/>\n'
            '</datasource>\n</field>\n</group>\n</group>\n'
            '<group name="data" type="NXdata">\n'
            '<link name="ds1" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/ds1"/>\n</group>\n</group>\n'
            '<group name="entry$var.serialno" type="NXentry">'
            '\n<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="ds2" type="NX_CHAR">\n<strategy mode="STEP"/>\n'
            '<datasource name="ds2" type="CLIENT">\n<record name="ds2"/>\n'
            '</datasource>\n</field>\n</group>\n</group>\n'
            '<group name="data" type="NXdata">\n'
            '<link name="ds2" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/ds2"/>\n</group>\n</group>\n'
            '<group name="entry$var.serialno" type="NXentry">'
            '\n<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="ds3" type="NX_CHAR">\n<strategy mode="STEP"/>\n'
            '<datasource name="ds3" type="CLIENT">\n<record name="ds3"/>\n'
            '</datasource>\n</field>\n</group>\n</group>\n'
            '<group name="data" type="NXdata">\n'
            '<link name="ds3" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/ds3"/>\n</group>\n</group>\n'
            '</definition>\n',
            "type":
                '<?xml version="1.0" ?>\n<definition>\n'
            '<group name="entry$var.serialno" type="NXentry">\n'
            '<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="ds1" type="NX_INT">\n<strategy mode="STEP"/>\n'
            '<datasource name="ds1" type="CLIENT">\n'
            '<record name="ds1"/>\n</datasource>\n</field>\n'
            '</group>\n</group>\n<group name="data" type="NXdata">\n'
            '<link name="ds1" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/ds1"/>\n'
            '</group>\n</group>\n</definition>\n',
            "shape":
                '<?xml version="1.0" ?>\n<definition>\n'
            '<group name="entry$var.serialno" type="NXentry">\n'
            '<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="ds2" type="NX_CHAR">\n<strategy mode="STEP"/>\n'
            '<datasource name="ds2" type="CLIENT">\n'
            '<record name="ds2"/>\n</datasource>\n'
            '<dimensions rank="1">\n<dim index="1" value="34"/>\n'
            '</dimensions>\n</field>\n'
            '</group>\n</group>\n<group name="data" type="NXdata">\n'
            '<link name="ds2" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/ds2"/>\n'
            '</group>\n</group>\n</definition>\n',
            "shapetype":
                '<?xml version="1.0" ?>\n<definition>\n'
            '<group name="entry$var.serialno" type="NXentry">\n'
            '<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="ds3" type="NX_FLOAT64">\n<strategy mode="STEP"/>\n'
            '<datasource name="ds3" type="CLIENT">\n'
            '<record name="ds3"/>\n</datasource>\n'
            '<dimensions rank="2">\n<dim index="1" value="3"/>\n'
            '<dim index="2" value="56"/>\n</dimensions>\n</field>\n'
            '</group>\n</group>\n<group name="data" type="NXdata">\n'
            '<link name="ds3" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/ds3"/>\n'
            '</group>\n</group>\n</definition>\n',
            }
        dsdict = {
            "empty": [],
            "one": [{"name": "onename"}],
            "two": [{"name": "ds1"}, {"name": "ds2"}],
            "three": [{"name": "ds1"}, {"name": "ds2"}, {"name": "ds3"}],
            "type": [{"name": "ds1", "dtype": "int"}],
            "shape": [{"name": "ds2", "shape": [34]}],
            "shapetype": [{"name": "ds3", "dtype": "float64",
                           "shape":[3, 56]}],
            }
        dname = "__dynamic_component__"
        dc = DynamicComponent(self._cf.dp)
        for lb, ds in dsdict.items():
            dc.setStepDictDSources(ds)
            cpname = dc.create()
            comp = self._cf.dp.Components([cpname])[0]
            self.assertEqual(cps[lb], comp)

    ## constructor test
    # \brief It tests default settings
    def ttest_create_dict_type(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)
        cps = {
            "type":
                '<?xml version="1.0" ?>\n<definition>\n'
            '<group name="entry$var.serialno" type="NXentry">\n'
            '<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="ds1" type="%s">\n<strategy mode="STEP"/>\n'
            '<datasource name="ds1" type="CLIENT">\n'
            '<record name="ds1"/>\n</datasource>\n</field>\n'
            '</group>\n</group>\n<group name="data" type="NXdata">\n'
            '<link name="ds1" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/ds1"/>\n'
            '</group>\n</group>\n</definition>\n',
            }
        dname = "__dynamic_component__"
        dc = DynamicComponent(self._cf.dp)
        for tp, nxstp in self.__npTn.items():
            dc.setStepDictDSources([{"name": "ds1", "dtype":tp}])
            cpname = dc.create()
            comp = self._cf.dp.Components([cpname])[0]
            self.assertEqual(cps["type"] % nxstp, comp)

    ## constructor test
    # \brief It tests default settings
    def ttest_create_dict_shape(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)
        cps = {
            "shape":
                '<?xml version="1.0" ?>\n<definition>\n'
            '<group name="entry$var.serialno" type="NXentry">\n'
            '<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="ds2" type="NX_CHAR">\n<strategy mode="STEP"/>\n'
            '<datasource name="ds2" type="CLIENT">\n'
            '<record name="ds2"/>\n</datasource>\n%s</field>\n'
            '</group>\n</group>\n<group name="data" type="NXdata">\n'
            '<link name="ds2" target="/entry$var.serialno:'
            'NXentry/NXinstrument/collection/ds2"/>\n'
            '</group>\n</group>\n</definition>\n',
            }

        dimbg = '<dimensions rank="%s">\n'
        dim = '<dim index="%s" value="%s"/>\n'
        dimend = '</dimensions>\n'

        dname = "__dynamic_component__"
        dc = DynamicComponent(self._cf.dp)
        for i in range(50):
            ms = [self.__rnd.randint(0, 3000)
                  for _ in range(self.__rnd.randint(0, 3))]
            dc.setStepDictDSources([{"name": "ds2", "shape":ms}])
            cpname = dc.create()
            mstr = ""
            if ms:
                mstr += dimbg % len(ms)
                for ind, val in enumerate(ms):
                    mstr += dim % (ind + 1, val)
                mstr += dimend

            comp = self._cf.dp.Components([cpname])[0]
            self.assertEqual(cps["shape"] % mstr, comp)

    ## constructor test
    # \brief It tests default settings
    def ttest_create_dict_shapetype(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)
        cps = {
            "shapetype":
                '<?xml version="1.0" ?>\n<definition>\n'
            '<group name="entry$var.serialno" type="NXentry">\n'
            '<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n'
            '<field name="%s" type="%s">\n<strategy mode="STEP"/>\n'
            '<datasource name="%s" type="CLIENT">\n'
            '<record name="%s"/>\n</datasource>\n'
            '%s</field>\n'
            '</group>\n</group>\n%s</group>\n</definition>\n',
            }

        link = '<group name="data" type="NXdata">\n' + \
            '<link name="%s" target="/entry$var.serialno:' + \
            'NXentry/NXinstrument/collection/%s"/>\n</group>\n'

        dimbg = '<dimensions rank="%s">\n'
        dim = '<dim index="%s" value="%s"/>\n'
        dimend = '</dimensions>\n'
        
        dname = "__dynamic_component__"

        arr = [
            {"name":"client", "full_name":"client"},
            {"name":"client_short", "full_name":"ttestp09/testts/t1r228"},
            {"name":"client_long", "full_name":"ttestp09/testts/t2r228"},
            {"name":"myclient_long", "full_name":"ttestp09/testts/t3r228"},
            {"name":"client", "full_name":"client"},
            {"name":"client_short", "full_name":"ttestp09/testts/t1r228"},
            {"name":"client_long", "full_name":"ttestp09/testts/t2r228"},
            {"name":"myclient_long", "full_name":"ttestp09/testts/t3r228"},
            {"name":"client", "full_name":"client"},
            {"name":"client_short", "full_name":"ttestp09/testts/t1r228"},
            {"name":"client_long", "full_name":"ttestp09/testts/t2r228"},
            {"name":"myclient_long", "full_name":"ttestp09/testts/t3r228"},
            ]

        simps2 = TestServerSetUp.TestServerSetUp(
            "ttestp09/testts/t2r228", "S2")
        simps3 = TestServerSetUp.TestServerSetUp(
            "ttestp09/testts/t3r228", "S3")

        db = PyTango.Database()
        try:
            simps2.setUp()
            simps3.setUp()

            dc = DynamicComponent(self._cf.dp)
            for i, ar in enumerate(arr):
                if '/' in ar["full_name"]:
                    db.put_device_alias(ar["full_name"], ar["name"])
#                print "I = ", i
                for tp, nxstp in self.__npTn.items():
                    lbl = self.getRandomName(20)
                    dc = DynamicComponent(self._cf.dp)
#                    print "TP = ", tp
                    ms = [self.__rnd.randint(0, 3000)
                          for _ in range(self.__rnd.randint(0, 3))]
                    ms2 = [self.__rnd.randint(0, 3000)
                          for _ in range(self.__rnd.randint(0, 3))]
                    tmptp = self.__rnd.choice(self.__npTn.keys())
                    if i == 0:
                        pass
                        dc.setDefaultLinkPath(False, self.__defaultpath)
                    elif i == 1:
                        dc.setDefaultLinkPath(True, self.__defaultpath)
                    elif i == 2:
                        dc.setLabelParams("{}", "{}",
                                          json.dumps({ar["name"]: False}),
                                          "{}", "{}")
                    elif i == 3:
                        dc.setLabelParams("{}", "{}",
                                          json.dumps({ar["name"]: True}),
                                          "{}", "{}")
                    elif i == 4:
                        dc.setDefaultLinkPath(True, self.__defaultpath)
                        dc.setLabelParams("{}", "{}",
                                          json.dumps({ar["name"]: False}),
                                          "{}", "{}")
                    elif i == 5:
                        dc.setDefaultLinkPath(False, self.__defaultpath)
                        dc.setLabelParams("{}", "{}",
                                          json.dumps({ar["name"]: True}),
                                          "{}", "{}")
                    elif i == 6:
                        dc.setDefaultLinkPath(False, self.__defaultpath)
                        dc.setLabelParams("{}", "{}",
                                          json.dumps({ar["full_name"]: True}),
                                          "{}",
                                          json.dumps({ar["name"]: ms2}))
                    elif i == 7:
                        dc.setLabelParams("{}", "{}", "{}",
                                          json.dumps({ar["name"]: tmptp}),
                                          "{}")
                    elif i == 8:
                        dc.setDefaultLinkPath(True, self.__defaultpath)
                        dc.setLabelParams(json.dumps({ar["name"]: lbl}),
                                          "{}",
                                          json.dumps({lbl: False}),
                                          "{}", "{}")
                    elif i == 9:
                        dc.setDefaultLinkPath(False, self.__defaultpath)
                        dc.setLabelParams(json.dumps({ar["name"]: lbl}),
                                          "{}",
                                          json.dumps({lbl: True}),
                                          "{}", "{}")
                    elif i == 10:
                        dc.setDefaultLinkPath(False, self.__defaultpath)
                        dc.setLabelParams(json.dumps({ar["name"]: lbl}), 
                                          "{}",
                                          json.dumps({ar["full_name"]: True}),
                                          "{}",
                                          json.dumps({lbl: ms2}))
                    elif i == 11:
                        dc.setLabelParams(json.dumps({ar["name"]: lbl}),
                                          "{}", "{}",
                                          json.dumps({lbl: tmptp}),
                                          "{}")
                    dc.setStepDictDSources([{"name": ar["full_name"],
                                             "shape": ms,
                                             "dtype": tp}])
                    cpname = dc.create()
                    mstr = ""
                    if ms:
                        mstr += dimbg % len(ms)
                        for ind, val in enumerate(ms):
                            mstr += dim % (ind + 1, val)
                        mstr += dimend

                    comp = self._cf.dp.Components([cpname])[0]
                    ds = ar["name"]
                    lk = link % (ds, ds)
                    self.assertEqual(cps["shapetype"] % (
                            ds,
                            nxstp, ds, ar["full_name"], mstr,
                            lk if i % 2 else ""),
                                     comp)
        finally:
            for ar in arr:
                if '/' in ar["full_name"]:
                    db.delete_device_alias(ar["name"])

            simps3.tearDown()
            simps2.tearDown()


    ## constructor test
    # \brief It tests default settings
    def test_create_dict_fieldpath(self):
        fun = sys._getframe().f_code.co_name
        print "Run: %s.%s() " % (self.__class__.__name__, fun)
        cps = {
            "shapetype":
                '<?xml version="1.0" ?>\n<definition>\n'
            '<group name="entry$var.serialno" type="NXentry">\n'
            '<group name="instrument" type="NXinstrument">\n'
            '<group name="collection" type="NXcollection">\n%s'
            '</group>\n</group>\n%s</group>\n</definition>\n',
            }
        
        defbg = '<?xml version="1.0" ?>\n<definition>\n'
        defend = '</definition>\n'
        groupbg = '<group name="%s" type="%s">\n'
        groupend = '</group>\n'

        field = '<field name="%s" type="%s">\n<strategy mode="STEP"/>\n' + \
            '<datasource name="%s" type="CLIENT">\n' + \
            '<record name="%s"/>\n</datasource>\n%s</field>\n'


        link = '<group name="data" type="NXdata">\n' + \
            '<link name="%s" target="%s/%s"/>\n</group>\n'

        dimbg = '<dimensions rank="%s">\n'
        dim = '<dim index="%s" value="%s"/>\n'
        dimend = '</dimensions>\n'
        
        dname = "__dynamic_component__"

        arr = [
            {"name":"client", "full_name":"client"},
            {"name":"client_short", "full_name":"ttestp09/testts/t1r228"},
            {"name":"client_long", "full_name":"ttestp09/testts/t2r228"},
            {"name":"myclient_long", "full_name":"ttestp09/testts/t3r228"},
            ]

        simps2 = TestServerSetUp.TestServerSetUp(
            "ttestp09/testts/t2r228", "S2")
        simps3 = TestServerSetUp.TestServerSetUp(
            "ttestp09/testts/t3r228", "S3")

        db = PyTango.Database()
        try:
            simps2.setUp()
            simps3.setUp()

            for i, ar in enumerate(arr):
                if '/' in ar["full_name"]:
                    db.put_device_alias(ar["full_name"], ar["name"])
                print "I = ", i
                for tp, nxstp in self.__npTn.items():
                    dc = DynamicComponent(self._cf.dp)
                    
                    lbl = self.getRandomName(20)
                    fieldname = self.getRandomName(20)
                    print "FIELD", fieldname
                    path = [
                        (self.getRandomName(20)
                         if self.__rnd.randint(0, 1) else None,
                         ("NX" + self.getRandomName(20))
                         if self.__rnd.randint(0, 1) else None)
                        for _ in range(self.__rnd.randint(0, 10))]
                    print "path0", path, len(path)
                    path = [nd for nd in path if nd != (None, None)]
                    print "path1", path, len(path)
                    mypath = ""
                    for node in path:
                        mypath += "/"
                        if node[0]:
                            mypath += node[0]
                            if node[1]:
                                mypath += ":"
                        if node[1]:
                            mypath += node[1]
#                    mypath += fieldname
                    print "path2", path, len(path)
                    print "PATH", path, mypath
                    print "TP = ", tp
                    ms = [self.__rnd.randint(0, 3000)
                          for _ in range(self.__rnd.randint(0, 3))]
                    ms2 = [self.__rnd.randint(0, 3000)
                          for _ in range(self.__rnd.randint(0, 3))]
                    tmptp = self.__rnd.choice(self.__npTn.keys())
                    if i == 0:
                        dc.setDefaultLinkPath(False, mypath)
                    elif i == 1:
                        dc.setDefaultLinkPath(True, mypath)
                    elif i == 2:
                        dc.setLabelParams("{}", 
                                          json.dumps({ar["name"]: 
                                                      mypath + "/" + fieldname}),
                                          json.dumps({ar["name"]: False}),
                                          "{}", "{}")
                    elif i == 3:
                        dc.setLabelParams("{}",
                                          json.dumps({ar["name"]:
                                                          mypath + "/" + fieldname}),
                                          json.dumps({ar["name"]: True}),
                                          "{}", "{}")
                    dc.setStepDictDSources([{"name": ar["full_name"],
                                             "shape": ms,
                                             "dtype": tp}])
                    cpname = dc.create()
                    mstr = ""
                    if ms:
                        mstr += dimbg % len(ms)
                        for ind, val in enumerate(ms):
                            mstr += dim % (ind + 1, val)
                        mstr += dimend

                    comp = self._cf.dp.Components([cpname])[0]
                    ds = ar["name"]
                    lk = link % (ds, mypath, ds)
                    if i < 2:
                        fd = field % (ds, nxstp, ds, ar["full_name"], mstr)
                    else:
                        fname = fieldname.lower()
                        fd = field % (fieldname.lower(), nxstp, ds, ar["full_name"], mstr)

                    print "path3", path, len(path), bool(path)
                    if path:

                        print "path", bool(path)
                        if i < 2:
                            lk = link % (ds, mypath, ds)
                        else:
                            lk = link % (fieldname.lower(), mypath, fieldname.lower())
                        mycps = defbg
                        for nm, gtp in path:
                            if not nm:
                                nm = gtp[2:] 
                            if not gtp:
                                gtp = 'NX' + nm
                            mycps += groupbg % (nm, gtp)
                        mycps += fd

                        for j in range(len(path) - 1):
                            mycps += groupend
                        mycps += lk if i % 2 else ""
                        mycps += groupend
                        mycps += defend

                        mycps2 = defbg
                        for k, (nm, gtp) in enumerate(path):
                            if not nm:
                                nm = gtp[2:] 
                            if not gtp:
                                gtp = 'NX' + nm
                            mycps2 += groupbg % (nm, gtp)
                            if not k:
                                mycps2 += lk if i % 2 else ""
                        mycps2 += fd

                        for _ in path:
                            mycps2 += groupend
                        mycps2 += defend
                        print "FIRST"
                    else:
                        if i < 2:
                            lk = link % (ds,  self.__defaultpath, ds)
                        else:
                            lk = link % (fieldname.lower(),  self.__defaultpath, fieldname.lower())
                        mycps = cps["shapetype"] % (
                            fd,
                            lk if i % 2 else "")
                        mycps = mycps2
                        print "SECOND"
                    try:
                        self.assertEqual(comp, mycps)
                    except:    
                        self.assertEqual(comp, mycps2)
        finally:
            for ar in arr:
                if '/' in ar["full_name"]:
                    db.delete_device_alias(ar["name"])

            simps3.tearDown()
            simps2.tearDown()

if __name__ == '__main__':
    unittest.main()
