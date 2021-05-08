from cs50 import get_float
while True:
    f = get_float("Change owed: ")
    if f > 0:
        break

n = f // 0.25
x = f % 0.25
n = n + x // 0.1
x = x % 0.1
n = n + x //0.05
x = x % 0.05
n = n + x / 0.01
print(f"{n:.0f}")