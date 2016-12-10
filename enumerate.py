from collections import defaultdict

import mpmath
from numpy import array
from numpy.linalg import solve
from numpy.polynomial import Polynomial as P
from scipy.special import comb
from sympy import nsimplify, latex, sympify, binomial

from transfer import transfer, rationalize, simplify, process, down_p, mul, lt


def exact(regex, n, what = None, use_overflow = True):
    ast = transfer(regex, what)
    overflow, (top, bottom) = simplify(*rationalize(ast))
    if not use_overflow: overflow = {}
    top = process(top)
    if not top:
        return overflow[n] if n in overflow else 0
    # p(z)/(1 - q(z)) -> p(z) + pq + pq^2 + pq^3 + ...
    assert bottom[0]
    _, p = down_p(('*', [('v', top), ('v', {0 : 1/bottom[0]})]))
    _, q = down_p(('*', [('v', bottom), ('v', {0 : -1/bottom[0]})]))
    q.pop(0)

    cur = p
    coeff = overflow[n] if n in overflow else 0
    for i in range(n + 1):
        coeff += cur[n] if n in cur else 0
        _, cur = mul(('v', cur), ('v', q))

    return list(map(int, coeff))


def newton(p, roots):
    deriv = p.deriv()
    r = roots
    r = r - p(r) / deriv(r)
    r = r - p(r) / deriv(r)
    return r


def heuristics(p, roots, symbolic=False):
    # simple heuristic: if something is close to a whole number
    x = []
    for root in roots:
        rl = mpmath.identify(root.real, tol=1e-4, maxcoeff=30)
        im = mpmath.identify(root.imag, tol=1e-4, maxcoeff=30)
        if not rl:
            rl = root.real if not symbolic else sympify(rl).evalf(5)
        if not im:
            im = root.imag if not symbolic else sympify(im).evalf(5)
        new = float(sympify(rl)) + float(sympify(im))*1j
        if abs(p(root)) > abs(p(new)) or abs(p(new)) < 1e-10:
            if symbolic:
                x.append(sympify(rl) + sympify(im) * 1j)
            else:
                x.append(new)
        else:
            if symbolic:
                x.append(sympify(root))
            else:
                x.append(root)
    return array(x)


def bucket(p, roots, threshold = 1e-3):
    buckets = defaultdict(int)
    for root in roots:
        keys = buckets.keys()
        added = False
        for key in keys:
            if abs(key - root) <= threshold:
                # use the better approximation
                left = p(key)
                right = p(root)
                if (abs(right) < abs(left)):
                    buckets[root] = buckets[key] + 1
                    buckets.pop(key)
                else:
                    buckets[key] += 1
                added = True
                break
        if not added:
            buckets[root] += 1
    return buckets


def collate(buckets):
    collection = []
    for (key, value) in buckets.items():
        for i in range(1, value + 1):
            collection.append((key, i))
    return sorted(collection)


def extract(regex, what = None, threshold = 1e-3):
    ast = transfer(regex, what)
    overflow, (top, bottom) = simplify(*rationalize(ast))
    pow, _ = lt(bottom)
    p = P([bottom[i] if i in bottom else 0 for i in range(pow + 1)][::])
    roots = p.roots()
    roots = newton(p, roots)
    roots = heuristics(p, roots)
    buckets = bucket(p, roots, threshold=threshold)
    # roots of mulitplicity k has expanded form binom[n+k-1,k-1] * (-a)**(n - k)
    degree = len(roots)
    basis = lambda n: array([comb(n + k - 1, k - 1) * (-1)**k * (root)**(-n - k) for (root, k) in collate(buckets)])
    mat = array([basis(n) for n in range(degree)])
    target = array([exact(regex, n, what=what, use_overflow=False) for n in range(degree)])
    coeffs = solve(mat, target)

    return (lambda n: abs(basis(n).dot(coeffs)) + (overflow[n] if n in overflow else 0)), (dict(buckets), coeffs, p, overflow)

if __name__ == '__main__':
    regex = "(00*1)*"
    # regex = "(%|1|11)(00*(1|11))*0* | 1"
    # regex = "(000)*(000)*(00)*(00)*(00)*"
    # regex = "1*(22)*(333)*(4444)*(55555)*" # 1 5 10 25
    # regex = "11*" * 5 # 5 compositions of n
    regex = "(11*)*" # all compositions of n
    regex = "(1|22|333)*"
    print([exact(regex, i) for i in range(10)])
    gf, (buckets, coeffs, p, overflow) = extract(regex, threshold=2e-3)
    print([round(gf(n)) for n in range(15)])

    def inverse_symbolic(n, threshold = 1e-5):
        rl = mpmath.identify(n.real, tol=1e-3, maxcoeff=30)
        im = mpmath.identify(n.imag, tol=1e-3, maxcoeff=30)
        if not rl or abs(n.real - float(nsimplify(rl))) > threshold:
            rl = nsimplify(n.real).evalf(5)
        if not im or abs(n.imag - float(nsimplify(im))) > threshold:
            im = nsimplify(n.imag).evalf(5)
        return (sympify(rl) + sympify(im) * 1j)

    def print_series(buckets, coeffs, overflow):
        n = sympify('n')
        s = 0
        for i, (root, power) in enumerate(collate(buckets)):
            symroot = inverse_symbolic(root)
            coeff = inverse_symbolic(coeffs[i])
            s += (coeff * binomial(n + power - 1, power - 1) * (-1)**power * symroot ** (-n - power))
        lt = latex(s)
        for k, c in overflow.items():
            lt += (r" + %s\delta_{n=%s}"%(c, k))
        print(lt)

    print_series(buckets, coeffs, overflow=overflow)