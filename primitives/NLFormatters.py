"""`NLFormatters.py` module -- naiveLoggerFormatters
Implements several formatters for the `naiveLogger` module
Formatters are functions that take a dict and return a formatted string. 

@author         rdcn
@version        1.0
@creation date  2025-01-25
@last update    2025-01-25
"""
from typing import Callable, Any, Iterable, List, Dict;
from datetime import datetime, timedelta;
from inspect import currentframe, getframeinfo, getouterframes;
from NLExtractors import get_fdata, get_test_fdata;

import logging;

NLFormatters_DATEFORMATS : Dict[str, str] = {
    "default"           : "%Y-%m-%d %H:%M:%S",
    "short"             : "%Y-%m-%d",
    "time"              : "%H:%M:%S",
    "date"              : "%Y-%m-%d",
    "zettelkasten"      : "%Y%m%d%H%M%S",
};

NLFormatters_FORMATS : Dict[str, str] = {
    "default"           : "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    "short"             : "%(levelname)s - %(message)s",
    "time"              : "%(asctime)s - %(levelname)s - %(message)s",
    "date"              : "%(asctime)s - %(levelname)s - %(message)s",
    "zettelkasten"      : "%(asctime)s - %(levelname)s - %(message)s",
};

NLFormatters_MESSAGE_FORMATS : Dict[str, str] = {
    "function"          :   "['{fmodule}' | line={fline} | {fname}] [{fname}({fargs}) -> {freturn_type} {freturn}] :: [exec_time={fexec_time}]",
    "test_function"     :   "['{fmodule}' | line={fline} | {fname}] [{fname}({fargs}) -> {freturn_type} {freturn}] :: [exec_time={fexec_time}] >>> expected={expected}, actual={actual} equal?={equal}",
}

def wrap_format(format: str, sep: str) -> str:
    """
    Given a format string and a separator, splits the format string into a list by the separator, 
    joins the first elements of the list back into a string with the same separator, and returns the 
    resulting string with the last element of the list at the end.

    Parameters
    ----------
        `format` (str)   :   the format string to be split
        `sep`     (str)   :   the separator to split the format string by

    Returns
    -------
        (str)            :   the formatted string

    Example
    -------
        >>> wrap_format("%(asctime)s - %(levelname)s - %(name)s - %(message)s", " - ")
        "[%(asctime)s - %(levelname)s - %(name)s] %(message)s"
    """
    flist = format.split(sep);
    data, msg = flist[0:-1], flist[-1];
    return f"{[sep.join(data)]} {msg}";

def format_function_call(fun: Callable, *args, **kwargs) -> str:
    """
    Given a function `fun`, returns a formatted string containing information about the function call.

    Parameters
    ----------
        `fun`   (Callable)      :   a function to extract data from

    Returns
    -------
        (str)            :   a formatted string containing information about the function call
    """
    return NLFormatters_MESSAGE_FORMATS["function"].format(**get_fdata(fun, *args));

def format_test_function_call(fun: Callable, *args, **kwargs) -> str:
    """
    Given a function `fun`, returns a formatted string containing information about the function call.

    Parameters
    ----------
        `fun`   (Callable)      :   a function to extract data from

    Returns
    -------
        (str)            :   a formatted string containing information about the function call
    """
    return NLFormatters_MESSAGE_FORMATS["test_function"].format(**get_test_fdata(fun, *args));
    

def get_caller_info() -> dict[str, Any]:
    """
    Returns a dictionary containing information about the caller of the current function.

    Returns
    -------
        (dict[str, Any])    :   a dictionary containing the following keys:
            `filename`  (str)   :   the filename of the caller
            `lineno`    (int)   :   the line number of the caller
            `function`  (str)   :   the name of the caller
    """
    return getframeinfo(currentframe().f_back);


if __name__ == "__main__":
    def g(x: int, y: int) -> float:
        return x + y;
    
    from typing import Type, TypeAlias, Generic;
    class Node:
        pass;
    
    def search(nodestack: List[Node]) -> Iterable[Node]:
        for node in nodestack:
            yield node;
    
    print(format_function_call(g, [1, 2]));
    print(format_function_call(search, [[1, 2]]));
    print(format_test_function_call(g, [1, 2], expected=3));
    