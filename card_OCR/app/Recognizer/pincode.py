import re

def is_pincode(txt):
    p = re.findall(r'([1-9]{1}[0-9]{5}|[1-9]{1}[0-9]{3}\\s[0-9]{3})',txt)
    return p