#from recordclass import recordclass
from coc import *

class judgement:
    __slots__ = ['ctx', 'typ', 'term']

    def __init__(self, ctx=0, typ=0, term=0):
        self.ctx = ctx; self.typ = typ; self.term = term

    def copy(self):
        return judgement(ctx=self.ctx, typ=self.typ, term=self.term)

t = judgement(ctx=[], typ=Sort(1), term=Sort(0))

states = ['warmup', 'loop', 'apply', 'new-var', 'abstract', 'make-lambda',
    'scope']

class Stack:
    def __init__(self):
        self.list = []

    def __iter__(self):
        return iter(self.list)

    def push(self, x):
        self.list.append(x)

    def index(self, i):
        return self.list[-1-i]

    def top(self):
        return self.index(0)

    def pop(self):
        return self.list.pop()

    def copy(self):
        return [j.copy() for j in self.list]

def interactive_parse(stack, log=print):
    t = judgement(ctx=[], typ=Sort(1), term=Sort(0))
    stack.push(t)

    yield 'warmup'

    #while (yield 'loop'):
    while True:
        #if (yield 'test'):
        #    t.term = Sort(1)
        while (yield 'loop'):
            t = judgement(ctx=[], typ=Sort(1), term=Sort(0))
            stack.push(t)
        t = stack.index(1)
        a = stack.top()
        alt_ctx = a.ctx
        alt_typ = a.typ
        alt_term = a.term

        if alt_ctx == t.ctx:
            if isinstance(t.typ, ProdType) and t.typ.args[0] == alt_typ and \
                    (yield 'apply'):
                t.typ = t.typ.type_with_arg(alt_term)
                #ap = app
                ap = Apply
                t.term = ap(t.term, alt_term)
            if (yield 'new-var') and isinstance(alt_typ, Sort):
                t.ctx = [alt_term.eval()] + t.ctx
                t.typ = t.typ.mkfree_var(0)
                t.term = t.term.mkfree_var(0)
        stack.pop()

        if len(t.ctx) > 0 and (yield 'abstract'):
            domain = t.ctx[0]
            if (yield 'make-lambda') or not isinstance(t.typ, Sort):
                t.typ = ProdType(domain, t.typ)
                t.term = Lambda(domain, t.term)
            else:
                t.term = ProdType(domain, t.term)
            t.ctx = t.ctx[1:]

        if (yield 'scope') and isinstance(t.typ, Sort):
            t.ctx = [t.term.eval()] + t.ctx
            t.typ = t.term.eval().mkfree_var(0)
            t.term = Var(0)

def test_show(ctx, typ, term):
    """
    vargen = std_vargen()
    ctx_var = []
    ctx_str = []
    for typ in reversed(ctx):
        typ_str = typ.show(ctx_var, vargen)
        var = next(vargen)
        ctx_var.append(var)
        ctx_str.append('{:s}: {:s}'.format(var, ctx_str))

    term_str = term.show(ctx_var, vargen)
    typ_str = typ.show(ctx_var, vargen)
    return '{:s} |- {:s} : {:s}'.format(', '.join(ctx_str), term_str, typ_str)
    """
    return show_judgement(judgement(ctx, typ, term))

def show_judgement(t):
    vargen = std_vargen()
    ctx_var = []
    ctx_str = []
    for typ in reversed(t.ctx):
        typ_str = typ.show(ctx_var, vargen)
        var = next(vargen)
        ctx_var = [var] + ctx_var
        ctx_str.append('{:s}: {:s}'.format(var, typ_str))

    term_str = t.term.show(ctx_var, vargen)
    typ_str = t.typ.show(ctx_var, vargen)
    return '{:s} |- {:s} : {:s}'.format(', '.join(ctx_str), term_str, typ_str)
