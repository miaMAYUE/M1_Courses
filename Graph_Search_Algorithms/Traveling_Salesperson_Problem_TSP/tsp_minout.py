import time
import random
import math
generated_nodes = 0
expanded_nodes = 0
N = 0
COST_MATRIX = []

class State:
    # Represents a state in the TSP search space.
    # A state is defined by the current city, the path cost so far (g), 
    # and the set of visited cities.
    def __init__(self, current_id, g, visited):
        # Initializes a State object.
        # Args:
        # current_id (int): The ID of the city the agent is currently in.
        # g (int): The cost from the starting city to the current city.
        # visited (set): A set of city IDs that have been visited.
        self.current_id = current_id
        self.g = g
        self.visited = visited
        self.num_visited = len(self.visited)

def expand(parent_node):
    # Generates all valid successor states from a given parent state.
    # Args: parent_node: The state from which to expand.
    # Returns: list[State]: A list of child State objects.
    global generated_nodes
    children = []
    if parent_node.num_visited == N:
        if parent_node.current_id != 0:
            cost = COST_MATRIX[parent_node.current_id][0]
            new_g = parent_node.g + cost
            final_state = State(current_id=0, g=new_g, visited=parent_node.visited)
            generated_nodes += 1
            children.append(final_state)
    else:
        for city_id in range(N):
            if city_id not in parent_node.visited:
                cost = COST_MATRIX[parent_node.current_id][city_id]
                new_g = parent_node.g + cost
                new_visited = parent_node.visited.union({city_id})
                child_node = State(current_id=city_id, g=new_g, visited=new_visited)
                generated_nodes += 1
                children.append(child_node)
    return children

def is_goal(node):
    # Checks if the current state is the goal state.
    # Args: node: The state to check.
    # Returns: bool: True if the state is the goal, False otherwise.
    return node.num_visited == N and node.current_id == 0

def min_out_h(node):
    # Calculates the Min-out h for a given state.
    # The Min-out h is the minimum cost of an edge from the current city to any unvisited city.
    # Args: node: The state for which to calculate the heuristic.
    # Returns: int: The estimated cost from the node to the goal.
    if is_goal(node):
        return 0
    if node.num_visited == N:
        return COST_MATRIX[node.current_id][0]
    min_cost = math.inf
    for city_id in range(N):
        if city_id not in node.visited:
            cost = COST_MATRIX[node.current_id][city_id]
            if cost < min_cost:
                min_cost = cost
    return min_cost if min_cost != math.inf else 0

def dfs(node, path, limit):
    # Performs the core recursive depth-limited search for IDA*.
    # The search is pruned based on the f-value (g + h).
    # Args:
    # node (State): The current state to process.
    # path (list[State]): The path taken to reach the current node.
    # limit (int): The current cost limit for the f-value.
    # Returns: tuple[bool, int]: A tuple containing:
    # A boolean indicating if a solution was found.
    # the cost of the solution if found, or the minimum f-value that exceeded the limit.
    global expanded_nodes
    f_node = node.g + min_out_h(node)
    if f_node > limit:
        return (False, f_node)
    if is_goal(node):
        return (True, node.g)
    expanded_nodes += 1
    new_limit = math.inf
    children_nodes = expand(node)
    for child in children_nodes:
        is_solved, value = dfs(child, path + [child], limit)
        if is_solved:
            return (True, value)
        new_limit = min(new_limit, value)
    return (False, new_limit)
def ida_star(root):
    # The main control loop for the Iterative Deepening A* (IDA*) search.
    # It repeatedly calls DFS with an increasing cost limit (f-value).
    # Args: root: The initial state of the search.
    # Returns: int or str: The optimal cost of the tour if found, otherwise "NO_SOLUTION".
    limit = min_out_h(root)
    path = [root]
    while True:
        solved, new_limit = dfs(root, path, limit)
        if solved:
            return new_limit
        if new_limit == math.inf:
            return "NO_SOLUTION"
        limit = new_limit

def generate_cost_matrix(city_count, seed):
    # Generates a symmetric cost matrix for a given number of cities.
    # Args:
    # city_count (int): The number of cities (N).
    # seed (int): The seed for the random number generator.
    # Returns: list[list[int]]: A 2D list representing the cost matrix where matrix[i][j] is the cost between city i and j.
    random.seed(seed)
    matrix = [[0] * city_count for _ in range(city_count)]
    for i in range(city_count):
        for j in range(i + 1, city_count):
            cost = random.randint(1, 100)
            matrix[i][j] = cost
            matrix[j][i] = cost
    return matrix

if __name__ == "__main__":
    # Main execution block.
    # It iterates through different city counts and random seeds, then calls the IDA* solver.
    city_counts_to_test = [5, 10, 11, 12]
    seeds_to_test = [1, 2, 3, 4, 5]   
    for city_count in city_counts_to_test:
        print(f"\nN = {city_count}")    
        for seed in seeds_to_test:
            N = city_count
            COST_MATRIX = generate_cost_matrix(N, seed)
            generated_nodes = 0
            expanded_nodes = 0        
            print(f"seed = {seed}")
            start_time = time.time()
            initial_visited = {0}
            start_node = State(current_id=0, g=0, visited=initial_visited)
            optimal_cost = ida_star(start_node)
            duration = time.time() - start_time
            print(f"Cost={optimal_cost}, Time={duration:.2f}s, Generated={generated_nodes}, Expanded={expanded_nodes}")