from ..parser import LR1Parser
from .grammar import CoolGrammar

CoolParser = LR1Parser(CoolGrammar)
