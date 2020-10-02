import os
path = os.path.dirname(os.path.abspath(__file__))

from difflib import SequenceMatcher

NM=[]
with open(path + '/../Dataset/common_names.txt', 'r') as states:
    for line in states:
        state = line.strip().lower()
        NM.append(state)

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def check(token, dict):
    best_guess, guess_name = 0, ''

    for name in dict:
        guess = similar(token, name)
        if guess > best_guess:
            best_guess, guess_name = guess, token
    return [best_guess, guess_name]

def scan_line(line, dict):
    sub_tokens = [tok.lower() for tok in line.split()]
    best_guess, best_name, adj_name = 0, '', ''

    for i,sub_token in enumerate(sub_tokens):
        token_guess, token_match = check(sub_token, dict)
        if token_guess > best_guess:
            best_guess, best_name = token_guess, token_match
            if(i<len(sub_tokens)-1):
                adj_name = sub_tokens[i+1]
    return [best_guess, best_name ,adj_name]

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

def find_best_guessed_name(tokens):
    best_guess, best_name, adj_name = 0, '', ''

    for token in tokens:
        token_guess, token_name, adj_token = scan_line(token, NM)
        # print(token_guess, token_name)
        if token_guess > best_guess:
            best_guess, best_name, adj_name = token_guess, token_name, adj_token

    if(best_guess >= 0.7):
        return [best_name,adj_name]
    else:
        return['']