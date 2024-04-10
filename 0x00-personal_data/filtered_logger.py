#!/usr/bin/env python3
import re
import logging

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=()):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = record.getMessage()
        for field in self.fields:
            message = filter_datum([field], self.REDACTION, message, self.SEPARATOR)
        record.msg = message
        return super().format(record)

def filter_datum(fields, redaction, message, separator):
    return re.sub(r'(?<=\b|^)(' + '|'.join(fields) + r')=[^{}]+(?=\b|$)'.format(re.escape(separator)), lambda x: x.group().split('=')[0] + '=' + redaction, message)

