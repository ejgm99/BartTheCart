import serial,time

class arduino_serial(): #interface for talking to arduino
    def __init__(self,path = "../../../../dev/ttyUSB0", rate = 250000):
        self.serial = serial.Serial(path, rate)
        self.out = "hello"
        self.mode = True
        time.sleep(2)
        print("yeet")
    def write(self, msg):
        self.serial.write(msg.encode("ascii"))
        print("        writing: "+msg)
        print("        flushng...")
        self.serial.flush()
        print("        flushed! ")
    def getDistance(self):
        self.response = self.serial.readline()
        if(len(self.response) > 2):
            return int(self.response)
        return 255
    def getResponse(self):
        print(self.serial.readline())
        print(self.response.decode("ascii"))
    def hardReset(self):
        print("Reseting arduino")
        self.write("00000000")
        self.serial.close()
        self.serial.open()
        time.sleep(1)
        self.serial.reset_input_buffer()
    def clearOut(self):
        self.serial.reset_output_buffer()
    def readLine(self):
        #out = 315
        #if(self.serial.in_waiting):
        #    print("actually recieved arduino data")
        out = self.serial.readline()
        return out
    def specialWrite(self,msg): #this willl be improved later but for now is just this
        time.sleep(2) #this delay is needed because of serial shenanigans
        self.write(msg)

        
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

def rapidSerialTest():
    s = arduino_serial()
    s.write("02000200")
    time.sleep(2)
    s.write("01000100")
    s.serial.reset_output_buffer()
 #   time.sleep(1)
#    s.write("9")
    time.sleep(3)
    s.write("9")

#rapidSerialTest()
 
