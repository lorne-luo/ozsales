import string

digs = string.digits + string.ascii_letters


def include_non_asc(string):
    for s in string:
        if ord(s) > 127:
            return True
    return False


def int2base(x, base=36):
    if base > 62:
        raise Exception(f'base should less than 63, {base} given.')

    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)
