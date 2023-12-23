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
    # A is either a Knigh or a Knave, but can't be both at the same time
    # This is represented by a exclusive OR formed by And(OR,NAND)
    And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))),
    # If A is knight, means that he's both Knight and Knave
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is knave, means that he can't be both Knight and Knave
    Implication(AKnave, Not(And(AKnight, AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A can be either a knight or Knave
    Biconditional(AKnight, Not(AKnave)),
    # B can be either a knight or Knave
    Biconditional(BKnight, Not(BKnave)),
    # If A is a Knight, he should be telling the truth, which is contradictory
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is Knave, then he's lying and both of them cannnot be knaves, sentence cannot be true
    Implication(AKnave, Not(And(AKnave, BKnave))),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A can be either a knight or Knave
    Biconditional(AKnight, Not(AKnave)),
    # B can be either a knight or Knave
    Biconditional(BKnight, Not(BKnave)),
    # If A is Knight, they are the same kind
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If A is Knave, they are not the same kind
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # If B is Knight, they are not the same kind
    Implication(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # If B is Knave, they are  the same kind
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A can be either a knight or Knave
    Biconditional(AKnight, Not(AKnave)),
    # B can be either a knight or Knave
    Biconditional(BKnight, Not(BKnave)),
    # C can be either a knight or Knave
    Biconditional(CKnight, Not(CKnave)),
    # If B is a Knight, then A said I'm a knave and C is nave
    Implication(
        BKnight,
        And(
            # If A Knight, then B Knave
            Implication(AKnight, AKnave),
            # If A Knave, then B not Knave
            Implication(AKnave, Not(AKnave)),
            CKnave,
        ),
    ),
    # If B is a Knave, then A said I'm a knave and C is nave is not true
    Implication(
        BKnave,
        And(
            # If A Knight, then A not Knave
            Implication(AKnight, AKnight),
            # If A Knave, then B Knave
            Implication(AKnave, Not(AKnight)),
            Not(CKnave),
        ),
    ),
    # if C is a Knight, then A is knight
    Implication(CKnight, AKnight),
    # if C is a Knave, then A is not knight
    Implication(CKnave, Not(AKnight)),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
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
