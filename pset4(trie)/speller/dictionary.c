// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// Represents a trie
node *root;


//Hashes words to number
// unsigned int hash(const char word)
// {
//     return tolower(word) = 'a';

// }
// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(sizeof(node));
    if (root == NULL)
    {
        return false;
    }
    root->is_word = false;
    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
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

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO
        int i = 0 ;
        node *tmp = root;
        while(word[i] != '\0')
        {
            int n = tolower(word[i]) - 'a';


            if(tmp ->children[n] == NULL)
            {
                node *w = malloc(sizeof(node));
                w ->is_word = false;
                for(int l = 0; l < N; l++)
                {
                    w -> children[l] = NULL;
                }
                tmp ->children[n] = w;
                tmp = tmp ->children[n];

            }
            else
            {
                tmp = tmp ->children[n];
            }
            i++;

        }
        tmp-> is_word = true;
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
    return 0;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    int i = 0;
    int wl = strlen(word);
    node *cpmw = root;

    while(i < wl)
    {
        int n = tolower(word[i]) - 'a';
        cpmw = cpmw ->children[n];
        if(cpmw == NULL)
        {
            break;
        }
        else if(i == wl -1 && cpmw ->is_word == true)
        {
            //free(cpmw);
            return true;
        }
        i++;
    }
    //free(cpmw);
    return false;
}

node *unl = NULL;
void unloadMain (node* ptr)
{
    if (ptr == NULL)
        return;
    for(int i = 0; i < N; i++)
    {
        if (ptr->children[i] != NULL)
            unloadMain(ptr->children[i]);
    }
    free(ptr);
}
// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    unloadMain(root);
    // if(unl == NULL)
    // {
    //     unl = root;
    // }
    // int i = 0;
    // while(i < N)
    // {
    //     if(unl ->children[i] != NULL)
    //     {
    //         unl = unl-> children[i];
    //         unload();
    //     }
    //     else
    //     i++;
    // }
    // free(unl);
    return true;
    //return false;
}
