from cs50 import get_string


def LengthOfInt(n):
    # Returns the character count of an integer
    i = 0

    while n != 0:
        # removing the last digit of the number n
        n //= 10
        # increasing count by 1
        i += 1

    return i


def GetIthDigit(n, i):
    # Returns ith digit FROM END (zero-indexed)
    while i > 0:
        n //= 10
        i -= 1

    return n % 10


def Luhn(n):
    # Executes Luhn's Algorithm and returns true if a int is valid
    l = LengthOfInt(n)
    print(l)
    total = 0
    # C equivalent: for (int i = 1; i <= l; i += 2)
    for i in range(1, l + 1, 2):
        x = GetIthDigit(n, i) * 2
        if LengthOfInt(x) == 2:
            # We need to seperate the digits
            total += GetIthDigit(x, 0)
            total += GetIthDigit(x, 1)
        else:
            total += x
    print(total)
    for i in range(0, l + 1, 2):
        total += GetIthDigit(n, i)
    print(total)

    if total % 10 == 0:
        return True
    else:
        return False


def main():
    # Declare n as a long
    x = 0
    while int(x) < 1:
        x = get_string("Number: ")
    n = int(x)

    # Check valid number based on Luhn's Algorithm
    if Luhn(n):
        # Length of n
        l = LengthOfInt(n)
        # First digit of n
        first = GetIthDigit(n, l - 1)
        # Second digit of n
        second = GetIthDigit(n, l - 2)

        if l == 15 and first == 3 and (second == 4 or second == 7):
            print("AMEX")
        elif l == 16 and first == 5 and (second == 1 or second == 2 or second == 3 or second == 4 or second == 5):
            print("MASTERCARD")
        elif (l == 13 or l == 16) and first == 4:
            print("VISA")
        else:
            # Does't work for any card, must be invalid
            print("INVALID")
    else:
        # Fails test
        print("INVALID")


main()