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
    # print(r.text)
    return decode_s(r.text)

def save_input(task, num):
    with open(f'{task}_input/{num}.txt', 'w') as f:
        f.write(req(f'get {task}{num}'))

###
save_input('lambdaman', 8)

###

print(req('get lambdaman'))

###


with open('lambdaman/12.txt') as f:
    data = f.read().strip()
    print(data)
    print(req('solve lambdaman12 ' + data))

