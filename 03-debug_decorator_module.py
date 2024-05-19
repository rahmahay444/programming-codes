# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:54:13 2024

@author: 20109
"""

import functools



def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  #create list of args
        kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()] #create list of kargs
        signature = ", ".join(args_repr + kwargs_repr) #create function signature
        print(f"Calling {func.__name__}({signature})") #print signature
        value = func(*args, **kwargs)
        print(f"{func.__name__}() returned {repr(value)}") #print the return value
        return value
    return wrapper_debug