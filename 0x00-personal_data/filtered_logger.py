#!/usr/bin/env python3
"""filter logger"""
import re
import logging
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """returns the messages"""
    obf_msg = message
    for f in fields:
        obf_msg = re.sub(r'{}=.*?{}'.format(f, separator),
                         f'{f}={redaction}{separator}', obf_msg)
    return obf_msg

