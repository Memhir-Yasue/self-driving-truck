from pynput import keyboard
import time


keys_pressed = []


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        keys_pressed[0] = key.char
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
def listen_board():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def listen_keyboard():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

if __name__ == "__main__":
    for i in list(range(9))[::-1]:
        print(i + 1)
        time.sleep(1)
    listen_keyboard()
