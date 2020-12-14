from __future__ import annotations
from typing import Iterable, List, Optional, Union
from grammar.symbols import NonTerminal, Production, Symbol, Terminal


class Item:
    """
    La clase  Item representara los items LR.
    Llamaremos item a una cadena de la forma X-> a.B donde:
    
    -a es lo que hemos visto
    -B es lo que nos falta por leer

    Por cada produccion X-> w, tenemos |w| + 1 posibles items 
    """
    def __init__(self,
                 production: Production,
                 pos: int,
                 lookaheads: Iterable[Union[Terminal, NonTerminal]] = []):
        self.production = production
        self.pos = pos
        self.lookaheads = frozenset(look for look in lookaheads)

    @property
    def IsReduceItem(self):
        return len(self.production.Right) == self.pos

    @property
    def NextSymbol(self) -> Optional[Union[Terminal, NonTerminal]]:
        if self.pos < len(self.production.Right):
            return self.production.Right[self.pos]
        else:
            return None

    def next_item(self) -> Optional[Item]:
        if self.pos < len(self.production.Right):
            return Item(self.production, self.pos + 1, self.lookaheads)
        else:
            return None

    def __eq__(self, other: Item):
        return ((self.pos == other.pos)
                and (self.production == other.production)
                and (self.lookaheads == other.lookaheads))

    def __str__(self):
        s = str(self.production.Left) + " -> "
        if len(self.production.Right) > 0:
            for i, c in enumerate(self.production.Right):
                if i == self.pos:
                    s += "."
                s += str(self.production.Right[i])
            if self.pos == len(self.production.Right):
                s += "."
        else:
            s += "."
        s += ", " + str(self.lookaheads)
        return s

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.production, self.pos, frozenset(self.lookaheads)))

    def __iter__(self):
        current = self
        while not current.IsReduceItem:
            yield current
            current = current.next_item()
        yield current

    def Preview(self, skip=1) -> List[Symbol]:
        unseen = self.production.Right[self.pos + skip:]
        return [unseen + (lookahead, ) for lookahead in self.lookaheads]

    def Center(self) -> Item:
        return Item(self.production, self.pos)
