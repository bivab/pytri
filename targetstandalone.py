import sys
# __________  Entry point  __________
from expression import NumericExpression, VariableExpression
from petri_net import PetriNet
from propositions import LessProposition, EUProposition, EqualsProposition
from transition import Transition
from state import State

def entry_point(argv):
    t = Transition([0], [1])
    p = PetriNet([t])
    i = 105000
    state = State([i,0], p)
    prop = EUProposition(LessProposition(NumericExpression(0),
    VariableExpression(0)), EqualsProposition(VariableExpression(1),
    NumericExpression(i)))
    if state.evaluate(prop):
        print "True"
    else:
        print "False"
    return 0
# _____ Define and setup target ___


def target(driver, args):
    driver.exe_name = 'pytri-%(backend)s'
    return entry_point, None

def portal(driver):
    raise 'fasdfasdf'

def jitpolicy(self):
    from pypy.jit.metainterp.policy import JitPolicy
    return JitPolicy()

if __name__ == '__main__':
    entry_point(sys.argv)

