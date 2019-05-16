"""
Utilities
"""

from threading import Thread


# Threaded function snippet
def threaded(fn):
    """To use as decorator to make a function call threaded.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


# Threaded function snippet returning a callback when the function has finished
def threaded_return(fn, callback_func):
    """To use as decorator to make a function call threaded.
    It will call the callback_func when the function returns.
    Needs import
    from threading import Thread"""

    def wrapper(*args, **kwargs):
        def do_callback():
            callback_func(fn(args, kwargs))

        thread = Thread(target=do_callback)
        thread.start()
        return thread

    return wrapper
