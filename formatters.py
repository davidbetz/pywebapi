from .general import debug

from .resources import formatters

active_formatters = {}

for formatter in formatters:
    formats = formatter.get_formats()
    for format in formats:
        active_formatters[format.lower()] = formatter