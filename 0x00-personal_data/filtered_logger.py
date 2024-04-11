#!/usr/bin/env python3
"""filter logger"""
import re
import csv
import logging
import mysql.connector
import os
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values"""
        msg = filter_datum(self.fields, self.REDACTION,
                           record.msg, self.SEPARATOR)
        msg = re.sub(r';(.)', r'; \1', msg)
        record.msg = msg
        return super().format(record)


def filter_datum(
        fields: List[str], redaction: str, message: str,
        separator: str) -> str:
    """returns the messages"""
    obf_msg = message
    for f in fields:
        obf_msg = re.sub(r'{}=.*?{}'.format(f, separator),
                         f'{f}={redaction}{separator}', obf_msg)
    return obf_msg


def get_logger() -> logging.Logger:
    """return a logging.Logger object"""

    logger = logging.getLogger('user_data')

    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()

    stream_handler.setFormatter(RedactingFormatter())

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a MySQLConnection object"""

    connection = mysql.connector.connect(
            host=os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost'),
            user=os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=os.environ.get('PERSONAL_DATA_DB_PASSWORD', ''),
            database=os.environ.get('PERSONAL_DATA_DB_NAME')
            )

    return connection


def main() -> None:
    """obtain a database connection using get_db"""

    db = get_db()

    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')

    logger = get_logger()

    for row in cursor:
        data = ''
        for i in range(len(row)):
            data += f'{cursor.column_names[i]}={row[i]};'
        logger.info(data)

    cursor.close()
    db.close()
