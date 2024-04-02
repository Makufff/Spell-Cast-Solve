from collections import deque

class Node:
    def __init__(self):
        self.children = {}
        self.is_end_word = False
        self.max_score = 0
        self.value = 0
        self.parent = None

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for char in word:
            node.value += letter_values[char]
            child = node.children.get(char, Node())
            child.parent = node
            node.children[char] = child
            node = child
        node.is_end_word = True
        node.max_score = node.value
        
        while node.parent:
            node = node.parent
            node.max_score = max(node.max_score, child.max_score)

letter_values = {char: value for value, char in enumerate('abcdefghijklmnopqrstuvwxyz', start=1)}
dictionary = set(open('dictionary.txt').read().split())

trie = Trie()
for word in dictionary:
    trie.insert(word)

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

def calculate_score(word, x, y, board, board_boosts):
    score = sum(letter_values[char] for char in word)
    for dx, dy in [(0, 0), (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 5 and 0 <= ny < 5:
            tile = board[ny][nx]
            if tile == '+':
                score += letter_values[word[-1]]
            elif tile == '*':
                score += 2 * letter_values[word[-1]]
            elif tile == '$' and len(word) > 1:
                score *= 2
    return score

def solver(board, board_boosts):
    N = len(board)
    results = []

    def dfs(node, path, score, x, y):
        nonlocal results

        if node.is_end_word:
            word = ''.join(path)
            word_score = calculate_score(word, x, y, board, board_boosts)
            results.append((word, word_score))

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 5 and 0 <= ny < 5:
                child = node.children.get(board[ny][nx], None)
                if child:
                    path.append(board[ny][nx])
                    dfs(child, path, score + child.value, nx, ny)
                    path.pop()

    for y in range(5):
        for x in range(5):
            root = trie.root
            dfs(root, deque(), 0, x, y)

    results.sort(key=lambda x: x[1], reverse=True)
    print("Top 5 words and scores:")
    for i, (word, score) in enumerate(results[:5], start=1):
        print(f"{i}. {word}: {score}")

    return results

# Example usage
board = load_board()
board_boosts = load_boosts()
solver(board, board_boosts)