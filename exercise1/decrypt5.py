from string import ascii_lowercase

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
    # computes a relative score for the likelihood of message_candidate beeing
    # a text in the english language (that is, the correct decrypted message)
    score = 0
    with open('/usr/share/dict/words') as dictionary:
        for word in dictionary.readlines():
            if message_candidate.lower().find(word.lower().strip()) > -1:
                # if message_candidate contains the word once or more
                # print(word.strip())
                score += 1
    print(score)
    return score

def guess_key(keylen, depth, ciphertext):

    # first, we create a symbol map: a list of symbols for each part of the key
    # that symbol was encrypted with, sorted by frequency
    symbol_map = ['' for i in range(keylen)]
    for i in range(len(ciphertext)):
        symbol_map[i % keylen] += ciphertext[i]
    for i in range(len(symbol_map)):
        symbol_map[i] = sorted(ascii_lowercase, key=lambda symbol: symbol_map[i].find(symbol), reverse=True)

    frequent_letters = 'etaonrishdlfcmugypwbvkjxqz'

    print(symbol_map)
