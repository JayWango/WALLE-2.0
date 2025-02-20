#!/bin/bash

gst-launch-1.0 -e rtspsrc location=rtsp://192.168.0.250:554/h264 ! rtph264depay ! h264parse ! nvv4l2decoder enable-max-performance=1 ! nvvidconv ! 'video/x-raw, format=BGRx, width=480, height=270' ! nvvidconv ! videoscale ! video/x-raw, width=480, height=270 ! ximagesink
