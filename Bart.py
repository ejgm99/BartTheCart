import numpy as np
import spiUtils as su
import ArduinoSerial
import Intervaller
from pynput.keyboard import Key, Listener
class Bart:
    def __init__(self):
        self.listener = Listener(on_press=self.on_press, on_release = self.on_release)
        self.speed = 0
        self.maxSpeed = 255
        self.minSpeed = 0
        self.run = True
        self.serialMode = True
        self.setThresholds()
        self.serial = ArduinoSerial.arduino_serial()
        self.second_int = Intervaller.intervaller(1)
    def updateSpeed(self, update):
        if(self.speed + update > self.maxSpeed):
            self.speed = self.maxSpeed
        elif(self.speed + update < self.minSpeed):
            self.speed = 0
        else:
            self.speed +=update
        writeSpeed(self.speed, 0,0)
    def avoidWall(self, dist):
        if(dist<self.distLvl):
            while (m.getDistance() < self.distLvl):
                self.rotate()     
    def rotate():#always go left, to clean room
        print("rotating... ")
        turn = motorWrite(10,'0',10,'1')
        m.write(turn)
        while(int(m.serial.readline())<distLvl):
            print("rotating.. ")
        m.write("00000000")
    def writeSpeed(speed, ax1, ax2):
        print("     Writing "+ str(speed)+ " " + str(ax1) + " " + str(ax2))
        out = motorWrite(speed, ax1, speed, ax2)
        m.write(out)
    def on_press(self, key):
        try:
            if key == key.space:
                #print("Space press")
                self.mode = not self.mode
                print("mode changed: ", self.mode)
                if self.mode == 0:
                    self.write("9")
                else:
                    go()
            if key == key.esc:
                #print("Escaping")
                self.run= False
                self.listener.stop()
        except AttributeError:
            print("not space")
    def on_release(self,key):
        return
    def setThresholds(self):
        self.smackLvl = 50
        self.yellLvl = 200
        self.distLvl = 15
    def sensorInputSetup(self):
        self.tArray = np.zeros(1)
        self.fArray = np.empty(1)
        self.sArray = np.empty(1)
        self.dArray = np.empty(1)
        self.dist = 0
        self.force = 0
        self.sound = 0
    def sensorInput(self):
            self.dist = int(m.serial.readline())
            self.force = su.readADC(channel=0)
            self.sound = su.readADC(channel=1)
            self.tArray = np.append(tArray,(time.time() - start))
            self.fArray = np.append(fArray,force)
            self.sArray = np.append(sArray,sound)
            self.dArray = np.append(dArray,dist)
    def serialDrive(self):
        if (self.force > self.smackLvl):
            print("Ouch!")
            self.updateSpeed(100)
            writeSpeed(speed,"0","0")
        if (self.sound > self.yellLvl):
            print("Oof my ear")
            self.updateSpeed(50)
        if(self.second_int.interval()):
            self.updateSpeed(-50)
        avoidWall(dist)
    def setup(self):
        self.sensorInputSetup()
        self.listener.start()
        self.serial.hardReset()
    def go(self):
        while(self.run):
            if(self.serialMode):
                self.sensorInput()
                self.serialDrive()
    def begin(self):
        setup()
        go()