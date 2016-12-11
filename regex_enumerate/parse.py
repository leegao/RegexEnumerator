from re import compile

x = compile(r'[^?+*()|]')

def parse_regex(re, stack):
    '''
    Rather than using a LL1 derivation, we will instead depend on traditional Shunting-Yards
    using three stacks to build the tree.
    stack = [alternates]
    alternates = ('|', concats)
    concats = ('.', atom)
    atom = ('tok', character) or ('eps', '%') or ('*', expr) or alternates
    A proof of correctness can be derived through structural induction on this data-scheme.
    '''
    if not re:
        assert len(stack) == 1
        return stack[-1]
    _, alternates = stack[-1] # stack of alternates
    assert _ == '|'
    if x.match(re):
        curr, re = re[0], re[1:]
        _, current_concat = alternates[-1]
        assert _ == '.'
        current_concat.append(('tok' if curr != '%' else 'eps', curr))
        return parse_regex(re, stack)
    elif re[0] == '(':
        # push onto stack
        stack.append(('|', [('.', [])]))
        return parse_regex(re[1:], stack)
    elif re[0] == ')':
        # pop from stack
        group = stack.pop(-1)
        _, alternates = stack[-1]
        assert _ == '|'
        _, current_concat = alternates[-1]
        assert _ == '.'
        current_concat.append(group)
        return parse_regex(re[1:], stack)
    elif re[0] == '|':
        alternates.append(('.', []))
        return parse_regex(re[1:], stack)
    elif re[0] == '*':
        _, current_concat = alternates[-1]
        assert _ == '.'
        current_concat[-1] = ('*', current_concat[-1])
        return parse_regex(re[1:], stack)
    elif re[0] == '+':
        # e+ -> ('.', e, e*)
        _, current_concat = alternates[-1]
        assert _ == '.'
        current_concat[-1] = ('.', [current_concat[-1], ('*', current_concat[-1])])
        return parse_regex(re[1:], stack)
    elif re[0] == '?':
        # e? -> (e | %)
        _, current_concat = alternates[-1]
        assert _ == '.'
        current_concat[-1] = ('|', [current_concat[-1], ('eps', '%')])
        return parse_regex(re[1:], stack)
    else:
        raise NotImplementedError()

def parse(re):
    return parse_regex(re.replace(' ', ''), [('|', [('.', [])])])