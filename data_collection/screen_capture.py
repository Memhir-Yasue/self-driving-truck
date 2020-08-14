import time
import keyboard

import cv2
import numpy as np
from mss import mss


def record():
    mon = {'top': 0, 'left': 0, 'width': 1650, 'height': 1000}
    screen_data = []
    with mss() as sct:
        # mon = sct.monitors[0]
        for i in list(range(9))[::-1]:
            print(i+1)
            time.sleep(1)
        while True:
            key_pressed = keyboard.read_key(True)
            if key_pressed == 'q':
                break
            print(key_pressed)
            last_time = time.time()
            img = sct.grab(mon)
            print('fps: {0}'.format(1 / (time.time()-last_time)))
            np_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
            processed_img = cv2.resize(np_img, (266, 133))
            # processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
            #
            # processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
            # cv2.imshow('test', processed_img)
            screen_data.append((processed_img, key_pressed))
            np.save('screens.npy', screen_data)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


if __name__ == "__main__":
    record()
