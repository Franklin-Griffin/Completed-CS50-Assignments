import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Format: python dna CSV SEQUENCE")
        quit()
    # TODO: Read database file into a variable
    filename = sys.argv[1]
    with open(filename) as f:
        reader = list(csv.reader(f))
        # Count rows
        row_count = len(reader)
        names = [""] * row_count
        # Count collumns
        col_count = len(reader[0])
        numbers = [[0 for x in range(col_count - 1)] for x in range(row_count)]
        sequences = reader[0][1:]
        # Loop rows (skip first row)
        for i in range(1, row_count, 1):
            # Loop collumns
            for j in range(col_count):
                # Current name/number of current collum
                x = reader[i][j]
                if not(x.isnumeric()):
                    names[i] = x
                else:
                    numbers[i][j - 1] = int(x)

    # Read DNA sequence file into a variable
    filename = sys.argv[2]
    seq = ""
    with open(filename) as f:
        # Store sequence in variable
        seq = f.readlines()[0].strip()
    # Find longest match of each STR in DNA sequence
    seqnumbers = [0 for x in sequences]
    for i in range(len(seqnumbers)):
        seqnumbers[i] = longest_match(seq, sequences[i])
    # TODO: Check database for matching profiles
    for i in range(len(numbers)):
        possible = True
        for j in range(len(numbers[0])):
            if numbers[i][j] != seqnumbers[j]:
                possible = False
        if possible:
            print(names[i])
            return
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
