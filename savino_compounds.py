#Savino's Fill in the blank clue generator
#gensim stuff from https://www.geeksforgeeks.org/nlp/nlp-gensim-tutorial-complete-guide-for-beginners/#6-create-word2vec-model-using-gensim

import gensim
import os
import numpy as np
import random
from multiprocessing import cpu_count
import gensim.downloader as api
from gensim.utils import simple_preprocess
from gensim.test.utils import get_tmpfile
from gensim import corpora
from gensim import models
from gensim.models.word2vec import Word2Vec
from PyDictionary import PyDictionary
import itertools

##########################################

# Note from Savino: I'm not including the models that I made in the GitHub repo because they are large files.
# You should be able to recreate them by uncommenting the code below.
# Running as is will probably throw an error since the model file is not included.

#Train Word2Vec model on text8 dataset
#dataset = api.load("text8")
#data =[]
#for word in dataset:
#    data.append(word)

#data_1 = data[:1200]
#data_2 = data[1200:]

# Training the Word2Vec model
#w2v_model = Word2Vec(data_1, min_count = 0, workers = cpu_count())

# update model
#w2v_model.build_vocab(data_2, update = True)
#w2v_model.train(data_2, total_examples = w2v_model.corpus_count, epochs = w2v_model.epochs)
#w2v_model.save("w2v_text8.model")
w2v_model = Word2Vec.load("w2v_text8.model")

#################################################

#ran into an error here, fixed with info from:
# https://stackoverflow.com/questions/67687962/typeerror-word2vec-object-is-not-subscriptable
#print(w2v_model.wv['time'])

# Source - https://stackoverflow.com/a
# Posted by KWierzbicki
# Retrieved 2025-12-14, License - CC BY-SA 4.0

#    : Do the two hop thing, find a dl of homophones

# get english words from here: https://github.com/dolph/dictionary/blob/master/popular.txt
clue_amt = 28  # must be multiple of 4

with open('popular.txt', 'r') as f:
    english_words = f.readlines()
english_words = set(english_words)

# get possible roots
with open('possible_roots.txt', 'r') as f:
    possible_roots = f.readlines()
possible_roots = set(possible_roots)

# get all the words from the connections shit
doc = open('editable_connect_list.txt', encoding ='utf-8')
words =[]
for word in doc.read().split():
    word = word.strip(',_-\'()\"“”‘’1234567890! .?').lower()
    word = word.translate({ord(i): None for i in ',_-\'(“”‘’)\""1 234567890!.?'})
    if word not in words:
        if (len(word)>3) and (len(word)<6):
            words.append(word)
#print(len(words))

# generate clue words and compound words
questions = {}
clue_num = 0
while True:
    while True:
        root = random.choice(list(possible_roots)).strip().lower()
        if root not in questions:
            break
    #print(root)
    compounds = []
    possible_compounds = []
    for word in list(english_words):
        word = word.strip().lower()
        if word.startswith(root) and word != root:
            prefix = word[len(root):]
            for word in list(english_words):
                if prefix == word.strip().lower() and len(prefix) > 2:
                    possible_compounds.append(prefix)
        elif word.endswith(root) and word != root: # and word[:-len(root)] in english_words:
            suffix = word[:-len(root)]
            for word in list(english_words):
                if suffix == word.strip().lower() and len(suffix) > 2:
                    possible_compounds.append(suffix)
#print(possible_compounds)
    if len(possible_compounds) >= 4:
        questions[root] = random.sample(possible_compounds,4)
        #clue_num = clue_num + 1
        print(len(questions), root, questions[root])
    if len(questions) >= clue_amt:
        break
#print(questions)
            
#score each question based on semantic similarity of answers to other answers
scored_questions = {}
for q in questions:
    suffixes = questions[q]
    unique_pairs = list(itertools.combinations(suffixes, 2))
    sim_scores = []
    for pair in unique_pairs:
        word1 = pair[0]
        word2 = pair[1]
        if word1 in w2v_model.wv and word2 in w2v_model.wv:
            sim = w2v_model.wv.similarity(word1, word2)
            sim_scores.append(sim)
    avg_score = sum(sim_scores) / len(sim_scores) if sim_scores else 0
    scored_questions[avg_score] = (q)
#print(scored_questions)

#sort by semantic similarity scores and assign to colors and print
sorted_scores = sorted(scored_questions.keys(), reverse=True)
final_clues = ''
for color in ['green', 'green', 'green', 'green']:
    for i in range(clue_amt//4):
        top_score = sorted_scores.pop(0)
        clue_word = scored_questions[top_score]
        answers = ''
        for value in questions[clue_word]:
            answers += value + ', '
        final_clues += (f"{color}, Part of a compound word with {clue_word}:, {answers[:-2]}\n")
print(final_clues)

with open('generated_clues.txt', 'w') as f:
    f.write(final_clues)

# Stuff I messed with but am not using:

#https://stackoverflow.com/questions/40445859/find-compound-words-in-list-of-words-using-trie

# num =0
# for i in range(25):
#    if eng.meaning(words[rand], True) is not None:
#        num+=1
# print(num)

# compounds = []
# for first_word in words:
#    for sec_word in words:
#        compounds.append(first_word + sec_word)
# print(compounds)

#Tokenizing the document
#doc = open('editable_connect_list.txt', encoding ='utf-8')
#tokenized =[]
#for sentence in doc.read().split('.'):
#    tokenized.append(simple_preprocess(sentence, deacc = True))
#print(tokenized)

#Create a dictionary of tokenized words
#my_dictionary = corpora.Dictionary(tokenized)
#my_dictionary.save('my_dictionary.dict')

#load_dict = corpora.Dictionary.load('my_dictionary.dict')

#print(load_dict)

# Create Bag of Words corpus
#BoW_corpus =[load_dict.doc2bow(doc, allow_update = True) for doc in tokenized]
#print(BoW_corpus)

# Word weight in Bag of Words corpus
#word_weight =[]
#for doc in BoW_corpus:
#    for id, freq in doc:
#        word_weight.append([my_dictionary[id], freq])
#print(word_weight)

# Create TF-IDF model
#tfIdf = models.TfidfModel(BoW_corpus, smartirs ='ntc')

# TF-IDF Word Weight
#weight_tfidf =[]
#for doc in tfIdf[BoW_corpus]:
#    for id, freq in doc:
#        weight_tfidf.append([my_dictionary[id], np.around(freq, decimals = 3)])
#print(weight_tfidf)


