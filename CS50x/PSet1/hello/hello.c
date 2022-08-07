#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Get name of user
    string name = get_string("What is your name? ");

    //Print hello + user's name
    printf("hello, %s\n", name);
}