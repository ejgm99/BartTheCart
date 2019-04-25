
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