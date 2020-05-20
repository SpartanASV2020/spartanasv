#streaming both cameras to web browser 

 

from imutils.video import VideoStream 

from flask import Response 

from flask import Flask 

from flask import render_template 

import threading 

import argparse 

import datetime 

import imutils 

import time 

import cv2 

import gps 

import numpy as np 

#Init gps session 

#session = gps.gps("localhost", "2947") 

#session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE) 

  

#Create output frame 

#Create lock to ensure thread-safe 

outputFrame = None 

lock = threading.Lock() 

 

#Init Flask 

app = Flask(__name__) 

 

#Init videostream through imutils 

webcam2 = VideoStream(src=2).start() 

vs = VideoStream(src=0).start() 

time.sleep(2.0) 

 

#Simple Flask app 

@app.route("/") 

def index(): 

# return the rendered template 

return render_template("index.html") 

 

 

def gps_embed(frameCount): 

# grab global references to the video stream, output frame, and 

# lock variables 

global vs, webcam2, outputFrame, lock, session 

 

# loop over frames from the video stream 

while True: 

# read the next frame from the video stream, resize it, 

# convert the frame to grayscale, and blur it 

frame1 = vs.read() 

frame1 = imutils.resize(frame1, width=400) 

frame2 = webcam2.read() 

frame2 = imutils.resize(frame2, width=400) 

frame = np.concatenate((frame1, frame2), axis=0) 

# grab the current timestamp and draw it on the frame 

timestamp = datetime.datetime.now() 

cv2.putText(frame, timestamp.strftime( 

"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), 

cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1) 

# attemp to read gps 

#try: 

#report = session.next() 

# Wait for a 'TPV' report and display the current time 

# To see all report data, uncomment the line below 

#print(report) 

#if report['class'] == 'TPV': 

#if hasattr(report, 'time'): 

#gps_test = ("Lat: {}; Lon: {}".format((lambda: str(('{:06.3f}'.format(report.lat)))+"N", lambda: str(('{:06.2f}'.format(-report.lat)))+"S")[0 > report.lat]() 

#, (lambda: str(('{:06.3f}'.format(report.lon)))+"E", lambda: str(('{:06.2f}'.format(-report.lon)))+"W")[0 > report.lon]())) 

#cv2.putText(frame, gps_test, (10, 15), 

#cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1) 

#except KeyError: 

#pass 

# acquire the lock, set the output frame, and release the 

# lock 

with lock: 

outputFrame = frame.copy() 

def generate(): 

# Take global frame and lock 

global outputFrame, lock 

# Grab frame-by-frame 

while True: 

# Wait to get lock 

with lock: 

# Simple check for frame 

if outputFrame is None: 

continue 

# Encode frame into jpg 

(flag, encodedImage) = cv2.imencode(".jpg", outputFrame) 

# Simple quality check 

if not flag: 

continue 

# Translate into byte format 

yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +  

bytearray(encodedImage) + b'\r\n') 

 

@app.route("/video_feed") 

def video_feed(): 

# return the response generated along with the specific media 

# type (mime type) 

return Response(generate(), 

mimetype = "multipart/x-mixed-replace; boundary=frame") 

 

 

# check to see if this is the main thread of execution 

if __name__ == '__main__': 

# construct the argument parser and parse command line arguments 

ap = argparse.ArgumentParser() 

ap.add_argument("-i", "--ip", type=str, required=True, 

help="ip address of the device") 

ap.add_argument("-o", "--port", type=int, required=True, 

help="ephemeral port number of the server (1024 to 65535)") 

ap.add_argument("-f", "--frame-count", type=int, default=32, 

help="# of frames used to construct the background model") 

args = vars(ap.parse_args()) 

# start a thread that will get gps data and add it in the frame 

t = threading.Thread(target=gps_embed, args=( 

args["frame_count"],)) 

t.daemon = True 

t.start() 

 

# start the flask app 

app.run(host=args["ip"], port=args["port"], debug=True, 

threaded=True, use_reloader=False) 

# release the video stream pointer 

vs.stop() 