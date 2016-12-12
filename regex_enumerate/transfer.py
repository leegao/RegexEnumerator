from collections import defaultdict

from regex_enumerate.parse import parse


def transfer(regex, what = None):
    '''
    Transfers a regular expression into a rational complex function (repr)
    | -> +
    . -> *
    * -> 1/(1 - .)
    % -> 1
    tok -> var
    :param regex
    :return: rational function
    '''
    ast = parse(regex) if isinstance(regex, str) else regex

    def helper(ast):
        t, data = ast
        if t == '|':
            if len(data) == 0:
                return ('num', 0)
            if len(data) == 1:
                return helper(data[0])
            if len(data) == 2:
                return ('+', [helper(data[0]), helper(data[1])])
            return ('+', [helper(data[0]), helper((t, data[1:]))])
        if t == '.':
            if len(data) == 0:
                return ('num', 1)
            if len(data) == 1:
                return helper(data[0])
            if len(data) == 2:
                return ('*', [helper(data[0]), helper(data[1])])
            return ('*', [helper(data[0]), helper((t, data[1:]))])
        if t == 'tok':
            return ('var', 'z') if not what or data in what else ('num', 1)
        if t == 'eps':
            return ('num', 1)
        if t == '*':
            z = helper(data)
            return ('/', (('num', 1), ('+', [('num', 1), ('-', z)])))
        else:
            raise Exception("IllegalState")

    return helper(ast)


def debug_print(ast):
    t, data = ast
    if t == '+':
        return ' + '.join('(%s)' % debug_print(p) for p in data)
    if t == '*':
        return ' * '.join('(%s)' % debug_print(p) for p in data)
    if t == '/':
        return ' / '.join('(%s)' % debug_print(p) for p in data)
    if t == '-':
        return '-(%s)' % debug_print(data)
    if t == 'num':
        return str(data)
    if t == 'var':
        return data
    raise Exception("IllegalState")


def rationalize(ast):
    '''
    Rationalizes a rational function into a pair of numerators and denominators.
    Does not perform GCD to get the least forms.
    :param ast
    :return: A pair of polynomials that forms the rational function.
    '''
    def down_r(ast):
        t, data = ast
        if t == 'var':
            return ('v', {1 : 1}), ('v', {0 : 1})
        if t == 'num':
            return ('v', {0 : data}), ('v', {0 : 1})
        if t == '-':
            n, d = down_r(data)
            n_ = down_p(('-', n))
            return n_, d
        if t == '+':
            assert len(data) == 2
            n1, d1 = down_r(data[0])
            n2, d2 = down_r(data[1])
            n3 = down_p(('+', [('*', [n1, d2]), ('*', [n2, d1])]))
            d3 = down_p(('*', [d1, d2]))
            return n3, d3
        if t == '*':
            assert len(data) == 2
            n1, d1 = down_r(data[0])
            n2, d2 = down_r(data[1])
            n3 = down_p(('*', [n1, n2]))
            d3 = down_p(('*', [d1, d2]))
            return n3, d3
        if t == '/':
            assert len(data) == 2
            n1, d1 = down_r(data[0])
            n2, d2 = down_r(data[1])
            n3 = down_p(('*', [n1, d2]))
            d3 = down_p(('*', [d1, n2]))
            return n3, d3
        raise Exception("IllegalState")

    (_, p), (_, q) = down_r(ast)
    return process(p), process(q)


def down_p(ast):
    t, data = ast
    if t == 'v':
        return ast
    if t == '+':
        v1 = down_p(data[0])
        v2 = down_p(data[1])
        v3 = add(v1, v2)
        return v3
    if t == '*':
        v1 = down_p(data[0])
        v2 = down_p(data[1])
        v3 = mul(v1, v2)
        return v3
    if t == '-':
        return neg(data)
    raise Exception("IllegalState")


def add(v1, v2):
    t1, d1 = v1
    t2, d2 = v2
    assert t1 == t2 == 'v'
    d3 = defaultdict(int)
    for p, n in d1.items():
        d3[p] += n
    for p, n in d2.items():
        d3[p] += n
    return 'v', process(dict(d3))


def neg(v):
    t, d = v
    assert t == 'v'
    d2 = {}
    for p, n in d.items():
        d2[p] = -n
    return 'v', process(d2)


def mul(v1, v2):
    t1, d1 = v1
    t2, d2 = v2
    assert t1 == t2 == 'v'
    d3 = defaultdict(int)
    for p1, n1 in d1.items():
        for p2, n2 in d2.items():
            d3[p1 + p2] += n1 * n2
    return 'v', process(dict(d3))


def process(p):
    q = {}
    for key, val in p.items():
        if val and abs(val) > 1e-10:
            q[key] = val
    return q


def leading_term(p):
    keys = list(process(p).keys())
    if not keys: return 0, 0
    key = max(keys)
    return (key, p[key])


def division(p, q):
    '''
    Computes the quotient and remainder of p/q
    :return: quotient, remainder
    '''
    ltp = leading_term(p)
    ltq = leading_term(q)
    if not ltp[0] and not ltp[1]: return {}, ({}, {0 : 1})
    if ltp[0] < ltq[0]:
        return {}, (p, q)
    lead = ltp[0] - ltq[0], ltp[1] / ltq[1]
    _, fl = mul(('v', q), ('v', {lead[0] : lead[1]}))
    _, rest = down_p(('+', [('v', p), ('-', ('v', fl))]))
    quotient_, remainder = division(rest, q)
    _, quotient = add(('v', {lead[0] : lead[1]}), ('v', quotient_))
    return quotient, remainder


def gcd(p, q):
    p = process(p)
    q = process(q)
    if not q: return p
    quotient, (remainder, _) = division(p, q)
    return gcd(q, remainder)


def simplify(p, q):
    quotient, (remainder, _) = division(p, q)
    g = gcd(remainder, q)

    simplr = division(remainder, g)
    simplq = division(q, g)
    assert not simplr[1][0]
    assert not simplq[1][0]

    return quotient, (simplr[0], simplq[0])


def print_poly(p):
    p = process(p)
    if not p: return '0'
    keys = sorted(p.keys())
    pk = lambda k: ('z**%s' % k) if k > 1 else 'z' if k else ''
    kk = lambda k: str(p[k]) if p[k] != 1 or not k else ''
    return ' + '.join([kk(key) + pk(key) for key in keys])


def print_rat(*args):
    if len(args) == 1:
        p, q = args[0]
    else:
        p, q = args
    p = print_poly(p)
    q = print_poly(q)
    size = max(len(p), len(q))
    return p + '\n' + ('-' * size) + '\n' + q


def print_simpl(*args):
    if len(args) == 1:
        args = args[0]
    l, (p, q) = args
    left = print_poly(l)
    lsize = len(left) + len(' + ')
    p = print_poly(p)
    q = print_poly(q)
    size = max(len(p), len(q))
    return (' ' * lsize) + p + '\n' + left + ' + ' +  ('-' * size) + '\n' + (' ' * lsize) + q
