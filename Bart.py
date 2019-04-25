import numpy as np

class Bart:
    self.listener = Listener(on_press=self.on_press, on_release = on_release)
    self.listener.start()
    self.run = True

    self.speed = 0
    self.maxSpeed = 255
    self.minSpeed = 0
    def updateSpeed(self, update):
        if(self.speed + update > self.maxSpeed):
            speed = self.maxspeed
        elif(self.speed + update < self.minSpeed):
            self.speed = 0
        else:
            self.speed +=update

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
        