"""
Comments and Analysis

1. The code implements the A* algorithm to solve a puzzle. The puzzle is represented as an n x n matrix, where each element can be a number or the underscore character _ representing the empty space.
2. The Node class represents a node in the search tree. It has attributes for the node's data (the puzzle state), level (the depth of the node in the tree), and fval (the calculated f-value for the node).
3. The generate_child method of the Node class generates child nodes by moving the empty space in four directions: up, down, left, and right. It returns a list of child nodes.
4. The shuffle method of the Node class moves the empty space in a given direction and returns the modified puzzle state. If the move is invalid (out of bounds), it returns None.
5. The copy method of the Node class creates a deep copy of a puzzle state matrix.
6. The find method of the Node class finds the position of the empty space in a puzzle state matrix.
7. The Puzzle class represents the puzzle-solving process. It has attributes for the puzzle size, open list (nodes to be explored), and closed list (nodes already explored).
8. The accept method of the Puzzle class accepts the start and goal puzzle states from the user.
9. The f method of the Puzzle class calculates the heuristic value f(x) for a given node using the heuristic function h(x) + g(x). Here, h(x) calculates the difference between the given puzzles, and g(x) is the level (depth) of the node.
10. The h method of the Puzzle class calculates the number of misplaced tiles (excluding the empty space) between two puzzle states.
11. The process method of the Puzzle class performs the A* algorithm. It initializes the start node, calculates its f-value, and adds it to the open list. Then, it enters a loop where it selects the node with the lowest f-value from the open list, generates its child nodes, calculates their f-values, and adds them to the open list. The current node is moved to the closed list. The loop continues until the goal node is reached (the difference between the current and goal nodes is 0).
12. The open list is sorted based on f-value in each iteration, ensuring that the node with the lowest f-value is selected next
"""

class Node:
    def __init__(self, data, level, fval):
        """ Initialize the node with the data, level of the node, and the calculated fvalue """
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        """ Generate child nodes from the given node by moving the blank space
            either in the four directions {up, down, left, right} """
        x, y = self.find(self.data, '_')
        """ val_list contains position values for moving the blank space in either of
            the 4 directions [up, down, left, right] respectively. """
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.shuffle(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = Node(child, self.level + 1, 0)
                children.append(child_node)
        return children

    def shuffle(self, puz, x1, y1, x2, y2):
        """ Move the blank space in the given direction and if the position values are out
            of limits, then return None """
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

    def copy(self, root):
        """ Copy function to create a similar matrix of the given node """
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

    def find(self, puz, x):
        """ Specifically used to find the position of the blank space """
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puz[i][j] == x:
                    return i, j


class Puzzle:
    def __init__(self, size):
        """ Initialize the puzzle size by the specified size, open and closed lists to empty """
        self.n = size
        self.open = []
        self.closed = []

    def accept(self):
        """ Accept the puzzle from the user """
        puz = []
        for i in range(0, self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    def f(self, start, goal):
        """ Heuristic Function to calculate heuristic value f(x) = h(x) + g(x) """
        return self.h(start.data, goal) + start.level

    def h(self, start, goal):
        """ Calculates the difference between the given puzzles """
        temp = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    temp += 1
        return temp

    def is_solvable(self, start, goal):
        """ Check if the puzzle is solvable """
        start_inversions = self.count_inversions(start)
        goal_inversions = self.count_inversions(goal)

        if self.n % 2 == 0:
            # For even-sized puzzles
            start_blank_row = self.find_blank_row(start)
            goal_blank_row = self.find_blank_row(goal)

            # Adjust the inversion counts for even-sized puzzles
            start_inversions += start_blank_row
            goal_inversions += goal_blank_row

        return start_inversions % 2 == goal_inversions % 2

    def count_inversions(self, puzzle):
        """ Count the number of inversions in the puzzle """
        flat_puzzle = [val for row in puzzle for val in row if val != '_']
        inversions = 0
        for i in range(len(flat_puzzle)):
            for j in range(i + 1, len(flat_puzzle)):
                if flat_puzzle[i] > flat_puzzle[j]:
                    inversions += 1
        return inversions

    def find_blank_row(self, puzzle):
        """ Find the row index containing the blank space """
        for i in range(self.n):
            if '_' in puzzle[i]:
                return i
        return -1

    def is_goal_state(self, current, goal):
        """ Check if the current node's state matches the goal state """
        for i in range(self.n):
            for j in range(self.n):
                if current[i][j] != goal[i][j]:
                    return False
        return True

    def process(self):
        """ Accept Start and Goal Puzzle state """
        print("Enter the start state matrix:")
        start = self.accept()
        print("Enter the goal state matrix:")
        goal = self.accept()

        if not self.is_solvable(start, goal):
            print("The given puzzle configuration is unsolvable.")
            return

        start = Node(start, 0, 0)
        start.fval = self.f(start, goal)
        """ Put the start node in the open list """
        self.open.append(start)
        print("\n\n")
        while True:
            cur = self.open[0]
            print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for i in cur.data:
                for j in i:
                    print(j, end=" ")
                print("")
            """ If the current node's state matches the goal state, we have reached the goal node """
            if self.is_goal_state(cur.data, goal):
                break
            for i in cur.generate_child():
                i.fval = self.f(i, goal)
                self.open.append(i)
            self.closed.append(cur)
            del self.open[0]

            """ Sort the open list based on f value """
            self.open.sort(key=lambda x: x.fval, reverse=False)


puz = Puzzle(3)
puz.process()


"""

Time Complexity Analysis:

The time complexity of the A* algorithm depends on the size of the puzzle (n) and the number of nodes expanded.
In the worst case, the algorithm explores all possible states until it finds the goal state.
Assuming there are k possible states reachable from each node, the worst-case time complexity can be approximated as O(k^d), 
where d is the depth of the goal state from the start state.
In this case, k is at most 4 (four possible directions to move the empty space), and d is unknown beforehand.

Space Complexity Analysis:

The space complexity of the A* algorithm depends on the maximum number of nodes stored in the open and closed lists during the search.
In the worst case, where all nodes need to be explored, the maximum number of nodes in the open list is proportional to the number of expanded nodes.
Therefore, the worst-case space complexity can be approximated as O(k^d), similar to the time complexity.

Note: The actual time and space complexity may vary depending on the specific puzzle instance and the efficiency of the heuristic function.

Overall, the code is well-structured and implements the A* algorithm for solving puzzles.
It would be helpful to have additional information about the specific puzzle being solved to provide more accurate time and space complexity analysis.

"""