#!/bin/bash

# "$1" indicates the first argument passed to the shell script when you run it
dirname=$1

mkdir -p ./"$dirname"
cd ./"$dirname"

gst-launch-1.0 -e rtspsrc location=rtsp://192.168.0.250:554/h264 ! rtph264depay ! h264parse ! nvv4l2decoder enable-max-performance=1 ! \
    nvvidconv ! tee name=t \
    t. ! queue ! autovideosink sync=false \
    t. ! queue ! 'video/x-raw(memory:NVMM), format=RGBA' ! \
        nvvidconv ! 'video/x-raw(memory:NVMM), format=NV12' ! \
        nvv4l2h265enc ! h265parse ! \
        splitmuxsink location=./out_%02d.mp4 max-size-time=1800000000000 sync=true

# 60000000000 ns = 1 minute
# so records for 30 minutes max per call 