import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import argparse
import threading


def add_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", action='store', dest='guest_name', help='Store Guest Name')
    parser.add_argument("-c", "--channel", action='store', dest='channel_name', help='Store Channel Name')
    return parser.parse_args()
    # print(results)

 
# The callback for when the client receives a CONNACK response from the server.
# def on_connect(guest,channel):
def on_connect(client, userdata, flags, rc):
    results = add_arguments()

    print("Welcome " + results.guest_name + "!")
    print("It is connected")
    
    client.subscribe("DusanTopic2/" + results.channel_name)
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    results = add_arguments()
    # print(results.guest_name + ": " + str(msg.payload).replace("'", ""))
    msg_value_ar = str(msg.payload).split('|')

    print(msg_value_ar[0][2:] + ": " + msg_value_ar[1][:-1])

    if msg.payload == "What":
        print(results.guest_name + ": " + str(msg.payload))


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)
results = add_arguments()

# Run client loop in deamon
thread = threading.Thread(target=client.loop_forever, args=())
thread.daemon = True                            # Daemonize thread
thread.start()  

while True:
    guest_message = input()
    publish.single("DusanTopic2/" + results.channel_name, results.guest_name + "|" + guest_message, hostname="test.mosquitto.org")



 

