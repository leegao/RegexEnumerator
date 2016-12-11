from collections import defaultdict
from functools import lru_cache

from regex_enumerate.parse import parse

class NFA(object):
    next = 0
    def __init__(self, p, q, transitions):
        self.p = p
        self.q = q
        self.transitions = transitions

    @classmethod
    def eps(cls):
        p = cls.fresh()
        return NFA(p, p, set())

    @classmethod
    def fresh(cls):
        cls.next += 1
        return cls.next

    def __str__(self):
        return str((self.p, self.q, self.transitions))


def compile(ast):
    t, data = ast
    if t == '|':
        if not data: return None
        if len(data) == 1: return compile(*data)
        else:
            rest = compile((t, data[1:]))
            current = compile(data[0])
            if not rest: return current
            p, q = NFA.fresh(), NFA.fresh()
            a, b, c, d = current.p, current.q, rest.p, rest.q
            return NFA(p, q,
                       current.transitions | rest.transitions | {(p, a, '%'), (p, c, '%'), (b, q, '%'), (d, q, '%')})
    elif t == '.':
        if not data: return NFA.eps()
        if len(data) == 1: return compile(*data)
        else:
            rest = compile((t, data[1:]))
            current = compile(data[0])
            if not rest: return rest
            a, b, c, d = current.p, current.q, rest.p, rest.q
            return NFA(a, d, current.transitions | rest.transitions | {(b, d, '%')})
    elif t == '*':
        # (p -> q)* = s -> p -> q -> t + q -> s + s -> t
        sub = compile(data)
        s = NFA.fresh()
        t = NFA.fresh()
        return NFA(s, t, sub.transitions | {(s, sub.p, '%'), (sub.q, t, '%'), (sub.q, sub.p, '%'), (s, t, '%')})
    elif t == 'eps':
        return NFA.eps()
    elif t == 'tok':
        # 0 -x-> 1
        p, q = NFA.fresh(), NFA.fresh()
        return NFA(p, q, {(p, q, data)})


def determinize(nfa):
    @lru_cache()
    def closure(s):
        '''
        Computes the set of states reachable by s through just %-transitions
        '''
        worklist = [s]
        seen = set()
        while worklist:
            u = worklist.pop(0)
            if u in seen: continue
            seen.add(u)
            for (p, q, c) in nfa.transitions:
                if p == u and c == '%':
                    worklist.append(q)
        return seen

    def construct(points, states):
        # close the points
        state = set()
        for point in points:
            state.update(closure(point))

        states.add(tuple(sorted(state)))

        # find all transitions out of state
        out = defaultdict(set)
        for point in state:
            for (p, q, c) in nfa.transitions:
                if point == p and c != '%':
                    out[c].add(q)

        dfa = []
        for c, into in out.items():
            next, rest = construct(into, states)
            dfa += rest
            dfa.append((state, next, c))

        return state, dfa

    start, dfa = construct({nfa.p}, set())
    return (start, nfa.q, dfa)


if __name__ == '__main__':
    nfa = compile(parse("a|b"))
    print(nfa)
    print(determinize(nfa))