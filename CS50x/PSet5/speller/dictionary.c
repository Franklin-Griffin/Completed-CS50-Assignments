// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <stdio.h>

#include "dictionary.h"

unsigned int _size = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 2];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];
node *prev[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *bucket = table[hash(word)];
    while (bucket != NULL)
    {
        if (strcasecmp(word, bucket->word) == 0)
        {
            return true;
        }

        bucket = bucket->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hash function
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Initialize prev
    for (int i = 0; i < N; i++)
    {
        prev[i] = table[i];
    }
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }
    char *word = malloc((LENGTH + 2) * sizeof(char));
    //Read lines from file
    while (fgets(word, LENGTH + 2, dict) != NULL)
    {
        // Remove trailing \n
        word[strlen(word) - 1] = '\0';
        unsigned int h = hash(word);
        node *newNode = malloc(sizeof(node));
        strcpy(newNode->word, word);
        newNode->next = NULL;
        if (table[h] == NULL)
        {
            // Add first node
            table[h] = newNode;
        }
        else
        {
            // Add node
            prev[h]->next = newNode;
        }
        // Save prev for future iterations
        prev[h] = newNode;
        _size++;
    }
    free(word);
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return _size;
}

void unload_node(node *n)
{
    if (n == NULL)
    {
        return;
    }
    unload_node(n->next);
    free(n);
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        unload_node(table[i]);
    }
    return true;
}
