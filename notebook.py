import requests, os
import ipdb
# import rich, rich.tree

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


class O:
    def __str__(self):          return self.encode()
    def __repr__(self):         return self.encode()
    def subst(self, _v, _o):    return self
    def expect_I(self):
        if not isinstance(self, I): ipdb.set_trace()
        return self
    def expect_S(self):     
        if not isinstance(self, S): ipdb.set_trace()
        return self
    def expect_TF(self):
        if not isinstance(self, TF): ipdb.set_trace()
        return self
    def expect_L(self):
        if not isinstance(self, L): ipdb.set_trace()
        return self
    def as_tree(self):
        return rich.tree.Tree(self.encode())
    def compile(self):
        return compile(ctx(), self)
    def eval_bytecode(self):
        return eval_bytecode(compile(ctx(), self))

class S(O):
    __slots__ = ['v']
    def __init__(self, v): self.v = v
    def encode(self): return encode_s(self.v)
    def as_tree(self): return rich.tree.Tree(f'S({self.v})')

class TF(O):
    __slots__ = ['v']
    def __init__(self, v): self.v = v
    def encode(self): return 'T' if self.v else 'F'
    def as_tree(self): return rich.tree.Tree(f'TF({self.v})')

class I(O):
    __slots__ = ['v']
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

    def as_tree(self): return rich.tree.Tree(f'I({self.v})')

class U(O):
    def __init__(self, v, x):
        assert v in {'-', '!', '#', '$'}
        self.v = v
        self.x = x

    def encode(self):
        return f'U{self.v} {self.x.encode()}'

    def subst(self, v, o):
        return U(self.v, self.x.subst(v))

    def __str__(self):
        return f'U({self.v}, {self.x})'

    def as_tree(self):
        t = rich.tree.Tree(f'U{self.v}')
        t.add(self.x.as_tree())
        return t

class B(O):
    def __init__(self, v, a, b):
        assert v in {'+', '-', '*', '/', '%', '<', '>', '=', '&', '|', '.',
                     'T', 'D', '$'}, f"unknown binary operator: {v}"
        self.v = v
        self.a = a
        self.b = b

    def subst(self, v, o):
        return B(self.v, self.a.subst(v, o), self.b.subst(v, o))

    def encode(self):
        return f'B{self.v} {self.a.encode()} {self.b.encode()}'

    def as_tree(self):
        t = rich.tree.Tree(f'B{self.v}')
        t.add(self.a.as_tree())
        t.add(self.b.as_tree())
        return t

class If(O):
    def __init__(self, c, t, e):
        self.c = c
        self.t = t
        self.e = e
    def encode(self):
        return f'? {self.c.encode()} {self.t.encode()} {self.e.encode()}'
    def subst(self, v, o):
        return If(self.c.subst(v, o), self.t.subst(v, o), self.e.subst(v, o))

    def as_tree(self):
        t = rich.tree.Tree('?')
        t.add(self.c.as_tree())
        t.add(self.t.as_tree())
        t.add(self.e.as_tree())
        return t

class L(O):
    def __init__(self, v, e):
        self.v = v
        self.e = e

    def subst(self, v, o):
        if self.v == v: # avoid the capture
            return self
        return L(self.v, self.e.subst(v, o))

    def encode(self):
        return f'L{self.v} {self.e.encode()}'

    def as_tree(self):
        t = rich.tree.Tree(f'L{self.v}')
        t.add(self.e.as_tree())
        return t

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

class parser:
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

def parse(s):
    return parser(s).expr()

class ctx:
    n = 0
    def __init__(self, subst={}):
        self.code = []
        self.subst = {**subst}
    def emit(self, x):
        self.code.append(x)
        return len(self.code) - 1
    def patch(self, idx):
        self.code[idx] = len(self.code)
    def fresh(self):
        self.__class__.n += 1
        return self.__class__.n
    def subctx(self, subst={}):
        return ctx(subst={**self.subst, **subst})

def compile(ctx, self):
    if isinstance(self, (S, I, TF)):
        ctx.emit(self)
    elif isinstance(self, U):
        compile(ctx, self.x)
        ctx.emit(f'U{self.v}')
    elif isinstance(self, B):
        if self.v == '$':
            compile(ctx, self.a)
            subctx = ctx.subctx()
            code = compile(subctx, self.b)
            subctx.emit('RETURN')
            ctx.emit(FunApp(code))
        else:
            compile(ctx, self.a)
            compile(ctx, self.b)
            ctx.emit(f'B{self.v}')
    elif isinstance(self, If):
        compile(ctx, self.c)
        ctx.emit('JE')
        je = ctx.emit(None)
        compile(ctx, self.t)
        ctx.emit('J')
        js = ctx.emit(None)
        ctx.patch(je)
        compile(ctx, self.e)
        ctx.patch(js)
    elif isinstance(self, L):
        sym = ctx.fresh()
        subctx = ctx.subctx({self.v: sym})
        code = compile(subctx, self.e)
        subctx.emit('RETURN')
        ctx.emit(Fun(sym, code))
    elif isinstance(self, V):
        sym = ctx.subst.get(self.v)
        if sym:
            ctx.emit(RefThunk(sym))
        else:
            print(f"WARN: unknown variable: {self.v}")
            ctx.emit('ERROR')
    return ctx.code

class Fun:
    __slots__ = ['sym', 'code']
    def __init__(self, sym, code):
        self.sym = sym
        self.code = code

    def __str__(self):
        return f'Fun({self.sym}, {self.code})'
    __repr__ = __str__

class FunApp:
    __slots__ = ['code', 'locals']
    def __init__(self, code, locals=None):
        self.code = code
        self.locals = locals or {}

    def __str__(self):
        return f'FunApp({self.code})'
    __repr__ = __str__

class RefThunk:
    __slots__ = ['sym']
    def __init__(self, sym):
        self.sym = sym

    def __str__(self):
        return f'RefThunk({self.sym})'
    __repr__ = __str__

class Frame:
    __slots__ = ['code', 'locals', 'len', 'ip']
    def __init__(self, code, locals=None):
        self.code = code
        self.locals = locals or {}
        self.len = len(code)
        self.ip = 0

class Closure:
    __slots__ = ['sym', 'code', 'locals']
    def __init__(self, sym, code, locals):
        self.sym = sym
        self.code = code
        self.locals = locals

    def __str__(self):
        return f'Closure({self.sym}, {self.code}, {self.locals})'
    __repr__ = __str__

def eval_bytecode(code):
    stack = []
    frames = []
    frame = Frame(code)
    while frame.ip < frame.len:
        self = frame.code[frame.ip]
        if isinstance(self, (S, I, TF)):
            stack.append(self)
        elif isinstance(self, Fun):
            stack.append(Closure(self.sym, self.code, frame.locals))
        elif isinstance(self, RefThunk):
            thunk = frame.locals[self.sym]
            assert isinstance(thunk, FunApp)
            frame.ip += 1
            frames.append(frame)
            frame = Frame(thunk.code, locals=thunk.locals)
            continue
        elif isinstance(self, FunApp):
            f = stack.pop()
            assert isinstance(f, Closure)
            frame.ip += 1
            frames.append(frame)
            self = FunApp(self.code, locals=frame.locals)
            frame = Frame(f.code, locals={**f.locals, f.sym: self})
            continue
        elif self == 'RETURN':
            frame = frames.pop()
            continue
        elif self == 'U-':
            # x = stack.pop().expect_I().v
            x = stack.pop().v
            stack.append(I(-x))
        elif self == 'U!':
            # x = stack.pop().expect_TF().v
            x = stack.pop().v
            stack.append(TF(not x))
        elif self == 'U#':
            # x = stack.pop().expect_S().encode()
            x = stack.pop().encode()
            stack.append(I(base94_to_base10(x[1:])))
        elif self == 'U$':
            # x = stack.pop().expect_I().encode()
            x = stack.pop().encode()
            stack.append(S(decode_s('S' + x[1:])))
        elif self == 'B+':
            # y = stack.pop().expect_I().v
            # x = stack.pop().expect_I().v
            y = stack.pop().v
            x = stack.pop().v
            stack.append(I(x + y))
        elif self == 'B-':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(I(x - y))
        elif self == 'B*':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(I(x * y))
        elif self == 'B/':
            y = stack.pop().v
            x = stack.pop().v
            v = abs(x) // abs(y)
            if x * y < 0:
                v = -v
            stack.append(I(v))
        elif self == 'B%':
            y = stack.pop().v
            x = stack.pop().v
            v = abs(x) % abs(y)
            if x * y < 0:
                v = -v
            stack.append(I(v))
        elif self == 'B<':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(TF(x < y))
        elif self == 'B>':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(TF(x > y))
        elif self == 'B=':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(TF(x == y))
        elif self == 'B&':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(TF(x and y))
        elif self == 'B|':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(TF(x or y))
        elif self == 'B$':
            y = stack.pop()
            x = stack.pop().v
            stack.append(TF(x or y))
        elif self == 'B.':
            y = stack.pop().v
            x = stack.pop().v
            stack.append(S(x + y))
        elif self == 'BT': # take
            y = stack.pop().v
            x = stack.pop().v
            stack.append(S(y[:x]))
        elif self == 'BD': # drop
            y = stack.pop().v
            x = stack.pop().v
            stack.append(S(y[x:]))
        elif self == 'JE':
            c = stack.pop().v
            frame.ip += 1
            if not c:
                frame.ip = frame.code[frame.ip]
                continue
        elif self == 'J':
            frame.ip += 1
            frame.ip = frame.code[frame.ip]
            continue
        else:
            assert False, f"unknown instruction: {self}"
        frame.ip += 1
    assert len(stack) == 1
    return stack[0]

def test(s, e):
    # rich.print(parse(s).as_tree())
    v = parse(s).eval_bytecode().v
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
test('B/ U- I( I#', -3)
test('B% U- I( I#', -1)
test('? B> I# I$ S9%3 S./', 'no')
test('B< I$ I#', False)
test('B> I$ I#', True)
test('B= I$ I#', False)
test('B| T F', True)
test('B& T F', False)
test('B. S4% S34', 'test')
test('BT I$ S4%34', 'tes')
test('B$ B$ L# L$ v# B. SB%,,/ S}Q/2,$_ IK', 'Hello World!')
test('B$ L# B$ L" B+ v" v" B* I$ I# v8', parse('I-').v)
test('B$ B$ L" B$ L# B$ v" B$ v# v# L# B$ v" B$ v# v# L" L# ? B= v# I! I" B$ L$ B+ B$ v" v$ B$ v" v$ B- v# I" I%', 16)

def req(command):
    r = requests.post(
        'https://boundvariable.space/communicate',
        data=encode_s(command),
        headers={'Authorization': 'Bearer 808ca256-780f-4a6d-81cb-f89355cd7440'}
    )
    e = parse(r.text)
    return e.eval_bytecode().v

# print(req('get lambdaman21'))
# submit('efficiency', 4, '2')
