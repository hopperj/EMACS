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
import sys, traceback

class SerialServer:

    def __init__(self, numberOfDevices=0, webAddress="http://192.168.100.207/monitor/new/", devicePrefix="/dev/ttyUSB", device=None, timeout=0.50, startCharacter='$'):
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
        self.timeout = timeout

        #self.run = True
        if device is not None:            
            self.device = device
            self.connect( self.device )
        else:
            self.connectSerial()


    def connect(self, device):
        ser = serial.Serial( device, baudrate=9600, timeout=self.timeout)
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
            ser = serial.Serial( self.devicePrefix+str(i), baudrate=9600, timeout=self.timeout)
            print "Added %d serial device"%i
            self.serialDevices.append( ser )


    def getData(self, ser):
        """
        Get data from serial and store as a dictionary
        """
        tmp = ""
        tmpData = ""
        data = {}
        try:
            ser.write('$')
            print "Start character sent"
            tmpData = ""
            tmp = ""
            while tmp != "\n":
                tmp = ser.read(1)
                tmpData += tmp
        except serial.SerialTimeoutException:
            # Return 1 indicating error and None as the data
            return [1, None]

        print "Got data",len(tmpData)
        if len(tmpData) < 1:
            return [1,None]
        print "tmpData:",tmpData
        try:
            for ele in tmpData.rstrip().split(","):
                k,v = ele.rstrip().split(':')
                data[k] = v
        except ValueError:
            print "error data:",ele
            print ele.rstrip().split(':')
            print "\n\n"
            traceback.print_exc(file=sys.stdout)
            return [1,None]

        return [0, data]


    def sendToWeb(self, data):
        """
        curl -H 'Content-Type: application/json' -d '{"device": 1, "sensor_name": "temp1", "value": 22, "created_at": "1000000987"}' 127.0.0.1:8000/monitor/new/
        """
        created_at = datetime.now()
        tmpData = {'device_id':data['device_id'], 'created_at':created_at}
        response = ""
        for k in ['temperature', 'pressure', 'humidity']:
            tmpData = {'device_id':data['device_id'], 'created_at':created_at, 'sensor_name':k, 'value':data[k]}
            # Put data into a json object
            payload = json.dumps(tmpData)
            # Build headers
            headers = {'content-type': 'application/json'}
            # {"device_id": "whiteroom", "sensor_name": "tempature", "value": 16, "created_at": "1001359001"}
            response = requests.put(self.webAddress, data=payload, headers=headers).json()
        # Make sure that device id is valid. -1 indicates an error.
        return response

    def sendToSerial(self, ser, res ):
        """
        Send control settings to Arduino
        """
        # !P @T #H
        # [[{"measure": "tempature", "id": 4, "value": "26", "device_id": 6},
        # {"measure": "pressure", "id": 4, "value": "26", "device_id": 6} ],
        # {"pressure_control": false, "device_name": "living room", "humidity_control": false, "tempature_control": false, "manufacturer_id": "whiteroom", "id": 6}]
        data = ""
        if len(res)<1:
            return

        # Massive super hack to parse data and prepare it for the arduino
        # Putting the capitol H in hackathon
        try:
            for e in res[:-1]:
                data = 'device_id'+':'+e['device_id']+','
                data += 'controller'+':'+res[-1][e['measure']+"control"]+','
                data += e['measure']+':'+e['value']
                if 'temp' in e['measure'].lower():
                    ser.write('!')
                    while ser.read(1) != '!':
                        pass
                    # @device_id:H43B01,controller:1,temperature:22.3
                    ser.write(data)
                elif 'pressure' in e['measure'].lower():
                    ser.write('@')
                    while ser.read(1) != '@':
                        pass
                    # @device_id:H43B01,controller:1,temperature:22.3
                    ser.write(data)        
                elif 'humidity' in e['measure'].lower():
                    ser.write('#')
                    while ser.read(1) != '#':
                        pass
                    # @device_id:H43B01,controller:1,temperature:22.3
                    ser.write(data)

            except:
                print "Couldn't parse key value pairs."


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
                ser.flush()
                print "Getting data from Arduino"
                err, data = self.getData(ser)
                if not err and data is not None:
                    print "Sending data to website"
                    res = self.sendToWeb( data )
                    if res is not None:
                        print "Sending control data back to arduino"
                        self.sendToSerial( ser, res )
                else:
                    print "There was an error"
                    print "--->",err, data
            dt = ( datetime.now() - d0 ).total_seconds()
            print "DeltaTime:",dt
            if dt < 2.0:
                print "\n\n\n"
                sleep( 2.0 - dt ) 


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
