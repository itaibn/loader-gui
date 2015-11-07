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
        return isinstance(other, Sort) && self.level == other.level

    def type(self, ctx):
        if self.level == 0:
            return Sort(1)
        else:
            return None

    def raise(self, i):
        return self

    def subs(self, i, x):
        return self

    def eval(self):
        return self

class Var(Term):
    def __init__(self, i):
        if type(i) is not int:
            raise TypeError
        if not i >= 0:
            raise ValueError

        self.id = i

    def __eq__(self, other):
        return isinstance(other, Var) && self.id == other.id

    def type(self, ctx):
        return ctx[self.i]

    def raise(self, i):
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

class PairingTerm(Term):
    def __init__(self, fst, snd, scopeQ):
        self.args = (fst, snd)
        if scopesQ:
            self.snd_scopes = 1

    def __eq__(self, other):
        return type(self) == type(other) && self.args == other.args

    def raise(self, i):
        return self.remake(self.args[0].raise(i), self.args[1].raise(i +
            self.snd_scopes))

    def subs(self, i, x):
        return self.remake(self.args[0].subs(i, x), self.args[1].subs(i +
            self.snd_scopes, x))

    def eval(self):
        return self.eval_remake(self.args[0].eval(), self.args[1].eval())

class ProdType(PairingTerm):
    def __init__(self, dom, cod):
        PairingTerm.__init__(self, dom, cod, True)

    def remake(self, *arg):
        return ProdType(*arg)

    eval_remake = remake

class Lambda(PairingTerm):
    def __init__(self, typ, out):
        PairingTerm.__init__(self, typ, out, True)

    def remake(self, *arg):
        return Lambda(*arg)

    eval_remake = remake

class Apply(PairingTerm):
    def __init__(self, func, arg):
        PairingTerm.__init__(self, func, arg, False)

    def remake(self, *arg):
        return Apply(*arg)

    def eval_remake(self, *arg):
        return app(*arg)

def app(func, arg):
    if isinstance(func, Lambda):
        return func.args[1].subs(0, arg).eval()
    else:
        return Apply(func, arg)
