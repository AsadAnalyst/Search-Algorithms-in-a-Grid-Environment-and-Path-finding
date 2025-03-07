import heapq
from typing import List, Tuple
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt


class SearchAlgorithm:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    @staticmethod
    def get_neighbors(x: int, y: int, grid: List[List[str]], wall: set) -> List[Tuple[int, int]]:
        row = len(grid)
        col = len(grid[0])
        neighbor = []
        for dx, dy in SearchAlgorithm.directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < row and 0 <= ny < col and (nx, ny) not in wall:
                neighbor.append((nx, ny))
        return neighbor

    @staticmethod
    def get_start_target(grid: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int], set]:
        start = target = (-1, -1)
        wall = set()
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 's':
                    start = (i, j)
                elif cell == 't':
                    target = (i, j)
                elif cell == '-1':
                    wall.add((i, j))
        return start, target, wall

    @staticmethod
    def reconstruct_path(parent, curr):
        path = []
        while curr:
            path.append(curr)
            curr = parent[curr]
        return path[::-1]

    @staticmethod
    def dfs(grid: List[List[str]]) -> Tuple[int, List[Tuple[int, int]]]:
        result = SearchAlgorithm.get_start_target(grid)
        start = result[0]
        target = result[1]
        wall = result[2]

        stack, visited = [start], set()
        parent = {start: None}

        while stack:
            curr = stack.pop()
            if curr == target:
                return 1, SearchAlgorithm.reconstruct_path(parent, curr)
            if curr in visited:
                continue
            visited.add(curr)
            for neighbor in reversed(SearchAlgorithm.get_neighbors(*curr, grid, wall)):
                if neighbor not in visited:
                    stack.append(neighbor)
                    parent[neighbor] = curr
        return -1, []

    @staticmethod
    def ucs(grid: List[List[str]]) -> Tuple[int, List[Tuple[int, int]]]:
        start, target, wall = SearchAlgorithm.get_start_target(grid)
        priority_queue = [(0, start)]
        visited = set()
        parent = {start: None}

        while priority_queue:
            cost, curr = heapq.heappop(priority_queue)
            if curr == target:
                return 1, SearchAlgorithm.reconstruct_path(parent, curr)
            if curr in visited:
                continue
            visited.add(curr)
            for neighbor in SearchAlgorithm.get_neighbors(*curr, grid, wall):
                if neighbor not in visited:
                    neighbor_cost = int(grid[neighbor[0]][neighbor[1]]) if grid[neighbor[0]][
                        neighbor[1]].isdigit() else 1
                    heapq.heappush(priority_queue, (cost + neighbor_cost, neighbor))
                    parent[neighbor] = curr
        return -1, []

    @staticmethod
    def best_first_search(grid: List[List[str]]) -> Tuple[int, List[Tuple[int, int]]]:
        start, target, wall = SearchAlgorithm.get_start_target(grid)
        priority_queue = [(SearchAlgorithm.manhattanDistance(start, target), start)]
        visited = set()
        parent = {start: None}

        while priority_queue:
            item = heapq.heappop(priority_queue)
            curr = item[1]

            if curr == target:
                return 1, SearchAlgorithm.reconstruct_path(parent, curr)
            if curr in visited:
                continue
            visited.add(curr)
            for neighbor in SearchAlgorithm.get_neighbors(*curr, grid, wall):
                if neighbor not in visited:
                    priority = SearchAlgorithm.manhattanDistance(neighbor, target)
                    heapq.heappush(priority_queue, (priority, neighbor))
                    parent[neighbor] = curr
        return -1, []

    @staticmethod
    def manhattanDistance(x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    @staticmethod
    def a_star(grid: List[List[str]]) -> Tuple[int, List[Tuple[int, int]]]:
        start, target, wall = SearchAlgorithm.get_start_target(grid)
        open_set = [(SearchAlgorithm.manhattanDistance(start, target), 0, start)]
        parent, totalCost = {start: None}, {start: 0}
        while open_set:
            _, curr_cost, curr = heapq.heappop(open_set)
            if curr == target:
                return 1, SearchAlgorithm.reconstruct_path(parent, curr)
            for neighbor in SearchAlgorithm.get_neighbors(*curr, grid, wall):
                neighbor_cost = int(grid[neighbor[0]][neighbor[1]]) if grid[neighbor[0]][neighbor[1]].isdigit() else 1
                new_cost = curr_cost + neighbor_cost
                if neighbor not in totalCost or new_cost < totalCost[neighbor]:
                    totalCost[neighbor] = new_cost
                    priority = new_cost + SearchAlgorithm.manhattanDistance(neighbor, target)
                    heapq.heappush(open_set, (priority, new_cost, neighbor))
                    parent[neighbor] = curr
        return -1, []

    @staticmethod
    def bfs(grid: List[List[str]]) -> Tuple[int, List[Tuple[int, int]]]:
        start, target, wall = SearchAlgorithm.get_start_target(grid)
        queue, visited = [(start, [start])], {start}
        while queue:
            curr, path = queue.pop(0)
            if curr == target:
                return 1, path
            for neighbor in SearchAlgorithm.get_neighbors(*curr, grid, wall):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return -1, []

    @staticmethod
    def visualize_grid(grid: List[List[str]], path: List[Tuple[int, int]] = [], color='red', title="Search"):
        grid_map = np.array([[int(cell) if cell not in ['s', 't'] else 0 for cell in row] for row in grid])
        plt.figure(figsize=(7, 5))
        plt.title(title)
        sb.heatmap(grid_map, annot=True, cmap='Greys', cbar=False, linewidths=.5, linecolor='black')
        for (x, y) in path:
            plt.plot(y + 0.5, x + 0.5, 'o', color=color)
        plt.show()


filename=input("Enter File Name that you want run :")
with open(filename, 'r') as file:
    grid = [line.strip().split() for line in file]

algos = {
    "BFS": (SearchAlgorithm.bfs, 'blue'),
    "DFS": (SearchAlgorithm.dfs, 'green'),
    "UCS": (SearchAlgorithm.ucs, 'purple'),
    "A* Search": (SearchAlgorithm.a_star, 'orange'),
    "Best First Search": (SearchAlgorithm.best_first_search, 'red')
}

for name, (func, color) in algos.items():
    found, path = func(grid)
    if found == 1:
        print(f"\n--------------- {name} --------------------")
        print(f"Path Found With {name}...")
        print("-->", path)
        SearchAlgorithm.visualize_grid(grid, path, color,name)
    else:
        print(f"There is No Path Found With {name}...")
