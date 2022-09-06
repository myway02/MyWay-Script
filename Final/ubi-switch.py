#Libraries
import paho.mqtt.client as paho
from paho import mqtt
from relay import set_relay
from pygame import mixer

# mendefinisikan variable
# broker = "localhost" # for local connection
broker = "industrial.api.ubidots.com"  # for online version
port = 1883
timeout = 60

##Sound setting up
#Initialize Mixer / turning on sound
mixer.init ()
pulang = mixer.Sound ("panggil.wav")

#Ubidots User & Pass setup
username = 'BBFF-DyvbwMnFx0yHw3RO0p4ZcvkoGIGZox'
password = 'BBFF-DyvbwMnFx0yHw3RO0p4ZcvkoGIGZox'


## subscribing topic for Ubidots
#relay_topic = '/v1.6/devices/test_device/relay/lv' 
#servo_topic = '/v1.6/devices/test_device/servo/lv'
switch_topic = '/v1.6/devices/myway/tombol_panggil/lv'


 
# waiting for callback 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe(relay_topic)
    #client.subscribe(servo_topic)
    client.subscribe(switch_topic)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload.decode('utf-8')))
    payload_decoded = msg.payload.decode('utf-8')

    #if msg.topic == relay_topic:
        #if float(payload_decoded) == 0.0:
            #print("matikan relay")
            #set_relay("low")
        #if float(payload_decoded) == 1.0:
            #print("nyalakan relay")
            #set_relay("high")

    #if msg.topic == servo_topic:
     #   if float(payload_decoded) == 0.0:
            #print("matikan servo")
      #  if float(payload_decoded) == 1.0:
       #     print("nyalakan servo")
            
     #Main       
    if msg.topic == switch_topic:
        print ('dipanggil tuh !!!')
        pulang.play ()
        
        
# Create an MQTT client and attach our routines to it.
client = paho.Client()
# client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(username=username,password=password)
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(broker, port, timeout)

client.loop_forever()
