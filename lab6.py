import os
import logging
from functools import wraps


class FileNotFound(Exception):
    """Custom exception raised when the expected file cannot be found."""
    pass


class FileCorrupted(Exception):
    """Custom exception raised when the file is corrupted or unreadable."""
    pass


def logged(exc_type, mode="console"):
    """
    Decorator that logs exceptions of a specific type.

    Parameters:
        exc_type: The type of exception that triggers logging.
        mode (str): Logging mode. 
                    "console" → logs to console,
                    "file" → logs to 'file_operations.log'.

    The decorator wraps a function and logs any specified exception
    using Python's logging module, then re-raises the exception.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exc_type as e:
                logger = logging.getLogger(func.__name__)
                logger.setLevel(logging.ERROR)

                # Determine the logging target
                if mode == "console":
                    handler = logging.StreamHandler()
                elif mode == "file":
                    handler = logging.FileHandler("file_operations.log", encoding="utf-8")
                else:
                    raise ValueError("Unknown logging mode")

                # Format for log messages
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                handler.setFormatter(formatter)

                # Attach handler, log the error, then detach handler
                logger.addHandler(handler)
                logger.error(str(e))
                logger.removeHandler(handler)

                # Re-raise the caught exception
                raise
        return wrapper
    return decorator


class FileManager:
    """
    Class that handles safe operations with .csv files:
    - reading
    - writing
    - appending
    Each method uses custom exceptions and logging depending on failure.
    """

    def __init__(self, filepath: str):
        """
        Initializes FileManager with a given file path.

        Raises:
            ValueError: If the file is not a .csv.
            FileNotFound: If the file does not exist.
        """
        self.filepath = filepath

        if not filepath.endswith('.csv'):
            raise ValueError("The file must be in .csv format.")

        if not os.path.exists(filepath):
            raise FileNotFound(f"File '{filepath}' not found.")

    @logged(FileCorrupted, mode="console")
    def read(self):
        """
        Reads and returns the contents of the file.

        Raises:
            FileCorrupted: If reading fails, indicating a possible corruption.
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            raise FileCorrupted("Error reading file. The file may be corrupted.")

    @logged(FileCorrupted, mode="file")
    def write(self, data: str):
        """
        Writes new data to the file, replacing existing content.

        Raises:
            FileCorrupted: If writing to the file fails.
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(data)
        except Exception:
            raise FileCorrupted("Error writing to file.")

    @logged(FileCorrupted, mode="file")
    def append(self, data: str):
        """
        Appends new data to the end of the file.

        Raises:
            FileCorrupted: If appending fails.
        """
        try:
            with open(self.filepath, 'a', encoding='utf-8') as f:
                f.write(data)
        except Exception:
            raise FileCorrupted("Error appending to file.")
