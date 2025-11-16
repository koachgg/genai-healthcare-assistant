"""
Logging Utility

Simple logging utility that writes messages to both console and a log file.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """
    Simple file and console logger.
    
    Attributes:
        log_dir: Directory where log files are stored
        log_file: File handle for the log file
    """
    
    def __init__(self, log_dir: str = "logs", log_filename: str = "application.log"):
        """
        Initialize the logger.
        
        Args:
            log_dir: Directory for log files (created if doesn't exist)
            log_filename: Name of the log file
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.log_file_path = self.log_dir / log_filename
        self.log_file = open(self.log_file_path, 'a', encoding='utf-8')
    
    def log(self, message: str, level: str = "INFO") -> None:
        """
        Write log message to console and file.
        
        Args:
            message: The log message
            level: Log level (INFO, WARNING, ERROR, DEBUG)
        """
        # Print to console
        print(f"[{level}] {message}")
        
        # Format with timestamp for file
        current_time = datetime.now()
        time_formatted = current_time.strftime("%Y-%m-%d %H:%M:%S")
        file_message = f"[{time_formatted}] [{level}] {message}"
        
        # Write to file and flush
        self.log_file.write(file_message + '\n')
        self.log_file.flush()
    
    def info(self, message: str) -> None:
        """Log an info message."""
        self.log(message, "INFO")
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.log(message, "WARNING")
    
    def error(self, message: str) -> None:
        """Log an error message."""
        self.log(message, "ERROR")
    
    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.log(message, "DEBUG")
    
    def close(self) -> None:
        """Close the log file."""
        if self.log_file:
            self.log_file.close()
    
    def __del__(self):
        """Ensure log file is closed on deletion."""
        self.close()


# Create global logger instance
_logger = Logger()

# Backward compatibility functions
def log(log_message: str) -> None:
    """
    Legacy log function for backward compatibility.
    
    Args:
        log_message: The message to be logged
    """
    _logger.log(log_message)