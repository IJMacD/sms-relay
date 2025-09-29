FROM python:3.9.20-slim
WORKDIR /app
COPY requirements.txt /app
RUN ["pip", "install", "-r", "requirements.txt"]
COPY udp_listener.py /app
CMD ["python", "udp_listener.py"]