from datetime import datetime
import re
import sys
import threading
import time

# input_file = sys.stdin
input_file = open("sample2.txt")

sms_parts = ""

def assemble_parts():
    global sms_parts
    try:
        print("---\nMulti SMS Received:\n---")
        byte_string = bytes.fromhex(sms_parts)
        print(byte_string.decode())
        sms_parts = ""
    except:
        print(sms_parts)

for line in input_file:
    line = line.replace("\\n", "\n")

    parts = re.split(r"sms =", line)
    if len(parts) == 2:

        data = re.split(r"\n\+", parts[1])

        msg = data[0].strip()

        if re.match(r"[0-9A-F]+", msg):
            if len(msg) % 2 == 1:
                # msg = msg[:-1]
                print("bad_part")
                continue

            if len(sms_parts) == 0:
                timer = threading.Timer(10.0, assemble_parts)
                timer.start()

            sms_parts = sms_parts + msg

        else:
            print("---\nSingle SMS Received:\n---")
            print(msg)

time.sleep(20)
