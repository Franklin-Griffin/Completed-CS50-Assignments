from cs50 import get_int

# Get height of pyramid
n = 0
while n < 1 or n > 8:
    n = get_int("Height: ")

# For each row
for i in range(n):
    # Spaces, hashes, spaces, hashes
    spaces = " " * (n - i - 1)
    hashes = "#" * (i + 1)
    print(spaces + hashes + "  " + hashes)