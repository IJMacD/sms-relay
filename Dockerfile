FROM ubuntu:24.04
RUN apt-get update && apt-get install -y apprise
COPY udp_listener.py /app/udp_listener.py
CMD ["python3", "/app/udp_listener.py"]