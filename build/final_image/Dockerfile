# Use appropriate base image
FROM quantumcrack/vulnmapai-base:latest

# Copy scripts into the container
WORKDIR /app
COPY . /app/

# Install Python libraries
RUN python -m pip install -r requirements.txt

# Set the script as the entrypoint
ENTRYPOINT ["python", "/app/main.py"]
