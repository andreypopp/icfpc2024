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

### expressions

class O:
    def __str__(self):          return self.encode()
    def subst(self, _v, _o):    return self
    def expect_I(self):     assert isinstance(self, I);  return self
    def expect_S(self):     assert isinstance(self, S);  return self
    def expect_TF(self):    assert isinstance(self, TF); return self
    def expect_L(self):     assert isinstance(self, L);  return self

class S(O):
    def __init__(self, v): self.v = v
    def encode(self): return encode_s(self.v)
    def eval(self): return self

class TF(O):
    def __init__(self, v): self.v = v
    def encode(self): return 'T' if self.v else 'F'
    def eval(self): return self

class I(O):
    alphabet = [ord('!')+x for x in range(94)]
    alphabet = (''.join([chr(x) for x in alphabet]))

    def __init__(self, v):
        self.v = v

    def encode(self):
        v = self.v
        if v == 0:
            return "0"
        b94 = ""
        while v > 0:
            remainder = v % 94
            b94 = self.alphabet[remainder] + b94
            v //= 94
        return 'I'+b94

    def eval(self):
        return self


class U(O):
    def __init__(self, v, x):
        assert v in {'-', '!', '#', '$'}
        self.v = v
        self.x = x

    def encode(self):
        return f'U{self.v} {self.x.encode()}'

    def subst(self, v, o):
        return U(self.v, self.x.subst(v))

    def eval(self):
        if self.v == '-':
            return I(-self.x.eval().expect_I().v)
        if self.v == '!':
            return TF(not self.x.eval().expect_TF().v)
        if self.v == '#':
            return I(base94_to_base10(self.x.eval().expect_S().encode()[1:]))
        if self.v == '$':
            return S(decode_s('S' + self.x.eval().expect_I().encode()[1:]))
        assert False, "unknown unary operator"
    def __str__(self):
        return f'U({self.v}, {self.x})'

class B(O):
    def __init__(self, v, a, b):
        assert v in {'+', '-', '*', '/', '%', '<', '>', '=', '&', '|', '.',
                     'T', 'D', '$'}, f"unknown binary operator: {v}"
        self.v = v
        self.a = a
        self.b = b

    def subst(self, v, o):
        return B(self.v, self.a.subst(v, o), self.b.subst(v, o))

    def eval(self):
        if self.v == '+':
            return I(self.a.eval().expect_I().v + self.b.eval().expect_I().v)
        if self.v == '-':
            return I(self.a.eval().expect_I().v - self.b.eval().expect_I().v)
        if self.v == '*':
            return I(self.a.eval().expect_I().v * self.b.eval().expect_I().v)
        if self.v == '/':
            return I(self.a.eval().expect_I().v // self.b.eval().expect_I().v)
        if self.v == '%':
            return I(self.a.eval().expect_I().v % self.b.eval().expect_I().v)
        if self.v == '<':
            return TF(self.a.eval().expect_I().v < self.b.eval().expect_I().v)
        if self.v == '>':
            return TF(self.a.eval().expect_I().v > self.b.eval().expect_I().v)
        if self.v == '=':
            return TF(self.a.eval().expect_I().v == self.b.eval().expect_I().v)
        if self.v == '&':
            return TF(self.a.eval().expect_TF().v and self.b.eval().expect_TF().v)
        if self.v == '|':
            return TF(self.a.eval().expect_TF().v or self.b.eval().expect_TF().v)
        if self.v == '.':
            return TF(self.a.eval().expect_S().v + self.b.eval().expect_S().v)
        if self.v == 'T': # take
            return S(self.b.eval().expect_S().v[:self.a.eval().expect_I().v])
        if self.v == 'D': # drop
            return S(self.b.eval().expect_S().v[self.a.eval().expect_I().v:])
        if self.v == '$':
            a = self.a.eval().expect_L()
            return a.e.subst(a.v, self.b).eval()
        else:
            assert False, f"unknown binary operator: {self.v}"

    def encode(self):
        return f'B{self.v} {self.a.encode()} {self.b.encode()}'

class If(O):
    def __init__(self, c, t, e):
        self.c = c
        self.t = t
        self.e = e
    def encode(self):
        return f'? {self.c.encode()} {self.t.encode()} {self.e.encode()}'
    def subst(self, v, o):
        return If(self.c.subst(v, o), self.t.subst(v, o), self.e.subst(v, o))
    def eval(self):
        c = self.c.eval()
        assert isinstance(c, TF)
        if c.v: return self.t.eval()
        else: return self.e.eval()

class L(O):
    def __init__(self, v, e):
        self.v = v
        self.e = e

    def eval(self):
        return self

    def subst(self, v, o):
        if self.v == v: # avoid the capture
            return self
        return L(self.v, self.e.subst(v, o))

    def encode(self):
        return f'L{self.v} {self.e.encode()}'

class V(O):
    def __init__(self, v):
        self.v = v

    def subst(self, v, o):
        if self.v == v: return o
        return self

    def encode(self):
        return f'v{self.v}'

def base94_to_base10(base94_num):
    b10 = 0
    power = 0
    for digit in reversed(base94_num):
        if digit not in I.alphabet:
            raise ValueError(f"Invalid character '{digit}' in base94 number")
        b10 += I.alphabet.index(digit) * (94 ** power)
        power += 1
    return b10

class parse:
    def __init__(self, s):
        self.tokens = s.split(' ')
    def expr(self):
        tok = self.tokens.pop(0)
        if tok[0] == 'I': return I(base94_to_base10(tok[1:]))
        if tok[0] == 'S': return S(decode_s(tok))
        if tok == 'T': return TF(True)
        if tok == 'F': return TF(False)
        if tok[0] == 'U': return U(tok[1], self.expr())
        if tok[0] == 'B': return B(tok[1], self.expr(), self.expr())
        if tok == '?': return If(self.expr(), self.expr(), self.expr())
        if tok[0] == 'L': return L(tok[1:], self.expr())
        if tok[0] == 'v': return V(tok[1:])
        assert False, f"unknown token: {tok}"

def test(s, e):
    v = parse(s).expr().eval().v
    assert v == e, f"expected {e}, got {v}"

test('T', True)
test('F', False)
test('I!', 0)
test('I"', 1)
test('I/6', 1337)
test('SB%,,/}Q/2,$_', 'Hello World!')
test('U- I$', -3)
test('U! T', False)
test('U# S4%34', 15818151)
test('U$ I4%34', 'test')
test('B+ I# I$', 5)
test('B- I$ I#', 1)
test('B* I$ I#', 6)
# TODO: test('B/ U- I( I#', -3)
# TODO: test('B% U- I( I#', -1)
test('B< I$ I#', False)
test('B> I$ I#', True)
test('B= I$ I#', False)
test('B| T F', True)
test('B& T F', False)
test('B. S4% S34', 'test')
test('BT I$ S4%34', 'tes')
test('B$ B$ L# L$ v# B. SB%,,/ S}Q/2,$_ IK', 'Hello World!')
test('B$ L# B$ L" B+ v" v" B* I$ I# v8', parse('I-').expr().v)
