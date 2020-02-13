from tools.firsts import compute_firsts
from tools.follows import compute_follows
from grammar.grammar import Grammar

def build_ll1_parsing_table(G:Grammar, firsts: dict, follows: dict):
    table = {}

    for production in G.Productions:
        x,alpha = production.Left, production.Right

        for t in firsts[alpha]:
            #si la tabla contiene entradas repetidas entonces la gramatica
            #no es LL(1)
            assert not table.get((x,t),None), "La gramatica no es LL(1)"
            table[(x,t)] = production

        if firsts[alpha].contains_epsilon:
            for t in follows[x]:
                assert not table.get((x,t),None), "La gramatica no es LL(1)"
                table[(x,t)] = production
    return table

def build_ll1_parser(G: Grammar):
    firsts = compute_firsts(G)
    follows = compute_follows(G, firsts)
    table = build_ll1_parsing_table(G, firsts, follows)

    def parser(w: list):
        #Asumimos que w termina en $
        stack = [G.startSymbol]
        cursor = 0
        output = []

        while stack:
            sym = stack.pop()
            if sym.IsTerminal:
                assert sym == w[cursor].token_type, "La cadena no pertenece al lenguaje"
                cursor += 1
            else:
                try:
                    production = table[(sym,w[cursor].token_type)]
                    output.append(production)
                    try:
                        for symbol in production.Right[::-1]:
                            stack.append(symbol)
                    except AttributeError:
                        pass
                except KeyError:
                    raise Exception('La cadena no pertenece al lenguaje')

        assert w[cursor].token_type == G.EOF, 'La cadena no pertenece al lenguaje'
        return output

    return parser
