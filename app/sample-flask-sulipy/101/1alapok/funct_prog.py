from functools import reduce

my_list = [1,2,3]
your_list = [10,20,30]
# square my_list
new_list = list(map(lambda num: num**2, my_list))


# List sorting
a = [(0,2), (4,3), (9,9), (10,-1)]
# List comprehension
comp_list = [char for char in 'hello']
# for char in 'hello':
#     comp_list.append(char)
# Set comprehension
# Dict comprehension
simple_dict = {
    'a': 1,
    'b': 2
}
my_dict = {k:v**2 for k,v in simple_dict.items()
    if v%2==0}

def multiply_by2(item):
    return item*2

def onyl_odd(item):
    return item % 2 != 0 

def accumulator(acc, item):
    return acc + item

print(list(map(multiply_by2, my_list)))
print(list(filter(onyl_odd, my_list)))
print(list(zip(my_list, your_list)))
print(reduce(accumulator, my_list, 0))

print(list(map(lambda item: item*2, my_list)))
print(list(filter(lambda item: item % 2 != 0, my_list)))
print(reduce(lambda acc, item: acc+item, my_list))

print(new_list)
# ezt azért kezdőnek nehéz kitalálnia
a.sort(key=lambda x: x[1])
print(a)
print(comp_list)
print(my_dict)