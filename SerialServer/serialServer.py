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

class SerialServer:

    def __init__(self, numberOfDevices=0, webAddress="http://192.168.100.207/monitor/new/", devicePrefix="/dev/ttyUSB", timeout=10.0, startCharacter='$'):
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


    def connectSerial(self):

        # Loop though the serial devices list. Close and delete each element.
        for i,ser in enumerate(self.serialDevices):
            try:
                ser.close()                
            except:
                pass
        del self.serialDevices

        self.serialDevices = []
        for i in range(self.numberOfDevices):
            ser = serial.Serial( self.devicePrefix+str(i), baudrate=9600, timeout=10.0)


    def getData(self, ser):
        
        tmp = ""
        data = {}
        try:
            ser.write(1)
            tmpData = ser.read(4096*5)
            ser.write("temperature:30")

        except serial.SerialTimeoutException:
            # Return 1 indicating error and None as the data
            return [1, None]

        for ele in tmpData.split("\n"):
            k,v = ele.split(':')
            data[k] = float(v)


        return data



    def sendToWeb(self, data):
        """
        curl -H 'Content-Type: application/json' -d '{"device": 1, "sensor_name": "temp1", "value": 22, "created_at": "1000000987"}' 127.0.0.1:8000/monitor/new/
        """
        payload = json.dumps(data)
        headers = {'content-type': 'application/json'}

        response = requests.put(self.webAddress, data=payload, headers=headers)
        print response


    def run(self):

        err, data = self.getData()
        if not err and data is not None:
            self.sendToWeb( data )


if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-d", "--devices", dest="noOfDevices",
                      help="Number of devices connected")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    SS = SerialServer(numberOfDevices = options.noOfDevices)
    data = {"device": 1, "sensor_name": "temp1", "value": 22, "created_at": "1000000987"}
    SS.sendToWeb( data )
