#!/usr/bin/env python
import os
import sys

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
    # return 'S' + ''.join([chr(enc.index(c) + 33) for c in s])

if os.environ.get('ICFP_DECODE_TEST', False):
    # Test the function
    test_strings = [
        r"SB%,,/}Q/2,$_",
        "S'%4}).$%8",
        "S'%4}3#/2%\"/!2$~"
        # "SB%,,/}Q/2,$_",  # "Hello World!"
        # "S4%34",          # "test"
        # "S9%3",           # "yes"
        # "S./",            # "no"
    ]
    for s in test_strings:
        try:
            decoded = decode_s(s)
            print(f"Encoded: {s}")
            print(f"Decoded: {decoded}")
            encoded = encode_s(decoded)
            matches = encoded == s
            print(f"Encode back: {encoded} matches: {matches}")
            print()
        except ValueError as e:
            print(f"Error decoding {s}: {str(e)}")
            print()

if len(sys.argv) > 1:
    cmd = sys.argv[1]
    if cmd == 'decode':
        v = sys.stdin.read()
        print(decode_s(v))
        sys.exit(0)
    elif cmd == 'encode':
        v = sys.stdin.read()
        print(encode_s(v))
        sys.exit(0)
    else:
        print("Unknown command")
        sys.exit(1)
