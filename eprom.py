
import serial,time #You need the pyserial library
import struct

ser = serial.Serial('/dev/ttyACM0', 250000, timeout=0)
#time.sleep(10);#my arduino bugs if data is written to the port after opening it
romsize=1024

while True:
    print("===========================================")
    print("           What do you want do do?         ")
    print("                                           ")
    print("              1-dump                       ")
    print("              2-burn                       ")
    print("              3-info                       ")
    print("                              2016         ")
    print("                                  Robson C ")
    print("===========================================")
    option=int(input())
    romsize=1*1024*1024
    block=0
    print(option)
    if(option==1):
        name=input("What the name of the file?")

        f = open(name, 'w')
        f.close()
        ser.flushInput()
        ser.write(b"\x55")
        ser.write(bytes("r","ASCII"))
        numBytes=0
        f = open(name, 'ab')
        while (numBytes<romsize):
            while ser.inWaiting()==0:
                print("Waiting. Current porcentage:%.2f"%(numBytes*100/romsize),"%",end='\r')
                time.sleep(0.1)
            data = ser.read(1)#must read the bytes and put in a file
            f.write(data)
            numBytes=numBytes+1
        f.close()
        print("Done/n")
    if(option==2):
        name=input("What's the name of the file?")
        print(name)
        f = open(name, 'rb')

        for i in range(8192):
            ser.write(b"\x55")
            ser.write(bytes("w","ASCII" ))
            time.sleep(0.001)
            ser.write(struct.pack(">B",i>>8))
            CHK=i>>8
            time.sleep(0.001)
            ser.write(struct.pack(">B",i&0xFF))
            CHK^=i&0xFF
            time.sleep(0.001)
            data=f.read(128);
            print(data)
            for j in range(len(data)):
                 CHK=CHK^data[j]
            time.sleep(0.001)
            print("Sector:",i)
            print("CHK:", CHK)
            response=~CHK
            while response!=CHK:
                ser.write(data)
                ser.write(struct.pack(">B",CHK&0xFF))
                timeout=30
                while ser.inWaiting()==0:
                    time.sleep(0.1)
                    print("waiting for CHK response")
                response=ord(ser.read(1))
                print("rsp", response)
        f.close()
