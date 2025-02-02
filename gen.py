import rich, rich.tree
from notebook import S, TF, I, U, B, If, L as Lbase, V, dec

class L(Lbase):
    idx = 0

    def __init__(self, lmd):
        v = dec[L.idx]
        L.idx += 1
        e = lmd(V(v))
        super(L, self).__init__(v, e)

class Raw:

    def __init__(self, data):
        self.data = data

    def encode(self):
        return self.data

    def as_tree(self): return rich.tree.Tree(f'Raw({self.data})')

def solve(what, e):
    return B('.', S(f'solve {what} '), e)

def app(lmd, arg):
    return B('$', lmd, arg)

def lambdaman6():
    def dup():
        return L(lambda v: B('.', v, v))
    def with_dup(f): return app(f, dup())
    r = with_dup(L(lambda dup: app(dup, app(dup, app(dup, S('R' * 25))))))
    return solve('lambdaman6', r)

def rle(s):
    cur = None
    n = 0
    res = ""
    for c in s:
        if cur is None or cur == c and n < 9:
            n += 1
            cur = c
        else:
            res += (str(n) + cur)
            cur = c
            n = 1
    res += (str(n) + cur)
    return res

def rle2(s, alpha):
    mark = 90 // len(alpha)
    # print(f"mark: {mark} {len(alpha)}")
    d = {}
    for i, c in enumerate(alpha):
        d[c] = i * mark
    res = ""
    cur = None
    n = 0
    for c in s:
        if cur is None or cur == c and n < mark:
            n += 1
            cur = c
        else:
            res += dec[d[cur] + n - 1]
            cur = c
            n = 1
    res += dec[d[cur] + n - 1]
    return Raw('S' + res), mark

udlr = "UDLR"
ns = "123456789"

def take(n, v): return B('T', I(n), v)
def drop(n, v): return B('D', I(n), v)
def to_int(v): return U('#', v)
def concat(a, b): return B('.', a, b)
def eq(a, b): return B('=',a,b)
def gt(a, b): return B('>',a,b)
def plus(a, b): return B('+',a,b)
def minus(a, b): return B('-',a,b)
def decr(a): return minus(a, I(1))
def app_self(f): return app(L(lambda self : app(self,self)), f)
empty_s = Raw("S")

def rle_encode(data):
    alpha = ''.join(sorted(list(set(data))))
    encoded, mark = rle2(data, alpha)
    def gen_if(next_mark, rev_alpha, mark, dup, self, data):
        if rev_alpha == "":
            return empty_s
        else:
            i = I(next_mark) if next_mark > 0 else U('-', I(abs(next_mark)))
            symbol = S(rev_alpha[0])
            if next_mark > 0:
                return If(
                     gt(to_int(take(1, data)), i),
                        concat(
                            app(app_self(app(dup, symbol)), minus(to_int(take(1, data)), i) ),
                            app(app(self, self), drop(1, data))),
                        gen_if(next_mark - mark, rev_alpha[1:], mark, dup, self, data)
                   )
            else:
                return concat(
                    app(app_self(app(dup, symbol)), minus(to_int(take(1, data)), i) ),
                    app(app(self, self), drop(1, data)))

    dup = L(lambda what: L(lambda self : L(lambda count: If(
            eq(count, I(1)),
            what,
            concat(what, app(app(self, self), decr(count))))
    )))

    main = L(lambda dup:
             L(lambda self:
                L(lambda data:
                    If(eq(take(1, data), empty_s), empty_s,
                       gen_if(mark * (len(alpha) - 1) - 1, alpha[::-1], mark, dup, self, data)
                    )
            )))
    e = app(app_self(app(main, dup)), encoded)
    return e

    # sum = L(lambda dup:
    #          L(lambda self:
    #             L(lambda data:

    #                 If(eq(take(1, data), stop), I(0), plus(to_int(take(1, data)), app(app(self, self), drop(1, data))))
    #         )))

    # e = app( app_self(app(main, dup)), Raw('S' + rle2('R' * 200, udlr)))
    #rich.print(e.as_tree())
    # return e
               # app(app_self( app(dup, S('U')) ), I(200)))))
    # raw = Raw("S#")
    # return to_int(take(1, raw))

    # print(rle2(open('lambdaman/7.txt').read().strip(), udlr))
    # print(rle2(open('task/spaceship12.sol').read().strip(), ns))
    # print(rle2("UUUU", udlr))
    # print(rle2("U" * 80, udlr))
    # print(rle("U" * 20 + 'R' * 10))

def test(): pass
# RRRRRRRRRDRRURRRRRRRRRDRRURRRRRRRRRDRRURRRRRRRRRDRRURRRRLDLLLLLLLLLULLDLLLLLLLLLULLDLLLLLLLLLULLDLLLLLLLLLULLDLLLLDRRRRRRRRRDRRURRRRRRRRRDRRURRRRRRRRRDRRURRRRRRRRRDRRURRRRRDULLD
def lambdaman10():
    lines = [l.strip() for l in open('lambdaman_input/10.txt').readlines()]
    i = 0
    j = 0
    dir = 'R'
    res = ""
    w = len(lines[0])
    while i < len(lines):
        line = lines[i]
        is_last = i == len(lines) - 1
        if i % 2 == 0:
            while True:
                if j < w - 1 and line[j + 1] == '.':
                    res += 'R'
                    j += 1
                    continue
                if j < w - 2 and line[j + 1] == '#':
                    res += 'DRRU'
                    j += 2
                    continue
                # move next line
                if j == w - 2 and line[j + 1] == '#':
                    res += 'DR'
                    j = w - 1
                    break
                if j == w - 1:
                    if lines[i + 1][w - 1] == '#':
                        res += 'LD'
                        j = w - 2
                    else:
                        res += 'D'
                        j = w - 1
                    break
                assert False
        else:
            while True:
                if j > 0 and line[j - 1] == '.':
                    res += 'L'
                    j -= 1
                    continue
                if j > 1 and line[j - 1] == '#':
                    res += 'ULLD'
                    j -= 2
                    continue
                # move next line
                if j == 1 and line[j - 1] == '#':
                    res += 'DL'
                    j = 0
                    break
                if j == 0:
                    if not is_last and lines[i + 1][0] == '#':
                        res += 'RD'
                        j = 1
                    elif not is_last:
                        res += 'D'
                        j = 0
                    break
                assert False
        # print(res)
        # print(j, w)
        # sys.exit(1)
        i += 1
    return solve('lambdaman10', rle_encode(res))

def lambdaman9():
    # 'lambdaman9': lambda: solve('lambdaman9', rle_encode(('R' * 49 + 'D' + 'L' * 49 + 'D')*25)),
    dup = L(lambda what: L(lambda self : L(lambda count: If(
            eq(count, I(1)),
            what,
            concat(what, app(app(self, self), decr(count))))
    )))

    main = L(lambda dup:
              app(app_self(app(dup,
              concat(app(app_self(app(dup, S('R'))), I(49)),
              concat(S('D'),
                  concat(
                    app(app_self(app(dup, S('L'))), I(49)),
                    S('D')
                  ))))), I(25))
            )
    e = solve('lambdaman9', app(main, dup))
    return e

if __name__ == '__main__':
    import sys
    cmds = {
            'rle_encode_test': lambda: rle_encode('RRRUUUDDDLLLUUU'),
            'rle_encode_s': lambda: rle_encode(sys.argv[2].strip()),
            'solve_rle': lambda: solve(sys.argv[2].strip(), rle_encode(open(sys.argv[3].strip()).read().strip())),
            'test': test,
            'lambdaman6': lambdaman6,
            # 'lambdaman9': lambda: solve('lambdaman9', rle_encode(('R' * 49 + 'D' + 'L' * 49 + 'D')*25)),
            'lambdaman9': lambdaman9,
            'lambdaman10': lambdaman10
    }
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        keys = '|'.join(cmds.keys())
        print(f'USAGE: gen.py <{keys}>')
        sys.exit(1)
    e = cmds[sys.argv[1]]()
    if e:
        print(e.encode())

