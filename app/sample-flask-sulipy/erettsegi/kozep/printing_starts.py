num = int(input("enter the number of rows:"))
for i in range(num):
    for j in range(num):
        print("*", end=" ")
    print()

for i in range(1, num+1):
    print(" * "*i)
    
for i in range(1, num+1):
    print(" "* (num-i) + "* "*i)

for i in range(num-1,0,-1):
    print(" "* (num-i) + "* "*i)

for i in range(num,0,-1):
    print("* "*i)