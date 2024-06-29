lines = [[], [], [], [], []]

for i in range(-99, 100, 1):
    lines[0].extend(['.', 'A'])
    lines[1].extend([str(i), '='])
    if i < 0:
        lines[2].extend(['.', '.'])
        lines[3].extend(['-1', '*'])
        lines[4].extend(['.', 'S'])
    else:
        lines[2].extend(['.', 'S'])

for line in lines:
    print(' '.join(line))
