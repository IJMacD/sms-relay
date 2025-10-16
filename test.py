import re
import sys
import threading
import time

sms_parts = []

def assemble_parts():
    global sms_parts
    print("---\nSMS Received:\n---")
    print("".join(sms_parts))
    sms_parts = []

for line in sys.stdin:
    line = line.replace("\\n", "\n")

    parts = re.split(r"sms =", line)
    if len(parts) == 2:

        data = re.split(r"\n\+", parts[1])

        try:
            byte_data = bytes.fromhex(data[0])

            if len(sms_parts) == 0:
                timer = threading.Timer(10.0, assemble_parts)
                timer.start()

            sms_parts.append(byte_data.decode())
        except ValueError:
            print("---\nSMS Received:\n---")
            print(data[0])

time.sleep(20)
