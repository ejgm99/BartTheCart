import serial

class arduino_serial(): #interface for talking to arduino
    def __init__(self,path, rate = 250000):
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
