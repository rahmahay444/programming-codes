
# Decorator Basics

## Python’s functions are objects


In Python, a decorator is a design pattern that allows you to modify the functionality 
of a function by wrapping it in another function.

The outer function is called the decorator, which takes the original function as an 
argument and returns a modified version of it.



To understand decorators, you must first understand that functions are objects in Python.
This has important consequences. Let’s see why with a simple example :
    

```python

def shout(word='yes'):
    return word.capitalize() + '!'

print shout()
# outputs : 'Yes!'

# As an object, you can assign the function to a variable like any
# other object 

scream = shout

# Notice we don’t use parentheses: we are not calling the function, we are
# putting the function `shout` into the variable `scream`. 
# It means you can then call `shout` from `scream`:

print scream()
# outputs : 'Yes!'

# More than that, it means you can remove the old name `shout`, and
# the function will still be accessible from `scream`

del shout
try:
    print shout()
except NameError as e:
    print e
    #outputs: "name 'shout' is not defined"

print scream()
# outputs: 'Yes!'

```



Another interesting property of Python functions is they can be defined
inside another function!

```python

def talk():

    # You can define a function on the fly in `talk` ...
    def whisper(word='yes'):
        return word.lower() + '...'

    # ... and use it right away!

    print whisper()

# You call `talk`, that defines `whisper` EVERY TIME you call it, then
# `whisper` is called in `talk`. 
talk()
# outputs: 
# "yes..."

# But `whisper` DOES NOT EXIST outside `talk`:

try:
    print whisper()
except NameError as e:
    print e
    #outputs : "name 'whisper' is not defined"*

```



## Functions references


You’ve seen that functions are objects. Therefore, functions:

- can be assigned to a variable
- can be defined in another function

That means that **a function can `return` another function**. Have a look! ☺

```python

def getTalk(kind='shout'):

    # We define functions on the fly
    def shout(word='yes'):
        return word.capitalize() + '!'

    def whisper(word='yes'):
        return word.lower() + '...'

    # Then we return one of them
    if kind == 'shout':
        # We don’t use '()'. We are not calling the function;
        # instead, we’re returning the function object
        return shout  
    else:
        return whisper


# How do you use this strange beast?

# Get the function and assign it to a variable
talk = getTalk()      

# You can see that `talk` is here a function object:
print talk
#outputs : <function shout at 0xb7ea817c>

# The object is the one returned by the function:
print talk()
#outputs : Yes!

# And you can even use it directly if you feel wild:
print getTalk('whisper')()
#outputs : yes...
```



If you can `return` a function, you can pass one as a parameter:

    
```python

def scream(word='yes'):
    return word.capitalize() + '!'


def doSomethingBefore(func): 
    print 'I do something before then I call the function you gave me'
    print func()

doSomethingBefore(scream)
#outputs: 
#I do something before then I call the function you gave me
#Yes!

```

---------------------------------------------------------------------------------------


Well, you just have everything needed to understand decorators. You see, decorators are 
“wrappers”, which means that **they let you execute code before and after the function 
they decorate** without modifying the function itself.


## Handcrafted decorators

How you’d do it manually:

```python
# A decorator is a function that expects ANOTHER function as parameter
def my_shiny_new_decorator(a_function_to_decorate):

    # Inside, the decorator defines a function on the fly: the wrapper.
    # This function is going to be wrapped around the original function
    # so it can execute code before and after it.
    def the_wrapper_around_the_original_function():

        # Put here the code you want to be executed BEFORE the original 
        # function is called
        print 'Before the function runs'

        # Call the function here (using parentheses)
        a_function_to_decorate()

        # Put here the code you want to be executed AFTER the original 
        # function is called
        print 'After the function runs'

    # At this point, `a_function_to_decorate` HAS NEVER BEEN EXECUTED.
    # We return the wrapper function we have just created.
    # The wrapper contains the function and the code to execute before
    # and after. It’s ready to use!
    return the_wrapper_around_the_original_function



# Now imagine you create a function you don’t want to ever touch again.
def a_stand_alone_function():
    print 'I am a stand alone function, don’t you dare modify me'


a_stand_alone_function() 
#outputs: I am a stand alone function, don't you dare modify me


# Well, you can decorate it to extend its behavior.
# Just pass it to the decorator, it will wrap it dynamically in 
# any code you want and return you a new function ready to be used:

    
a_stand_alone_function_decorated = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function_decorated()
#outputs:
#Before the function runs
#I am a stand alone function, don't you dare modify me
#After the function runs
```





Now, you probably want that every time you call `a_stand_alone_function`, 
`a_stand_alone_function_decorated` is called instead. That’s easy, just overwrite 
`a_stand_alone_function` with the function returned by `my_shiny_new_decorator`:

    
```python
a_stand_alone_function = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function()
#outputs:
#Before the function runs
#I am a stand alone function, don’t you dare modify me
#After the function runs

# And guess what? That’s EXACTLY what decorators do!
```



## Decorators Shortcuts

The previous example, using the decorator syntax:

```python
@my_shiny_new_decorator
def another_stand_alone_function():
    print 'Leave me alone'

another_stand_alone_function()  
#outputs:  
#Before the function runs
#Leave me alone
#After the function runs
```

Yes, that’s all, it’s that simple. `@decorator` is just a shortcut to:

```python
another_stand_alone_function = my_shiny_new_decorator(another_stand_alone_function)
```



Of course, you can accumulate decorators:

```python
def bread(func):
    def wrapper():
        print "</''''''\>"
        func()
        print "<\______/>"
    return wrapper

def ingredients(func):
    def wrapper():
        print '#tomatoes#'
        func()
        print '~salad~'
    return wrapper

def sandwich(food='--ham--'):
    print food

sandwich()
#outputs: --ham--

sandwich = bread(ingredients(sandwich))
sandwich()
#outputs:
#</''''''\>
# #tomatoes#
# --ham--
# ~salad~
#<\______/>
```

Using the Python decorator syntax:

```python
@bread
@ingredients
def sandwich(food='--ham--'):
    print food

sandwich()
#outputs:
#</''''''\>
# #tomatoes#
# --ham--
# ~salad~
#<\______/>
```

The order you set the decorators MATTERS:

```python
@ingredients
@bread
def strange_sandwich(food='--ham--'):
    print food

strange_sandwich()
#outputs:
##tomatoes#
#</''''''\>
# --ham--
#<\______/>
# ~salad~




---------------------------------------------------------------------------------------


The decorator to make it bold

def makebold(fn):
    # The new function the decorator returns
    def wrapper():
        # Insertion of some code before and after
        return '<b>' + fn() + '</b>'
    return wrapper

# The decorator to make it italic
def makeitalic(fn):
    # The new function the decorator returns
    def wrapper():
        # Insertion of some code before and after
        return '<i>' + fn() + '</i>'
    return wrapper

@makebold
@makeitalic
def say():
    return 'hello'

print say() 
#outputs: <b><i>hello</i></b>


# This is the exact equivalent to 
def say():
    return 'hello'
say = makebold(makeitalic(say))

print say() 
#outputs: <b><i>hello</i></b>
```


---------------------------------------------------------------------------------------


Advanced uses of decorators.


## Passing arguments to the decorated function

```python
# It’s not black magic, you just have to let the wrapper 
# pass the argument:

def a_decorator_passing_arguments(function_to_decorate):
    
    def a_wrapper_accepting_arguments(arg1, arg2):
        print 'I got args! Look:', arg1, arg2
        function_to_decorate(arg1, arg2)
    return a_wrapper_accepting_arguments

# Since when you are calling the function returned by the decorator, you are
# calling the wrapper, passing arguments to the wrapper will let it pass them to 
# the decorated function

@a_decorator_passing_arguments
def print_full_name(first_name, last_name):
    print 'My name is', first_name, last_name
    
print_full_name('Peter', 'Venkman')
# outputs:
#I got args! Look: Peter Venkman
#My name is Peter Venkman
```



## Decorating methods

Methods and functions are really the same.  
The only difference is that methods expect that their first argument is a reference 
to the current object (`self`). 

That means you can build a decorator for methods the same way! Just remember 
to take `self` into consideration:

    
```python
def method_friendly_decorator(method_to_decorate):
    def wrapper(self, lie):
        lie = lie - 3 
        return method_to_decorate(self, lie)
    return wrapper


class Lucy(object):
    def __init__(self):
        self.age = 32
    
    @method_friendly_decorator
    def sayYourAge(self, lie):
        print 'I am {0}, what did you think?'.format(self.age + lie)
        
l = Lucy()
l.sayYourAge(-3)
#outputs: I am 26, what did you think?
```

If you’re making general-purpose decorator--one you’ll apply to any function or method, 
no matter its arguments--then just use `*args, **kwargs`:

```python
def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    # The wrapper accepts any arguments
    def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
        print 'Do I have args?:'
        print args
        print kwargs
        # Then you unpack the arguments, here *args, **kwargs
        # If you are not familiar with unpacking, check:
        # http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
        function_to_decorate(*args, **kwargs)
    return a_wrapper_accepting_arbitrary_arguments



@a_decorator_passing_arbitrary_arguments
def function_with_no_argument():
    print 'Python is cool, no argument here.'

function_with_no_argument()
#outputs
#Do I have args?:
#()
#{}
#Python is cool, no argument here.



@a_decorator_passing_arbitrary_arguments
def function_with_arguments(a, b, c):
    print a, b, c
    
function_with_arguments(1,2,3)
#outputs
#Do I have args?:
#(1, 2, 3)
#{}
#1 2 3 
 

@a_decorator_passing_arbitrary_arguments
def function_with_named_arguments(a, b, c, platypus='Why not ?'):
    print 'Do {0}, {1} and {2} like platypus? {3}'.format(
    a, b, c, platypus)

function_with_named_arguments('Bill', 'Linus', 'Steve', platypus='Indeed!')
#outputs
#Do I have args ? :
#('Bill', 'Linus', 'Steve')
#{'platypus': 'Indeed!'}
#Do Bill, Linus and Steve like platypus? Indeed!

```



## Passing arguments to the decorator


This can get somewhat twisted, since a decorator must accept a function as an argument. 
Therefore, you cannot pass the decorated function’s arguments directly to the decorator.

Before rushing to the solution, let’s write a little reminder: 

```python
# Decorators are ORDINARY functions
def my_decorator(func):
    print 'I am an ordinary function'
    def wrapper():
        print 'I am function returned by the decorator'
        func()
    return wrapper

# Therefore, you can call it without any '@'

def lazy_function():
    print 'zzzzzzzz'

decorated_function = my_decorator(lazy_function)
#outputs: I am an ordinary function
            
# It outputs 'I am an ordinary function', because that’s just what you do:
# calling a function. Nothing magic.

@my_decorator
def lazy_function():
    print 'zzzzzzzz'
    
#outputs: I am an ordinary function
```



Let’s get evil. ☺

```python
def decorator_maker():
    
    print 'I make decorators! I am executed only once: '+\
          'when you make me create a decorator.'
            
    def my_decorator(func):
        
        print 'I am a decorator! I am executed only when you decorate a function.'
               
        def wrapped():
            print ('I am the wrapper around the decorated function. '
                  'I am called when you call the decorated function. '
                  'As the wrapper, I return the RESULT of the decorated function.')
            return func()
        
        print 'As the decorator, I return the wrapped function.'
        
        return wrapped
    
    print 'As a decorator maker, I return a decorator'
    return my_decorator
            
# Let’s create a decorator. It’s just a new function after all.
new_decorator = decorator_maker()  
     
#outputs:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator

# Then we decorate the function
            
def decorated_function():
    print 'I am the decorated function.'
   
decorated_function = new_decorator(decorated_function)
#outputs:
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function
     
# Let’s call the function:
decorated_function()
#outputs:
#I am the wrapper around the decorated function. 
#I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
```



Let’s combine first two steps:

```python
def decorated_function():
    print 'I am the decorated function.'
    
decorated_function = decorator_maker()(decorated_function)

#outputs:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function.

# Finally:
decorated_function()    
#outputs:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
```


Let’s make it *even shorter*:

```python
@decorator_maker()
def decorated_function():
    print 'I am the decorated function.'
#outputs:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function.

#Eventually: 
decorated_function()    
#outputs:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
```



# Best practices: decorators
'''
- Decorators were introduced in Python 2.4, so be sure your code will be run on >= 2.4. 
- Decorators slow down the function call. Keep that in mind.
- **You cannot un-decorate a function.** (There *are* hacks to create decorators that can be removed, but nobody uses them.) So once a function is decorated, it’s decorated *for all the code*.
- Decorators wrap functions, which can make them hard to debug.  (This gets better from Python >= 2.5; see below.)

# How can the decorators be useful?

**Now the big question:** What can I use decorators for? 

Seem cool and powerful, but a practical example would be great. Well, there are 1000 
possibilities. Classic uses are extending a function behavior from an external lib 
(you can’t modify it), or for debugging (you don’t want to modify it because it’s 
temporary). 

.......

This really is a large playground.


  [1]: http://stackoverflow.com/questions/739654/understanding-python-decorators#answer-739665
  [2]: http://en.wikipedia.org/wiki/Decorator_pattern
  [3]: https://realpython.com/primer-on-python-decorators

'''



'''
 Code ref : https://gist.github.com/Zearin/2f40b7b9cfc51132851a 
 
'''



'''
    Diff between args(postional args) and kargs(keyword args) :
        https://realpython.com/python-kwargs-and-args/
'''

