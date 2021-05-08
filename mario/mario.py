from cs50 import get_int

n = get_int("Height: ") + 1
for i in range(n):
    for x in range(n-i):
        print(" ",end = "")
    for y in range(2):
        for y in range(i):
            print("#",end = "")
        print("  ",end = "")
    print()