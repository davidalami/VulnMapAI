# Use appropriate base image
FROM quantumcrack/vulnmapai-base:0.1 as base

# Copy scripts into the container
WORKDIR /app
COPY advising ./advising
COPY exploit ./exploit
COPY orchestration ./orchestration
COPY recon ./recon
COPY report ./report
COPY resources ./resources
COPY utils ./utils
COPY webapp ./webapp
COPY config.py .
COPY constants.py .
COPY main.py .
COPY requirements.txt .

# Install Python libraries
RUN python -m pip install -r requirements.txt

# Set the script as the entrypoint
ENTRYPOINT ["python", "/app/main.py"]

FROM base as test

# copy the test files
COPY tests ./tests

# run pytest tests
RUN pytest -svv

# Go back to the base image
FROM base as prod

