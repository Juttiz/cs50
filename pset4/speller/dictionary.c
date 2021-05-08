// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N] ;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    //Initialize hash table
    for (int i = 0; i < N; i++)
    {
        //hashtable[i] = malloc(sizeof(node));
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];


    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO
        int h = hash(word);
        //int wordlength = strlen(word) + 1;

        // while( n ->next !=NULL)
        // {
        //     n = n->next;
        // }
        node *w = malloc(sizeof(node));
        if(!w)
        {
            return 1;
        }
        node *tmp = hashtable[h];
        for(int l = 0 ; l < LENGTH ; l++)
        {
            if(word[l] != '\0')
            {
                w -> word[l] = word[l];
            }
            else if(word[l] == '\0')
            {
                w -> word[l] = word[l];
                break;
            }
        }
        if(hashtable[h] !=NULL)
        {
        hashtable[h] = w;
        w ->next = tmp;

        }
        else
        {
            hashtable[h] = w;
            w ->next = NULL;

        }

    }

    // Close dictionary
    fclose(file);


    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    unsigned int s = 0;
    node *n = malloc(sizeof(node));

    for(int i = 0; i <= N ; i++)
    {
        n = hashtable[i];
        int sum = 0;
        while(n != NULL)
        {
            n = n ->next;
            sum++;
        }

        s += sum;
    }
    return s;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    int h = hash(word);
    node *cpr = hashtable[h];
    int wl = strlen(word) + 1;
    char *cmpw = malloc(wl*sizeof(char));


    for(int i = 0; i < wl ; i++)
    {
        cmpw[i] = tolower(word[i]);
    }

//     while( cpr != NULL)
//     {

//         for(int i = 0; i < wl; i++)
//         {
//             cmps[i] = cpr ->word[i];
//         }
//         if(strcmp(cmps , cmpw) == 0)
//         {
//             free(cpr);
//             free(cmpw);
//             free(cmps);
//             return true;

//         }
//         else
//         {
//             cpr = cpr->next;
//         }

//     }
//     free(cpr);
//     free(cmpw);
//     free(cmps);
//     return false;
    while(cpr != NULL)
    {
        for(int i = 1; i < wl; i++)
        {
            if(strlen(cmpw) != strlen(cpr->word))
            {
                break;
            }
            else if(cmpw[i] != cpr ->word[i])
            {
                break;
            }
            else if(i == wl - 1)
            {

                free(cmpw);

                return true;
            }
        }
        cpr = cpr ->next;
    }

    free(cmpw);

    return false;

}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    for(int i = 0; i < N; i++ )
    {
        while(hashtable[i] != NULL)
        {
            node *tmp = hashtable[i];
            hashtable[i] = hashtable[i] ->next;
            free(tmp);
        }
    }
    free(hashtable);
    return true;
    //free(hashtable);
    //return false;
}
