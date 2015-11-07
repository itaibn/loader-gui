from coc import *

states = []

def interactive_parse():
    ctx = []
    typ = Sort(1)
    term = Sort(0)

    while (yield 'loop'):
        alt_ctx, alt_typ, alt_term = yield from interactive_parse()
        if alt_ctx == ctx:
            
