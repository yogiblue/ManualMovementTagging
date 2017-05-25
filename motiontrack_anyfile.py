# Use manual tagging of movement frame by frame
# press x to step through the video frame by frame
# records the mouse position for each frame
# click the mouse to put an empty line in the file
# NOTE, it's all a bit hard coded because only I'm using it currently

import globals

import os
import datetime

import numpy as np
import cv2

from Tkinter import Tk
from tkFileDialog import askopenfilename
from scipy import ndimage


def mouse_callback(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        print x,y
        fd.write("0000, 0, 0\n")
        globals.currentx = x
        globals.currenty = y
    elif event==cv2.EVENT_MOUSEMOVE:
        #print x,y
        globals.currentx = x
        globals.currenty = y

def main():
    print "Doing motion tracking on a single video...."

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    # user selects a file in a directory of videos
    # the python script then knows where to process files
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)


    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


    # print os.path.basename(filename)
    # print os.path.dirname(filename)

    # go to the directory
    os.chdir(os.path.dirname(filename))

    simpleFile = os.path.basename(filename)

    # just in case we want to delay processing for when we are asleep
    #sleep(43200)


    global fd
    fd = open(simpleFile[:len(simpleFile)-4] + '.csv','a')

    #fd.write('Date, Total sum, All pixels, All>100, All>200, All>240\n')
    fd.write('Time, xcord, ycord\n')

    f = simpleFile

    print "Doing " + f

    #datetimeString = f[startpos:endpos]
    #date_object = datetime.datetime.strptime(datetimeString, fmt)

    date_object = datetime.datetime(2017,1,1,0,0)

    print date_object

    # open the video processing stuff
    cap = cv2.VideoCapture(f)
    if cv2.__version__=='2.4.6':
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
    else:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_blobs.avi',fourcc, 20.0, (640,480))

    count = 0
    timeVideo = 0

    #print cv2.__version__

    if int(major_ver)  < 3 :
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
    else :
        fps = cap.get(cv2.CAP_PROP_FPS)
        print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)

    #extract the background
    if cv2.__version__=='2.4.6':
        print "Using opencv2 version 2.4.6"
        fgbg = cv2.BackgroundSubtractorMOG()
    elif cv2.__version__=='3.0.0':
        print "Using opencv2 version 3.0.0"
        fgbg = cv2.createBackgroundSubtractorKNN()
    else:
        print "Using opencv2 untested version "
        fgbg = cv2.createBackgroundSubtractorKNN()

    width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)   # float
    height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT) # float

    print width, " ", height

    xsize = int(width)
    ysize = int(height)

    speed = 0
    print "speed is ", speed
    #cv2.namedWindow("video")
    #xsize = 640
    #ysize = 480

    # set up an array for tracking
    track_res = np.zeros((ysize, xsize), dtype=np.uint8)
    track_res.astype(int)
    track_res_total = np.zeros((ysize, xsize), dtype=np.uint8)
    track_res_total.astype(int)

    track_res_trim = track_res
    #create some empty image arrays
    dilated_image = track_res_trim
    blurred_image = track_res_trim
    #average_image = track_res_trim
    average_image = np.zeros((ysize, xsize, 3), dtype=np.uint8)
    average_image.astype(int)
    bt = average_image
    avg_image_write_count = 0


    # initialise variables
    count = 0
    img_count = 0
    img_write = 0
    frame_count = 0

    while(cap.isOpened()):

        # read the frame
        ret, frame1 = cap.read()

        #if count==0:
            #average_image = frame1
            #low_values_indices = average_image >= 0
            #average_image[low_values_indices] = 0
            #bt = average_image

        if ret==False:
            print "End of video"
            break;

        # show the result array as a frame - nice to look at
        cv2.putText(frame1, str(date_object), (50,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,255,255))
        #incrementing the time depends on the frames per second and how the frequency
        #of the recording of those frames - so it's not so straightforward
        #date_object = date_object + datetime.timedelta(0,0,333333)
        date_object = date_object + datetime.timedelta(0,0,1000000/fps)

        # move on
        k = cv2.waitKey(speed)


        if k & 0xFF == ord('q'):
            break

        if k & 0xFF == ord('x'):
            if speed==0:
                speed=int(fps)
            else:
                speed=0
        #print globals.currentx,globals.currenty

        cv2.imshow('video',frame1)
        if count==0:
            cv2.setMouseCallback("video", mouse_callback)

        if frame_count==1:
            #print("here")
            fd.write(str(date_object))
            fd.write(',')
            fd.write(str(globals.currentx))
            fd.write(',')
            fd.write(str(globals.currenty))
            fd.write('\n')
            speed = 0
            frame_count=0

        frame_count=frame_count + 1

        count = count + 1
        img_write = img_write + 1
        #cv2.imshow('trackres', track_res_total)


    # the end
    if exit == True:
        print "Quitting analysis"

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print "Finished"
    # end
    fd.close()



if __name__=="__main__":
    main()
