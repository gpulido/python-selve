#!/usr/bin/python

import time
import serial
from enum import Enum
import logging

from selve.utils import * 
from selve.iveo import *
from selve.protocol import process_response


_LOGGER = logging.getLogger(__name__)

class Gateway():   

    def __init__(self, port, discover = True):
        """                
        Arguments:
            port {String} -- Serial port string as it is used in pyserial
        
        Keyword Arguments:
            discover {bool} -- True if the gateway should try to discover 
                               the devices on init (default: {True})
        """
        self.port = port
        if discover:
            self.discover()
    
    def configserial(self):
        """
        Configure the serial port
        """
        self.ser = serial.Serial(
            port=self.port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1)
        self.ser.timeout = 0
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2

            
    def executeCommand(self, command):
        """[summary]
        Execute the given command using the serial port.
        It opens a communication to the serial port each time a
        command is executed.
        At this moment it doesn't keep a queue of commands. If
        a command blocks the serial it will wait.
        
        Arguments:
            command {protocol.MethodCall} -- Command to be send 
            through the serial port
        
        Returns:
            MethodResponse -- if the command was executed 
            sucessufully
            ErrorResponse -- if the gateway returns an error
        """
        commandstr = command.serializeToXML()
        _LOGGER.info('Gateway writting: ' + str(commandstr))

        try:
            self.configserial()

        except Exception as e:            
            _LOGGER.error ('error open serial port: ' + str(e))
            exit()
        
        if self.ser.isOpen():
            try:
                self.ser.flushInput()
                self.ser.flushOutput()
                self.ser.write(commandstr)
                self.ser.flush()
                #time.sleep(0.5)
                response_str = ""
                while True:
                    response = self.ser.readline().strip()
                    response_str += response.decode()
                    _LOGGER.info('read data: ' + response_str)
                    if response.decode() == '':
                        break
                    
                self.ser.close()
                _LOGGER.info('read data: ' + response_str)
                return process_response(response_str)
            except Exception as e1:
                _LOGGER.exception ("error communicating...: " + str(e1))
        else:
            _LOGGER.error ("cannot open serial port")
        
        return None

    # def serial_data(self, data):
    #     print (data)

    def discover(self):
        """[summary]
            Discover all devices registered on the usb-commeo        
        """
        command = IveoCommandGetIds()
        num_retries = 5
        retry_n = 0
        while not hasattr(command, "ids") and retry_n <=num_retries:
            command.execute(self)
            retry_n += 1
            time.sleep(1)
        
        if not hasattr(command, "ids"):
            _LOGGER.info("Associated Devices not found") 
            self.devices = {}
        else:
            _LOGGER.debug(f'discover ids: {command.ids}')
            self.devices = dict([(id, IveoDevice(self, id , True) )for id in command.ids])
        self.list_devices() 
       

    def is_id_registered(self, id):
        """[summary]
        check if a device id is registered on the gateway
        Arguments:
            id {int} -- Device id to check
        
        Returns:
            boolean -- True if the id is registered
                       False otherwise
        """
        return id in self.devices
        
    def list_devices(self):
        """[summary]
        Print the list of registered devices
        """ 
        for id, device in self.devices.items():
            print(str(device))
            #_LOGGER.info(str(device))
            
    def teach_channel(self, channel):
        command = IveoCommandTeach(channel)
        _LOGGER.info("Trying to teach channel " + str(channel))
        command.execute(self)
        if command.executed:
            _LOGGER.info("Channel " + str(channel) + "sucessfully teach" )

if __name__ == '__main__':
    #print (singlemask(2).decode('utf-8'))
    _LOGGER.setLevel(logging.DEBUG)
    #manual = MethodCall("selve.GW.iveo.getIDs",[])
    portname = '/dev/cu.usbserial-DJ00T875'
    gat = Gateway(portname, False)
    gat.discover()
    devices = list(gat.devices.values())
    #device = IveoDevice(gat, 0)
    #device.stop(False)
    #gat.list_devices()

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

