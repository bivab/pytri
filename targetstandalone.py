import sys
import os
# __________  Entry point  __________
from expression import NumericExpression, VariableExpression
from petri_net import PetriNet
from propositions import LessProposition, EUProposition, EqualsProposition
from transition import Transition
from state import State
from parse import parse_net, parse_props

def entry_point(argv):
    file = argv[1]
    p, state = parse_net(read_file(file))
    props = parse_props(argv[2])
    for p in props:
        print p.label(),"= ",
        # XXX add time here
        res = state.evaluate(p)
        # XXX and here
        if res:
            print "True"
        else:
            print "False"
    return 0

def read_file(filename):
    fd = os.open(filename, os.O_RDONLY, 0777)
    content = []
    while 1:
        s = os.read(fd, 4096)
        if not s:
            break
        content.append(s)
    file_content = "".join(content)
    os.close(fd)
    return file_content

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

