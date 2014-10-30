from string import ascii_lowercase
from itertools import product
from functools import reduce

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

        # decrypt the cipher symbol
        out += ascii_lowercase[(symbol_index + key_symbol_index + 1) % len(ascii_lowercase)]

    # print(out)
    return out

def plausibility_check(message_candidate):
    # computes a relative score for the likelihood of message_candidate being
    # a text in the english language (that is, the correct decrypted message)
    score = 0
    with open('/usr/share/dict/words') as dictionary:
        for word in dictionary.readlines():
            if message_candidate.lower().find(word.lower().strip()) > -1:
                # if message_candidate contains the word once or more
                # print(word.strip())
                score += 1
    # print(score)
    return score

def guess_key(keylen, depth, ciphertext):

    # first, we create a symbol map: a list of symbols for each part of the key
    # that symbol was encrypted with, and from that a frequency map: the
    # ascii letters sorted by frequency in their respective lists
    symbol_map = ['' for i in range(keylen)]
    frequency_map = ['' for i in range(keylen)]
    for i in range(len(ciphertext)):
        symbol_map[i % keylen] += ciphertext[i]
    for i in range(len(symbol_map)):
        frequency_map[i] = sorted(ascii_lowercase, key=lambda symbol: symbol_map[i].find(symbol), reverse=True)

    # lowercase ascii letters, sorted by relative frequency in the english
    # language. See https://en.wikipedia.org/wiki/Letter_frequency
    frequent_letters = 'etaonrishdlfcmugypwbvkjxqz'

    # generate the list of permutations used to iterate over the key candidates
    # there has to be a better way to do this - if you know it, please tell me
    # the indexlist is generated as follows:
    # 1) we take the nth cartesian product of range(depth), where n = keylen
    #    that means for our key candidates we take the [depth] most frequent
    #    letters from each list
    # 2) we sort the resulting list of tuples be the tuple's digit sum
    # when we use the resulting list to generate our list of key candidates,
    # they will be ordered by likelihood of them being the correct key
    # actually, this is probably not needed. what the fuck.
    indexlist = list(product(range(depth), repeat=keylen))
    # indexlist.sort(key = lambda x: reduce(lambda y,z: y+z, x))
    # commented out because probably useless

    

    print(symbol_map)
    print(frequency_map)


# max_score = 0
# message = ""
# for key_candidate in product('etao', repeat=5):
#     key_candidate = ''.join(key_candidate)
#     print(key_candidate)
#     message_candidate = decrypt(key_candidate, crypt)
#     print(message_candidate)
#     score = plausibility_check(message_candidate)
#     if score > max_score:
#         message = message_candidate
#         max_score = score
#
# print(message)
