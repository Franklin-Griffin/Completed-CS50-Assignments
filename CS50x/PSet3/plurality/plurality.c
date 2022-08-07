#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);


int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // Loop candidates
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            // Candidate found
            candidates[i].votes++;
            return true;
        }
    }
    // All passes failed
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // Linear search

    // The candidate with top votes found so far
    int max = 0;
    int maxCandidateIndex[] = {-1, -1, -1, -1, -1, -1, -1, -1}; // 8 -1 for max of 8 candidates

    //The amount of OCCUPIED values of maxCandidateIndex
    int arrayLen = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > max)
        {
            // Clear previous winners
            for (int j = 0; j < arrayLen; j++)
            {
                maxCandidateIndex[i] = -1;
            }

            // New top votes, make sure to add it to the array!
            maxCandidateIndex[0] = i;
            // 1 value is occupied
            arrayLen = 1;
            // Set new max
            max = candidates[i].votes;
        }
        else if (candidates[i].votes == max)
        {
            // New top votes, make sure to add it to the array!
            maxCandidateIndex[arrayLen] = i;
            // +1 value is occupied
            arrayLen++;
        }
    }

    // Print full array
    for (int i = 0; i < arrayLen; i++)
    {
        if (maxCandidateIndex[i] == -1)
        {
            return;
        }
        else
        {
            printf("%s\n", candidates[maxCandidateIndex[i]].name);
        }
    }

    return;
}