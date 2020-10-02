import re

def is_email(txt):
    e = re.findall(r'((?:[a-zA-Z0-9_\-\.]+)@(?:[a-zA-Z0-9_\-\.]+)\.?(?:[a-zA-Z]{2,5}))',txt)
    return e 
