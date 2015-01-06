#!/usr/bin/env python3.4

from collections import namedtuple
import simplejson as json

Letter = namedtuple('Letter', 'cyrillic ipa ordinal')

alphabet_cyr_file = 'alphabet_cyr.json'
alphabet_ascii_file = 'alphabet_ascii.json'
dataset_cyr = 'koryak_cyrillic.txt'
dataset_lat = 'koryak_latin.txt'

# load the alphabets

with open(alphabet_cyr_file) as alphcyr:
    alphabet_cyr = json.load(alphcyr)

with open(alphabet_ascii_file) as alphascii:
    alphabet_ascii = json.load(alphascii)


# load the dataset in cyrillic and latin

with open(dataset_cyr) as cyr_data:
    words_cyr = cyr_data.read().splitlines()
    
with open(dataset_lat) as lat_data:
    words_lat = lat_data.read().splitlines()

def tokenise(string, alphabet):
    '''this function tokenises a string based on an alphabet'''

    tokenised = []

    while string != '':
        copystring = string
        while copystring != '':
            if copystring in alphabet:
                tokenised.append(copystring)
                string = string[len(copystring):]
                break
            else:
                if len(copystring) == 1:
                    string = string[1:]
            copystring = copystring[:len(copystring) - 1]

    return tokenised

def sort_words(words, alphabet):
    '''this function converts each word into its ordinal representation
    (i.e.) "гыммо" -> [4, 32, 16, 16, 19], 
    assembles a list of those 
    sorts them with the standard sorted function
    then converts them back into alphabetic representations'''

    letter_orders = {l: n for n, l in enumerate(alphabet)}
    tokenised_words = [tokenise(w, alphabet) for w in words]
    words_as_orders = []

    for w in tokenised_words:
        word_as_orders = [letter_orders[c] for c in w]
        words_as_orders.append(word_as_orders)

    sorted_w_orders = sorted(words_as_orders)
    sorted_words = []
    for w in sorted_w_orders:
        # convert it back into tokens
        try:
            word = ''.join(map(lambda n: alphabet[n], w))
            sorted_words.append(word)
        except KeyError as e:
            print(e)

    return sorted_words

def create_sorted_dictionary(words, alphabet):
    sorted_words = sort_words(words, alphabet)
    sorted_words = '\n'.join(sorted_words)

    with open('sorted_words.txt', 'w') as sorted_words_file:
        sorted_words_file.write(sorted_words)

    return True, len(sorted_words)

    print('wrote {} entries'.format(len(sorted_words)))

if __name__ == '__main__':
    print('creating a sorted dictionary of unique words')
    num_entries = create_sorted_dictionary(set(words_cyr), alphabet_cyr)[1]
    print('wrote {} entries'.format(num_entries))
