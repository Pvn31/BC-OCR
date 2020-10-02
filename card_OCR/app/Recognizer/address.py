import os
import re
path = os.path.dirname(os.path.abspath(__file__))

from difflib import SequenceMatcher

# Ct=[]
# with open(path + '/../address.txt', 'r') as cities:
#     for line in cities:
#         city = line.strip().lower()
#         Ct.append(city)

# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

# def check(token, dict):
#     best_guess, guess_name = 0, ''

#     for name in dict:
#         guess = similar(token, name)
#         if guess > best_guess:
#             best_guess, guess_name = guess, name
#     return [best_guess, guess_name]

# def scan_line(line, dict):
#     sub_tokens = [tok.lower() for tok in line.split()]
#     best_guess, best_name = 0, ''

#     for sub_token in sub_tokens:
#         token_guess, token_match = check(sub_token, dict)
#         if token_guess > best_guess:
#             best_guess, best_name = token_guess, token_match
#     return [best_guess, best_name]


def is_address(tokens):

    address = []

    for token in tokens:
        commas = re.findall(r'\,',token)
        if(len(commas)>=2):
            address.append(token)
    return address