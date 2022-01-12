#!/usr/bin/env python3

import numpy as np
import random

word_file = "/usr/share/dict/words"
num_chars = 5

include_pattern = "_a_or"
anti_patterns = [ "rv", "", "", "", "" ]
include_letters = "aorv"
exclude_letters = "beisplmn"
rr = 100                        # score randomization range

words = {}
words_no_repeat = []

# load words
with open(word_file) as f:
    for line in f:
        word = line.rstrip().lower()
        if len(word) != num_chars:
            continue
        if not word.isalpha():
            continue
        words[word] = True

# build letter histogram and list of words with no repeating letters
hist = [0] * 26
for word in words:
    used = [False] * 26 
    repeat = False
    for c in word:
        index = ord(c) - ord('a')
        hist[index] += 1
        if used[index]:
            repeat = True
        else:
            used[index] = True
    if not repeat:
        words_no_repeat.append(word)

#for i in range(len(hist)):
#    print(i, chr(i+ord('a')), hist[i])

# filter word list according to provided constraints
words_filtered = []
unique_combos = {}
for word in words_no_repeat:
    for c in word:
        include_test = True
        for ic in include_letters:
            if ic not in word:
                include_test = False
                break
        exclude_test = True
        for ec in exclude_letters:
            if ec in word:
                exclude_test = False
                break
        pattern_test = True
        for i, pc in enumerate(include_pattern):
            if pc.isalpha() and word[i] != pc:
                pattern_test = False
        anti_pattern_test = True
        for i, ap in enumerate(anti_patterns):
            if word[i] in ap:
                anti_pattern_test = False
    if include_test and exclude_test and pattern_test and anti_pattern_test:
        unique = ''.join(sorted(word))
        if unique not in unique_combos:
            unique_combos[unique] = [ word ]
        else:
            unique_combos[unique].append(word)
        words_filtered.append(word)
            
# score non repeating words
random.seed()
scores_filtered = []
for word in unique_combos:
    #score = random.randrange(rr)
    score = 0
    for c in word:
        index = ord(c) - ord('a')
        score += hist[index]
    scores_filtered.append(score)

idx = np.argsort(-np.array(scores_filtered))
for i in idx:
    print( scores_filtered[i], unique_combos[list(unique_combos)[i]] )
