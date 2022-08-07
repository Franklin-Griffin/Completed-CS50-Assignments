#include <cs50.h>
#include <stdio.h>

int LengthOfInt(long n)
{
    int i = 0;
    while (n != 0)
    {
        // removing the last digit of the number n (thanks to integer division)
        n = n / 10;

        // increasing count by 1
        i++;
    }
    return i;
}

int GetIthDigit(long n, int i) //Returns ith digit FROM END (zero-indexed)
{
    while (i > 0)
    {
        n /= 10;
        i--;
    }
    return n % 10;
}

//Executes Luhn's Algorithm and returns true if a long is valid
bool Luhn(long n)
{
    int l = LengthOfInt(n);
    int total = 0;
    for (int i = 1; i <= l; i += 2)
    {
        int x = GetIthDigit(n, i) * 2;
        if (LengthOfInt(x) == 2)
        {
            //We need to seperate the digits
            total += GetIthDigit(x, 0);
            total += GetIthDigit(x, 1);
        }
        else
        {
            total += x;
        }
    }
    for (int i = 0; i <= l; i += 2)
    {
        total += GetIthDigit(n, i);
    }
    return total % 10 == 0 ? true : false;
}

int main(void)
{
    long n = 0;
    do
    {
        n = get_long("Number: ");
    }
    while (n < 1);

    //Check valid number based on Luhn's Algorithm
    if (Luhn(n))
    {
        //Length of n
        int l = LengthOfInt(n);
        //First digit of n
        int first = GetIthDigit(n, l - 1);
        //Second digit of n
        int second = GetIthDigit(n, l - 2);

        if (l == 15 && first == 3 && (second == 4 || second == 7))
        {
            printf("AMEX\n");
        }
        else if (l == 16 && first == 5 && (second == 1 || second == 2  || second == 3  || second == 4  || second == 5))
        {
            printf("MASTERCARD\n");
        }
        else if ((l == 13 || l == 16) && first == 4)
        {
            printf("VISA\n");
        }
        else
        {
            //Does't work for any card, must be invalid
            printf("INVALID\n");
        }
    }
    else
    {
        //Fails test
        printf("INVALID\n");
    }
}