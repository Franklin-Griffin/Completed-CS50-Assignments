from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Biconditional, signals must be equal, so can't both be true and can't both be false
    Not(Biconditional(AKnight, AKnave)),
    # Again, a biconditional means signals must be equal, so if A was a knave, 
    # AKnight would be false and the other statement would need to be false as well
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Not(Biconditional(AKnight, AKnave)),
    Not(Biconditional(BKnight, BKnave)),
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Not(Biconditional(AKnight, AKnave)),
    Not(Biconditional(BKnight, BKnave)),
    # Again, a biconditional implies the two signals must be the same
    Biconditional(AKnight, Biconditional(AKnight, BKnight)),
    # Biconditional(AKnight, BKnave) also works
    Biconditional(BKnight, Not(Biconditional(AKnight, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Not(Biconditional(AKnight, AKnave)),
    Not(Biconditional(BKnight, BKnave)),
    Not(Biconditional(CKnight, CKnave)),
    Biconditional(AKnight, Or(AKnight, AKnave)),
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    Biconditional(BKnight, CKnave),
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
