#range(100)
#list(range(100))

def generator_function():
    for i in range(num):
        yield i*2

for item in generator_function(1000):
    print(item)

# def make_list(num):
#     result = []
#     for i in range(num):
#         result.append(i*2)
#     return result

# my_list = make_list(100)
# print(my_list)