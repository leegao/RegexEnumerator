from collections import defaultdict

import mpmath
from numpy import array
from numpy.linalg import solve
from numpy.polynomial import Polynomial as P
from scipy.special import comb
from sympy import nsimplify, latex, sympify, binomial

from transfer import transfer, rationalize, simplify, process, down_p, mul, lt


def exact(regex, n, what = None, use_overflow = True):
    '''
    Compute an exact enumeration for the number of words of length n in the language
    given by the regular expression. You can provide an optional set of letters
    within your alphabet that contribute to the count.
    :return: Number of words of size n in regex.
    '''
    ast = transfer(regex, what)
    # p(z)/q(z) = overflow(x) + top(z)/bottom(z) where each is a polynomial and the quotient is irreducible.
    overflow, (top, bottom) = simplify(*rationalize(ast))

    # Generally, the overflow is some low-order polynomial that gives no contribution asymptotically.
    # Tick this if you are computing the boundary values for the algebraic enumeration.
    if not use_overflow: overflow = {}
    # Normalize the numerator if it is zero.
    top = process(top)
    if not top:
        return overflow[n] if n in overflow else 0

    # Dynamic program for coefficient extraction.
    # In essence, we draw inspiration from Matrix Computations' use of Krylov Methods.
    #     p(z)/(1 - q(z)) -> p(z) + pq + pq^2 + pq^3 + ...
    # which lets us invert a polynomial using only polynomial multiplications.
    assert bottom[0]
    # Normalize into the p(z)/(1 - q(z)) form
    _, p = down_p(('*', [('v', top), ('v', {0 : 1/bottom[0]})]))     # p = top(z)/bottom(0)
    _, q = down_p(('*', [('v', bottom), ('v', {0 : -1/bottom[0]})])) # q = -bottom(z)/bottom(0)
    q.pop(0) # get rid of the +/-1 in q(z), effectively q(z) - 1.

    qn = p # tracks p(z) * q(z)**n
    coefficients = overflow[n] if n in overflow else 0 # overflow contributes at a finite scale
    for i in range(n + 1):
        coefficients += qn[n] if n in qn else 0
        # update p*q**n to p*q**(n + 1)
        _, qn = mul(('v', qn), ('v', q))

    return int(coefficients)


def exact_coefficients(regex, what = None, use_overflow = True):
    '''
    from itertools import islice
    print("The first 10 coefficients of (0|1)* are")
    for coefficient in islice(exact_coefficients("(0|1)*"), 10):
      print(coefficient)
    '''
    n = 0
    while True:
        yield exact(regex, what, use_overflow) # TODO: inline this in the future so we don't recompute the quotients
        n += 1


def newton(polynomial, roots):
    '''
    Let's refine the computation of the roots a little more.
    In general, numpy does a good job trading off between truncation
    and roundoff errors. However, we can usually get a bit closer to
    where we want by explicitly refining the polynomial.

    Note: don't add too many iterations. Roundoff will kick in and we'll
    end up refining noise.
    '''
    derivatives = polynomial.deriv()
    r = roots
    # Heuristic: do two iterations
    r = r - polynomial(r) / derivatives(r)
    r = r - polynomial(r) / derivatives(r)
    return r


def closed_form(polynomial, roots, symbolic=False):
    '''
    A simple heuristic to check if an approximate root is close to some algebraically
    expressible number.
    :param symbolic: Return an exact symbolic representation (via sympy), for LaTeX
    '''
    x = []
    for root in roots:
        rl = mpmath.identify(root.real, tol=1e-4, maxcoeff=30)
        im = mpmath.identify(root.imag, tol=1e-4, maxcoeff=30)
        if not rl:
            rl = root.real if not symbolic else sympify(rl).evalf(5)
        if not im:
            im = root.imag if not symbolic else sympify(im).evalf(5)
        new = float(sympify(rl)) + float(sympify(im))*1j
        # Arbitrary roundoff
        if abs(polynomial(root)) > abs(polynomial(new)) or abs(polynomial(new)) < 1e-10:
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


def cluster_roots(polynomial, roots, threshold = 1e-3):
    '''
    Clusters roots that are close together. Since algebraic
    enumeration requires an exact knowledge of the multiplicity
    of each root, round-off error may force our enumeration to
    use the wrong models, which will not generalize outside of the
    boundary-value problem that we're solving.
    '''
    clusters = defaultdict(int)
    for root in roots:
        existing_roots = clusters.keys()
        added = False
        for existing_root in existing_roots:
            if abs(existing_root - root) <= threshold:
                # use the better approximation
                left = polynomial(existing_root)
                right = polynomial(root)
                if (abs(right) < abs(left)):
                    clusters[root] = clusters[existing_root] + 1
                    clusters.pop(existing_root)
                else:
                    clusters[existing_root] += 1
                added = True
                break
        if not added:
            clusters[root] += 1
    return clusters


def collate(clusters):
    collection = []
    for (root, multiplicity) in clusters.items():
        for k in range(1, multiplicity + 1):
            collection.append((root, k))
    return sorted(collection)


def extract_coefficients_algebraically(regex, what = None, threshold = 1e-3):
    ast = transfer(regex, what)
    # rationalize(regex) = overflow(z) + top(z)/bottom(z), where the quotient is irreducible.
    overflow, (top, bottom) = simplify(*rationalize(ast))
    pow, _ = lt(bottom)
    p = P([bottom[i] if i in bottom else 0 for i in range(pow + 1)][::])
    roots = p.roots()
    roots = newton(p, roots)
    roots = closed_form(p, roots)
    buckets = cluster_roots(p, roots, threshold=threshold)
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
    gf, (buckets, coeffs, p, overflow) = extract_coefficients_algebraically(regex, threshold=2e-3)
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