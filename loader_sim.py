from coc import *

states = ['loop', 'apply', 'new-var', 'abstract', 'make-lambda', 'scope']

def interactive_parse(out=None, log=print):
    ctx = []
    typ = Sort(1)
    term = Sort(0)

    while (yield 'loop'):
        recurse_out = [None] * 3
        yield from interactive_parse(recurse_out)
        alt_ctx, alt_typ, alt_term = recurse_out

        if alt_ctx == ctx:
            if isinstance(alt_typ, ProdType) and alt_type.args[0] == typ and \
                    (yield 'apply'):
                typ = alt_typ.args[1].subs(0, term)
                term = app(alt_term, term)
            if (yield 'new-var') and isinstance(alt_typ, Sort):
                ctx = [alt_type] + ctx
                typ = typ.mkfree_var(0)
                term = term.mkfree_var(0)

        if len(ctx) > 0 and (yield 'abstract'):
            domain = ctx[0]
            ctx = ctx[1:]
            if (yield 'make-lambda') or not isinstance(typ, Sort):
                typ = ProdType(domain, typ)
                term = Lambda(domain, term)
            else:
                term = ProdType(domain, term)

        if (yield 'scope') and isinstance(term, Sort):
            ctx = [term] + ctx
            typ = term.eval().mkfree_var(0)
            term = Var(0)

        log(test_show(term, ctx))

    if out is not None:
        out[0] = ctx
        out[1] = typ
        out[2] = term

def test_show(term, ctx):
    v = std_vargen()
    vctx = []
    for _ in range(len(ctx)):
        vctx = [next(v)] + vctx
    return term.show(vctx, v)
