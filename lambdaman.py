from collections import deque
from difflib import SequenceMatcher

movements = [(0, 1, 'R'), (1, 0, 'D'), (0, -1, 'L'), (-1, 0, 'U')]
opposites = {'R': 'L', 'D': 'U', 'L': 'R', 'U': 'D'}

def opposite_path(path):
    return ''.join([opposites[c] for c in reversed(path)])

def gstart(grid):
    if isinstance(grid, str):
        grid = grid.strip().split('\n')
        grid = [list(row) for row in grid]
    return next((i, j) for i, row in enumerate(grid) for j, x in enumerate(row)
                if x == 'L')

def gpills(grid):
    if isinstance(grid, str):
        grid = grid.strip().split('\n')
        grid = [list(row) for row in grid]
    return {(i, j) for i, row in enumerate(grid) for j, x in enumerate(row)
               if x == '.'}

def gcard(grid):
    return len(gpills(grid))

def solve(grid):
    grid = grid.strip().split('\n')
    grid = [list(row) for row in grid]
    card = gcard(grid)

    rows, cols = len(grid), len(grid[0])

    x, y = gstart(grid)
    queue = deque([(x, y, "", frozenset([(x, y)]))])
    seen = set([(x, y)])

    while queue:
        x, y, path, pseen = queue.popleft()
        moved = 0
        for dx, dy, dir in movements:
            nx, ny = x + dx, y + dy
            if (nx, ny) in seen:
                continue
            seen.add((nx, ny))
            pseen = pseen | {(nx, ny)}
            if len(pseen) == card:
                yield npath, pseen
                continue
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 'x':
                npath = path + dir
                moved = True
                queue.append((nx, ny, npath, pseen))
        if not moved:
            yield path, pseen

i1 = """
xxx.x...
...L..xx
.xxxxxxx
"""

i2 = """
L...x.
x.x.x.
xx....
...xxx
.xx..x
....xx
"""

i3 = """
......
.x....
..x...
...x..
..xLx.
.x...x
......
"""

i4 = """
xxxxxxxxxxxxxxxxxxxxx
x...x.x.........x...x
x.xxx.x.xxxxx.xxx.xxx
x...x.x.....x.......x
xxx.x.x.xxx.xxxxxxxxx
x.x....L..x.x.......x
x.xxxxx.xxx.x.xxx.xxx
x.x.x...x.......x...x
x.x.xxxxxxx.xxxxxxx.x
x.x...x.x...x.x.....x
x.x.xxx.x.xxx.xxx.x.x
x.....x...x.......x.x
x.xxx.xxx.xxx.xxxxx.x
x.x.x...x...x...x...x
xxx.x.x.x.xxxxx.xxx.x
x...x.x...x.....x...x
x.xxx.x.x.xxxxx.xxxxx
x.....x.x.....x.x...x
x.xxx.x.x.x.x.x.x.xxx
x.x...x.x.x.x.x.....x
xxxxxxxxxxxxxxxxxxxxx
"""

i5 = """
.....xxxxxxxx...
....x...........
...x..xxxxxx....
..x..x......x...
.x..x...xx...x..
.x..x..xL.x...x.
.x...x....x...x.
..x...xxxx...x..
...x........x...
....xxxxxxxx....
................
"""

i7 = """
xxxxxxxxxxxxxxxxxxxxxxxxxxxx
x............xx............x
x.xxxx.xxxxx.xx.xxxxx.xxxx.x
x.xxxx.xxxxx.xx.xxxxx.xxxx.x
x.xxxx.xxxxx.xx.xxxxx.xxxx.x
x..........................x
x.xxxx.xx.xxxxxxxx.xx.xxxx.x
x.xxxx.xx.xxxxxxxx.xx.xxxx.x
x......xx....xx....xx......x
xxxxxx.xxxxxxxxxxxxxx.xxxxxx
xxxxxx.xxxxxxxxxxxxxx.xxxxxx
xxxxxx.xx..........xx.xxxxxx
xxxxxx.xx.xxx..xxx.xx.xxxxxx
xxxxxx.xx.x......x.xx.xxxxxx
x.........x......x.........x
xxxxxx.xx.x......x.xx.xxxxxx
xxxxxx.xx.xxxxxxxx.xx.xxxxxx
xxxxxx.xx..........xx.xxxxxx
xxxxxx.xx.xxxxxxxx.xx.xxxxxx
xxxxxx.xx.xxxxxxxx.xx.xxxxxx
x............xx............x
x.xxxx.xxxxx.xx.xxxxx.xxxx.x
x.xxxx.xxxxx.xx.xxxxx.xxxx.x
x...xx........L.......xx...x
xxx.xx.xx.xxxxxxxx.xx.xx.xxx
xxx.xx.xx.xxxxxxxx.xx.xx.xxx
x......xx....xx....xx......x
x.xxxxxxxxxx.xx.xxxxxxxxxx.x
x.xxxxxxxxxx.xx.xxxxxxxxxx.x
x..........................x
xxxxxxxxxxxxxxxxxxxxxxxxxxxx
"""

i8 = open('./lambdaman_input/8.txt').read().strip()
i11 = open('./lambdaman_input/11.txt').read().strip()
i12 = open('./lambdaman_input/12.txt').read().strip()

def solve2(grid):
    pills_todo = gpills(grid)
    current = ""
    last_run = ""
    paths = solve(grid)
    for path, pills in paths:
        if not pills_todo:
            break
        # print('cur', current)
        # print('now', path)
        # print('las', last_run)
        yes = False
        for p in pills:
            if p in pills_todo:
                yes = True
                break
        if yes:
            pills_todo = pills_todo - pills
            current = current + opposite_path(last_run) + path
            # input()
            last_run = path
    return current

with open('./lambdaman/12.txt', 'w') as f:
    f.write(solve2(i12))
