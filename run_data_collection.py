import os
import time

import cv2
from pynput import keyboard
import numpy as np
from mss import mss

key_pressed = []


def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        key_pressed.append(key.char)
        print(key_pressed)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    print('{0} released'.format(key))
    if key.char == 'q':
        return False
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def open_file(f_name):
    if os.path.isfile(f_name):
        print('File exists, loading previous data!')
        t_data = list(np.load(f_name, allow_pickle=True))
        return t_data
    else:
        print('File does not exist, starting fresh!')
        return []


def count_down(seconds):
    for i in list(range(seconds - 1))[::-1]:
        print(i + 1)
        time.sleep(1)


def record(keys_list, training_data_storage, training_file_name):

    mon = {'top': 0, 'left': 0, 'width': 1650, 'height': 1000}
    with mss() as sct:
        # mon = sct.monitors[0]
        print(keys_list)
        try:
            if keys_list[0] == 'q':
                cv2.destroyAllWindows()
                return
        except Exception:
            print("key is empty!")

        last_time = time.time()
        img = sct.grab(mon)

        print('fps: {0}'.format(1 / (time.time()-last_time)))
        np_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        processed_img = cv2.resize(np_img, (165, 100))
        try:
            training_data_storage.append((processed_img, keys_list[0]))
        except Exception:
            print("frame is skipped!")
            pass

        # if len(screen_data) % 50 == 0:
        np.save(training_file_name, training_data_storage)

        # if cv2.waitKey(25) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break
        key_pressed.clear()


if __name__ == "__main__":
    file_name = 'test.npy'
    training_data = open_file(f_name=file_name)
    count_down(5)
    while True:
        keyboard.Listener(on_press=on_press, on_release=on_release).start()
        record(key_pressed, training_data_storage=training_data, training_file_name=file_name)