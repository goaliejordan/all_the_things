import os
import time

import ImageGrab

# Globals
# ------------------

x_pad = 156
y_pad = 345

def screenGrab():
    """
     All coordinates assume a screen resolution of 1280x1024, and Chrome 
     maximized with the Bookmarks Toolbar enabled.
     Down key has been hit 4 times to center play area in browser.
     x_pad = 156
     y_pad = 345
     Play area =  x_pad+1, y_pad+1, 796, 825
     """
    box = (x_pad+1, y_pad+1, 796, 825)
    save_directory = os.getcwd()
    time_stamp = int(time.time())
    image_file_name = '{}\\full_snap__{}.png'.format(save_directory, time_stamp)
    im = ImageGrab.grab(box)
    im.save(image_file_name, 'PNG')


def main():
    screenGrab()


if __name__ == '__main__':
    main()





