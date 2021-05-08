from cs50 import get_string
from sys import argv
import sys

def main():
    while True:
        if len(sys.argv) ==2:
            break
        print("usage: python crack.py keyword")
        exit(1)
    cipher = []
    n = 0

    for i in range(len(argv[1])):
        # cipher[i] =
        if argv[1][i].isupper():
            cipher.append(ord(argv[1][i]) - 65)
        elif argv[1][i].islower():
            cipher.append(ord(argv[1][i]) - 97)
        else:
            print("usage: python crack.py keyword")
            exit(1)
    s = get_string("plaintext: ")
    print("ciphertext: ")
    for c in s:
        if c.isalpha():
            if c.isupper():
                x = n%len(argv[1])
                l = ((ord(c)-65) + cipher[x])%26 +65
                print(f"{chr(l)}",end = "")
                n+=1
            elif c.islower():
                x = n%len(argv[1])
                l = ((ord(c)-97) + cipher[x])%26 +97
                print(f"{chr(l)}", end = "")
                n+=1
        else:
            print(c,end = "")
    print("")

if __name__ == "__main__" :
    main()