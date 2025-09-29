import os
import socket
import re
import apprise

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
            print("-----")
            print("SMS Received:")
            print("-----")

            if apobj:
                apobj.notify(title="SMS Received", body=parts[1])
        
        # Decode the received data and print the message and sender's address
        print(f"Received from {address}: {string}", end="")
    
        # parts = re.split(r"servicecell:", string)
        # if len(parts) == 2:
        #     print("-----")
        #     print("Service Cell Info:")
        #     print(parts[1])
        #     print("-----")

        #     if apobj:
        #         apobj.notify(title="Service Cell Info", body=parts[1])
            