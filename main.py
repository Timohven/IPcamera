#import numpy as np
import cv2
import glob
import os

TIMEOUT, FREQUENCY, CURRENTFRAME = 0, 0, 0
USER, PASS,IP, PORT, ADDRESS = '', '', '', '', ''
def makeOSsettings():
    my_cwd = os.getcwd()
    new_dir = 'frames'
    path = os.path.join(my_cwd, new_dir)
    if os.path.exists(path):
        print(f'Folder {path} already exists')
    else:
        os.mkdir(path)
    print(path)
    return path

def makeSettings():
    global TIMEOUT, FREQUENCY, USER, PASS, IP, ADDRESS, PORT, CURRENTFRAME
    with open('settings.txt', 'r') as f:
        lines = f.readlines()
    USER = lines[0].split()[1]
    PASS = lines[1].split()[1]
    IP = lines[2].split()[1]
    PORT = lines[3].split()[1]
    ADDRESS = lines[4].split()[1]
    TIMEOUT = int(lines[5].split()[1]) # in min
    FREQUENCY = int(lines[6].split()[1]) # frame per min
    CURRENTFRAME = int(lines[7].split()[1])

makeSettings()
cap = cv2.VideoCapture(0)
cap.open(f"rtsp://{USER}:@{IP}:{PORT}/{ADDRESS}")
if not cap.isOpened():
    print("Cannot open camera")
    exit()
path = makeOSsettings()
count = 0
fps = cap.get(cv2.CAP_PROP_FPS)
print(f'current FPS: {fps}')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        exit()
    # Our operations on the frame come here
    # Display the resulting frame
    cv2.imshow('Cam1', frame)
    curFrame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    if curFrame%((60*fps)/FREQUENCY) == 0: # 2 frames per min
        # save frames
        cv2.imwrite(f'{path}\\frame{CURRENTFRAME:04}.jpg', frame)
        print(f'current {count}th frame saved in file frame{CURRENTFRAME:04}.jpg')
        CURRENTFRAME += 1

    count += 1
    if (cv2.waitKey(1) & 0xFF == ord('q') or (CURRENTFRAME == TIMEOUT*2)):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# save video
# img_array = []
# for filename in glob.glob(f'{path}\\*.jpg'):
#    img = cv2.imread(filename)
#    height, width, layers = img.shape
#    size = (width,height)
#    img_array.append(img)
#
# out = cv2.VideoWriter(f'{path}\\video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
#
# for i in range(len(img_array)):
#    out.write(img_array[i])
# out.release()