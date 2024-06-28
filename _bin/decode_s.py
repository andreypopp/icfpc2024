import os
import sys

enc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`|~ \n"

def decode_s(s):
    return ''.join([enc[ord(c) - 33] for c in s[1:]]j


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

print(decode_s(sys.argv[1]))
