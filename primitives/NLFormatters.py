"""`NLFormatters.py` module -- naiveLoggerFormatters
Implements several formatters for the `naiveLogger` module
Formatters are functions that take a dict and return a formatted string. 

@author         rdcn
@version        1.0
@creation date  2025-01-25
@last update    2025-01-27
"""
import logging;

class NL_ST_Formatter(logging.Formatter):
    """ naiveLogger Stream Handler Formatter

    Common formatter for a stream handler logger.
    """
    def __init__(self) -> None:
        super().__init__(fmt="%(asctime)s - %(levelname)s - %(message)s",
                         datefmt="%Y-%m-%d %H:%M:%S");

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a `logging.LogRecord` object into a string.
        """
        return super().format(record);
    
    @staticmethod
    def get_formatter() -> "NL_ST_Formatter":
        return NL_ST_Formatter();
    
class NL_ST_Colorful_Formatter(logging.Formatter):
    """ naiveLogger Stream Handler Colorful Formatter

    Colorful formatter for a stream handler logger.
    """
    def __init__(self) -> None:
        super().__init__(fmt=f"\x1b[32m%(asctime)s\x1b[0m - %(levelname)s - \x1b[33m%(message)s\x1b[0m",
                         datefmt="%Y-%m-%d %H:%M:%S");

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a `logging.LogRecord` object into a string.
        """
        match record.levelname:
            case "DEBUG": record.levelname = "\x1b[34mDEBUG\x1b[0m";
            case "INFO": record.levelname = "\x1b[32mINFO\x1b[0m";
            case "WARNING": record.levelname = "\x1b[33mWARNING\x1b[0m";
            case "ERROR": record.levelname = "\x1b[31mERROR\x1b[0m";
            case "CRITICAL": record.levelname = "\x1b[31mCRITICAL\x1b[0m";
        return super().format(record);
    
    @staticmethod
    def get_formatter() -> "NL_ST_Colorful_Formatter":
        return NL_ST_Colorful_Formatter();
