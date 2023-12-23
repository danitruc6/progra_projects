import itertools
import random
import copy


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # if the count is equal to the number of cells, all cells are mines
        if self.count == len(self.cells):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if the count is zero, that means there are not mines and all cells are safe
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # 1) mark the cell as move that has been made
        self.moves_made.add(cell)

        # 2) Mark the cells as safe and add it to the safes
        self.mark_safe(cell)

        # Add a new sentence to the knowledge base, made with the close neighbors cells
        neighbors_cells = self.get_neighbors(cell)

        mine_count = 0
        # Now cleaning the cells which state are determined
        undertermined_neighbors = set()
        for neighbor in neighbors_cells:
            if neighbor in self.mines:
                mine_count += 1
            if neighbor not in self.safes and neighbor not in self.mines:
                undertermined_neighbors.add(neighbor)

        new_sentence = Sentence(undertermined_neighbors, count - mine_count)
        self.knowledge.append(new_sentence)

        # 4) (Update knowledge base based on inferences)
        self.check_knowled_for_safe_or_mine()

        # # 5) (Add new sentences to the knowledge base) the kno the knowledge base)wledge base)
        self.clean_knowledge()
        self.update_inference()

    def check_knowled_for_safe_or_mine(self):
        """
        Iterate through the existing sentences and mark additional cells as safe or mines

        """
        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
            check_mines = sentence.known_mines()
            check_safes = sentence.known_safes()

            # Update self.mines and self.safes based on known information
            # if there are safe cells, mark them as safe cell
            if check_safes:
                # using a copy to avoid runtime error changing size of set during iteration
                for safe_cell in check_safes.copy():
                    self.mark_safe(safe_cell)
            # if there are mine cells, mark them as mine cell
            if check_mines:
                # using a copy to avoid runtime error changing size of set during iteration
                for mine_cell in check_mines.copy():
                    self.mark_mine(mine_cell)

    def clean_knowledge(self):
        """
        Removes any empty sentence or duplicate present in the knowledge
        """
        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
        # Remove duplicates using list comprehention
        self.knowledge = [
            i for n, i in enumerate(self.knowledge) if i not in self.knowledge[:n]
        ]

    def update_inference(self):
        """
        Iterate through pairs of sentences and add new sentences if they can be inferred
        """
        for i in range(len(self.knowledge)):
            for j in range(i + 1, len(self.knowledge)):
                sentence_i = self.knowledge[i]
                sentence_j = self.knowledge[j]

                if sentence_i.cells.issubset(sentence_j.cells):
                    # construct the new sentence set2 - set1 = count2 - count1
                    new_inference_sentence = Sentence(
                        sentence_j.cells - sentence_i.cells,
                        sentence_j.count - sentence_i.count,
                    )
                    if len(new_inference_sentence.cells) != 0:
                        self.knowledge.append(new_inference_sentence)

    def get_neighbors(self, cell):
        """
        Get close neighbors given a cell coordinates
        """
        neighbors_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # if i and j indexes are within range and not equal to cell
                if 0 <= i < self.height and 0 <= j < self.width and (i, j) != cell:
                    neighbors_cells.add((i, j))
        return neighbors_cells

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = {(i, j) for i in range(self.height) for j in range(self.width)}
        possible_moves -= self.moves_made
        possible_moves -= self.mines

        if possible_moves:
            return random.choice(list(possible_moves))
        else:
            return None
