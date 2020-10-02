import re

def is_contact(txt):
    m = re.findall(r'((?:(?:\+*)(?:(?:0[ -]+)*|(?:91[ -])*))(?:\d{12}|\d{10}|\d{3}[\ -]\d{3}[\ -]\d{4}|\d{5}[\ -]\d{5}))|\d{5}(?:[- ]*)\d{6}',txt)
    return m
