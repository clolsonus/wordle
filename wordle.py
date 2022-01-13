#!/usr/bin/env python3

import argparse
import numpy as np

word_file = "/usr/share/dict/words"

ap = argparse.ArgumentParser(description="Help generate wordle guesses.")
ap.add_argument('--max-repeats', type=int, default=2, help='maximum times a letter is allowed to repeat.')
ap.add_argument('--include', type=str, default="", help='list of letters to be included.')
ap.add_argument('--exclude', type=str, default="", help='list of letters to be excluded.')
ap.add_argument('--pattern', type=str, default="_____", help='pattern of known characters in their proper position, use underscore for unknown positions.')
args = ap.parse_args()

num_chars = 5
anti_patterns = [ "", "", "", "", "" ]

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

# build letter histogram, and also a list of words with no repeating letters
hist = [0] * 26
for word in words:
    used = [0] * 26 
    repeat = False
    for c in word:
        index = ord(c) - ord('a')
        hist[index] += 1
        used[index] += 1
        if np.max(used) > args.max_repeats:
            repeat = True
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
        for ic in args.include:
            if ic not in word:
                include_test = False
                break
        exclude_test = True
        for ec in args.exclude:
            if ec in word:
                exclude_test = False
                break
        pattern_test = True
        for i, pc in enumerate(args.pattern):
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
            
# score words with no repeating letters
scores_filtered = []
for word in unique_combos:
    score = 0
    for c in word:
        index = ord(c) - ord('a')
        score += hist[index]
    scores_filtered.append(score)
idx = np.argsort(-np.array(scores_filtered))
print("Unique letter combinations:")
for i in idx:
    print( scores_filtered[i], unique_combos[list(unique_combos)[i]] )

# score the whole word list
scores_filtered = []
for word in words_filtered:
    score = 0
    for c in word:
        index = ord(c) - ord('a')
        score += hist[index]
    scores_filtered.append(score)
idx = np.argsort(-np.array(scores_filtered))
print("All words, with repeated letters:")
for i in idx:
    print( scores_filtered[i], words_filtered[i] )
