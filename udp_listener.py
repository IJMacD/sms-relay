import os
import socket
import re
import apprise
import threading

sms_parts = []

def assemble_parts():
    global sms_parts, apobj
    content = "".join(sms_parts)
    sms_parts = []

    print("---\nSMS Received:\n---")
    print(content)

    if apobj:
        apobj.notify(title="SMS Received", body=content)


# Define the host and port
# '' means listening on all available network interfaces
HOST = ''
PORT = 555

# Use whitespace or comma to separate
apprise_urls = os.environ.get("APPRISE_URLS")

if apprise_urls:
    apobj = apprise.Apprise()
    l = re.split(r"\s|,", apprise_urls)
    ok = apobj.add(l)
    if ok:
        print("Added", len(l), "apprise", "url" if len(l) == 1 else "urls")

# Create a UDP socket
# AF_INET specifies the IPv4 address family
# SOCK_DGRAM specifies that it is a UDP socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    # Bind the socket to the host and port
    s.bind((HOST, PORT))

    print(f"UDP server listening on port {PORT}...")

    while True:
        # Wait for data to arrive
        # The buffer size of 1024 bytes specifies the maximum amount of data to be received at once
        data, address = s.recvfrom(1024)

        string = data.decode('utf-8')

        parts = re.split(r"sms =", string)
        if len(parts) == 2:
            # Ignore message format part that starts with + on newline
            data = re.split(r"\n\+", parts[1])

            msg = data[0].strip()

            if re.match(r"[0-9A-F]+", msg):
                if len(sms_parts) == 0:
                    timer = threading.Timer(10.0, assemble_parts)
                    timer.start()

                if len(msg) % 2 == 1:
                    # Message definitely has some corruption
                    print(f"Corrupt message part found. Length={len(msg)}")
                    msg = msg[:-1]

                byte_data = bytes.fromhex(msg)
                sms_parts.append(byte_data.decode())
            else:
                print("---\nSMS Received:\n---")
                print(msg)

                if apobj:
                    apobj.notify(title="SMS Received", body=msg)

        # Decode the received data and print the message and sender's address
        # print(f"Received from {address}: {string}", end="")
        print(string, end="")
