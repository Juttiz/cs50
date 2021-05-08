from cs50 import get_string
from sys import argv
import os

words = set()

def main():
    while True:
        if len(argv) ==2:
            break
        print("usage: python bleep.py dictionary")
        exit(1)


    load(argv[1])
    s = get_string("What message would you like to censor?\n")
    st = s.split()
    for i in range(len(st)):
        if check(st[i]) == True:
            for c in st[i]:
                print("*",end = "")
        else:
            print(f"{st[i]}",end = "")
        print(" ",end = "")
    print()



def check(word):
    if word.lower() in words:
        return True
    else:
        return False

def load(dictionary):
    while True:
        if os.path.abspath(__file__) != "":
            break
        print("file not found")
        exit(1)

    file = open(dictionary,"r")
    for line in file:
        words.add(line.rstrip("\n"))
    file.close()
    return True

if __name__ == "__main__":
    main()