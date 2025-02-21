import os

# -c 3 --> sends 3 ping requests
# -W 3 --> waits 3 seconds before ping request times out 

ping_cmd = "ping -c 3 -W 3 192.168.0.250"  # Linux

ret = os.system(ping_cmd)

if ret != 0:
    print("Left cam not connected")
else:
    print("Left cam connected")