import numpy as np
import spiUtils as su
import ArduinoSerial
import Intervaller
from pynput.keyboard import Key, Listener
import threading
import dataAnalysis as d
import time
#import time.time()
print(threading.current_thread().getName())
class Bart:
    def __init__(self):
        self.listener = Listener(on_press=self.on_press, on_release = self.on_release)
        self.speed = 0
        self.maxSpeed = 80
        self.minSpeed = 0
        self.run = True
        self.serialMode = True
        self.setThresholds()
        self.serial = ArduinoSerial.arduino_serial()
        self.second_int = Intervaller.intervaller(3)
        self.elapsedTime = self.second_int.elapsedTime
    def updateSpeed(self, update):
        if(self.speed + update > self.maxSpeed):
            self.speed = self.maxSpeed
        elif(self.speed + update < self.minSpeed):
            self.speed = 0
        else:
            self.speed +=update
        self.writeSpeed(self.speed, 0,0)
    def avoidWall(self, dist):
        if(dist<self.distLvl):
            self.writeSpeed(0,0,0)
            self.rotate()     
    def rotate(self):#always go left, to clean room
        print("rotating... ")
        #turn = self.motorWrite(50,'1',50,'0')
        #self.serial.write(turn)
        self.serial.specialWrite("10200020")
        while(int(self.serial.readLine())<self.distLvl):
            print("rotating.. ", int(self.serial.readLine()))
        self.serial.write("00000000")
    def writeSpeed(self, speed, ax1, ax2):
        ax1 = str(ax1)
        ax2 = str(ax2)
        out = self.motorWrite(speed, ax1, speed, ax2)
        self.serial.write(out)
    def on_press(self, key):
        try:
            if (key   == key.space):
                print("Space pressed", self.serialMode)
                self.serialMode = not self.serialMode
                print("mode changed: ", self.serialMode)
                    
            if key == key.esc:
                print("Escaping")
                self.run= False
        except(AttributeError):
            return
    def on_release(self,key):
        return
    def setThresholds(self):
        self.smackLvl = 200   
        self.yellLvl = 200
        self.distLvl = 80
    def sensorInputSetup(self):
        self.tList = []
        self.fList = []
        self.sList = []
        self.dList = []
        self.vList = []
        self.dist = 0
        self.force = 0
        self.sound = 0
    def sensorInput(self):
        self.dist = int(self.serial.readLine())
        #print("Distance ", self.dist)
        self.force = su.readADC(channel=0)
        self.sound = su.readADC(channel=1)
        #print("Force ",self.force)
        #print("Sound ",self.sound)
        self.tList.append(self.elapsedTime())
        self.fList.append(self.force)
        self.sList.append(self.sound)
        self.dList.append(self.dist)
        self.vList.append(self.speed)
    def motorWrite(self, left, left_dir, right, right_dir):
        left = str(left)
        right= str(right)
        while(len(left)<3):
            left = '0'+left
        while(len(right)<3):
            right = '0'+right
        out = left_dir + str(left) + right_dir+ str(right)
        return out;
    def serialDrive(self):
        if (self.force > self.smackLvl):
            print("Ouch ", self.force)
            self.updateSpeed(20)
        if (self.sound > self.yellLvl):
            print("Oof my ears",self.sound)
            self.updateSpeed(15)
        if(self.second_int.interval()):
            print("Speed Decreased")
            self.updateSpeed(-3)
        print(self.dist)
        self.avoidWall(self.dist)
    def setup(self):
        self.sensorInputSetup()
        self.listener.start()
        self.serial.hardReset()

    def go(self):
        sentNine = False
        while(self.run):
            print("Running ", self.serialMode)
            print(threading.current_thread().getName())
            if(self.serialMode):
                print(self.serial.serial.in_waiting)
                #print("In serial mode...")
                self.sensorInput() #measures data
                self.serialDrive() #acts on measured data
                if sentNine == True: #
                    print("Setting sent nine to false...")
                    sentNine = False
            else:
                if not sentNine: #"latch" so we don't send 9 constantly to the arduino while it is in serial mode
                    print("In rc mode...")
                    self.serial.specialWrite("9") #
                    sentNine = True
                print("Safe to press space bar for 5 seconds")
                time.sleep(5)
                print("dont press the space bar")
    def begin(self):
        
        self.setup()
        self.go()
        self.tArray = np.array(self.tList)
        self.fArray = np.array(self.fList)
        self.sArray = np.array(self.sList)
        self.dArray = np.array(self.dList)
        self.vArray = np.array(self.vList)
        d.dataAnalysis(self.tArray, self.dArray, self.sArray, self.fArray, self.vArray)

        self.writeSpeed(0,0,0)
        self.listener.stop()

b = Bart()
b.begin()
