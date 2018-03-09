#!/usr/bin/python

import time
import serial
from HW_Thread import *
from utils import *
from protocol import *
from enum import Enum


class ParameterType(Enum):
    INT = "int"
    STRING = "string"
    BASE64 = "base64"

class DeviceType(Enum):
    UNKNOWN = 0
    SHUTTER = 1
    BLIND = 2
    AWNING = 3
    SWITCH = 4
    DIMMER = 5
    NIGHT_LIGHT = 6
    DRAWN_LIGHT = 7
    HEATING = 8
    COOLING = 9
    COOLING2 = 10
    GATEWAY = 11

class CommandType(Enum):
    STOP = 0
    DRIVEAWAY = 1
    DEPARTURE = 2
    POSITION_1 = 3
    POSITION_2 = 4

class IveoCommand(Enum):
    FACTORY = "commandFactory"
    TEACH = "commandTeach"
    LEARN = "commandLearn"
    MANUAL = "commandManual"
    AUTOMATIC = "commandAutomatic"
    RESULT = "commandResult"
    GETIDS = "getIDs"
    SETLABEL = "setLabel"
    SETCONFIG = "setConfig"
    GETCONFIG = "getConfig"



class CommandIveo(MethodCall):

    def __init__(self, method_name, parameters = []):
         super().__init__("selve.GW.iveo." + method_name.value, parameters)

class CommandSingleIveo(CommandIveo):

    def __init__(self, method_name, iveoID):
        super().__init__(method_name, [(ParameterType.INT, iveoID)])

class CommandMaskIveo(CommandIveo):

    def __init__(self, method_name, mask, command):
        super().__init__(method_name, [(ParameterType.BASE64, mask), (ParameterType.INT, command.value)])

class IveoCommandFactory(CommandSingleIveo):

     def __init__(self, iveoID):
         super().__init__(IveoCommand.FACTORY, iveoID)

class IveoCommandTeach(CommandSingleIveo):
     def __init__(self, iveoID):
         super().__init__(IveoCommand.TEACH, iveoID)

class IveoCommandLearn(CommandSingleIveo):
     def __init__(self, iveoID):
         super().__init__(IveoCommand.LEARN, iveoID)
         
class IveoCommandManual(CommandMaskIveo):
    def  __init__(self, mask, command):
        super().__init__(IveoCommand.MANUAL, mask, command)

class IveoCommandAutomatic(CommandMaskIveo):
    def  __init__(self, mask, command):
        super().__init__(IveoCommand.AUTOMATIC, mask, command)

class IveoCommandResult(MethodCall):
    def __init__(self, command, mask, state):
        super().__init__(IveoCommand.RESULT, [(ParameterType.INT, command), (ParameterType.BASE64, mask), (ParameterType.INT, state)])

class IveoComandSetLabel(CommandIveo):
    def __init__(self, iveoId, label):
        super().__init__(IveoCommand.SETLABEL, [(ParameterType.INT, iveoId), (ParameterType.STRING, label)])

class IveoComandSetConfig(CommandIveo):
    def __init__(self, iveoId, activity, device_type):
        super().__init__(IveoCommand.SETCONFIG, [(ParameterType.INT, iveoId), (ParameterType.INT, activity), (ParameterType.INT, device_type)])

class IveoComandGetConfig(CommandSingleIveo):
    def __init__(self, iveoId):
        super().__init__(IveoCommand.GETCONFIG, iveoId)
    
    def process_response(self, methodResponse):
        self.name = methodResponse.parameters[0][1]
        self.activity = methodResponse.parameters[2][1]
        self.deviceType = DeviceType(int(methodResponse.parameters[3][1]))

class IveoCommandGetIds(CommandIveo):
    def __init__(self):
        super().__init__(IveoCommand.GETIDS)
    
    def process_response(self, methodResponse):
        self.ids = true_in_list(b64bytes_to_bitlist(methodResponse.parameters[0][1]))

class Gateway():

    def __init__(self, port):
        self.port = port
        self.discover()
        #self.configserial()
        #self.hw =  HW_Interface(self.ser, 100)
        #self.hw.register_callback(self.serial_data)
    
    def configserial(self):
        self.ser = serial.Serial(
            port=self.port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
        self.ser.timeout = 0
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2

            
    def executeCommand(self, command):
        commandstr = command.serializeToXML()
        print( "Gateway writting: " + str(commandstr))
        
        try:
            self.configserial()

        except Exception as e:
            print ("error open serial port: " + str(e))
            exit()
        
        if self.ser.isOpen():
            try:
                self.ser.flushInput()
                self.ser.flushOutput()
                
                self.ser.write(commandstr)
                time.sleep(0.5)
                numOfLines = 0
                response_str = "" 
                while True:
                    response = self.ser.readall()
                    response_str += str(response.decode())
                    print("read data: " + response_str)
                    if (response.decode()== ''):
                        break
                    
                self.ser.close()
                return process_response(response_str)
            except Exception as e1:
                print ("error communicating...: " + str(e1))
        else:
            print ("cannot open serial port")
        
        return None

        
        #self.hw.write_HW(commandstr)    

    #def close(self):
        #self.hw.kill()
        #self.ser.close() 

    def serial_data(self, data):
        print (data)

    def discover(self):
        command = IveoCommandGetIds()
        command.execute(self)
        self.devices = [IveoDevice(self, id) for id in command.ids]
        for device in self.devices:
            device.discover_properties()
            print(str(device))
            



class IveoDevice():

    def __init__(self, gateway, iveoID):
        self.iveoID = iveoID
        self.gateway = gateway
        self.mask = singlemask(iveoID)
        self.device_type = DeviceType.UNKNOWN
        self.name = "Not defined"
    
    def stop(self):
        command = IveoCommandManual(self.mask , CommandType.STOP)
        self.gateway.executeCommand(command)

    def moveDown(self):
        command = IveoCommandManual(self.mask , CommandType.DEPARTURE)
        self.gateway.executeCommand(command)

    def moveUp(self):
        command = IveoCommandManual(self.mask , CommandType.DRIVEAWAY)
        self.gateway.executeCommand(command)
    
    def moveIntermediatePosition1(self):
        command = IveoCommandManual(self.mask , CommandType.POSITION_1)
        self.gateway.executeCommand(command)

    def moveIntermediatePosition2(self):
        command = IveoCommandManual(self.mask , CommandType.POSITION_2)
        self.gateway.executeCommand(command)

    def discover_properties(self):
        command = IveoComandGetConfig(self.iveoID)
        command.execute(self.gateway)
        self.device_type = command.deviceType
        self.name = command.name
    
    def __str__(self):
        return "Device of type: " + self.device_type.name + " on channel " + str(self.iveoID) + " with name " + self.name
        
        



if __name__ == '__main__':
    #print (singlemask(2).decode('utf-8'))

    #manual = MethodCall("selve.GW.iveo.getIDs",[])
    portname = '/dev/cu.usbserial-DJ00T875'
    gat = Gateway(portname)

    # device1 = IveoDevice(gat, 1)
    # device2 = IveoDevice(gat, 2)
    # device1.moveDown()
    # time.sleep(5)
    # device1.moveUp()
    # device2.moveDown()
    # time.sleep(3)
    # device1.stop()
    # device2.stop
    # time.sleep(1)
    # device1.stop()
    #command = IveoCommandGetIds()
    #command.execute(gat)
    #print (command.ids)
    #response = b'<?xml version="1.0"? encoding="UTF-8">\r\n<methodResponse>\r\n\t<array>\r\n\t\t<string>selve.GW.iveo.commandManual</string>\r\n\t\t<int>1</int>\r\n\t</array>\r\n</methodResponse>\r\n\n<?xml version="1.0"? encoding="UTF-8">\r\n<methodCall>\r\n<methodName>selve.GW.iveo.commandResult</methodName>\r\n\t<array>\r\n\t\t<int>0</int>\r\n\t\t<base64>AQAAAAAAAAA=</base64>\r\n\t\t<int>0</int>\r\n\t</array>\r\n</methodCall>\r\n\n'
    #c = response.decode()
    #print(c)
    #deserialize(response)

