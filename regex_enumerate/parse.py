from parsy import generate, string, regex, success

x = regex(r'[^%*()|]')


@generate
def e2():
    c = yield (string('%').map(lambda c: ('eps', c)) | x.map(lambda c: ('tok', c)) | (string('(') >> e << string(')')))
    star = yield string('*').at_most(1)
    raise StopIteration(c if not star else ('*', c))


@generate
def e1():
    concats = yield e2.at_least(1)
    raise StopIteration(('.', concats))


@generate
def e():
    left = yield e1
    right = yield (string('|') >> e1).many()
    raise StopIteration(('|', [left] + right))


def parse(re):
    return e.parse(re.replace(' ', ''))
