"""Contains utilities for formatting data (column names, strings, type conversion, etc.)"""

import codecs
import re
import ftfy

def to_snake_case(col_name):
    """
    Convert camel case variable names to snake case (lowercased and underscore-separated).
    Mostly taken from: https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case.
    
    Parameters:
    ----------
    col : str
        Name of DataFrame column as a string
            
    Returns
    -------
    str
        String where capitalized words are separated by underscores and 
        characters have been lowercased
    
    Examples
    --------
    >>> to_snake_case('varName')
    >>> 'var_name'
    """
    col_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', col_name)
    col_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', col_name)\
                 .replace('BYOB', '_byob')\
                 .lower()\
                 .replace('.', '')
    col_name = re.sub('(\d+)', r'_\1_', col_name)
    return re.sub('_+', '_', col_name).strip('_')


def clean_byte_unicode_chars(text):
    if isinstance(text, str):
        # case 1
        if re.search("^b'", text):
            # return text with first 2 and last char removed
            return text[2:-1]
        # case 2
        if re.search('^b"u', text):
            # return text w/ first 4 and last 2 chars removed
            return text[4:-2]
        # case 3
        if re.search('^b"{', text):
            # return text with first 2 and last char removed
            return text[2:-1]
        # case 4
        if re.search('b"\'', text):
            # return text w/ first 3 and last 2 chars removed
            return text[3:-2]
    else: 
        return text

    
def fix_encoding(text):
    if text is not None:
        text = codecs.decode(text, 'unicode_escape')
        text = ftfy.fix_text(text)
    return text
