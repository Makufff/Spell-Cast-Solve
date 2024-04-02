# import
from time import time
from collections import deque
from copy import deepcopy

dictionary = open("dictionary.txt", "r").read().split("\n")

alphabet = list("abcdefghijklmnopqrstuvwxyz")

letter_values = {
    "a": 1,
    "b": 4,
    "c": 5,
    "d": 3,
    "e": 1,
    "f": 5,
    "g": 3,
    "h": 4,
    "i": 1,
    "j": 7,
    "k": 6,
    "l": 3,
    "m": 4,
    "n": 2,
    "o": 1,
    "p": 4,
    "q": 8,
    "r": 2,
    "s": 2,
    "t": 2,
    "u": 4,
    "v": 5,
    "w": 5,
    "x": 7,
    "y": 4,
    "z": 8
}

def load_board():
    board_file = open("position.txt", "r").read().split("\n")
    board_file = [list(row) for row in board_file]

    for i in range(len(board_file)):
        board_file[i] = [tile for tile in board_file[i] if tile not in list("$+*")]

    return board_file

def load_boosts():
    board_file = open("position.txt", "r").read().split("\n")
    board_file = [list(row) for row in board_file]

    boosts = {
        "$": [],
        "+": [],
        "*": []
    }

    for y, row in enumerate(board_file):
        x_offset = 1
        for x, tile in enumerate(row):
            if tile in list("$+*"):
                boosts[tile].append([x - x_offset, y])
                x_offset += 1

    return boosts

def load_dictionary(letter_count = None):    
    return set([word[:letter_count] for word in dictionary])

def load_redundant_starters(length):
    starters_file = open(f"caches/redundant-{length}.txt", "r").read().split("\n")
    return set(starters_file)

# load in dictionaries
dictionary = load_dictionary()
dictionary_caches = []

# load board in position file
board = load_board()
board_boosts = load_boosts()

class SearchNode:
    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y

    def letter(self):
        return board[self.y][self.x]

    def word(self):
        word = ""
        curr = self
        while True:
            word = curr.letter() + word
            if curr.parent is None:
                break
            else:
                curr = curr.parent
        return word
    
    def score(self):
        score = 0
        curr = self

        doubleWordScore = False
        while True:
            letter_multiplier = 1
            for doubleLetterBoost in board_boosts["+"]:
                if doubleLetterBoost[0] == curr.x and doubleLetterBoost[1] == curr.y:
                    letter_multiplier = 2
                    break
            for tripleLetterBoost in board_boosts["*"]:
                if tripleLetterBoost[0] == curr.x and tripleLetterBoost[1] == curr.y:
                    letter_multiplier = 3
                    break
            if not doubleWordScore:
                for doubleWordBoost in board_boosts["$"]:
                    if doubleWordBoost[0] == curr.x and doubleWordBoost[1] == curr.y:
                        doubleWordScore = True
                        break

            score += letter_values[curr.letter()] * letter_multiplier

            if curr.parent is None:
                break
            else:
                curr = curr.parent

        if doubleWordScore:
            score *= 2
        
        if len(self.word()) >= 6:
            score += 10

        return score
    
    def chain(self):
        nodes = deque()
        curr = self
        while True:
            nodes.appendleft(curr)
            if curr.parent is None:
                break
            else:
                curr = curr.parent
        return list(nodes)
    
    def chain_contains(self, target_node):
        for node in self.chain():
            if node.x == target_node.x and node.y == target_node.y:
                return True
        return False

    def adjacent_nodes(self):
        adjacent = []
        adjacent.append(SearchNode(self, self.x, self.y - 1))
        adjacent.append(SearchNode(self, self.x + 1, self.y - 1))
        adjacent.append(SearchNode(self, self.x + 1, self.y))
        adjacent.append(SearchNode(self, self.x + 1, self.y + 1))
        adjacent.append(SearchNode(self, self.x, self.y + 1))
        adjacent.append(SearchNode(self, self.x - 1, self.y + 1))
        adjacent.append(SearchNode(self, self.x - 1, self.y))
        adjacent.append(SearchNode(self, self.x - 1, self.y - 1))

        valid_adjacent = []
        for node in adjacent:
            if node.x >= 0 and node.x < 5 and node.y >= 0 and node.y < 5:
                valid_adjacent.append(node)

        return valid_adjacent
    
class Move:
    swap = False
    swapped_node: SearchNode = None
    swapped_letter: str = None
    swap_result: str = None

    score = 0

    def __init__(self, frontal_node: SearchNode, score: int):
        self.frontal_node = frontal_node
        self.score = score

    def extract_word(move):
        if move.swap:
            return move.swap_result
        else:
            return move.frontal_node.word()

def search_from_node(root_node, depth):
    global board

    moves = deque()

    frontier = deque()
    frontier.appendleft(root_node)

    while len(frontier) > 0:
        curr = frontier.pop()

        candidate_word = curr.word()
        if candidate_word in dictionary:
            moves.appendleft(Move(curr, curr.score()))
            
        if len(candidate_word) > depth:
            break

        usefulBranch = True
        for i in range(2, depth):
            if len(candidate_word) < i:
                break
            if candidate_word[:i] not in dictionary_caches[i - 2]:
                usefulBranch = False
                break

        if usefulBranch:
            for adjacent_node in curr.adjacent_nodes():
                if not curr.chain_contains(adjacent_node):
                    frontier.appendleft(adjacent_node)

    return list(moves)

def search_board(depth) -> list[Move]:
    global dictionary_caches
    dictionary_caches = [load_dictionary(x) for x in range(2, depth)]

    words = []
    for y in range(5):
        for x in range(5):
            words += search_from_node(SearchNode(None, x, y), depth)

    return words

if __name__ == "__main__":
    # take time for profiling
    start_time = time()

    # search the board
    print("Starting search for best move...")
    moves = search_board(depth=12)

    # remove duplicate words
    unique_moves = []
    for move in moves:
        if Move.extract_word(move) not in [Move.extract_word(unique_move) for unique_move in unique_moves if not unique_move.swap]:
            unique_moves.append(move)
    moves = unique_moves

    # sort words by score
    moves.sort(key=lambda move : move.score, reverse=True)

    # separate by swaps and no swaps
    swap_moves = []
    no_swap_moves = []

    for move in moves:
        if move.swap:
            swap_moves.append(move)
        else:
            no_swap_moves.append(move)

    # display top computer moves
    print("MOVES WITH SWAPS")
    for i, move in enumerate(swap_moves[:5]):
        print(f"{i + 1}. {move.swap_result} via swap at ({move.swapped_node.x + 1}, {move.swapped_node.y + 1}) to {move.swapped_letter} - {move.score} points")

    print("\nMOVES WITHOUT SWAPS")
    for i, move in enumerate(no_swap_moves[:5]):
        print(f"{i + 1}. {move.frontal_node.word()} - {move.score} points")

    print("\nSearch completed!")
    print(f"Words Found: {len(moves)}\nElapsed Time: {round(time() - start_time, 3)}s")