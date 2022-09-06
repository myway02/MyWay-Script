#libaries
import serial
import pynmea2
import RPi.GPIO as GPIO
import time
import pyrebase
from pygame import mixer
 
 
##GPIO pin setup for raspberry
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

##Sound Setting up
#initializing mixer
mixer.init () #t

#inputing sound
sound1 = mixer.Sound ("halangan.wav")
sound2 = mixer.Sound ("TIT.wav")

##Firebase setup
config = {
  "apiKey": "AIzaSyDVi7usbyRtNiKfW8zuGsw7cV-GwCK7c9o",
  "authDomain": "way-app-fc040.firebaseapp.com",
  "databaseURL": "https://way-app-fc040-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "projectId": "way-app-fc040",
  "storageBucket": "way-app-fc040.appspot.com",
  "messagingSenderId": "636107727117",
  "appId": "1:636107727117:web:02c6e0274cb4d2ff32d044"
}

#initializing database
firebase = pyrebase.initialize_app(config)


print("Send Data to Firebase Using Raspberry Pi")
print("—————————————")

##Main Ultra Function
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

#Detecting an object
def object_detection (distance):
       # Jika jarak dibawah 200 cm maka status adalah bahaya
       status = "aman"
       if distance < 280 :
           status = "bahaya"
       if distance <= 150 :
           status = "sangat bahaya"
       return status


##Main GPS ffucntion
#setup port with serial
def port_setup(port):
    ser = serial.Serial(port, baudrate=9600, timeout=2)
    return ser

#get some data
def parseGPSdata(ser):
        keywords = ["$GPRMC","$GPGGA"]
        gps_data = ser.readline()
        gps_data = gps_data.decode("utf-8")  # transform data into plain string

        if len(gps_data) > 5:  # Check to see if the GPS gave any useful data
            if gps_data[0:6] in keywords:   # Check t see if the message code
                gps_msg = pynmea2.parse(gps_data)
                lat = gps_msg.latitude
                lng = gps_msg.longitude
                return (lat,lng)
            else:
                return None
        else:
            return None


#Loop
if __name__ == "__main__":


    # access serial port GPS 
    gps_port = "/dev/ttyACM0"
    ser = port_setup(gps_port)

    # Print out GPS cordinates
    print("GPS coordinate Stream:")
    while True:
        try:
            #Distance detection
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            status = object_detection (dist)
            print ("status adalah : ", status)
            
            #Sound output
            if status == 'bahaya':
                sound1.play ()
            if status == 'sangat bahaya':
                sound2.play ()
            #Gap time for sound 
            time.sleep(1)
            
            
            #Firebase storage setup
            storage = firebase.storage()
            database = firebase.database()
            
            #Distance Storage push
            database.child("Jarak")
            data = {"distance": dist ,                  
                    "keadaan" : status}
            database.set(data)
            database.child("storage jarak")
            database.push(data)
            time.sleep(1)
            
            #Position Storage Push
            gps_coords = parseGPSdata(ser)
            if gps_coords is None:  # if no valid data was received
                print("No Data")
            else:
                print(f"latitude: {gps_coords[0]} , longitude: {gps_coords[1]} ")
                database.child("Lokasi")
                dt = {"lokasi" : (f"http://maps.google.com/?q={gps_coords[0]},{gps_coords[1]}")}
                database.set(dt)
                database.child("Storage Lokasi")
                database.push(dt)

        except serial.SerialException as e:  # catch any serial communication errors
            print(f"\nERROR: {e}")
            print("... reconnecting to serial\n")
            ser = port_setup()

        except KeyboardInterrupt as e:  # Catch when user hits Ctrl-C and end program
            print("--- Program shutting down ---")
            break

