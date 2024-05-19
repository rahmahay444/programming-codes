# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 14:40:18 2024

@author: 20109
"""

'''
Timer decorator module
'''


# from timer_decorator_module import timer

# @timer
# def waste_some_time(num_times):
#      for _ in range(num_times):
#          sum([number**2 for number in range(10000)])


# waste_some_time(1)
# #Finished waste_some_time() in 0.0010 secs

# waste_some_time(999)
# #Finished waste_some_time() in 0.3260 secs



'''
Debug module
'''

# from debug_decorator_module import debug

# @debug
# def make_greeting(name, age=None):
#     if age is None:
#         return f"Howdy {name}!"
#     else:
#         return f"Whoa {name}! {age} already, you're growing up!"
    
    
# make_greeting("Ali")
# # Calling make_greeting('Ali')
# # make_greeting() returned 'Howdy Ali!'


# make_greeting("Ahmed", age=24)
# # Calling make_greeting('Ahmed', age=24)
# # make_greeting() returned "Whoa Ahmed! 24 already, you're growing up!"



'''
Slow code module
'''

from slow_code_decorator_module import slow_down

@slow_down
def countdown(from_number):
     if from_number < 1:
         print("Liftoff!")
     else:
         print(from_number)
         countdown(from_number - 1)


countdown(3)
