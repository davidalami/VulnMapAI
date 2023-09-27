# Use Kali Linux as the base image
FROM kalilinux/kali-rolling

# Avoid tzdata asking for geographic area and timezone
ENV DEBIAN_FRONTEND=noninteractive

# Update and Install Dependencies
RUN apt update \
    && apt install -y --no-install-recommends \
    build-essential \
    wget \
    libssl-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev \
    libreadline-dev \
    zlib1g-dev \
    nmap \
    metasploit-framework \
    inetutils-ping \
    netcat-traditional \
    telnet \
    ftp \
    openvpn \
    tmux \
    kali-linux-default \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and Compile Python 3.8
WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz \
    && tar -xvf Python-3.8.12.tgz \
    && cd Python-3.8.12 \
    && ./configure --enable-optimizations \
    && make altinstall

# Create a symbolic link for python3.8
RUN ln -sf /usr/local/bin/python3.8 /usr/bin/python

# Upgrade pip
RUN python -m ensurepip --default-pip \
    && python -m pip install --upgrade pip

# Copy scripts into the container
WORKDIR /app
COPY . /app/

# Install Python libraries
RUN python -m pip install -r requirements.txt

# Set the script as the entrypoint
ENTRYPOINT ["python", "/app/main.py"]
