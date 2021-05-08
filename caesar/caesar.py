from sys import argv
from cs50 import get_string

while True:

    if int(argv[1])>0:
        break

k = int(argv[1])
s = get_string("plaintext: ")

print("ciphertext: ", end = "")
for c in s:
    if c.islower():
        n = (((ord(c) + k) - 97) % 26) + 97
        print(f"{chr(n)}", end = "")
    elif c.isupper():
        n = (((ord(c) + k) - 65) % 26) + 65
        print(f"{chr(n)}", end = "")
    else:
        print((c), end = "")

print("")

