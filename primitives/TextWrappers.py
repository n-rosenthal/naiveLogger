""" `TextWrappers.py` module
Implements functions and classes related to text wrapping, aliasing, alignment and other utilities.

@author         rdcn
@version        1.0
@creation date  2025-01-25
@last update    2025-01-27
"""
from typing import List;

import string;
import stringprep;
import unicodedata;
import re;
import sys;

class TextWrapperError(Exception):
    """
    Exception class for text wrapping errors.
    """
    pass;

class TextAlignmentError(TextWrapperError):
    """
    Exception class for text alignment errors.
    """
    def __init__(self, message: str):
        super().__init__(message);
        self.message = message;
        
    def __str__(self):
        return self.message;
    
    def __repr__(self):
        return self.message;

def l_align(text: str
                | List[str]
                | bytes,
            width: int,
            char: str = " ") -> str:
    """
    Aligns `text` to the left with `width` characters using `char` as the filler character.

    Parameters
    ----------
        `text`  (str)   :   the text to be aligned
        `width` (int)   :   the width of the aligned text
        `char`  (str)   :   the character to use as the filler character

    Returns
    -------
        (str)            :   the aligned text
    """
    match type(text).__name__:
        case "str":
            return text.ljust(width, char);
        case "bytes":
            return text.ljust(width, char.encode("utf-8"));
        case "list":
            return [str(x).ljust(width, char) for x in text];
        case _:
            raise TextAlignmentError(f"Type <{type(text).__name__}> is not supported");

def r_align(text: str, width: int, char: str = " ") -> str:
    """
    Aligns `text` to the right with `width` characters using `char` as the filler character.

    Parameters
    ----------
        `text`  (str)   :   the text to be aligned
        `width` (int)   :   the width of the aligned text
        `char`  (str)   :   the character to use as the filler character

    Returns
    -------
        (str)            :   the aligned text
    """
    match type(text).__name__:
        case "str":
            return text.rjust(width, char);
        case "bytes":
            return text.rjust(width, char.encode("utf-8"));
        case "list":
            return [str(x).rjust(width, char) for x in text];
        case _:
            raise TextAlignmentError(f"Type <{type(text).__name__}> is not supported");

def c_align(text: str, width: int, char: str = " ") -> str:
    """
    Aligns `text` to the center with `width` characters using `char` as the filler character.

    Parameters
    ----------
        `text`  (str)   :   the text to be aligned
        `width` (int)   :   the width of the aligned text
        `char`  (str)   :   the character to use as the filler character

    Returns
    -------
        (str)            :   the aligned text
    """
    match type(text).__name__:
        case "str":
            return text.center(width, char);
        case "bytes":
            return text.center(width, char.encode("utf-8"));
        case "list":
            return [str(x).center(width, char) for x in text];
        case _:
            raise TextAlignmentError(f"Type <{type(text).__name__}> is not supported");

def align(text: str, width: int, char: str = " ", dir: str = "l") -> str:
    """
    Aligns `text` with `width` characters in the specified direction `dir` using `char` as the filler character.

    Parameters
    ----------
        `text`  (str)   :   the text to be aligned
        `width` (int)   :   the width of the aligned text
        `char`  (str)   :   the character to use as the filler character
        `dir`   (str)   :   the direction of the alignment, either "l" for left, "r" for right, or "c" for center

    Returns
    -------
        (str)            :   the aligned text
    """
    return pad(text, width, char, dir);

def pad(text: str, width: int, char: str = " ", dir: str = "l") -> str:
    """
    Pads `text` with `char` to `width` characters in the specified direction.

    Parameters
    ----------
        `text`  (str)   :   the text to be padded
        `width` (int)   :   the width of the padded text
        `char`  (str)   :   the character to use as the padding character
        `dir`   (str)   :   the direction of the padding, either "l" for left, "r" for right, or "c" for center

    Returns
    -------
        (str)            :   the padded text
    """
    match dir:
        case "l" | "L": return l_align(text, width, char);
        case "r" | "R": return r_align(text, width, char);
        case "c" | "C": return c_align(text, width, char);
        case _:
            raise TextAlignmentError(f"Direction <{dir}> is not supported");

    return text;

def shorten(text: str, width: int, short_text: str = "...") -> str:
    """
    Shortens `text` to `width` characters or less by replacing excess characters with an ellipsis.

    Parameters
    ----------
        `text`  (str)   :   the text to be shortened
        `width` (int)   :   the maximum width of the shortened text
        `short_text`    :   the text to use as the ellipsis

    Returns
    -------
        (str)            :   the shortened text
    """
    if len(text) > width:
        return text[:width - len(short_text)] + short_text;
    else:
        return text;

def wrap(text: str, width: int = -1, char: str = " ") -> str:
    """
    Wraps `text` to `width` characters or less by inserting line breaks.

    Parameters
    ----------
        `text`  (str)   :   the text to be wrapped
        `width` (int)   :   the maximum width of the wrapped text
        `char`  (str)   :   the character to use as the line break

    Returns
    -------
        (str)            :   the wrapped text
    """
    if width == -1:
        width = len(char);
    return char*width + text + char*width;

def tag_wrap(p: str, tag: str) -> str:
    """
    Wraps `p` with HTML tags specified by `tag`

    Parameters
    ----------
        `p`    (str)   :   the text to be wrapped
        `tag`  (str)   :   the HTML tag to use for wrapping

    Returns
    -------
        (str)            :   the wrapped text
    """
    if "<" in tag: tag = tag.replace("<", "");
    if ">" in tag: tag = tag.replace(">", "");
    if "/" in tag: tag = tag.replace("/", "");
    return tagify(tag)[0] + p + tagify(tag)[1];

def tagify(tag: str) -> str:
    """
    Returns a tuple containing the opening and closing HTML tags for a given tag.

    Parameters
    ----------
        `tag`  (str)   :   the HTML tag to be used for wrapping

    Returns
    -------
        (str, str)      :   a tuple containing the opening and closing HTML tags
    """
    return ("<" + tag + ">", "</" + tag + ">");

def ident(text: str, lenght: int) -> str:
    """
    Indents `text` with `lenght` spaces.

    Parameters
    ----------
        `text`  (str)   :   the text to be indented
        `lenght` (int)   :   the number of spaces to indent with

    Returns
    -------
        (str)            :   the indented text
    """
    return " "*lenght + text;