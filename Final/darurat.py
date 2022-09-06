#Libraries
import telepot
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
from telepot.loop import MessageLoop
from subprocess import call 

#setting up GPIO for push button
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_Button = 16
GPIO.setup(GPIO_Button, GPIO.IN)
 
#Main Function
def handle(msg):
    global telegramText
    global chat_id
  
    chat_id = msg['chat']['id']
    telegramText = msg['text']
  
    print('Message received from ' + str(chat_id))
  
  #when program started, the main () goes on 
    if telegramText == '/start':
        bot.sendMessage(chat_id, 'My Way siap membantu anda.')#Put your welcome note here

    while True:
        main()
    
           
#bot setting up
bot = telepot.Bot('5502929834:AAHfXiIb3PjLz2RdYOHTNxIOLXg5HdHVi5Y')
bot.message_loop(handle)        

def main():
    
    while GPIO.input(GPIO_Button) == 1:
        print("Pengguna dalam bahaya")
        motion = 1
        sendNotification(motion)
                 
    if GPIO.input(GPIO_Button) == 0:
        print('Pengguna aman')
        
        
#sending infinite notification to telegram
def sendNotification(motion):   
    global chat_id
    if motion == 1:
        bot.sendMessage(chat_id, 'Segera periksa Way-App. Pengguna dalam bahaya !!!')
        time.sleep(5)
        
while 1:
    time.sleep(2)

