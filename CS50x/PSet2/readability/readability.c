#include <cs50.h>
#include <stdio.h>
//Length of strings
#include <string.h>
//Upper and lower
#include <ctype.h>
//Round function
#include <math.h>

int main(void)
{
    //Promt user for the text to test
    string text = get_string("Text: ");

    //Get the length of a string
    int length = strlen(text);

    //Floats so result not truncated when normalizing
    float L = 0;
    float S = 0;
    //Word count (the first letter will not be a space, so make sure to count the first word)
    float W = 1;

    //Loop string
    for (int i = 0; i < length; i++)
    {
        //If it is uppercase or lowercase, it must be a letter
        if (isupper(text[i]) || islower(text[i]))
        {
            L++;
        }
        else if (text[i] == ' ')
        {
            W++;
        }
        else if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            S++;
        }
    }

    //Normalize counts to 100 words
    L = L * 100.0 / W;
    S = S * 100.0 / W;

    //Coleman-Liau index test
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}