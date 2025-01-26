"""`NLExtractors.py` module -- naiveLoggerExtractors
Extract meaningful data from functions, classes and variables at run time, for logging.

@author         rdcn
@version        1.0
@creation date  2025-01-26
@last update    2025-01-26
"""

from typing import Callable, Any, Iterable, List, Dict;
from time import time, perf_counter, process_time;
import inspect;

def get_fdata(fun:      Callable,
              args:     Any = None) -> dict[str, Any]:
    """
    Given a function `fun`, returns a dict with common data concerning the funciont
    
    Parameters
    -----------
        `fun`   (Callable)      :   a function to extract data from
        `args`  (List[Any])     :   a list of arguments to pass to the function
        
    Returns
    -----------
        (dict[str, Any])    :   a dict populated with data from `fun`.
    """
    if inspect.isfunction(fun):
        init = time();
        return {
            "fmodule"       :   fun.__module__,
            "fname"         :   fun.__name__,
            "fline"         :   fun.__code__.co_firstlineno,
            "fdoc"          :   fun.__doc__,
            "fargs"         :   ", ".join([type(arg).__name__ + " " + str(arg) for arg in args]),
            "freturn"       :   str(fun(*args)),
            "freturn_type"  :   type(fun(*args)).__name__,
            "fexec_time"    :   f"{(time() - init) // 1000} ms",
        };
    else:
        raise TypeError(f"Object {fun} is not a function");

def get_test_fdata(fun:      Callable,
                   args:     Any = None,
                   expected: Any = None) -> dict[str, Any]:
    """
    Given a function `fun`, returns a dict with common data concerning the function (see `NLExtractors.get_fdata()`), but
    also containing the expected and actual values of the function call and whether they
    are equal or not.

    Parameters
    ----------
        `fun`    (Callable)     :   a function to extract data from
        `args`   (Any)          :   a list of arguments to pass to the function
        `expected` (Any)        :   the expected value of the function call

    Returns
    -------
        (dict[str, Any])    :   a dict populated with data from `fun`.
    """
    fdata : Dict[str, Any] = get_fdata(fun, args);
    fdata["expected"] = expected;
    fdata["actual"] = fun(*args);
    fdata["equal"] = fdata["expected"] == fdata["actual"];
    return fdata;

def get_vdata(var: Any, varname: str = None) -> dict[str, Any]:
    """
    Given a variable `var`, returns a dict with common data concerning the variable

    Parameters
    -----------
        `var`  (Any)   :   a variable to extract data from

    Returns
    -----------
        (dict[str, Any])    :   a dict populated with data from `var`.
    """
    try:
        name = var.__name__;
    except:
        name = var.__class__.__name__;
    
    return {
        "name"          :   " ".join([varname for varname, varval in inspect.currentframe().f_back.f_locals.items() if varval == var]),
        "type"          :   type(var),
        "value"         :   var,
    };
    

def get_cdata(cls: Any) -> dict[str, Any]:
    """
    Given a class `cls`, returns a dict with common data concerning the class

    Parameters
    -----------
        `cls`  (Any)   :   a class to extract data from

    Returns
    -----------
        (dict[str, Any])    :   a dict populated with data from `cls`.
    """
    return {
        "name"          :   cls.__name__,
        "module"        :   cls.__module__,
        "doc"           :   cls.__doc__,
        "dict"          :   cls.__dict__ or {},
    };


def get_mdata(mod: Any) -> dict[str, Any]:
    """
    Given a module `mod`, returns a dict with common data concerning the module

    Parameters
    -----------
        `mod`  (Any)   :   a module to extract data from

    Returns
    -----------
        (dict[str, Any])    :   a dict populated with data from `mod`.
    """
    return {
        "name"          :   mod.__name__,
        "doc"           :   mod.__doc__,
        "dict"          :   mod.__dict__ or {},
    };