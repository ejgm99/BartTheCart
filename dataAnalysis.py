import matplotlib.pyplot as plt
import numpy as np


def dataAnalysis(t,d,s,f,v):
    smackLvl = 200
    yellLvl = 200
    distLvl = 80
    
    plt.subplot(4,1,1)
    plt.scatter(t,d)
    plt.title('Distance vs Time')
    plt.xlabel('Time')
    plt.ylabel('Distance')
    axes = plt.gca()
    axes.set_ylim([0,300])
    dLine = np.array([distLvl for i in range(0,len(t))])
    plt.plot(t,dLine,'g')
    
    plt.subplot(4,1,2)
    plt.scatter(t,s)
    plt.title('Sound vs Time')
    plt.xlabel('Time')
    plt.ylabel('Sound')
    axes = plt.gca()
    axes.set_ylim([0,500])
    sLine = np.array([yellLvl for i in range(0,len(t))])
    plt.plot(t,sLine,'g')

    plt.subplot(4,1,3)
    plt.scatter(t,f)
    plt.title('Force vs Time')
    plt.xlabel('Time')
    plt.ylabel('Force')
    axes = plt.gca()
    axes.set_ylim([0,1024])
    fLine = np.array([smackLvl for i in range(0,len(t))])
    plt.plot(t,fLine,'g')
    
    plt.subplot(4,1,4)
    plt.scatter(t,v)
    plt.title('Speed vs Time')
    plt.xlabel('Time')
    plt.ylabel('Speed')
    axes = plt.gca()
    axes.set_ylim([0, 80])

    plt.tight_layout()
    plt.savefig('BartData.png')    
    #plt.show()