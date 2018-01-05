
def include_non_asc(string):
    for s in string:
        if ord(s)>127:
            return True
    return False