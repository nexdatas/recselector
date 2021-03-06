#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2017 DESY, Jan Kotanski <jkotan@mail.desy.de>
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
# \package test nexdatas
# \file Converter1to2Test.py
# unittests for field Tags running Tango Server
#
import unittest
import os
import sys
import random
import struct
import binascii
import string
import json
import time

from nxsrecconfig.Converter import Converter1to2, ConverterXtoY

# if 64-bit machione
IS64BIT = (struct.calcsize("P") == 8)

if sys.version_info > (3,):
    long = int


# test fixture
class Converter1to2Test(unittest.TestCase):

    # constructor
    # \param methodName name of the test method

    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)
        try:
            self.__seed = long(binascii.hexlify(os.urandom(16)), 16)
        except NotImplementedError:
            self.__seed = long(time.time() * 256)

        self.__rnd = random.Random(self.__seed)

    # Exception tester
    # \param exception expected exception
    # \param method called method
    # \param args list with method arguments
    # \param kwargs dictionary with method arguments
    def myAssertRaise(self, exception, method, *args, **kwargs):
        err = None
        try:
            error = False
            method(*args, **kwargs)
        except exception as e:
            error = True
            err = e
        self.assertEqual(error, True)
        return err

    def myAssertDict(self, dct, dct2):
        self.assertTrue(isinstance(dct, dict))
        # if not isinstance(dct2, dict):
        #     print "NOT DICT", type(dct2), dct2
        #     print "DICT", type(dct), dct
        self.assertTrue(isinstance(dct2, dict))
        # if set(dct.keys()) ^ set(dct2.keys()):
        #     print 'DCT', dct.keys()
        #     print 'DCT2', dct2.keys()
        #     print "DIFF", set(dct.keys()) ^ set(dct2.keys())
        self.assertEqual(len(list(dct.keys())), len(list(dct2.keys())))
        for k, v in dct.items():
            self.assertTrue(k in dct2.keys())
            if isinstance(v, dict):
                self.myAssertDict(v, dct2[k])
            else:
                # if v != dct2[k]:
                #     print 'VALUES', k, v, dct2[k]
                self.assertEqual(v, dct2[k])

    def myAssertJSONDict(self, dct, dct2):
        self.assertTrue(isinstance(dct, dict))
        # if not isinstance(dct2, dict):
        #     print "NOT DICT", type(dct2), dct2
        #     print "DICT", type(dct), dct
        self.assertTrue(isinstance(dct2, dict))
        # if set(dct.keys()) ^ set(dct2.keys()):
        #     print 'DCT', dct.keys()
        #     print 'DCT2', dct2.keys()
        #     print "DIFF", set(dct.keys()) ^ set(dct2.keys())
        self.assertEqual(len(list(dct.keys())), len(list(dct2.keys())))
        for k, v in dct.items():
            self.assertTrue(k in dct2.keys())
            if isinstance(v, dict):
                self.myAssertDict(v, dct2[k])
            else:
                try:
                    vv = json.loads(v)
                    dc = json.loads(dct2[k])
                    if isinstance(vv, dict):
                        self.myAssertDict(vv, dc)
                except Exception:
                    # if v != dct2[k]:
                    #     print 'VALUES', k, v, dct2[k]
                    self.assertEqual(v, dct2[k])

    def getRandomString(self, maxsize):
        letters = [chr(i) for i in range(256)]
        size = self.__rnd.randint(1, maxsize)
        return ''.join(self.__rnd.choice(letters) for _ in range(size))

    def getRandomName(self, maxsize):
        if sys.version_info > (3,):
            letters = string.ascii_letters + string.digits
        else:
            letters = string.letters + string.digits
        size = self.__rnd.randint(1, maxsize)
        return ''.join(self.__rnd.choice(letters) for _ in range(size))

    # test starter
    # \brief Common set up
    def setUp(self):
        print("SEED = %s" % self.__seed)
        print("\nsetting up...")

    # test closer
    # \brief Common tear down
    def tearDown(self):
        print("tearing down ...")

    def test_constructor(self):
        fun = sys._getframe().f_code.co_name
        print("Run: %s.%s() " % (self.__class__.__name__, fun))

        # mysel = {}
        cv = Converter1to2()
        self.assertTrue(isinstance(cv, ConverterXtoY))
        self.myAssertDict(cv.names, {
            "AutomaticComponentGroup": "ComponentPreselection",
            "AutomaticDataSources": "PreselectedDataSources",
            "ComponentGroup": "ComponentSelection",
            "DataSourceGroup": "DataSourceSelection",
            "DataRecord": "UserData",
            "HiddenElements": "UnplottedComponents",
            "DynamicLinks": "DefaultDynamicLinks",
            "DynamicPath": "DefaultDynamicPath"

        })
        self.myAssertDict(cv.pnames, {
            "Labels": "label",
            "LabelPaths": "nexus_path",
            "LabelLinks": "link",
            "LabelTypes": "data_type",
            "LabelShapes": "shape",
        })

    def test_convert(self):
        fun = sys._getframe().f_code.co_name
        print("Run: %s.%s() " % (self.__class__.__name__, fun))

        mysel = {}
        cv = Converter1to2()
        cv.names = {}
        cv.pnames = {}
        cv.convert(mysel)
        self.assertEqual(mysel, {'ChannelProperties': '{}'})

        for i in range(1000):
            mysel = {}
            tnames = dict(
                (self.getRandomName(20), self.getRandomName(20))
                for _ in range(self.__rnd.randint(1, 20)))
            for k in list(tnames.keys()):
                if k in list(tnames.values()):
                    tnames.pop(k)
            names = {}
            for k, vl in tnames.items():
                names[vl] = k
            cv.names = dict(names)
            keys1 = self.__rnd.sample(list(names.keys()), self.__rnd.randint(
                0, len(list(names.keys()))))
            keys2 = set([self.getRandomName(20) for _ in range(5)])
            keys2.update(keys1)
            for k in keys2:
                mysel[k] = self.getRandomName(20)
            for k in list(mysel.keys()):
                if k in names.values():
                    mysel.pop(k)
                    keys2.remove(k)
            osel = dict(mysel)
            cv.convert(mysel)
            res = {}
            for k, vl in osel.items():
                if k in names:
                    res[names[k]] = vl
                else:
                    res[k] = vl
            res['ChannelProperties'] = "{}"
            self.myAssertDict(mysel, res)

    def test_convert_names(self):
        fun = sys._getframe().f_code.co_name
        print("Run: %s.%s() " % (self.__class__.__name__, fun))

        mysel = {}
        cv = Converter1to2()
        cv.names = {}
        cv.pnames = {}
        cv.convert(mysel)
        self.assertEqual(mysel, {'ChannelProperties': '{}'})

        for i in range(1000):
            mysel = {}
            tnames = dict(
                (self.getRandomName(20), self.getRandomName(20))
                for _ in range(self.__rnd.randint(1, 20)))
            for k in list(tnames.keys()):
                if k in list(tnames.values()):
                    tnames.pop(k)
            names = {}
            for k, vl in tnames.items():
                names[vl] = k
            cv.names = dict(names)
            keys1 = self.__rnd.sample(list(names.keys()), self.__rnd.randint(
                0, len(list(names.keys()))))
            keys2 = set([self.getRandomName(20) for _ in range(5)])
            keys2.update(keys1)
            for k in keys2:
                mysel[k] = self.getRandomName(20)
            for k in list(mysel.keys()):
                if k in names.values():
                    mysel.pop(k)
                    keys2.remove(k)
            osel = dict(mysel)
            cv.convert(mysel)
            res = {}
            for k, vl in osel.items():
                if k in names:
                    res[names[k]] = vl
                else:
                    res[k] = vl
            res['ChannelProperties'] = "{}"
            self.myAssertDict(mysel, res)

    def test_convert_names_pnames(self):
        fun = sys._getframe().f_code.co_name
        print("Run: %s.%s() " % (self.__class__.__name__, fun))

        mysel = {}
        cv = Converter1to2()
        pnames = dict(cv.pnames)
        names = dict(cv.names)
        cv.convert(mysel)
        self.assertEqual(mysel, {'ChannelProperties': '{}'})

        for i in range(200):
            mysel = {}
            keys0 = self.__rnd.sample(list(pnames.keys()), self.__rnd.randint(
                0, len(list(pnames.keys()))))
            keys1 = self.__rnd.sample(list(names.keys()), self.__rnd.randint(
                0, len(list(names.keys()))))
            keys2 = set([self.getRandomName(20) for _ in range(2)])
            for k in keys2:
                if k in pnames.keys() or k in names.keys() or \
                   k in pnames.values() or k in names.values():
                    keys2.remove(k)
            keys2.update(keys0)
            keys2.update(keys1)
            for k in keys2:
                if k in pnames:
                    mysel[k] = json.dumps(dict(
                        (self.getRandomName(20), self.getRandomName(20))
                        for _ in range(self.__rnd.randint(1, 20))))
                else:
                    mysel[k] = self.getRandomName(20)
            osel = dict(mysel)
            cv.convert(mysel)
            res = {}
            prop = {}
            for k, vl in osel.items():
                if k in pnames:
                    prop[pnames[k]] = json.loads(vl)
                elif k in names:
                    res[names[k]] = vl
                else:
                    res[k] = vl
            res['ChannelProperties'] = json.dumps(prop)
            self.maxDiff = None
            self.myAssertJSONDict(mysel, res)


if __name__ == '__main__':
    unittest.main()
