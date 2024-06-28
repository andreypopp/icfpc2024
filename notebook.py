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

import requests, os

def req(command):
    r = requests.post(
        'https://boundvariable.space/communicate',
        data=encode_s(command),
        headers={'Authorization': 'Bearer 808ca256-780f-4a6d-81cb-f89355cd7440'}
    )
    # print(r.text)
    return decode_s(r.text)

def save_input(task, num):
    input = req(f'get {task}{num}')
    with open(f'{task}_input/{num}.txt', 'w') as f:
        f.write(input)

def save_output(task, num, data):
    with open(f'{task}/{num}.txt', 'w') as f:
        f.write(data)

def get_input(task, num):
    if not os.path.exists(f'{task}_input/{num}.txt'):
        save_input(task, num)
    with open(f'{task}_input/{num}.txt') as f:
        return f.read().strip()

def submit(task, num, data):
    print(req(f'solve {task}{num} {data}'))

def solve_and_submit(task, num, solve):
    input = get_input(task, num)
    output = solve(input)
    submit(task, num, output)
    save_output(task, num, output)

###

save_input('spaceship', 23)
###

# print(req('get lambdaman'))
# print(req('get spaceship'))
print(req('get 3d'))
# print(req('get efficiency'))

###

def y_combinator(f):
    return (lambda x: x(x))(lambda y: f(lambda *args: y(y)(*args)))

def rle(n, w):
    if n == 0: return ''
    else: return w+rle(n-1, w)
