"""
Author: Jason Hopper
Date: 2014-11-14
Takes sensor data from Environmental sensors and publishes them to website
"""


import serial
from urllib2 import Request, urlopen, URLError
from optparse import OptionParser
import json
import requests
from datetime import datetime
from time import sleep

class SerialServer:

    def __init__(self, numberOfDevices=0, webAddress="http://192.168.100.207/monitor/new/", devicePrefix="/dev/ttyUSB", device=None, timeout=10.0, startCharacter='$'):
        # Main web address
        self.webAddress = webAddress
        # Serial timeout value
        self.timeout = timeout
        # device location and prefix /dev/ttyUSB*
        self.devicePrefix = devicePrefix
        # How many serial devices are connected?
        self.numberOfDevices = numberOfDevices
        # List of active serial devices
        self.serialDevices = []

        self.startCharacter = startCharacter

        #self.run = True
        if device is not None:            
            self.device = device
            self.connect( self.device )
        else:
            self.connectSerial()


    def connect(self, device):
        ser = serial.Serial( device, baudrate=9600, timeout=10.0)
        self.serialDevices = [ ser ]

    def closeAll(self):
        """
        Close all serial devices
        """
        # Loop though the serial devices list. Close and delete each element.
        for i,ser in enumerate(self.serialDevices):
            try:
                ser.close()                
            except:
                pass
        del self.serialDevices


    def connectSerial(self):
        """
        First make sure all serial devices are closed
        and then open them again.
        """
        self.closeAll()

        self.serialDevices = []
        for i in range(self.numberOfDevices):
            ser = serial.Serial( self.devicePrefix+str(i), baudrate=9600, timeout=10.0)
            print "Added %d serial device"%i
            self.serialDevices.append( ser )


    def getData(self, ser):
        """
        Get data from serial and store as a dictionary
        """
        tmp = ""
        data = {}
        try:
            ser.write('$')
            tmpData = ser.read(100)
            print "Got data"
        except serial.SerialTimeoutException:
            # Return 1 indicating error and None as the data
            return [1, None]

        print tmpData

        for ele in tmpData.split(","):
            k,v = ele.split(':')
            data[k] = v


        return [0, data]


    def sendToWeb(self, data):
        """
        curl -H 'Content-Type: application/json' -d '{"device": 1, "sensor_name": "temp1", "value": 22, "created_at": "1000000987"}' 127.0.0.1:8000/monitor/new/
        """
        # Put data into a json object
        payload = json.dumps(data)
        # Build headers
        headers = {'content-type': 'application/json'}

        response = requests.put(self.webAddress, data=payload, headers=headers)
        # Make sure that device id is valid. -1 indicates an error.
        return response.json()

    def sendToSerial(self, ser, res ):
        """
        Send control settings to Arduino
        """
        data = ""
        for k,v in res.items():
            data += k+":"+str(v)+","

        # Get rid of the last
        data = data[-1]
        ser.write('@')
        ser.write(data)

    def run(self):
        """
        Itterate over all serial devices over and over
        getting data, sending to web server, get control data
        and send back to arduino.
        """
        while 1:
            print "Looping"
            d0 = datetime.now()
            for ser in self.serialDevices:
                print "Getting data from Arduino"
                err, data = self.getData(ser)
                if not err and data is not None:
                    print "Sending data to website"
                    res = self.sendToWeb( data )
                    print "Sending control data back to arduino"
                    self.sendToSerial( ser, res )
                else:
                    print "There was an error"
                    print err, data
            dt = ( datetime.now() - d0 ).total_seconds()
            if dt > 10:
                sleep( 10 - dt ) 


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-d", "--devices", dest="noOfDevices",
                      help="Number of devices connected")
    parser.add_option("-s", "--server", dest="server",
                      help="Server to send data too")    
    parser.add_option("-p", "--prefix", dest="devicePrefix",
                      help="Prefix for devices")
    parser.add_option("--serial", dest="serial",
                      help="Specific serial device")
    (options, args) = parser.parse_args()

    SS = SerialServer(numberOfDevices = int(options.noOfDevices), webAddress=options.server, device=options.serial)
    #data = {"device": 1, "sensor_name": "temp1", "value": 22, "created_at": "1000000987"}
    #res = SS.sendToWeb( data )
    #SS.sendToSerial( ser, res )
    print "Going into run mode"
    try:
        SS.run()
    except KeyboardInterrupt:
        #SS.run = False
        SS.closeAll()
