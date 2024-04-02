# Discord [Activity] Spell Cast
- Spelling Solve

# Technical Solution
1. Data Loading:
- The code loads necessary resources such as the game board, dictionary, and letter scores from external files.
- Game board and boosts are loaded from the "position.txt" file, while the dictionary is loaded from "dictionary.txt".
- Letter scores are predefined in a dictionary within the code.
2. Search Space Representation:
- Each position on the game board is represented as a node in a graph structure using the SearchNode class.
- The class keeps track of the current position, the parent node, and methods to calculate word formation, score, adjacent nodes, etc.
3. Searching Algorithm:
- The search_board() function searches the entire game board for valid moves.
- It utilizes depth-first search (DFS) starting from each position on the board to explore possible words.
- At each step, it checks if the formed word is present in the loaded dictionary.
- The search is optimized by considering redundant starters loaded from cache and dictionary caching for different word lengths.
4. Move Evaluation:
- Each valid move is represented by the Move class, which contains information about the move, including the score and the word formed.
- The score for each move is calculated considering various factors such as letter values, letter multipliers (double letter, triple letter), and word multipliers (double word).
5. Performance Optimization:
- To optimize performance, the code utilizes data structures like deque for efficient manipulation of move lists and caching of dictionary entries for different word lengths.
- Duplicate words are removed to improve efficiency and reduce redundancy in move calculation.
# Big O Analysis
Time Complexity:
- Search Algorithm (DFS):
 - The time complexity of the DFS algorithm depends on the number of nodes explored.
 - In the worst case, it explores all possible paths on the board, resulting in a time complexity of O(b^d), where b is the branching factor (number of possible moves from each position) and d is the maximum depth of the search.
- Word Formation and Scoring:
 - Calculating the score for each move involves iterating over the formed word, which has a maximum length of the board size (assuming all letters are used).
 - The time complexity for scoring each move is O(1) since it depends on a fixed number of iterations over the word.
- Overall:
 - The overall time complexity is dominated by the search algorithm, making it O(b^d), where b and d depend on the board size and the maximum depth considered for the search.
# Space Complexity:
- The space complexity primarily depends on the data structures used to represent the game board, moves, and dictionary caches.
- The space complexity is O(n), where n is the size of the game board, as additional data structures like move lists and caches require constant space relative to the board size.
- Caching redundant starters and dictionary entries for different word lengths might add additional space overhead but remains relatively small compared to the board size.
# Conclusion
- The provided code efficiently searches for the best moves on the game board by exploring the search space using DFS and considering various scoring factors.
- Despite the exponential time complexity of the search algorithm, the code employs optimizations to enhance performance, such as caching and duplicate removal.
- Overall, the solution demonstrates an effective approach to solving word game puzzles, balancing between computational complexity and practical performance.





