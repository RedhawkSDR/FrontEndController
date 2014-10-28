#!/usr/bin/env python
#
# This file is protected by Copyright. Please refer to the COPYRIGHT file
# distributed with this source distribution.
#
# This file is part of REDHAWK FrontEndController.
#
# REDHAWK FrontEndController is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# REDHAWK FrontEndController is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#
#
# AUTO-GENERATED CODE.  DO NOT MODIFY!
#
# Source: FrontEndController.spd.xml
from ossie.cf import CF
from ossie.cf import CF__POA
from ossie.utils import uuid

from ossie.resource import Resource
from ossie.threadedcomponent import *
from ossie.properties import simple_property
from ossie.properties import struct_property

import Queue, copy, time, threading
from ossie.resource import usesport, providesport
from ossie.cf import ExtendedCF
from ossie.cf import ExtendedCF__POA

class FrontEndController_base(CF__POA.Resource, Resource, ThreadedComponent):
        # These values can be altered in the __init__ of your derived class

        PAUSE = 0.0125 # The amount of time to sleep if process return NOOP
        TIMEOUT = 5.0 # The amount of time to wait for the process thread to die when stop() is called
        DEFAULT_QUEUE_SIZE = 100 # The number of BulkIO packets that can be in the queue before pushPacket will block

        def __init__(self, identifier, execparams):
            loggerName = (execparams['NAME_BINDING'].replace('/', '.')).rsplit("_", 1)[0]
            Resource.__init__(self, identifier, execparams, loggerName=loggerName)
            ThreadedComponent.__init__(self)

            # self.auto_start is deprecated and is only kept for API compatibility
            # with 1.7.X and 1.8.0 components.  This variable may be removed
            # in future releases
            self.auto_start = False
            # Instantiate the default implementations for all ports on this component
            self.port_DomainManager_out = PortCFDomainManagerOut_i(self, "DomainManager_out")

        def start(self):
            Resource.start(self)
            ThreadedComponent.startThread(self, pause=self.PAUSE)

        def stop(self):
            if not ThreadedComponent.stopThread(self, self.TIMEOUT):
                raise CF.Resource.StopError(CF.CF_NOTSET, "Processing thread did not die")
            Resource.stop(self)

        def releaseObject(self):
            try:
                self.stop()
            except Exception:
                self._log.exception("Error stopping")
            Resource.releaseObject(self)

        ######################################################################
        # PORTS
        # 
        # DO NOT ADD NEW PORTS HERE.  You can add ports in your derived class, in the SCD xml file, 
        # or via the IDE.

        # 'CF/DomainManager' port
        class PortCFDomainManagerOut(ExtendedCF__POA.QueryablePort):
            """This class is a port template for the PortCFDomainManagerOut_i port and
            should not be instantiated nor modified.
            
            The expectation is that the specific port implementation will extend
            from this class instead of the base CORBA class ExtendedCF__POA.QueryablePort.
            """
            pass

        port_DomainManager_out = usesport(name="DomainManager_out",
                                          repid="IDL:CF/DomainManager:1.0",
                                          type_="control")

        ######################################################################
        # PROPERTIES
        # 
        # DO NOT ADD NEW PROPERTIES HERE.  You can add properties in your derived class, in the PRF xml file
        # or by using the IDE.
        allocationId = simple_property(id_="allocationId",
                                       name="allocationId",
                                       type_="string",
                                       defvalue="My_Allocation_Id",
                                       mode="readwrite",
                                       action="external",
                                       kinds=("configure",),
                                       description="""When performing an allocation on FEI Devices, a unique ID is used to represent the request.  In the case of multi-out devices this ID is also required to be used as the connection ID.""")
        
        tunerType = simple_property(id_="tunerType",
                                    name="tunerType",
                                    type_="string",
                                    mode="readwrite",
                                    action="external",
                                    kinds=("configure",),
                                    description="""Used when performing the tuner allocation request.  Valid values are taken from the FEI Specification: TX, RX, CHANNELIZER, DDC, RX_DIGITIZER, RX_DIGTIZIER_CHANNELIZER""")
        
        class FEIDevice(object):
            deviceName = simple_property(id_="deviceName",
                                         name="deviceName",
                                         type_="string")
        
            outputPortName = simple_property(id_="outputPortName",
                                             name="outputPortName",
                                             type_="string")
        
            tunerPortName = simple_property(id_="tunerPortName",
                                            name="tunerPortName",
                                            type_="string",
                                            defvalue="DigitalTuner_in")
        
            def __init__(self, **kw):
                """Construct an initialized instance of this struct definition"""
                for attrname, classattr in type(self).__dict__.items():
                    if type(classattr) == simple_property:
                        classattr.initialize(self)
                for k,v in kw.items():
                    setattr(self,k,v)
        
            def __str__(self):
                """Return a string representation of this structure"""
                d = {}
                d["deviceName"] = self.deviceName
                d["outputPortName"] = self.outputPortName
                d["tunerPortName"] = self.tunerPortName
                return str(d)
        
            def getId(self):
                return "FEIDevice"
        
            def isStruct(self):
                return True
        
            def getMembers(self):
                return [("deviceName",self.deviceName),("outputPortName",self.outputPortName),("tunerPortName",self.tunerPortName)]
        
        FEIDevice = struct_property(id_="FEIDevice",
                                    name="FEIDevice",
                                    structdef=FEIDevice,
                                    configurationkind=("configure",),
                                    mode="readwrite",
                                    description="""Information about the FEI Device which will be controlled.  Device and port names are required.""")
        
        class InputComponent(object):
            componentName = simple_property(id_="componentName",
                                            name="componentName",
                                            type_="string")
        
            inputPortName = simple_property(id_="inputPortName",
                                            name="inputPortName",
                                            type_="string")
        
            def __init__(self, **kw):
                """Construct an initialized instance of this struct definition"""
                for attrname, classattr in type(self).__dict__.items():
                    if type(classattr) == simple_property:
                        classattr.initialize(self)
                for k,v in kw.items():
                    setattr(self,k,v)
        
            def __str__(self):
                """Return a string representation of this structure"""
                d = {}
                d["componentName"] = self.componentName
                d["inputPortName"] = self.inputPortName
                return str(d)
        
            def getId(self):
                return "InputComponent"
        
            def isStruct(self):
                return True
        
            def getMembers(self):
                return [("componentName",self.componentName),("inputPortName",self.inputPortName)]
        
        InputComponent = struct_property(id_="InputComponent",
                                         structdef=InputComponent,
                                         configurationkind=("configure",),
                                         mode="readwrite",
                                         description="""Information about the component which will be connected to the FEI Device.""")
        
        class TuneRequest(object):
            frequency = simple_property(id_="frequency",
                                        name="frequency",
                                        type_="float")
        
            sampleRate = simple_property(id_="sampleRate",
                                         name="sampleRate",
                                         type_="float")
        
            def __init__(self, **kw):
                """Construct an initialized instance of this struct definition"""
                for attrname, classattr in type(self).__dict__.items():
                    if type(classattr) == simple_property:
                        classattr.initialize(self)
                for k,v in kw.items():
                    setattr(self,k,v)
        
            def __str__(self):
                """Return a string representation of this structure"""
                d = {}
                d["frequency"] = self.frequency
                d["sampleRate"] = self.sampleRate
                return str(d)
        
            def getId(self):
                return "TuneRequest"
        
            def isStruct(self):
                return True
        
            def getMembers(self):
                return [("frequency",self.frequency),("sampleRate",self.sampleRate)]
        
        TuneRequest = struct_property(id_="TuneRequest",
                                      name="TuneRequest",
                                      structdef=TuneRequest,
                                      configurationkind=("configure",),
                                      mode="readwrite")
        

'''uses port(s)'''

class PortCFDomainManagerOut_i(FrontEndController_base.PortCFDomainManagerOut):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.outConnections = {}
        self.port_lock = threading.Lock()

    def connectPort(self, connection, connectionId):
        self.port_lock.acquire()
        try:
            port = connection._narrow(CF.DomainManager)
            self.outConnections[str(connectionId)] = port
        finally:
            self.port_lock.release()

    def disconnectPort(self, connectionId):
        self.port_lock.acquire()
        try:
            self.outConnections.pop(str(connectionId), None)
        finally:
            self.port_lock.release()

    def _get_connections(self):
        self.port_lock.acquire()
        try:
            return [ExtendedCF.UsesConnection(name, port) for name, port in self.outConnections.iteritems()]
        finally:
            self.port_lock.release()

    def configure(self, configProperties):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.configure(configProperties)
                    except Exception:
                        self.parent._log.exception("The call to configure failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def query(self, configProperties):
        retVal = None
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        retVal = port.query(configProperties)
                    except Exception:
                        self.parent._log.exception("The call to query failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

        return retVal

    def registerDevice(self, registeringDevice, registeredDeviceMgr):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.registerDevice(registeringDevice, registeredDeviceMgr)
                    except Exception:
                        self.parent._log.exception("The call to registerDevice failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def registerDeviceManager(self, deviceMgr):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.registerDeviceManager(deviceMgr)
                    except Exception:
                        self.parent._log.exception("The call to registerDeviceManager failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def unregisterDeviceManager(self, deviceMgr):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.unregisterDeviceManager(deviceMgr)
                    except Exception:
                        self.parent._log.exception("The call to unregisterDeviceManager failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def unregisterDevice(self, unregisteringDevice):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.unregisterDevice(unregisteringDevice)
                    except Exception:
                        self.parent._log.exception("The call to unregisterDevice failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def installApplication(self, profileFileName):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.installApplication(profileFileName)
                    except Exception:
                        self.parent._log.exception("The call to installApplication failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def uninstallApplication(self, applicationId):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.uninstallApplication(applicationId)
                    except Exception:
                        self.parent._log.exception("The call to uninstallApplication failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def registerService(self, registeringService, registeredDeviceMgr, name):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.registerService(registeringService, registeredDeviceMgr, name)
                    except Exception:
                        self.parent._log.exception("The call to registerService failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def unregisterService(self, unregisteringService, name):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.unregisterService(unregisteringService, name)
                    except Exception:
                        self.parent._log.exception("The call to unregisterService failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def registerWithEventChannel(self, registeringObject, registeringId, eventChannelName):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.registerWithEventChannel(registeringObject, registeringId, eventChannelName)
                    except Exception:
                        self.parent._log.exception("The call to registerWithEventChannel failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def unregisterFromEventChannel(self, unregisteringId, eventChannelName):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.unregisterFromEventChannel(unregisteringId, eventChannelName)
                    except Exception:
                        self.parent._log.exception("The call to unregisterFromEventChannel failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def registerRemoteDomainManager(self, registeringDomainManager):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.registerRemoteDomainManager(registeringDomainManager)
                    except Exception:
                        self.parent._log.exception("The call to registerRemoteDomainManager failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def unregisterRemoteDomainManager(self, unregisteringDomainManager):
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        port.unregisterRemoteDomainManager(unregisteringDomainManager)
                    except Exception:
                        self.parent._log.exception("The call to unregisterRemoteDomainManager failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

    def _get_domainManagerProfile(self):
        retVal = ""
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        retVal = port._get_domainManagerProfile()
                    except Exception:
                        self.parent._log.exception("The call to _get_domainManagerProfile failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

        return retVal

    def _get_deviceManagers(self):
        retVal = None
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        retVal = port._get_deviceManagers()
                    except Exception:
                        self.parent._log.exception("The call to _get_deviceManagers failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

        return retVal

    def _get_applications(self):
        retVal = None
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        retVal = port._get_applications()
                    except Exception:
                        self.parent._log.exception("The call to _get_applications failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

        return retVal

    def _get_applicationFactories(self):
        retVal = None
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        retVal = port._get_applicationFactories()
                    except Exception:
                        self.parent._log.exception("The call to _get_applicationFactories failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

        return retVal

    def _get_fileMgr(self):
        retVal = None
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        retVal = port._get_fileMgr()
                    except Exception:
                        self.parent._log.exception("The call to _get_fileMgr failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

        return retVal

    def _get_allocationMgr(self):
        retVal = None
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        retVal = port._get_allocationMgr()
                    except Exception:
                        self.parent._log.exception("The call to _get_allocationMgr failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

        return retVal

    def _get_identifier(self):
        retVal = ""
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        retVal = port._get_identifier()
                    except Exception:
                        self.parent._log.exception("The call to _get_identifier failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

        return retVal

    def _get_name(self):
        retVal = ""
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        retVal = port._get_name()
                    except Exception:
                        self.parent._log.exception("The call to _get_name failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

        return retVal

    def _get_remoteDomainManagers(self):
        retVal = None
        self.port_lock.acquire()

        try:
            for connId, port in self.outConnections.items():
                if port != None:
                    try:
                        retVal = port._get_remoteDomainManagers()
                    except Exception:
                        self.parent._log.exception("The call to _get_remoteDomainManagers failed on port %s connection %s instance %s", self.name, connId, port)
        finally:
            self.port_lock.release()

        return retVal

