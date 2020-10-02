import re
from difflib import SequenceMatcher

# def is_website(txt):
#     isemail = False
#     subtokens = [tok.lower() for tok in txt.split()]
#     for subtoken in subtokens:
#         if(isemail):
#             return subtoken
#         a = SequenceMatcher(None, subtoken, 'web').ratio()
#         b = SequenceMatcher(None, subtoken, 'website').ratio()
#         c = SequenceMatcher(None, subtoken, 'www').ratio()
#         if(max(a,b,c)>0.9):
#             isemail = True

#     txt = txt.lower()
#     w = re.findall(r'(^(?:http\:\/\/|https\:\/\/)?(?:[a-z0-9][a-z0-9\-]*\.?)+[a-z0-9][a-z0-9\-]*$)',txt)
#     return w

def is_website(txt):
    txt = txt.lower()
    if(txt.find("\\\\") >= 0 or txt.find("www") >= 0 or txt.find('http') >= 0):
        return txt
    else:
        return ' '