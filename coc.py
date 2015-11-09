class Term:
    pass

class Sort(Term):
    def __init__(self, level):
        if type(level) is not int:
            raise TypeError
        if not 0 <= level <= 1:
            raise ValueError

        self.level = level

    def __eq__(self, other):
        return isinstance(other, Sort) and self.level == other.level

    def type(self, ctx):
        if self.level == 0:
            return Sort(1)
        else:
            return None

    def mkfree_var(self, i):
        return self

    def subs(self, i, x):
        return self

    def eval(self):
        return self

    def show(self, ctx, vargen):
        if self.level == 0:
            return '*'
        else:
            return '[]'

    def __repr__(self):
        return 'S{}'.format(self.level)

class Var(Term):
    def __init__(self, i):
        if type(i) is not int:
            raise TypeError
        if not i >= 0:
            raise ValueError

        self.id = i

    def __eq__(self, other):
        return isinstance(other, Var) and self.id == other.id

    def type(self, ctx):
        return ctx[self.i]

    def mkfree_var(self, i):
        if self.id < i:
            return self
        else:
            return Var(self.id + 1)

    def subs(self, i, x):
        if self.id < i:
            return self
        elif self.id > i:
            return Var(self.id - 1)
        else:
            return x

    def eval(self):
        return self

    def show(self, ctx, vargen):
        return ctx[self.id]

    def __repr__(self):
        return '[{}]'.format(self.id)

class PairingTerm(Term):
    def __init__(self, fst, snd, scopeQ):
        self.args = (fst, snd)
        if scopeQ:
            self.snd_scopes = 1
        else:
            self.snd_scopes = 0
        self.scopes = scopeQ

    def __eq__(self, other):
        return type(self) == type(other) and self.args == other.args

    def mkfree_var(self, i):
        return self.remake(self.args[0].mkfree_var(i), self.args[1].mkfree_var(i
            + self.snd_scopes))

    def subs(self, i, x):
        """
        snd_x = x
        for i in range(self.snd_scopes):
            snd_x = snd_x.mkfree_var(0)
        return self.remake(self.args[0].subs(i, x), self.args[1].subs(i +
            self.snd_scopes, snd_x))
        """
        if self.snd_scopes == 0:
            return self.remake(self.args[0].subs(i, x), self.args[1].subs(i, x))
        elif self.snd_scopes == 1:
            return self.remake(self.args[0].subs(i, x),
                               self.args[1].subs(i+1, x.mkfree_var(0)))
        else:
            raise AssertionError

    def eval(self):
        return self.eval_remake(self.args[0].eval(), self.args[1].eval())

    def show_args(self, ctx, vargen):
        arg0 = self.args[0].show(ctx, vargen)
        if self.snd_scopes > 0:
            try:
                inner_var = next(vargen)
            except StopIteration:
                raise ValueError('vargen run out of variable names')
            new_ctx = [inner_var] + ctx
        else:
            new_ctx = ctx
            inner_var = None
        arg1 = self.args[1].show(new_ctx, vargen)
        return inner_var, arg0, arg1

    def __repr__(self):
        return '<{}>{}'.format(type(self).__name__, self.args)
            
class ProdType(PairingTerm):
    def __init__(self, dom, cod):
        PairingTerm.__init__(self, dom, cod, True)

    def remake(self, *arg):
        return ProdType(*arg)

    eval_remake = remake

    def show(self, ctx, vargen):
        v, d, c = self.show_args(ctx, vargen)
        return '(forall {} : {}. {})'.format(v, d, c)

class Lambda(PairingTerm):
    def __init__(self, typ, inner):
        PairingTerm.__init__(self, typ, inner, True)

    def remake(self, *arg):
        return Lambda(*arg)

    eval_remake = remake

    def show(self, ctx, vargen):
        v, t, i = self.show_args(ctx, vargen)
        return '(\\{} : {}. {})'.format(v, t, i)

class Apply(PairingTerm):
    def __init__(self, func, arg):
        PairingTerm.__init__(self, func, arg, False)

    def remake(self, *arg):
        return Apply(*arg)

    def eval_remake(self, *arg):
        return app(*arg)

    def show(self, ctx, vargen):
        _, f, x = self.show_args(ctx, vargen)
        return '({} {})'.format(f, x)

def app(func, arg):
    if isinstance(func, Lambda):
        return func.args[1].subs(0, arg).eval()
    else:
        return Apply(func, arg)

def std_vargen():
    alphabet = 'abcd'
    for v in alphabet:
        yield v
    n = 0
    while True:
        for v in alphabet:
            yield v + str(n)
        n += 1

def arr(a, b):
    return ProdType(a, b.mkfree_var(0))

def church(n):
    expr = Var(0)
    for _ in range(n):
        expr = app(Var(1), expr)
    return Lambda(Sort(0), Lambda(arr(Var(0), Var(0)), Lambda(Var(1), expr)))
