import sys

from crossword import *


class CrosswordCreator:
    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # print(self.crossword.variables)
        # {Variable(0, 1, 'down', 5), Variable(0, 1, 'across', 3), Variable(4, 1, 'across', 4), Variable(1, 4, 'down', 4)}

        # Iterate over the values in the domain of the variable
        for variable in self.crossword.variables:
            # creating a copy to avoid altering the size during the iteration
            for domain in self.domains[variable].copy():
                # Check if the length of the value is not equal to the length of the variable
                if len(domain) != variable.length:
                    # Remove the inconsistent values from the domain of the variable
                    self.domains[variable].remove(domain)

        # print(self.domains)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # initial condition
        revised = False

        overlap = self.crossword.overlaps[x, y]

        # if not overlap, then return false
        if overlap is None:
            return revised

        # getting the idexes from overlap
        i, j = overlap

        for x_value in self.domains[x].copy():
            satifies_constrain = False
            for y_value in self.domains[y]:
                if x_value[i] == y_value[j]:
                    satifies_constrain = True
            if satifies_constrain is False:
                self.domains[x].remove(x_value)
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        arc_queue = arcs if arcs is not None else self.get_all_arcs()
        # print("arc queue")
        # print(arc_queue)
        """ 
        the neighbors of (1, 4) down : 4 are {Variable(4, 1, 'across', 4)}
        the neighbors of (0, 1) across : 3 are {Variable(0, 1, 'down', 5)}
        the neighbors of (4, 1) across : 4 are {Variable(1, 4, 'down', 4), Variable(0, 1, 'down', 5)}
        the neighbors of (0, 1) down : 5 are {Variable(0, 1, 'across', 3), Variable(4, 1, 'across', 4)}

        [(Variable(0, 1, 'down', 5), Variable(0, 1, 'across', 3)), 
        (Variable(0, 1, 'down', 5), Variable(4, 1, 'across', 4)), 
        (Variable(0, 1, 'across', 3), Variable(0, 1, 'down', 5)), 
        (Variable(4, 1, 'across', 4), Variable(0, 1, 'down', 5)), 
        (Variable(4, 1, 'across', 4), Variable(1, 4, 'down', 4)), 
        (Variable(1, 4, 'down', 4), Variable(4, 1, 'across', 4))]
        """

        while arc_queue:
            # Dequeue first element from arcs
            x, y = arc_queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                # removing y from the neighbors set
                for z in self.crossword.neighbors(x) - {y}:
                    arc_queue.append((z, x))

        # print(f"Resulting domains: {self.domains}")
        # Resulting domains: {Variable(0, 1, 'across', 3): {'SIX'}, Variable(4, 1, 'across', 4): {'NINE'},
        # Variable(1, 4, 'down', 4): {'FIVE', 'NINE'}, Variable(0, 1, 'down', 5): {'SEVEN'}}
        return True

    def get_all_arcs(self):
        """
        Generate a list of all arcs in the problem.
        An arc is a tuple (x, y) representing a binary constraint between variables x and y.
        """
        all_arcs = []

        # getting all the arcs generated from all of the neighbors of the x variable
        for x in self.crossword.variables:
            # print(f"the neighbors of {x} are {self.crossword.neighbors(x)}")
            for y in self.crossword.neighbors(x):
                all_arcs.append((x, y))

        return all_arcs

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # checking if all variables have assignments
        for variable in self.crossword.variables:
            if variable not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        assignment_words = set()
        for variable, word in assignment.items():
            # first, checking if word is the same length of variable
            if len(word) != variable.length:
                return False
            # second, checking if there are conflicts with neighbors
            for neighbor in self.crossword(variable):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[variable, neighbor]
                    if word[i] != assignment[neighbor][j]:
                        return False
            # third, check if the word are distinct
            if word in assignment_words:
                return False
            assignment_words.add(word)
        # if all conditions are met, return true
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
