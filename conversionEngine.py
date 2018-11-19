import threading
import cv2
import numpy as np
import base64
import queue
import os
import time

def extractFrames():
	# globals
	outputDir    = 'frames'
	clipFileName = 'clip.mp4'
	# initialize frame count
	count = 0

	# open the video clip
	vidcap = cv2.VideoCapture(clipFileName)

	# create the output directory if it doesn't exist
	if not os.path.exists(outputDir):
	  print("Output directory {} didn't exist, creating".format(outputDir))
	  os.makedirs(outputDir)

	# read one frame
	success,image = vidcap.read()

	print("Reading frame {} {} ".format(count, success))
	while success:

	  # write the current frame out as a jpeg image
	  cv2.imwrite("{}/frame_{:04d}.jpg".format(outputDir, count), image)   
	  success,image = vidcap.read()
	  print('Reading frame {}'.format(count))
	  count += 1


def convertFrames():
	# globals
	outputDir    = 'frames'

	# initialize frame count
	count = 0

	# get the next frame file name
	inFileName = "{}/frame_{:04d}.jpg".format(outputDir, count)

	# load the next file
	inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)

	while inputFrame is not None:
	    print("Converting frame {}".format(count))

	    # convert the image to grayscale
	    grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
	    
	    # generate output file name
	    outFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

	    # write output file
	    cv2.imwrite(outFileName, grayscaleFrame)

	    count += 1

	    # generate input file name for the next frame
	    inFileName = "{}/frame_{:04d}.jpg".format(outputDir, count)

	    # load the next frame
	    inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)



def displayFrames():
	# globals
	outputDir    = 'frames'
	frameDelay   = 42       # the answer to everything

	# initialize frame count
	count = 0

	startTime = time.time()

	# Generate the filename for the first frame 
	frameFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

	# load the frame
	frame = cv2.imread(frameFileName)

	while frame is not None:
	    
	    print("Displaying frame {}".format(count))
	    # Display the frame in a window called "Video"
	    cv2.imshow("Video", frame)

	    # compute the amount of time that has elapsed
	    # while the frame was processed
	    elapsedTime = int((time.time() - startTime) * 1000)
	    print("Time to process frame {} ms".format(elapsedTime))
	    
	    # determine the amount of time to wait, also
	    # make sure we don't go into negative time
	    timeToWait = max(1, frameDelay - elapsedTime)

	    # Wait for 42 ms and check if the user wants to quit
	    if cv2.waitKey(timeToWait) and 0xFF == ord("q"):
	        break    

	    # get the start time for processing the next frame
	    startTime = time.time()
	    
	    # get the next frame filename
	    count += 1
	    frameFileName = "{}/grayscale_{:04d}.jpg".format(outputDir, count)

	    # Read the next frame file
	    frame = cv2.imread(frameFileName)



# filename of clip to load
filename = 'clip.mp4'

#initialize the threads
extract = threading.Thread(target=extractFrames, args=())
convert = threading.Thread(target=convertFrames, args=())
display = threading.Thread(target=displayFrames, args=())

#start the threads
extract.start()
convert.start()
display.start()
#join the threads
extract.join()
convert.join()
display.join()

print("Finished displaying all frames")
    # cleanup the windows
cv2.destroyAllWindows()