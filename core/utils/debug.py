import time
import pprint
import functools
from functools import wraps


def repeat(num_times=1):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value

        return wrapper_repeat

    return decorator_repeat


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print("Finished %s in %8.4f secs" % (func.__name__, run_time))
        print('')
        return value

    return wrapper_timer


def trace_print(depth=None):
    """Print traceback"""

    def wrapper(func, *args, **kwargs):
        def func_wrapper(*args, **kwargs):
            import traceback
            skip = -2
            if depth:
                tracks = traceback.format_stack()[skip - depth:skip]
            else:
                tracks = traceback.format_stack()[:skip]

            for line in tracks:
                print(line.strip())
            print('')
            return func(*args, **kwargs)

        return func_wrapper

    return wrapper


def retry(ExceptionToCheck, tries=4, delay=3, backoff=1.5, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def django_db_hits(func):
    """print django db hits"""
    from django.db import connection
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        queries = len(connection.queries)
        value = func(*args, **kwargs)
        queries2 = len(connection.queries)

        print("Django db hits: %s" % (queries2 - queries))
        return value

    return wrapper
