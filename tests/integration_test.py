import pytest
import socket
import subprocess
import time


def is_port_open(host, port, timeout=1):
    """Check if a given port is open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            return True
        except socket.error:
            return False


def test_server_start():
    # Run the python script in the background
    process = subprocess.Popen(["python", "main.py", "127.0.0.1"])

    # Give an initial delay, assuming the server might not start instantly
    time.sleep(2)

    # Check if the server starts within 60 seconds
    for _ in range(60):
        if is_port_open("127.0.0.1", 1337):
            # If server started, end the test as successful
            process.terminate()
            return

        time.sleep(1)

    # If the server didn't start within 60 seconds, or if the python process had a problem
    process.terminate()
    assert False, "Server did not start within 60 seconds or had an error"

