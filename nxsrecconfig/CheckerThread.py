#!/usr/bin/env python
#   This file is part of nxsrecconfig - NeXus Sardana Recorder Settings
#
#    Copyright (C) 2014-2017 DESY, Jan Kotanski <jkotan@mail.desy.de>
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
#

"""  Component CheckerThread - thread which checks tango server attributes"""

import Queue
import PyTango
import threading


#: (:obj:`list` < :obj:`str`>) default attributes to check
ATTRIBUTESTOCHECK = ["Value", "Position", "Counts", "Data",
                     "Voltage", "Energy", "SampleTime"]


class TangoDSItem(object):

    """ Tango DataSource item
    """
    __slots__ = 'name', 'device', 'attr'

    def __init__(self, name=None, device=None, attr=None):
        """ constructor

        :param name: datasource name
        :type name: :obj:`str`
        :param device: datasource device
        :type device: :obj:`str`
        :param attr: device attribute
        :type attr: :obj:`str`
        """
        #: (:obj:`str`) datasource name
        self.name = str(name) if name is not None else None
        #: (:obj:`str`) datasource device
        self.device = str(device) if device is not None else None
        #: (:obj:`str`) datasource device attribute
        self.attr = str(attr) if attr is not None else None


class CheckerItem(list):

    """ Checker list Item
    """

    def __init__(self, name):
        """ constructor

        :param name: checker item name
        :type name: :obj:`str`
        """
        super(CheckerItem, self).__init__()
        #: (:obj:`str`) checker name
        self.name = name
        #: (:obj:`str`) datasource with first error
        self.errords = None
        #: (:obj:`str`) first error message
        self.message = None
        #: (:obj:`bool`) enabled flag
        self.active = True


class CheckerThread(threading.Thread):

    """ Single CheckerThread
    """

    def __init__(self, index, queue):
        """ constructor

        :brief: It creates ElementThread from the runnable element
        :param index: the current thread index
        :type index: :obj:`int`
        :param queue: queue with tasks
        :type queue: :class:`Queue.Queue`
        """
        threading.Thread.__init__(self)
        #: (:obj:`int`) thread index
        self.index = index
        #: (:class:`Queue.Queue`) queue with runnable elements
        self.__queue = queue

    def run(self):
        """ runner

        :brief: It runs the defined thread
        """
        full = True
        while full:
            try:
                elem = self.__queue.get(block=False)
                self.__check(elem)

            except Queue.Empty:
                full = False

    @classmethod
    def __check(cls, checkeritem):
        """ checks oen device list item which usually corresponds
        to one components

        :param checkeritem: device list item
        :type checkeritem: :obj:`list` <:class:`CheckerItem`>
        """
        for ds in checkeritem:
            try:
                dp = PyTango.DeviceProxy(ds.device or ds.name)
                state = dp.command_inout("State")
                if state in [PyTango.DevState.FAULT]:
                    raise FaultStateError("FAULT STATE")
                dp.ping()
                if not ds.attr:
                    for gattr in ATTRIBUTESTOCHECK:
                        if hasattr(dp, gattr):
                            _ = getattr(dp, gattr)
                elif ds.attr.startswith("@"):
                    pass
                elif ds.attr.endswith("()"):
                    _ = getattr(dp, ds.attr[:-2])
                else:
                    _ = getattr(dp, ds.attr)
                if state in [PyTango.DevState.ALARM]:
                    raise AlarmStateError("ALARM STATE")
            except AlarmStateError as e:
                checkeritem.message = "ALARM_STATE"
                checkeritem.errords = ds.name
            except Exception as e:
                checkeritem.message = str(e)
                checkeritem.errords = ds.name
                checkeritem.active = False
                break


class AlarmStateError(Exception):

    """ Alarm State Exception class
    """


class FaultStateError(Exception):

    """ Fault State Exception class
    """
