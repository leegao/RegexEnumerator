# Regex Enumerator

Enumerate Regular Expressions the Fun Way.

$$
[z^n] \frac{p(z)}{q(z)} = \Theta({n + k - 1 \choose k - 1}\rho^{-n}) ~~~ \text{where $\rho$ is the smallest root of $q(z)$, and $k$ its multiplicity.}
$$

<sub>*Or how I learned to stop worrying and start counting things with calculus*</sub>

-----

Have you ever wondered about how many different strings you can form that fits your favorite regex?

Yeah, chances are you probably haven't. But it's on your mind now.

Here's one of my favorite regexes:

    (0+, )*0+
    
It specifies the class of languages that are comma-separated list of strings of zeros. For example,
`000, 0, 00000` belongs to this language, but `0,,0` and `0,0,` does not.

Now, it might seem like a masochistic endeavor, but if you enumerate every possible word in this language, you'll
find that there are no empty strings, 1 single letter string, 1 two letter string, 2 three letter strings, 3 four letter
strings, and so on. This pattern actually looks like

    0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, ...

"Why, that is the fibonacci sequence! How did it end up in such a mundane place?"

Now, I could give you a combinatorial interpretation for this amazeballs result, but I still get shivers up my spine
whenever I think back to my undergrad Combinatorics course. Instead, I'll give a more general way to compute these
enumerations.

However, that's not the end of it. It turns out that this algorithm can also compute a closed-form expression
for this sequence.
$$
\left(- \frac{1}{2} + \frac{\sqrt{5}}{2}\right)^{- n - 1} \left(- \frac{\sqrt{5}}{10} + \frac{1}{2}\right) + \left(- \frac{\sqrt{5}}{2} - \frac{1}{2}\right)^{- n - 1} \left(\frac{\sqrt{5}}{10} + \frac{1}{2}\right)
$$

Now, this might not look very pretty, but it's still pretty cool that there is a (computable) closed form expression that
counts every regular expression.

-----------------------------------

### Installation

This library is just meant to be a demonstration. For now, you can install it by adding the `regex_enumerate` directory
to your `PYTHONPATH`. Note that you will first need to install `numpy`, `scipy`, and `sympy` in order to support solving a few
linear equations and to translate numerically computed roots into algebraic forms, if they are available.

### Usage

`regex_enumerate` offers a few library functions for you to use.

* `enumerate_coefficients`: Runs the magical algorithm to give you an algorithm that can compute
  the count of words of size `n` in time that is only proportional (linearly) to the number of terms in your
  regular expression.
  
      from regex_enumerate import enumerate_coefficients
      from itertools import islice
      
      print(list(islice(enumerate_coefficients('(00+,)00+'), 10)))
      # [0.0, 1.0, 0.99999999999999989, 1.9999999999999998, 2.9999999999999996, 4.9999999999999982, 7.9999999999999982, 12.999999999999998, 20.999999999999993, 33.999999999999986].

      