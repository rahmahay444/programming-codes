# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:38:33 2024

@author: 20109
"""

import functools
import time

# ...

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__}() in {run_time:.4f} secs")
        return value
    return wrapper_timer




'''
[1] : https://realpython.com/primer-on-python-decorators/#timing-functions
'''