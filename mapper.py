#!/usr/bin/env python3.4

'''this implementation is broken and cannot be finished with the current data'''

import simplejson as json

alphabet_cyr_file = 'alphabet_cyr.json'
alphabet_other_file = 'alphabet_other.json'

special_cases = {
    "г'": 'ʕ',
    'д': 'd͡z',
    'ы': 'ə',
    'ӈ': 'ŋ',
    'ч': 't͡ʃ',
    'ж': 'ʒ',
    'ш': 'ʃ',
    'щ': 'ɕ',
    'ц': 't͡s',
}


def find_correspondences(words_cyr,  words_lat):
    correspondences = []
    # make the correspondences
    for n, (cyr, lat) in enumerate(zip(words_cyr, words_lat)):
        cyr_tokens = tokenise(cyr, alphabet_cyr)
        lat_tokens = tokenise(lat, alphabet_ascii)
        try:
            assert(len(cyr_tokens) == len(lat_tokens))
        except AssertionError:
            print(cyr_tokens, lat_tokens, n)
            raise AssertionError

        for c, l in zip(cyr_tokens, lat_tokens):
            correspondences.append((c, l))


    # remove outliers
    correspondences = list(set(correspondences))
    return correspondences


with open(alphabet_cyr_file) as cf:
    alphabet_cyr = json.load(cf)

with open(alphabet_other_file) as of:
    alphabet_other = json.load(of)

sorted_lat = sorted(alphabet_other, key=lambda x: alphabet_other[x])
with open(alphabet_other_file, 'w') as other_file:
    json.dump(sorted_lat, other_file, indent=4)

alphabet = []
for cyr, lat in zip(alphabet_cyr, sorted_lat):
    entry = {'cyr': cyr}
    if cyr in special_cases:
        entry['ipa'] = special_cases[cyr]
    else:
        entry['ipa'] = lat
    alphabet.append(entry)

with open('alphabet.json', 'w') as af:
    json.dump(alphabet, af, indent=4, ensure_ascii=False)