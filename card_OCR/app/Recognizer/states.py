import os
path = os.path.dirname(os.path.abspath(__file__))

from difflib import SequenceMatcher

St=[]
with open(path + '/../Dataset/States.txt', 'r') as states:
    for line in states:
        state = line.strip().lower()
        St.append(state)

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

# def is_state(txt):
#     sub_tokens = [tok.lower() for tok in txt.split()]
#     best_guess, best_name = 0, ''
#     for sub_token in sub_tokens:
#         token_guess, token_match = check(sub_token, St)
#         if token_guess > best_guess:
#             best_guess, best_name = token_guess, token_match
#     if(best_guess>=0.8):
#         return [best_name]
#     else:
#         return ['']

def find_best_guessed_state(tokens):
    best_guess, best_name = 0, ''

    for token in tokens:
        token_guess, token_name = scan_line(token, St)
        # print(token_guess, token_name)
        if token_guess > best_guess:
            best_guess, best_name = token_guess, token_name

    if(best_guess >= 0.8):
        return [best_name]
    else:
        return['']