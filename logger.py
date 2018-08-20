import sys, os
import logging
from logging import handlers


def setup(basedir='.', *params):
    l = logging.getLogger("Heliomaster")
    l.setLevel(logging.DEBUG)

    formatter = logging.Formatter('{asctime}: {levelname:<8}: {message}', style='{')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.NOTSET)
    stdout_handler.setFormatter(formatter)
    l.addHandler(stdout_handler)

    for p in params:
        if p.IsEnabled:
            h = handlers.TimedRotatingFileHandler(os.path.join(basedir, p.Filename),
                                                  when='midnight', backupCount=p.BackupCount, delay=True)
            h.setLevel(p.Level)
            h.setFormatter(formatter)
            l.addHandler(h)

    return l
