
enc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n"
dec = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

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

req('get index')
