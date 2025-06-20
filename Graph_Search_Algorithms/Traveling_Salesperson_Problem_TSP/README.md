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


# Note
DFS：如果到limit边界的最后一次递归都没找到goal，则不满足if (b <= limit)，直接new_limit = b，然后把（false，b）返回给上一层，再探索当前节点的兄弟节点。如果是递归到底都没找到（还没达到limit），则返回（false，∞），再探索当前节点的兄弟节点。

b = c + h(child) 是从当前节点到子节点的（g+h），b = nb + c 是从root到子节点的（g+h），所以从递归底层一层一层往回返时，每一层的b都会变成从当前节点到子节点的（g+h），最终变成从root计算的（g+h）。

new_limit 最终会是在本次搜索中，所有刚好超过当前limit的路径里，f 值最小的那一个，这个值来自最底层节点，且这个值将作为下一次迭代的阈值。其中，“最底层”为“f 值刚好超过 limit 的那一层边界”。

怎么确保IDA*每次调用DFS时，limit都比上一次增大：
因为上一次递归到底时，最后一层的 b = c + h(child)
不再符合 b <= limit，即 new_limit > 当前层的limit。
而new_limit返回给上一层的nb，上一层为当前层后，由 b = nb + c 可知仍有 b > 当前层的limit。
而对于这一层展开的节点们：第一个节点new_limit = min(b, ∞)，必然大于当前层的limit；
除第一个以外的节点们：new_limit = min(各自的b, 由前序节点传来的new_limit)，已证各自的b > 当前层的limit，所以仍能保持new_limit > 当前层的limit。所以当一层一层追溯回从root开始计算的c时，仍有new_limit > limit。

在IDA*的多次DFS调用中，每一次新的（更深的）调用都会完全重复之前所有（更浅的）调用的工作。
but，在一个典型的搜索树中，绝大多数的节点都位于最深的几层。
优点：IDA*本质上是深度优先搜索，它只需要存储当前路径上的节点，所以其内存使用量与搜索深度成线性关系（O(bd)）。
而A*算法需要一个OPEN列表来存储所有待扩展的节点，在最坏的情况下，其内存使用量与搜索空间中的节点总数成正比，可能是指数级的（O(b^d)）。