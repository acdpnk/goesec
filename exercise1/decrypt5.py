from string import ascii_lowercase
from itertools import product
from functools import reduce
from math import sqrt

crypt_path = "crypt5.txt"
crypt = ""

with open(crypt_path) as cryptfile:
    crypt = cryptfile.read()

def decrypt(key, ciphertext):
    # decrypt ciphertext using key, by way of a Vigenre cipher

    key = key.lower()
    ciphertext = ciphertext.lower().replace('\n','').replace(' ','')
    out = ''

    # print(ciphertext)
    for i in range(len(ciphertext)):
        # for each symbol in the ciphertext


        # get the symbol's index in the alphabet
        symbol_index = ascii_lowercase.index(ciphertext[i])

        # get the key_symbol
        key_symbol = key[i % len(key)]

        # get the key_symbol's index in the alphabet
        key_symbol_index = ascii_lowercase.index(key_symbol)

        # decrypt the cipher symbol and append to out
        out += ascii_lowercase[(symbol_index - key_symbol_index + len(ascii_lowercase)) % len(ascii_lowercase)]

    # print(out)
    return out

def rotate(text):
    return text[1:] + text[0]

def guess_key(keylen, ciphertext):
    key = ''
    for i in range(keylen):
        best = ''
        best_error = -1
        for char in ascii_lowercase:
                error = calculate_key_error(frequency_fingerprint(keylen, decrypt(char, ciphertext))[i])
                if best_error == -1 or error < best_error:
                    best_error = error
                    best = char
        print("%s %s" % (best, best_error))
        key += best
    return key



def frequency_fingerprint(keylen, text):
    symbol_map = ['' for i in range(keylen)]
    frequency_map = [{} for i in range(keylen)]
    for i in range(len(text)):
        symbol_map[i % keylen] += text[i]
    for i in range(len(symbol_map)):
        for char in ascii_lowercase:
            freq = max(0, symbol_map[i].count(char))
            frequency_map[i][char] = freq

        frequency_map[i] = scale_dict(frequency_map[i], 12.702)
    # print(frequency_map)
    return frequency_map


def calculate_key_error(decrypted_dict):
    # lowercase ascii letters, sorted by relative frequency in the english
    # language. See https://en.wikipedia.org/wiki/Letter_frequency
    # frequent_letters = 'etaonrishdlfcmugypwbvkjxqz'
    frequent_letters = {
        'a': 8.167,
        'b': 1.492,
        'c': 2.782,
        'd': 4.253,
        'e': 12.702,
        'f': 2.228,
        'g': 2.015,
        'h': 6.094,
        'i': 6.966,
        'j': 0.153,
        'k': 0.772,
        'l': 4.025,
        'm': 2.406,
        'n': 6.749,
        'o': 7.507,
        'p': 1.929,
        'q': 0.095,
        'r': 5.987,
        's': 6.327,
        't': 9.056,
        'u': 2.758,
        'v': 0.978,
        'w': 2.360,
        'x': 0.150,
        'y': 1.974,
        'z': 0.074
    }
    error = 0
    for letter in decrypted_dict:
        error += pow(frequent_letters[letter] - decrypted_dict.get(letter, 0), 2)
    return error


def scale_dict(dictionary, scale_to):
    vals = list(iter(dictionary.values()))
    vals = sorted(vals, reverse=True)
    max_value = vals[0]
    # print(vals)
    for (key, value) in dictionary.items():
        dictionary[key] = value * (scale_to / max_value)
    # print(dictionary)
    return dictionary

def get_key_symbol(cipher_symbol, plaintext_symbol):
    return ascii_lowercase[(ascii_lowercase.index(cipher_symbol) - ascii_lowercase.index(plaintext_symbol))  + len(ascii_lowercase) % len(ascii_lowercase)]


message = ""

key_candidate = guess_key(5, crypt)

print(key_candidate)
print(decrypt(key_candidate, crypt))
