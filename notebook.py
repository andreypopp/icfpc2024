enc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n"
dec = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "

forward = {}
backward = {}
for c1, c2 in zip(enc, dec):
    forward[c1] = c2
    backward[c2] = c1

def decode_s(s):
    return ''.join([backward[c] for c in s[1:]])

def encode_s(s):
    return 'S' + ''.join([forward[c] for c in s])

###

import requests

def req(command):
    r = requests.post(
        'https://boundvariable.space/communicate',
        data=encode_s(command),
        headers={'Authorization': 'Bearer 808ca256-780f-4a6d-81cb-f89355cd7440'}
    )
    return decode_s(r.text)

###

from collections import deque

def solve_lambda_man(grid):
    # Find Lambda-Man's starting position
    start = None
    pills = set()
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'L':
                start = (i, j)
            elif cell == '.':
                pills.add((i, j))

    # Define possible moves
    moves = [
        ('U', -1, 0),
        ('R', 0, 1),
        ('D', 1, 0),
        ('L', 0, -1)
    ]

    # BFS
    queue = deque([(start, '', set())])
    visited = set()

    while queue:
        (i, j), path, collected = queue.popleft()
        
        if (i, j) in pills:
            collected = collected | {(i, j)}
        
        if len(collected) == len(pills):
            return path

        if (i, j, tuple(sorted(collected))) in visited:
            continue
        
        visited.add((i, j, tuple(sorted(collected))))

        for direction, di, dj in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj] != '#':
                queue.append(((ni, nj), path + direction, collected))

    return None  # No solution found

# Example usage
grid = [
"#####################",
"#...#.#.........#...#",
"#.###.#.#####.###.###",
"#...#.#.....#.......#",
"###.#.#.###.#########",
"#.#....L..#.#.......#",
"#.#####.###.#.###.###",
"#.#.#...#.......#...#",
"#.#.#######.#######.#",
"#.#...#.#...#.#.....#",
"#.#.###.#.###.###.#.#",
"#.....#...#.......#.#",
"#.###.###.###.#####.#",
"#.#.#...#...#...#...#",
"###.#.#.#.#####.###.#",
"#...#.#...#.....#...#",
"#.###.#.#.#####.#####",
"#.....#.#.....#.#...#",
"#.###.#.#.#.#.#.#.###",
"#.#...#.#.#.#.#.....#",
"#####################",
]

solution = solve_lambda_man(grid)
print(solution) # UDLLLDURRRRRURR

###

from heapq import heappush, heappop

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve_lambda_man2(grid):
    # Find Lambda-Man's starting position and pills
    start = None
    pills = set()
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'L':
                start = (i, j)
            elif cell == '.':
                pills.add((i, j))

    # Define possible moves
    moves = [('U', -1, 0), ('R', 0, 1), ('D', 1, 0), ('L', 0, -1)]

    # A* search
    heap = [(0, 0, start, '', frozenset())]
    visited = set()

    while heap:
        _, cost, (i, j), path, collected = heappop(heap)
        
        if (i, j) in pills:
            collected = collected | {(i, j)}
        
        if len(collected) == len(pills):
            return path

        state = (i, j, collected)
        if state in visited:
            continue
        
        visited.add(state)

        for direction, di, dj in moves:
            ni, nj = i + di, j + dj
            if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj] != '#':
                new_collected = collected | ({(ni, nj)} if (ni, nj) in pills else set())
                new_cost = cost + 1
                print(pills - new_collected)
                heuristic = min(manhattan_distance((ni, nj), p) for p in (pills - new_collected))
                heappush(heap, (new_cost + heuristic, new_cost, (ni, nj), path + direction, new_collected))

    return None  # No solution found

# Example usage
grid = [
    "###.#...",
    "...L..##",
    ".#######"
]

solution = solve_lambda_man2(grid)
print(solution)

###

print(req('get scoreboard'))

###


print(req('solve lambdaman3 DRDRLLULDLLUUURRLDUULUURRRRRDDULLLRDRDRD'))
