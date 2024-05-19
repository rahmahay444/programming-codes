# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 15:16:22 2024

@author: 20109
"""

import functools
import time

# ...

def slow_down(func):
    """Sleep 1 second before calling the function"""
    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)
    return wrapper_slow_down