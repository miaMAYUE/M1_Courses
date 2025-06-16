# Mandatory Assignment 4：Solving the Traveling Salesperson Problem with IDA*

### Project Overview

This project implements and compares the performance of the Iterative Deepening A* (IDA*) search algorithm to solve the **Traveling Salesperson Problem (TSP)**. Two variations of IDA* are implemented: one with a null heuristic (`h(n)=0`) and another with a **Min-out heuristic**. The primary goal is to analyze and contrast their efficiency in terms of runtime, expanded nodes, and generated nodes across various problem sizes.

---

### 1. Problem Background

- This assignment tackles the **Traveling Salesperson Problem (TSP)**, a well-known **NP-hard** problem.
- **Objective**: Given N cities, a salesperson must find a tour that starts at a designated city, visits each city exactly once, and returns to the start, all while minimizing the total travel cost.
- For more details, see the [Wikipedia article](https://en.wikipedia.org/wiki/Travelling_salesman_problem).

---

### 2. Algorithms & Heuristics

The following algorithms were implemented for this task:
1. **IDA*** with a null heuristic function (`h(n)=0`).
2. **IDA*** with the **Min-out heuristic function**.

> **Min-out Heuristic `h(n)` Definition**
>
> If the search is currently at a node `n` corresponding to city `i`, the heuristic is the minimum cost to travel from city `i` to any of the remaining unvisited cities.
>
> `h(n) = min(cost(i, j_1), cost(i, j_2), ..., cost(i, j_k))`
>
> where `j_1, ..., j_k` are the IDs of all unvisited cities.

---

### 3. Experimental Setup

- **Programming Language**: Any language is permitted.
- **City Configuration**:
    - The number of cities `N` tested were **5, 10, 11, and 12**.
    - City IDs range from `0` to `N-1`. The tour always starts and ends at city `0`.
- **Problem Generation**:
    - For each `N`, **5 unique problems** were generated for performance evaluation.
    - The cost between any two cities, `cost(i, j)`, is a randomly generated integer in the range **[1, 100]**.
    - To ensure reproducibility and fair comparison, fixed random **seeds of 1, 2, 3, 4, and 5** were used for the 5 problems, respectively.

---

### 4. Evaluation Metrics

- A **time limit of 20 minutes** was set for each problem instance.
- The performance of each algorithm for a given `N` is summarized in a table with the following metrics:

| Metric | Description |
| :--- | :--- |
| **Solved Problems** | The number of problems (out of 5) solved within the time limit. |
| **Average Runtime** | The average time taken across all 5 problems. Unsolved problems are counted as 20 minutes. |
| **Average Optimal Cost** | The average cost of the optimal path found, averaged over *solved* problems only. |
| **Avg. Expanded Nodes** | The average number of nodes expanded during the search, averaged over *solved* problems only. |
| **Avg. Generated Nodes** | The average number of nodes generated during the search, averaged over *solved* problems only. |

> **Note**: For all metrics except runtime, reported values are truncated integers. If no problems were solved, the value is "NA".

---

### 5. Implementation Details

#### State Representation

A class structure was used to represent the search state, which includes the current location and the set of visited cities.

```cpp
class State {
    bool visited[N];   // Flags for visited cities.
    int num_visited;     // The number of visited cities.
    int current_id;      // The ID of the current city.
};
```
This representation cleverly avoids cycles in the search space. A state is uniquely defined by (current_id, visited_set). Therefore, standard cycle detection within the IDA* implementation was unnecessary.

### Code Correctness & Comments
- Correctness Check: The validity of the implementations was verified by ensuring that for any given problem instance, all algorithms produced the same optimal solution cost. While optimal paths might differ, the minimum cost must be identical.
- Code Documentation: Each function/method in the source code includes comments explaining its purpose, arguments, and return values.

### Time Measurement
- Runtime was measured within the program using standard library functions for tracking wall-clock time.