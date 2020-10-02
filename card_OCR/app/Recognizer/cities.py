import os
path = os.path.dirname(os.path.abspath(__file__))

from difflib import SequenceMatcher

Ct=[]
with open(path + '/../Dataset/cities.txt', 'r') as cities:
    for line in cities:
        city = line.strip().lower()
        Ct.append(city)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def check(token, dict):
    best_guess, guess_name = 0, ''

    for name in dict:
        guess = similar(token, name)
        if guess > best_guess:
            best_guess, guess_name = guess, name
    return [best_guess, guess_name]

def scan_line(line, dict):
    sub_tokens = [tok.lower() for tok in line.split()]
    best_guess, best_name = 0, ''

    for sub_token in sub_tokens:
        token_guess, token_match = check(sub_token, dict)
        if token_guess > best_guess:
            best_guess, best_name = token_guess, token_match
    return [best_guess, best_name]


# def is_city(txt):
#     sub_tokens = [tok.lower() for tok in txt.split()]
#     # print("is state =>",sub_tokens)
#     best_guess, best_name = 0, ''
#     for sub_token in sub_tokens:
#         token_guess, token_match = check(sub_token, Ct)
#         if token_guess > best_guess:
#             best_guess, best_name = token_guess, token_match
    
#     if(best_guess>=0.8):
#         return [best_name]
#     else:
#         return ['']

def find_best_guessed_city(tokens):
    best_guess, best_name = 0, ''

    for token in tokens:
        token_guess, token_name = scan_line(token, Ct)
        # print(token_guess, token_name)
        if token_guess > best_guess:
            best_guess, best_name = token_guess, token_name

    if(best_guess >= 0.8):
        return [best_name]
    else:
        return['']