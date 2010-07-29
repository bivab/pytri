import sys
import os
import time
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
    for prop in props:
        print prop.label()
    g_start = time.time()
    for p in props:
        print p.label(),"= ",
        start = time.time()
        res = state.evaluate(p)
        end = time.time()
        if res:
            print "True",
        else:
            print "False",

        print "(%f)" % (end -start,)
    g_end = time.time()
    print "Total runtime %f" % (g_end - g_start, )
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

