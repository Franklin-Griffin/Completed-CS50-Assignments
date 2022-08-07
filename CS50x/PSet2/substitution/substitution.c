#include <cs50.h>
#include <stdio.h>
//For strlen
#include<string.h>
//Upper and lower
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    string key = argv[1];
    for (int i = 0; i < 26; i++)
    {
        //Check non-alpha characters
        if (!isalpha(key[i]))
        {
            printf("%c: Only letters allowed.\n", key[i]);
            return 1;
        }
        for (int j = 0; j < i; j++)
        {
            if (key[i] == key[j])
            {
                //Duplicate letter
                printf("%c: Each letter should be used exactly once", key[i]);
                return 1;
            }
        }
    }
    string plain = get_string("plaintext: ");
    string cipher = plain; //For consistent length
    int len = strlen(plain);
    for (int i = 0; i < len; i++)
    {
        if (isupper(plain[i]))
        {
            int ascii = (int)plain[i];
            //Normalize and zero-indez
            int index = ascii - 65;
            cipher[i] = toupper(key[index]);
        }
        else if (islower(plain[i]))
        {
            int ascii = (int)plain[i];
            //Normalize and zero-indez
            int index = ascii - 97;
            cipher[i] = tolower(key[index]);
        }
        else
        {
            cipher[i] = plain[i];
        }
    }
    printf("ciphertext: %s\n", cipher);
    return 0;
}