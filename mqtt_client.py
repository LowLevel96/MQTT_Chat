import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import argparse
import threading
import curses
from curses import wrapper, textpad

# Global Variables
guest_name = ""
channel_name = ""
pad = None
x = 0
y = 0

def add_arguments():
    global guest_name, channel_name
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", action='store', dest='guest_name', help='Store Guest Name')
    parser.add_argument("-c", "--channel", action='store', dest='channel_name', help='Store Channel Name')

    guest_name = parser.parse_args().guest_name
    channel_name = parser.parse_args().channel_name

def on_connect(client, userdata, flags, rc):
    results = add_arguments()
    
    client.subscribe("DusanTopic2/" + channel_name)
 
def on_message(client, userdata, msg):
    global pad

    msg_value_ar = str(msg.payload).split('|')
    # print("OK")

    # stdscr.addstr(y-2, x+3, "                           ")
    # stdscr.refresh()
    
    
    if msg_value_ar[0][2:] == guest_name:
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        pad.addstr(msg_value_ar[0][2:], curses.color_pair(1))
    else:
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        pad.addstr(msg_value_ar[0][2:], curses.color_pair(2))

    
    pad.addstr(": " + msg_value_ar[1][:-1] + "\n")
    pad.refresh(0,0, 7,15, 28, int(x/3 + x+x/2-2))

def handle_mqtt():

    client = mqtt.Client()
   
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)

    # Run client loop in deamon
    thread = threading.Thread(target=client.loop_forever, args=())
    thread.daemon = True                            # Daemonize thread
    thread.start()

    # while True:
    #     guest_message = input()
    #     publish.single("DusanTopic2/" + results.channel_name, results.guest_name + "|" + guest_message, hostname="test.mosquitto.org")
   

# stdscr = curses.initscr()

def messages_screen(stdscr):
    global pad

    pad = curses.newpad(8, int(x/3 + x+x/2-2))

    # pad.addstr("In PAD definition")
    # pad.refresh( 0, 0, 7, 15, 28, int(x/3 + x+x/2-2))
    
    # curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    # pad.bkgd(' ', curses.color_pair(1))

    pad.scrollok(1)

    ncols = int(x+x/2)
    ulx = int(x/3)

    textpad.rectangle(stdscr, y+3, ulx-1, 15, ulx + ncols)
    



    
def test_textpad(x, y, stdscr, insert_mode=False):
    ncols, nlines = int(x+x/2), 1
    uly, ulx = y, int(x/3)

    win = curses.newwin(nlines, ncols, uly, ulx)
    textpad.rectangle(stdscr, uly-1, ulx-1, uly + nlines, ulx + ncols)
    stdscr.refresh()

    
    
    return textpad, win

    # stdscr.addstr(uly-2, ulx, 'Press any key to write again.')
    # stdscr.addstr(uly-2, ulx, '                                     ')

    # return contents

def main(stdscr):

    global pad, x, y
    

    add_arguments()
    handle_mqtt()

    stdscr.clear()

    x, y = stdscr.getmaxyx()
    y=int(stdscr.getmaxyx()[0] / 7)
    x=int(stdscr.getmaxyx()[1] / 2 - 2)

    messages_screen(stdscr)


    stdscr.addstr(y-2, x+3, "LowChat")
    stdscr.addstr(y, x, "Welcome " + channel_name)

    textpad, win = test_textpad(x, y*7-2, stdscr, True)

    while True:
        # messages_screen(y, x, stdscr)
        box = textpad.Textbox(win, True)
        contents = box.edit()
        win.clear()
        stdscr.refresh()

        # pad.addstr(contents + "\n")
        # pad.refresh( 0,0, 7,15, 28, int(x/3 + x+x/2-2))

        publish.single("DusanTopic2/" + channel_name, guest_name + "|" + contents, hostname="test.mosquitto.org")

    stdscr.refresh()
    stdscr.getkey()
    

wrapper(main)


# def main():
    

# if __name__ == "__main__":
#     main()


