"""
`loggers.py` module implements a simplified access to the `logging` module.

@author         rdcn
@version        1.0
@creation date  2025-01-27
@last update    2025-01-27
"""

import logging;
import inspect;

import primitives.NLFormatters as NLFormatters;

from typing import Dict, Any, List, Optional, Final;

class LoggerBuilder(logging.Logger):
    @staticmethod
    def build(name: str = inspect.currentframe().f_back.f_code.co_name,
              level: Any = logging.NOTSET,
              handlers: Optional[List[logging.Handler]] = None,
              propagate: bool = True,
              parent: Optional[logging.Logger] = None) -> logging.Logger:
        logger : logging.Logger = logging.Logger(name=name, level=level);
        
        #   Sets the level of Logger if `level` is an integer
        if isinstance(level, int):
            logger.setLevel(level);
        
        #   Sets the handlers of Logger if `handlers` is a list of `logging.Handler` objects
        if isinstance(handlers, list):
            for handler in handlers:
                logger.addHandler(handler);
        
        #   Sets the propagation of Logger if `propagate` is a boolean
        if isinstance(propagate, bool):
            logger.propagate = propagate;
            
        #   Sets the parent of Logger if `parent` is a `logging.Logger` object
        if isinstance(parent, logging.Logger):
            logger.parent = parent;
        
        return logger;
    
    @staticmethod
    def build_from_dict(dict: Dict[str, Any]) -> logging.Logger:
        return LoggerBuilder.build(**dict);
    
    @staticmethod
    def build_default() -> logging.Logger:
        """
        The DEFAULT Logger is a Logger with
        -   `level` set to `logging.DEBUG`
        -   `propagate` set to `False`
        -   `handlers` set to `logging.StreamHandler`, `logging.FileHandler`
        -   `parent` set to `None`
        """
        #   Handlers
        stream_handler : logging.StreamHandler = logging.StreamHandler();
        stream_handler_formatter : logging.Formatter = NLFormatters.NL_ST_Formatter.get_formatter();
        stream_handler.setFormatter(stream_handler_formatter);
        
        file_handler : logging.FileHandler = logging.FileHandler("naiveLogger.log");
        file_handler_formatter : logging.Formatter = NLFormatters.NL_ST_Formatter.get_formatter();
        file_handler.setFormatter(file_handler_formatter);
        
        #   Logger
        logger : logging.Logger = LoggerBuilder.build(
            level = logging.DEBUG,
            propagate = False,
            handlers = [stream_handler, file_handler],
            parent = None
        );
        
        return logger;
    
    def build_colorful_default() -> logging.Logger:
        """
        The DEFAULT Logger is a Logger with
        -   `level` set to `logging.DEBUG`
        -   `propagate` set to `False`
        -   `handlers` set to `logging.StreamHandler`, `logging.FileHandler`
        -   `parent` set to `None`
        """
        #   Handlers
        stream_handler : logging.StreamHandler = logging.StreamHandler();
        stream_handler_formatter : logging.Formatter = NLFormatters.NL_ST_Colorful_Formatter.get_formatter();
        stream_handler.setFormatter(stream_handler_formatter);
        
        file_handler : logging.FileHandler = logging.FileHandler("naiveLogger.log");
        file_handler_formatter : logging.Formatter = NLFormatters.NL_ST_Colorful_Formatter.get_formatter();
        file_handler.setFormatter(file_handler_formatter);
        
        #   Logger
        logger : logging.Logger = LoggerBuilder.build(
            level = logging.DEBUG,
            propagate = False,
            handlers = [stream_handler, file_handler],
            parent = None
        );
        
        return logger;
    
    
if __name__ == '__main__':
    J : logging.Logger = LoggerBuilder.build_colorful_default();
    J.info("info");
    J.debug("debug");
    J.warning("warning");
    J.error("error");
    J.critical("critical");