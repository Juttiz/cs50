import crypt
from sys import argv
import sys

k = argv[1][:2]



def main():
    while True:
        if len(sys.argv) ==2:
            break
        print("usage: python crack.py hash")
        return


    print(f"{k}")

    print(f"{check()}")

def check():
    a = ""
    b = ""
    c = ""
    d = ""
    e = ""
    for i in range(58):
        for j in range(58):
            for x in range(58):
                for l in range(58):
                    for n in range(58):
                        a = chr(65+n)
                        if crypt.crypt(a+b+c+d+e,k) == argv[1]:
                            return a+b+c+d+e
                    b = chr(65 + l)
                c = chr(65 + x)
            d = chr(65 + j)
        e = chr(65 + i)

if __name__ == "__main__" :
    main()