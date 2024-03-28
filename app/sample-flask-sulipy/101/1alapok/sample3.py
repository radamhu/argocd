user = {
    'name': 'Golem',
    'age': 5006,
    'can_swim' : False
}

for item in user:
    print(item)
print('')
for item in user.items():
    print(item)
print('')
for key, value in user.items():
    print(key, value)
print('')
for k, v in user.items():
    print(k, v)
print('')
for item in user.values():
    print(item)
print('')
for item in user.keys():
    print(item)
print('')

my_list = [1,2,3,4,5,6,7,8,9,10]
counter = 0
for item in my_list:
    counter = counter + item
print(counter)

print('next')

for _ in range(0,10,2):
    print(_)

print('')
for _ in range(10,0,-1):
    print(_)

print('')
for _ in range(2):
    print(list(range(10)))

print('')
for i,char in enumerate(list(range(10))):
    print(i ,char)
    if char == 5:
        print(f'index of 50 is:  {i}')

print('')
i = 0
while i < 10:
    print(i)
    i = i + 1
else:
    print('done')

while True:
    response = input('say something: ')
    if (response == 'bye'):
        break

picture = [
    [0,0,0,1,0,0,0],
    [0,0,1,1,1,0,0],
    [0,1,1,1,1,1,0],
    [1,1,1,1,1,1,1],
    [0,0,0,1,0,0,0],
    [0,0,0,1,0,0,0],
]

for row in picture:
    for pixel in row:
        if (pixel == 1):
            print('*', end='')
        else:
            print(' ', end='')
    print('')

some_list = ['a','b','c','b','d','m','n','n']

duplicates = []
for value in some_list:
    if some_list.count(value) > 1:
        if value not in duplicates:
            duplicates.append(value)

print(duplicates)