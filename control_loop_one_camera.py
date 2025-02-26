import subprocess
import signal
import time
import RPi.GPIO as GPIO
import threading
import logging
from pathlib import Path
from datetime import datetime
import os

from pump.pump_system import pump_system

# Interrupts gstreamer processes after given hours. Runs in background.
def delayed_interrupt_gstreamer(hours):
    def delayed_execution():
        time.sleep(hours * 60)  # Convert hours to seconds -- UPDATE: changed 3600 to 60 for testing purposes
        subprocess.Popen(["./cam/interrupt_gstreamer.sh"])

    thread = threading.Thread(target=delayed_execution)
    thread.daemon = True
    thread.start()

# 1st Button Switch Crude Power On/Power Off
# 2nd Button Toggle Camera Preview and Start Recording
# 3rd Graceful emergency shutoff

class smalle():
    def __init__(self, directory, preview_time, deployment_time):
        # CONFIGURATION VARIABLES
        self.logintro = "Location Date Smalle #."
        self.dirname = f"recordings/{directory}"
        self.dirname = self.check_and_update_dir(self.dirname)
        self.preview_state = preview_time               # minutes to stay in preview state before starting record
        self.deployment_duration = deployment_time      # in hours -- update: changed from 11 to 1 for testing purposes

    def check_and_update_dir(self, dirname):
        i = 1
        new_dirname = dirname
        while True:
            if not Path(new_dirname).exists():
                break
            new_dirname = f"{dirname}_{i}"
            i += 1
        return new_dirname
    
    def check_camera_connectivity(self, ip):
        # -c 3 --> sends 3 ping requests
        # -W 3 --> waits 3 seconds before ping request times out 
        ping_cmd = f"ping -c 3 -W 3 {ip}"
        ret = os.system(ping_cmd)

        if (ret == 0):
            return True
        return False
        
    def camera_preview_state(self, preview):
        print("Preview Mode")
        # Hold in preview mode for the time specified in the setup parameter       
        time.sleep(60 * self.preview_state)
        subprocess.Popen(["./cam/interrupt_gstreamer.sh"])
        preview.wait()

    def run(self):
    # Set Time
        rtc_process = subprocess.Popen(['python3', './rtc/nano_setTimeRTC.py'])
        time.sleep(2)

        if (self.check_camera_connectivity('192.168.0.250')):
            print("Left camera detected")

            # Preview State
            preview_proc = subprocess.Popen(["./cam/cams_preview_left.sh"])
            self.camera_preview_state(preview_proc)

            print("Transitioning to record mode")
            # Recording State
            self.recording_process = subprocess.Popen(["./cam/cams_recording_left.sh", self.dirname])
            
        elif (self.check_camera_connectivity('192.168.0.251')):
            print("Right camera detected")

            # Preview State
            preview_proc = subprocess.Popen(["./cam/cams_preview_right.sh"])
            self.camera_preview_state(preview_proc)

            print("Transitioning to record mode")
            # Recording State
            self.recording_process = subprocess.Popen(["./cam/cams_recording_right.sh", self.dirname])

        else: 
            print("No camera detected")
            exit(0)

        # Run commands to shutoff display in record mode 
        subprocess.run(["xset", "-display", ":0.0", "dpms", "force", "off"])

        # Thread in background that waits for the set deployment duration, which after interrupts the recording process
        delayed_interrupt_gstreamer(self.deployment_duration)

	# Configure logging - don't log until after Preview mode
        # Get the current date and time and format the date and time from JetsonOS for log file name
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H.%M.%S")
        log_directory = Path("logs")
        log_directory.mkdir(parents=True, exist_ok=True)
        logfile =  log_directory / f"LOG_{formatted_datetime}.log"
        logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        current_datetime = datetime.now()
        logging.info("\n*******" + self.logintro)
        logging.info('Transitioning to record mode')
        logging.info(current_datetime)
        logging.info("Writing to directory " + self.dirname)
        
        # Waits until recording process ends. delayed_interrupt_gstreamer will interrupt the process.
        self.recording_process.wait()
	
        subprocess.run(["xset", "-display", ":0.0", "dpms", "force", "on"])
        current_datetime = datetime.now()
        logging.info(self.logintro)
        logging.info('Ending record mode')
        logging.info(current_datetime)


# driver code
if __name__ == '__main__':
    video_directory = input("Enter name of folder to store recordings in: ")
    preview_time = int(input("Enter preview duration (in minutes): "))
    deployment_time = int(input("Enter deployment duration (in hours): "))
    s = smalle(video_directory, preview_time, deployment_time)
    s.run()
