from cs50 import get_string
cards = []


def main():
    while True:
        s = get_string("Number: ")
        if check(s) == True:
            break

    # if len(s) != 16:
    #     print("INVALID")
    # else:
    n = 0
    for c in s:
        cards.append(ord(c)-48)
    for i in range(len(s)%2,len(s),2):
        n = n + cards[i]*2%10 + cards[i]*2//10
    for q in range((len(s)+1)%2,len(s),2):
        n = n + cards[q]
    if n%10 != 0:
        print("INVALID")
    elif cards[0]==5 and 0<cards[1]<6:
        print("MASTERCARD")
    elif cards[0]==4:
        print("VISA")
    elif cards[0]==3 and (cards[1] == 4 or 7):
        print("AMEX")
    else:
        print("INVALID")

def check(string):
    if string =="":
        return
    for c in string:
        if ord(c)-48 < 0 or ord(c)-48>9:
            return
    return True
if __name__ == "__main__" :
    main()