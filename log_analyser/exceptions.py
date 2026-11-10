class LogAnalyserError(Exception):
    """Base exception for log analyser errors."""


class LogFileError(LogAnalyserError):
    """Raised when a log file cannot be read."""
