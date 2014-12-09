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
# AUTO-GENERATED
#
# Source: FrontEndController.spd.xml
from ossie.resource import start_component
import logging

from FrontEndController_base import *

from ossie.utils import redhawk
import frontend
from redhawk.frontendInterfaces import FRONTEND

class FrontEndController_i(FrontEndController_base):
    
    """
    This component was developed to support the REDHAWK LiveDVD.  It also serves to provides a simple
    example of FEI Allocations and connections.  It was developed with REDHAWK 1.10.0.  
    """
    
    targetComponent=None
    targetDevice=None
    domain = None
    targetComponentPort = None
    targetDevicePort = None
    feiTunerPort = None
    connected = False
    
    def initialize(self):
        FrontEndController_base.initialize(self)
        self.addPropertyChangeListener("TuneRequest", self.TuneRequest_changed)
        
    def start(self):
        FrontEndController_base.start(self)
        
        if not self.connected:
            self.connectAndTune()
    
    def stop(self):
        self._log.debug("Stop called.")
        
        try:
            if self.connected:
                self.targetDevice.deallocateCapacity(self.allocationRequest)
                self.targetDevicePort.disconnectPort(self.allocationId)
        except:
            self._log.error("Exception occurred while deallocating and disconnecting.")
        finally:
            self.connected = False
            FrontEndController_base.stop(self)
            
    
    def TuneRequest_changed(self, propid, oldval, newval):
        self._log.debug("Received Tune Request Change")
        self._log.debug("Currently Connected: " + str(self.connected))
        
        if self.connected:
            try:
                if (oldval.frequency != newval.frequency):
                    self._log.debug("Trying to set frequency to: " + str(newval.frequency))
                    self.feiTunerPort.setTunerCenterFrequency(self.allocationId, newval.frequency*1e6)
                    
                if (oldval.sampleRate != newval.sampleRate):
                    self._log.debug("Trying to set sample rate to: " + str(newval.sampleRate))
                    self.feiTunerPort.setTunerOutputSampleRate(self.allocationId, newval.sampleRate*1e6)
            
            except FRONTEND.BadParameterException as ex:
                self._log.error("Bad Parameter Exception Thrown: " + str(ex))
            except FRONTEND.NotSupportedException as ex:
                self._log.error("Not Supported Exception Thrown: " + str(ex))
            except FRONTEND.FrontendException as ex:
                self._log.error("Front End Exception Thrown: " + str(ex))    
            except Exception as ex: 
                self._log.error("Failed to set property: " + str(ex))
            finally:
                self.TuneRequest.frequency = self.feiTunerPort.getTunerCenterFrequency(self.allocationId) / 1e6
                self._log.debug("Actual frequency: " + str(self.TuneRequest.frequency))
                
                self.TuneRequest.sampleRate = self.feiTunerPort.getTunerOutputSampleRate(self.allocationId) / 1e6
                self._log.debug("Actual sample rate: " + str(self.TuneRequest.sampleRate))

        
    def connectAndTune(self):
        
        # Lets make sure we have everything we need before continuing.
        if not self.InputComponent.componentName:
            self._log.error("Stopping. Component name must be specified.")
            self.stop()
            return
        
        if not self.InputComponent.inputPortName:
            self._log.error("Stopping. Component input port name must be specified.")
            self.stop()
            return
        
        if not self.FEIDevice.deviceName:
            self._log.error("Stopping. Device name must be specified.")
            self.stop()
            return
        
        if not self.FEIDevice.outputPortName:
            self._log.error("Stopping. Device output port name must be specified.")
            self.stop()
            return
        
        if not self.FEIDevice.tunerPortName:
            self._log.error("Stopping. Device tuner port name must be specified.")
            self.stop()
            return
                
        # While the domain port does give us a direct connection to the domain, the
        # API exposed is cleaner from the domain instance returned via the redhawk.attach method.
        try:
            domainname = self.port_DomainManager_out._get_name()
            self.domain = redhawk.attach(domainname)
        except Exception as ex:
            self._log.error("Failed to connect to domain: " + str(ex))
            self.stop()
            return

        if self.domain is None:
            self._log.error("Stopping.  Could not connect to domain.")
            self.stop()
            return
        
        
        self._log.debug("Searching for the current waveform in the domain")
        waveform = self.findWaveformByComponentInstanceName(self._name)
        
        if waveform is None:
            self._log.error("Stopping. Could not find the running waveform.")
            self.stop();
            return
             
        self._log.debug("Searching for the component in the waveform: " + str(waveform.name))
        
        # Gets the component from the application.  The component name can be the name or instantition.  ex.  DataConverter or DataConveter_3
        # This allows you to use the same component multiple times in a waveform and know for certain which one you are connecting to.
        for comp in waveform.comps:
            if self.InputComponent.componentName in comp._instanceName:
                self.targetComponent = comp
                break
        
        if self.targetComponent is None:
            self._log.error("Stopping.  Could not find the component: " + self.InputComponent.componentName)
            self.stop();
            return
             
         
        self._log.debug("Searching device managers for device: " + self.FEIDevice.deviceName)
        
        self.targetDevice = self.findByDeviceName(self.FEIDevice.deviceName)
        
        if self.targetDevice is None:
            self._log.error("Stopping. Could not find the device: " + self.FEIDevice.deviceName)
            self.stop()
            return


        # Gets the references to the input and output ports
        self.targetComponentPort = self.targetComponent.getPort(self.InputComponent.inputPortName)
        self.targetDevicePort = self.targetDevice.getPort(self.FEIDevice.outputPortName)
        self.feiTunerPort = self.targetDevice.getPort(self.FEIDevice.tunerPortName)
         
        if self.targetComponentPort is None:
            self._log.error("Stopping.  Could not find the component input port: " + self.InputComponent.inputPortName)
            self.stop()
            return
             
        if self.targetDevicePort is None:
            self._log.error("Stopping.  Could not find the component output port: " + self.FEIDevice.outputPortName)
            self.stop()
            return
         
        if self.feiTunerPort is None:
            self._log.error("Stopping.  Could not find the tuner port: " + self.FEIDevice.tunerPortName)
            self.stop()
            return
         
        self.allocationRequest = frontend.createTunerAllocation(
                                                    tuner_type              =   self.tunerType, 
                                                    allocation_id           =   self.allocationId,
                                                    center_frequency        =   self.TuneRequest.frequency * 1e6, 
                                                    sample_rate             =   self.TuneRequest.sampleRate * 1e6,
                                                    sample_rate_tolerance   =   20.0
                                                    )
         
         
         
        self._log.debug("Performing allocation of FEI Device")
        self._log.debug("Allocation contains: " + str(self.allocationRequest))
        
        retVal = False
        
        try:
            retVal = self.targetDevice.allocateCapacity(self.allocationRequest)
        except CF.Device.InvalidCapacity as ex:
            self._log.error("Device has invalid capacity, allocation failed: " + str(ex))
        except CF.Device.InvalidState as ex:
            self._log.error("Device in invalid state, allocation failed: " + str(ex))
        except Exception as ex:
            self._log.error("Exception thrown while allocating: " + str(ex))
         
        if (retVal is False):
            self._log.error("Allocation failed.  Stopping.")
            self.stop()
            return
        
        
        self._log.debug("Allocation succeeded!")
        
        # Makes the actual connection
        self._log.debug("Connecting component and device ports")
        self.targetDevicePort.connectPort(self.targetComponentPort, self.allocationId)
        self.connected = True
 
        self._log.debug("Starting device and component")
        
        # Make sure device and component are started
        self.targetDevice.start()
        self.targetComponent.start()
        
    # This component does no processing so we can just return FINISH so 
    # the process method does not get called again.
    def process(self):
        return FINISH
        

    def findWaveformByComponentInstanceName(self, name):
        # Gets a reference to the running application
        for app in self.domain.apps:
            # Find desired application
            for comp in app.comps:
                self._log.trace("Checking if " + name + " is in " + comp._instanceName)
                if name in comp._instanceName:
                    return app

        return None


    def findByDeviceName(self, dev_name):
        for devMgr in self.domain.devMgrs:
            for dev in devMgr.devs:
                self._log.trace("Checking if " + dev_name + " is in " + dev._instanceName)
                if dev_name in dev._instanceName:
                    return dev
                
        return None
        
  
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.debug("Starting Component")
    start_component(FrontEndController_i)

