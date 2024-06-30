from notebook import S, TF, I, U, B, If, L as Lbase, V, dec

class L(Lbase):
    idx = 0

    def __init__(self, lmd):
        v = dec[L.idx]
        L.idx += 1
        e = lmd(V(v))
        super(L, self).__init__(v, e)

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

if __name__ == '__main__':
    import sys
    cmds = {
        'lambdaman6': lambdaman6
    }
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        keys = '|'.join(cmds.keys())
        print(f'USAGE: gen.py <{keys}>')
        sys.exit(1)
    e = cmds[sys.argv[1]]()
    print(e.encode())

