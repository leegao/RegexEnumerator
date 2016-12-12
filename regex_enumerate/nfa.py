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
            return NFA(a, d, current.transitions | rest.transitions | {(b, c, '%')})
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

    states = {}

    def construct(points, first = True):
        # close the points
        state = set()
        for point in points:
            state.update(closure(point))

        key = tuple(sorted(state))
        if key in states and not first: return state, states[key], False
        if key not in states:
            states[key] = []
        changed = False

        # find all transitions out of state
        out = defaultdict(set)
        for point in state:
            for (p, q, c) in nfa.transitions:
                if point == p and c != '%':
                    out[c].add(q)

        dfa = []
        for c, into in out.items():
            next, rest, cur = construct(into, False)
            changed |= cur
            dfa += rest
            dfa.append((state, next, c))

        if sorted(dfa) != sorted(states[key]):
            states[key] = list(dfa)
            changed = True
        return state, dfa, changed

    start, dfa, changed = construct({nfa.p})
    iterations = 10
    while changed and iterations > 0:
        start, dfa, changed = construct({nfa.p})
        iterations -= 1
    return (start, nfa.q, dfa)


def reconstruct(start, final_atom, dfa):
    # get a list of all states
    states = [tuple(sorted(start))]
    seen = {tuple(sorted(start))}
    for (p, q, c) in dfa:
        ps, qs = tuple(sorted(p)), tuple(sorted(q))
        if ps not in seen: states.append(ps)
        seen.add(ps)
        if qs not in seen: states.append(qs)
        seen.add(qs)
    # reassign dfa
    # original = list(dfa)
    hash = {}
    accepts = set()
    for i, state in enumerate(states):
        hash[state] = i + 1
        if final_atom in state: accepts.add(i + 1)
    dfa = sorted(set([(hash[tuple(sorted(p))], hash[tuple(sorted(q))], c) for p, q, c in dfa]))
    n = len(states)
    @lru_cache()
    def R(i, j, k):
        '''
        R(i, j, k) is the regular expression for the language that goes from state i to
        state j using only intermediate steps from the subset of states of {1, ..., k}
        '''
        if k == 0:
            # find all transitions (i, j, c)
            alts = []
            for (p, q, c) in dfa:
                if p == i and q == j:
                    alts.append(('tok', c))
            if i == j:
                alts.append(('eps', '%'))
            return ('|', alts)
        else:
            # R(i,j,k-1) + R(i,k,k-1) R(k,k,k-1)* R(k,j,k-1), unless i = k or j = k
            if k != i and k != j:
                left = R(i, j, k - 1)
                ik = R(i, k, k - 1)
                kk = R(k, k, k - 1)
                kj = R(k, j, k - 1)
                return ('|', [left, ('.', [ik, ('*', kk), kj])])
            if k == i and k != j:
                # R(i, i)*R(i, j)
                ii = R(i, i, k - 1)
                ij = R(i, j, k - 1)
                return ('.', [('*', ii), ij])
            else:
                # R(i, j)R(j, j)*
                jj = R(j, j, k - 1)
                ij = R(i, j, k - 1)
                return ('.', [ij, ('*', jj), ])

    return R, dfa, accepts, n


def reduce(regex):
    # canonicalize operations on 0 and %
    zero = ('|', [])
    eps = lambda x: x == ('eps', '%') or x == ('.', [])
    t, data = regex
    if regex == zero: return zero
    if eps(regex): return ('eps', '%')

    if t == '|':
        rest = [sub for sub in map(reduce, data) if sub != zero]
        nullable = [sub for sub in rest if eps(sub)]
        rest = [sub for sub in rest if not eps(sub)]
        if nullable: rest += [('eps', '%')]
        if len(rest) is 1: return rest[0]
        return ('|', rest) if rest else zero

    if t == '.':
        rest = [sub for sub in map(reduce, data) if not eps(sub)]
        if zero in rest: return zero
        if len(rest) is 1: return rest[0]
        return ('.', rest) if rest else ('eps', '%')

    if t == '*':
        t_, data_ = reduce(data)
        if (t_, data_) == zero:
            return zero
        if t_ == 'eps':
            return ('eps', '%')
        if t_ == '*':
            # e** = e*
            return data_
        if t_ == '|':
            assert data_
            # (% + e)* = e*
            if any(sub for sub in data_ if eps(sub)):
                data__ = [sub for sub in data_ if not eps(sub)]
                return reduce(('*', ('|', data__)))
            return ('*', (t_, data_))
        if t_ == '.':
            assert data_
            # (e.e)* = (e.e)*
            return ('*', (t_, data_))
    return (t, data)


def atomic(ast):
    t, data = ast
    if t in {'tok', 'eps', '*'}: return True


def print_regex(ast):
    t, data = ast
    if t == 'tok':
        return data
    if t == 'eps':
        return '%'
    if t == '.':
        return ''.join(('(%s)' if not atomic(sub) else '%s') % print_regex(sub) for sub in data) if data else '%'
    if t == '|':
        return '|'.join('%s' % print_regex(sub) for sub in data) if data else '{}'
    if t == '*':
        return ('(%s)*' if not atomic(data) else '%s') % print_regex(data)


def disambiguate(regex):
    nfa = compile(parse(regex)) if isinstance(regex, str) else compile(regex)
    dfa = determinize(nfa)
    R, dfa, accepts, n = reconstruct(*dfa)
    regex = reduce(('|', [R(1, k, n) for k in accepts]))
    return regex, (R, dfa, accepts, n)


if __name__ == '__main__':
    from itertools import islice
    # 0(0)*|(2|0(0)*2)(2)*|(1|0(0)*1)(1)*(2(2)*)|(1|0(0)*1)(1)*|%
    # 1(1)*|0(0)*(1(1)*)|(2|1(1)*2)(2)*|0(0)*((2|1(1)*2)(2)*)|0(0)*|%
    nfa = compile(parse("0*0*1*2*"))
    dfa = determinize(nfa)
    R, dfa, accepts, n = reconstruct(*dfa)
    regex = reduce(('|', [R(1, k, n) for k in accepts]))
    print(print_regex(regex))
    from regex_enumerate.enumerate import exact_coefficients, generating_function, algebraic_form
    print(list(islice(exact_coefficients(regex), 10)))
    print(generating_function(regex))
    print(algebraic_form(regex))