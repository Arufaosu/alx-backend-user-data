#!/usr/bin/env python3
"""filter logger"""
import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=[]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values"""
        msg = filter_datum(self.fields, self.REDACTION,
                           record.msg, self.SEPARATOR)
        msg = re.sub(r';(.)', r'; \1', msg)
        record.msg = msg
        return super().format(record)

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """returns the messages"""
    obf_msg = message
    for f in fields:
        obf_msg = re.sub(r'{}=.*?{}'.format(f, separator),
                         f'{f}={redaction}{separator}', obf_msg)
    return obf_msg

