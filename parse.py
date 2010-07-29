from petri_net import PetriNet
from state import State
import expression
import propositions
import transition

from pypy.rlib.parsing.regexparse import parse_regex
from pypy.rlib.parsing.lexer import Lexer, Token, SourcePos

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

# Petri Net Tokens #
Places = r'P:'
States = r'S:'
Transition = r'T:'
From = r'->'
Number = r'([1-9][0-9]*)|0+'
Separator = r'\|'
rexs = [Places, Transition, From, Number, Separator, Comment, Whitespace, States]
names = ['Places', 'Transition', 'Arrow', 'Number', 'Separator', 'Comment', 'Whitespace', 'State']
ignores = ['Whitespace', 'Comment']
lexer = Lexer([parse_regex(r) for r in rexs], names, ignores)


def parse_net(inp):
    p = PetriNetParser(inp)
    return p.parse()

def parse_props(inp):
    p = PropParser(inp)
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

    def parse(self):
        assert self.i == 0
        self.tokens = lexer.tokenize(self.code)
        self.tokens.reverse()
        token = self.tokens.pop()
        assert token.name == 'Places'
        self.places = self.parse_number()
        while self.tokens[-1].name == 'Transition':
            self.tokens.pop()
            self.parse_transition()
        token = self.tokens.pop()
        assert token.name == 'State'
        net = PetriNet(self.transitions)
        states = self.parse_list()
        state = State(states, net)
        return net, state

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

# Formula tokens #
E, U, Dollar, NotToken = [r'E', r'U', r'$', 'not']
CTL_UNARY_OP = r'X|G'
BOOL_BIN_OP = r'&|\|'
Bools = r'false|true'
Operations = r'=|<'
Par = r'\(|\)'
f_rexs = [Par, BOOL_BIN_OP, E, CTL_UNARY_OP, U, Dollar, Bools, NotToken, Number, Comment, Whitespace, Operations]
f_names = ['Par', 'BOOL_BIN', 'E', 'CTL_UNARY', 'U', 'Dollar', 'Bools', 'Not', 'Number', 'Comment', 'Whitespace', 'Op']
f_lexer = Lexer([parse_regex(r) for r in f_rexs], f_names, ignores)
class PropParser(object):
    def __init__(self, code):
        self.code = code
        self.props = []

    def parse(self):
        self.tokens = f_lexer.tokenize(self.code)
        self.tokens.reverse()
        while self.tokens:
            token = self.tokens.pop()
            assert token.name == 'E'
            if self.tokens[-1].name == 'CTL_UNARY':
                self.props.append(self.parse_unary_operator())
            else:
                self.props.append(self.parse_binary_operator())
        return self.props

    def parse_unary_operator(self):
        token = self.tokens.pop().source
        formula = self.parse_binary_boolean()
        if token == 'X':
            return propositions.EXProposition(formula)
        elif token == 'G':
            return propositions.EGProposition(formula)
        else:
            assert 0, 'no no no'

    def parse_binary_operator(self):
        left = self.parse_binary_boolean()
        token = self.tokens.pop().name
        assert token == 'U'
        right = self.parse_binary_boolean()
        return propositions.EUProposition(left, right)

    def parse_binary_boolean(self):
        lhs = self.parse_unary_boolean()
        if self.tokens and self.tokens[-1].name == 'BOOL_BIN':
            token = self.tokens.pop()
            rhs = self.parse_binary_boolean()
            if token.source == '&':
                return propositions.AndProposition(lhs, rhs)
            else:
                return propositions.OrProposition(lhs, rhs)
        else:
            return lhs

    def parse_unary_boolean(self):
        token = self.tokens[-1]
        if token.name == 'Not':
            self.tokens.pop()
            return propositions.NegationProposition(self.parse_proposition())
        return self.parse_proposition()

    def parse_proposition(self):
        token = self.tokens[-1]
        if token.name == 'Bools':
            return self.parse_boolean()
        if token.name == 'Par':
            return self.parse_sub_proposition()

        lhs = self.parse_atomic()
        assert self.tokens[-1].name == 'Op'
        op = self.tokens.pop()
        rhs = self.parse_atomic()
        if op.source == '=':
            return propositions.EqualsProposition(lhs, rhs)
        elif op.source == '<':
            return propositions.LessProposition(lhs, rhs)
        else:
            assert 0, 'oh noes'

    def parse_boolean(self):
        token = self.tokens.pop()
        if token.source == 'true':
            return propositions.TrueProposition()
        return propositions.FalseProposition()

    def parse_atomic(self):
        token = self.tokens[-1]
        if token.name == 'Dollar':
            v = self.parse_variable()
            assert isinstance(v, expression.VariableExpression)
        else:
            value = self.parse_number()
            assert isinstance(value, int)
            v = expression.NumericExpression(value)
            assert isinstance(v, expression.NumericExpression)
        return v

    def parse_variable(self):
        assert self.tokens.pop().name == 'Dollar'
        return expression.VariableExpression(self.parse_number())

    def parse_sub_proposition(self):
        assert self.tokens.pop().source == '('
        prop = self.parse_binary_boolean()
        assert isinstance(prop, propositions.Proposition)
        assert self.tokens.pop().source == ')'
        return prop

    def parse_number(self):
        assert self.tokens[-1].name == 'Number'
        return int(self.tokens.pop().source)
