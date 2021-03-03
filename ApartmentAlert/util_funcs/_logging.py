import functools
from datetime import datetime


def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('Suche auf {} um {}'.format(func.__name__.split("_")[2].upper(),
                                          str(datetime.now().strftime("%d.%b %y %H:%M:%S"))))
        result = func(*args, **kwargs)
        return result

    return wrapper
