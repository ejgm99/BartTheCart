import serial,time

arduino_path = "../../../../dev/ttyUSB0"

import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import spiUtils as su
import time
import numpy as np
from pynput.keyboard import Key, Listener



# threshold stuff
smackLvl = 50
yellLvl = 200
distLvl = 15

mode = True

# Setup GPIO pin as input for gate pin
GPIO.setmode(GPIO.BCM)
gatePin = 27
GPIO.setup(gatePin, GPIO.IN)
start = time.time()



class arduino_serial(): #interface for talking to arduino
    def __init__(self,path, rate = 250000):
        self.serial = serial.Serial(path, rate)
        self.out = "hello"
        self.mode = True
        time.sleep(2)
        self.listener = Listener(on_press=self.on_press, on_release = on_release)
        self.listener.start()
        self.run = True
        print("yeet")
    def write(self, msg):
        self.serial.write(msg.encode("ascii"))
        print("        writing: "+msg)
        print("        flushng...")
        self.serial.flush()
        print("        flushed! ")
        #self.getResponse()
    def prepareDirections(self):
        self.out = "hello"
    def getDistance(self):
        self.response = self.serial.readline()
        if(len(self.response) > 2):
            return int(self.response)
        return 255
    def getResponse(self):
        print(self.serial.readline())
        print(self.response.decode("ascii"))
    def on_press(self, key):
        try:
            if key == key.space:
                #print("Space press")
                self.mode = not self.mode
                print("mode changed: ", self.mode)
                if self.mode == 0:
                    self.write("9")
                else:
                    loop()
            if key == key.esc:
                #print("Escaping")
                self.run= False
                self.listener.stop()
        except AttributeError:
            print("not space")

def on_release(key):
    #print('{0} release'.format(key) )
    if key == Key.esc:
        return False

class intervaller():
    def __init__(self, period):
        self.start = time.time()
        self.period = period
        self.isInterval = 0
        self.currentSecond = 0
    def interval(self):
        #print("    Interval scaffolding")
        #print("    t-s  : ", int(time.time()-self.start))
        #print("    isInt: ", self.isInterval)
        if (int(time.time()-self.start)%self.period ==0) and (self.currentSecond != int(time.time()-self.start)):
            self.isInterval = 1
            self.currentSecond = int(time.time()-self.start)
            
         #   print("    returning true")
            return True
        if (int(time.time()-self.start%self.period != 0)) and (self.currentSecond != int(time.time()-self.start)):
            self.isInterval = 0
          #  print("    returning false")
        return False

        
m = arduino_serial(arduino_path)

def motorWrite(left, left_dir, right, right_dir):
    left = str(left)
    right= str(right)
    while(len(left)<3):
        left = '0'+left
    while(len(right)<3):
        right = '0'+right
    out = left_dir + str(left) + right_dir+ str(right)
    print(out)
    return out;

def writeSpeed(speed, ax1, ax2):
    print("     Writing "+ str(speed)+ " " + str(ax1) + " " + str(ax2))
    out = motorWrite(speed, ax1, speed, ax2)
    m.write(out)

def distanceSensorTest(ser):
    ser.getLine()
        

def reset():
    print("Reseting arduino")
    m.write("00000000")
    m.serial.close()
    m.serial.open()
    time.sleep(1)
    m.serial.reset_input_buffer()
    
    
def serialTest(): #proof that the arduino can recieve serial and send to the odrive
    print("Beginning serial test")
    m = arduino_serial(arduino_path)
    m.serial.close()
    m.serial.open()
    one_int = intervaller(2)
    fifteen = intervaller(15)
    speed = 50;
    print(fifteen.interval())
    time.sleep(1)
    start = time.time()
    while not fifteen.interval():
        #print("--------", time.time()-start,"----------")
        #print(one_int.interval())
        if(one_int.interval()):
            print("------", time.time()-start,"------")
            out = motorWrite(speed,"1", speed, "1")
            print("Writing: "+ out)
            speed = speed +15
            m.write(out)
    

def avoidWall(dist):
    if(dist<distLvl):
        while (m.getDistance() < distLvl):
            rotate()
        

def rotate():#always go left, to clean room
    print("rotating... ")
    turn = motorWrite(10,'0',10,'1')
    m.write(turn)
    while(int(m.serial.readline())<distLvl):
        print("rotating.. ")
    m.write("00000000")
        


speed = 0
maxSpeed = 255
minSpeed = 0
def updateSpeed(update):
    if(speed + update >255):
        speed = 255
    elif(speed + update < 0):
        speed = 0
    else:
        speed = update+speed

def dataAnalysis(t,d,s,f):
    print("Time")
    print(t)
    print("Distance")
    print(d)
    print("Sound")
    print(s)
    print("Force")
    print(f)
    plt.subplot(3,1,1)
    plt.scatter(t,d)
    plt.title('Distance vs Time')
    plt.xlabel('Time')
    plt.ylabel('Distance')
    axes = plt.gca()
    axes.set_ylim([0,240])
    dLine = np.array([distLvl for i in range(0,len(t))])
    plt.plot(t,dLine,'g')
    
    plt.subplot(3,1,2)
    plt.scatter(t,s)
    plt.title('Sound vs Time')
    plt.ylabel('Sound')
    axes = plt.gca()
    axes.set_ylim([0,1024])
    sLine = np.array([yellLvl for i in range(0,len(t))])
    plt.plot(t,sLine,'g')

    plt.subplot(3,1,3)
    plt.scatter(t,f)
    plt.title('Force vs Time')
    plt.ylabel('Force')
    axes = plt.gca()
    axes.set_ylim([0,1024])
    fLine = np.array([smackLvl for i in range(0,len(t))])
    plt.plot(t,fLine,'g')

    plt.tight_layout()
    plt.show()
    
    
def loop():    
    #with Listener(on_press=m.on_press, on_release = on_release) as listener:
     #   listener.join()
    
    #listener = Listener(on_press=m.on_press, on_release = on_release)
    #listener.start()
    #listener.join()
#    m = arduino_serial(arduino_path)
    print(m.serial.in_waiting)
    time.sleep(1)
    #start = time.time()
    print("Begin cleaning ")
    speed = 0
    reset()
    start = time.time()
    tArray = np.zeros(1)
    fArray = np.empty(1)
    sArray = np.empty(1)
    dArray = np.empty(1)
    
    #thirty_int 
    second_int = intervaller(3)
    one_int = intervaller(1)
    print("Begin loop")
    while m.run:
        #  print("mode",m.mode)
        print("run",m.run)
        if m.mode:
                   
            #print(second_int.interval())
    #        print("---Loop---", time.time()-start )
    #        print("Distance is ", dist
            #listener.join()
            dist = int(m.serial.readline())
           # print(dist)
            force = su.readADC(channel=0)
            sound = su.readADC(channel=1)
            tArray = np.append(tArray,(time.time() - start))
            fArray = np.append(fArray,force)
            sArray = np.append(sArray,sound)
            dArray = np.append(dArray,dist)

            if (force > smackLvl):
                print("Ouch!")
                speed += 100
                writeSpeed(speed,"0","0")
            if (sound > yellLvl):
                print("Oof my ear")
                speed += 50
                writeSpeed(speed, "0","0")
            if (speed > 255) :
                speed = 255
                writeSpeed(speed,"0","0")
            elif (speed > 0):
                if(second_int.interval()):
                    #updateSpeed(-50)
                    speed -= 50
                    if(speed<0):
                        speed = 0
                    print("speed changed")
                    writeSpeed(speed,"0","0")
            avoidWall(dist)
            #if (time.time() - start > 10):
             #   dataAnalysis(tArray, dArray, sArray, fArray)
            #out = motorWrite(speed, '0', speed, '0')
            #print(out)
            #if(interval(start, 5)):
            #if(one_int.interval()):
            #    m.write(out)
            #print(speed)
            #print("\n")
            #xtime.sleep(5)
    
loop()
#serialTest()

print("done")
#m = arduino_serial(arduino_path)
#m.write("02550255")
