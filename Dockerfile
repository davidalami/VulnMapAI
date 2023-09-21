FROM python:3.8-slim

# Install nmap
RUN apt-get update && apt-get install -y nmap && apt-get clean

# Install python-nmap
RUN pip install python-nmap

# Copy your Python script into the container
COPY main.py /app/

# Set the working directory
WORKDIR /app

# Set the script as the entrypoint
ENTRYPOINT ["python", "/app/main.py"]
