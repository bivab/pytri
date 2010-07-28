from pypy.rlib.parsing.regexparse import parse_regex
from pypy.rlib.parsing.lexer import Lexer, Token, SourcePos
from petri_net import PetriNet
import transition
# taken from rlib/parsing/test/python_lexer.py
# reg exp helper methods
def group(*choices):
    return '(' + '|'.join(choices) + ')'
def any(*choices):
    return group(*choices) + '*'
def maybe(*choices):
    return group(*choices) + '?'

# Comments and Whitespace, the ignored stuff
Whitespace = r'[ \f\t\r\n]*'
slashStarComment = r'(/\*([^\*]|\*[^/])*\*?\*/)'
slashSlashComment = r'//[^\n]*\n'
poundComment = r'#[^\n]*\n'
Comment = group(slashStarComment, slashSlashComment, poundComment)

Places = r'P:'
Transition = r'T:'
From = r'->'
Number = r'([1-9][0-9]*)|0+'
Separator = r'\|'

rexs = [Places, Transition, From, Number, Separator, Comment, Whitespace]
names = ['Places', 'Transition', 'Arrow', 'Number', 'Separator', 'Comment', 'Whitespace']
ignores = ['Whitespace', 'Comment']

def parse_net(inp):
    p = PetriNetParser(inp)
    return p.parse()

class PetriNetParser(object):
    """
P:5
T:0|2|3 -> 1|2|3
T:1 -> 1|2|3
T:2 -> 1|2|3
T:2 -> 1|2|3
T:4 -> 1|2|3
"""
    def __init__(self, code):
        self.code = code
        self.transitions = []
        self.i = 0

    def _get_lexer(self):
        if not hasattr(self, 'lexer'):
            self.lexer = Lexer([parse_regex(r) for r in rexs], names, ignores)
        return self.lexer

    def parse(self):
        assert self.i == 0
        self.tokens = self._get_lexer().tokenize(self.code)
        self.tokens.reverse()
        token = self.tokens.pop()
        assert token.name == 'Places'
        self.places = self.parse_number()
        while self.tokens:
            token = self.tokens.pop()
            assert token.name == 'Transition'
            self.parse_transition()
        return PetriNet(self.transitions)

    def parse_number(self):
        assert self.tokens[-1].name == 'Number'
        return int(self.tokens.pop().source)

    def parse_transition(self):
        sources = self.parse_list()
        assert self.tokens.pop().name == 'Arrow'
        targets = self.parse_list()
        self.transitions.append(transition.Transition(sources, targets))

    def parse_list(self):
        targets = []
        targets.append(self.parse_number())
        while self.tokens and self.tokens[-1].name == 'Separator':
            self.tokens.pop()
            targets.append(self.parse_number())
        return targets
