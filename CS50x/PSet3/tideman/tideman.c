#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // Loop candidates
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            // Candidate found
            ranks[rank] = i;
            return true;
        }
    }
    // All passes failed
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // Loop entries             except the last one
    for (int i = 0; i < candidate_count - 1; i++)
    {
        // Update value for all who are ranked below this value
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // Loop candidates
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pair p;
                p.winner = i;
                p.loser = j;
                pairs[pair_count] = p;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // Selection sort
    for (int i = 0; i < pair_count; i++)
    {
        int max = 0;
        int maxindx = 0;
        for (int j = i; j < pair_count; j++)
        {
            int difference = preferences[pairs[j].winner][pairs[j].loser];
            if (difference > max)
            {
                maxindx = j;
                max = difference;
            }
        }
        // Swap
        pair temp = pairs[i];
        pair n;
        n.winner = pairs[maxindx].winner;
        n.loser = pairs[maxindx].loser;
        pairs[i] = n;
        pairs[maxindx] = temp;
    }
    return;
}

bool HasLoop(int lock1[], int lock2[], int winner, int cur, int lock_count)
{
    // Check for loop (recursively)
    if (cur == winner)
    {
        // Loop
        return true;
    }
    bool loopFound = false;
    for (int i = 0; i < lock_count; i++)
    {
        if (lock1[i] == cur)
        {
            if (HasLoop(lock1, lock2, winner, lock2[i], lock_count))
            {
                return true;
            }
        }
    }
    // No loops
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // Loop pairs
    int lock_count = 0;
    for (int i = 0; i < pair_count; i++)
    {
        bool loop = false;
        int winner = pairs[i].winner;
        int loser = pairs[i].loser;
        int cur = loser;
        int lock1[pair_count];
        int lock2[pair_count];
        if (!HasLoop(lock1, lock2, winner, cur, lock_count))
        {
            locked[winner][loser] = true;
            lock1[lock_count] = winner;
            lock2[lock_count] = loser;
            lock_count++;
            printf("%s %s\n", candidates[winner], candidates[loser]);
        }
    }

    return;
}

// Print the winner of the election
void print_winner(void)
{
    // Loop candidates
    for (int i = 0; i < candidate_count; i++)
    {
        bool canWin = true;
        // Again
        for (int j = 0; j < candidate_count; j++)
        {
            // If inner loop beat outer loop
            if (locked[j][i])
            {
                // Cannot win (not base)
                canWin = false;
                break;
            }
        }

        if (canWin)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
    return;
}