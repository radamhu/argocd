# parameters
# default parameters
def say_hello(name='Manci', emoji=':('):
    print(f'hello {name} {emoji}')

# positional arguments
say_hello('Roland', ':)')
say_hello('Emily', ':)')

# keyword arguments : old method
# say_hello(emoji=':)', name='Bibi')

picture = [
    [0,0,0,1,0,0,0],
    [0,0,1,1,1,0,0],
    [0,1,1,1,1,1,0],
    [1,1,1,1,1,1,1],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
]

def show_tree():
    for row in picture:
        for pixel in row:
            if (pixel == 1):
                print('*', end='')
            else:
                print(' ', end='')
        print('')

print(show_tree)
show_tree()

from ast import arg
from inspect import ArgSpec
import re


#def sum(num1, num2):
#    print('hiii')
#    return num1 + num2

#print(sum(4,5))

def test(a):
    '''
    Info about function tests and prints param
    '''
    print(a)

print(test.__doc__)

# clean code 
def is_even(num):
    return num % 2 == 0
    
print(is_even(50))

# *args **kwargs
# *args : tuple can accept any number of argument
# **kwargs : dictionary 
# Rule: params, *args, default parametersm **kwargs
def super_func(*args, **kwargs):
    #print(*args)
    #print(kwargs)
    total = 0
    for items in kwargs.values():
        total += items
    return sum(args) + total

print(super_func(1,2,3,4,5, num1=5, num2=10))

def highest_even(li):
    evens = []
    for item in li:
        if item % 2 == 0:
            evens.append(item)
    return max(evens)

print(highest_even([10,2,3,4,8,11]))

print(bool(0))