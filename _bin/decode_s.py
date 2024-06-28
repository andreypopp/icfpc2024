import os
import sys

enc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n"

def decode_s(s):
    return ''.join([enc[ord(c) - 33] for c in s[1:]])

def encode_s(s):
    return 'S' + ''.join([chr(enc.index(c) + 33) for c in s])

if os.environ.get('ICFP_DECODE_TEST', False):
    # Test the function
    test_strings = [
        r"SB%,,/}Q/2,$_"
        # "SB%,,/}Q/2,$_",  # "Hello World!"
        # "S4%34",          # "test"
        # "S9%3",           # "yes"
        # "S./",            # "no"
    ]
    for s in test_strings:
        try:
            decoded = decode_icfp_string(s)
            print(f"Encoded: {s}")
            print(f"Decoded:  {decoded}")
            print()
        except ValueError as e:
            print(f"Error decoding {s}: {str(e)}")
            print()

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
