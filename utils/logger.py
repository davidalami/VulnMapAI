import logging

class Logger:

    def __init__(self, name, log_level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Create a file handler for writing log files
        log_file_path = 'runtime.log'
        file_handler = logging.FileHandler(log_file_path)

        # Create a console handler for printing logs to the console
        console_handler = logging.StreamHandler()

        # Create a formatter and set it for both handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add both handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
