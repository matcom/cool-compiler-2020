def evaluate_parse(productions, tokens):
    def evaluate_production(production, left_parse, tokens, inherited_value=None):
        body = production.Right
        attributes = production.attributes

        synteticed = [None] * (len(body) + 1)
        inherited = [None] * (len(body) + 1)
        inherited[0] = inherited_value

        for i, symbol in enumerate(body, 1):
            if symbol.IsTerminal and not symbol.IsEpsilon:
                assert not inherited[i]
                synteticed[i] = next(tokens).lex
            elif symbol.IsNonTerminal:
                next_production = next(left_parse)
                rule = attributes[i]
                if rule:
                    inherited[i] = rule(inherited, synteticed)
                synteticed[i] = evaluate_production(
                    next_production, left_parse, tokens, inherited[i])

        rule = attributes[0]
        return rule(inherited, synteticed) if rule else None

    tok = iter(tokens)
    prod = iter(productions)
    root = evaluate_production(next(prod), prod, tok)

    return root


def evaluate_right_parse(productions, tokens):
    def evaluate_production(production, right_parse, tokens):
        body = production.Right
        size = len(body) + 1
        attributes = production.attributes
        synteticed = [None] * size

        for i, symbol in enumerate(body, 1):
            if symbol.IsTerminal and not symbol.IsEpsilon:
                synteticed[size - i] = next(tokens).lex
            elif symbol.IsNonTerminal:
                next_production = next(right_parse)
                synteticed[size - i] = evaluate_production(
                    next_production, right_parse, tokens)

        rule = attributes[0]
        return rule([], synteticed) if rule else None
    # Pasar los tokens en orden inverso y quitar el caracter de final de cadena de la lista de tokens
    tok = iter(tokens[::-1][1::])
    prod = iter(productions)
    root = evaluate_production(next(prod), prod, tok)

    return root
