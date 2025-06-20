import time
import random
import math
generated_nodes = 0
expanded_nodes = 0
N = 0
COST_MATRIX = []

class State:
    def __init__(self, current_id, g, visited):
        self.current_id = current_id
        self.g = g
        self.visited = visited
        self.num_visited = len(self.visited)

def expand(parent_node):
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
    return node.num_visited == N and node.current_id == 0

def dfs(node, path, limit):
    global expanded_nodes

    if is_goal(node):
        return (True, node.g)

    expanded_nodes += 1
    new_limit = math.inf
    solved = False
    children_nodes = expand(node)
    for child in children_nodes:
        f = child.g
        if f <= limit:
            is_solved, value = dfs(child, path + [child], limit)
            if is_solved:
                solved = True
                new_limit = min(value, new_limit)
                break
            else:
                new_limit = min(value, new_limit)
        else:
            new_limit = min(f, new_limit)
    if solved:
        return (True, new_limit)
    else:
        return (False, new_limit)

def ida_star(root):
    limit = 0
    path = [root]
    while True:
        solved, new_limit = dfs(root, path, limit)
        if solved:
            return new_limit
        if new_limit == math.inf:
            return "NO_SOLUTION"
        limit = new_limit

def generate_cost_matrix(city_count, seed):
    random.seed(seed)
    matrix = [[0] * city_count for m in range(city_count)]
    for i in range(city_count):
        for j in range(i + 1, city_count):
            cost = random.randint(1, 100)
            matrix[i][j] = cost
            matrix[j][i] = cost
    return matrix

if __name__ == "__main__":
    city_counts_to_test = [5, 10, 11, 12]
    seeds_to_test = [1, 2, 3, 4, 5]   
    for city_count in city_counts_to_test:
        print(f"\nN = {city_count}")    
        results = []
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
