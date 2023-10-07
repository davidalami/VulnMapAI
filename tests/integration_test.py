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
    """
    Test the startup of the server by running a Python script in the background.

    The test performs the following steps:
    1. Initiates the server by running 'main.py' script with '127.0.0.1' as an argument.
    2. Waits for an initial duration to account for any startup delay.
    3. Checks for 60 seconds to see if the server starts and becomes accessible on '127.0.0.1:1337'.
    4. If the server starts within the duration, the test is considered successful.
    5. If the server doesn't start within 60 seconds, or if the Python script encounters an issue,
       the test is marked as failed.

    Returns:
        None. If the server doesn't start as expected, an assertion error is raised.
    """
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

