import numpy as np
import random
import itertools

with open('pre_homophones.txt', 'r') as f:
    pre_homophones = f.readlines()
    
# from here: https://legacy.earlham.edu/~peters/writing/homofone.html
better_homophones_dict = {}
for line in pre_homophones:
    line = line.strip().split(',')
    clean_line = []
    for word in line:
        if word.strip() == '':
            line.remove(word)
        if '[' in word: word = word.split('[')[0]
        if '(' in word: word = word.split('(')[0]
        word = word.translate({ord(i): None for i in ',_-\'(“”‘’)\""1 234567890!.?'})
        clean_line.append(word)
    if len(clean_line) > 1:
        for word in clean_line:
            homs = []
            for hom in clean_line:
                if word != hom:
                    homs.append(hom)
            better_homophones_dict[word] = homs

# for key in better_homophones_dict:
#     print(key, better_homophones_dict[key])

# ## Load homophone clues from: https://gist.github.com/tomByrer/cb5c9fae362c896ecd02#file-english-homophones-txt
# with open('homophones.txt', 'r') as f:
#     homophones = f.readlines()

# homophones_dict = {}
# for line in homophones:
#     line = line.strip().split(' / ')
#     for i in range(len(line)):
#         word = line[i].strip().lower()
#         homophones_dict[word] = [w.strip().lower() for j, w in enumerate(line) if j != i]

# Load synonym clues from Nico's file
with open('nico_hints.txt', 'r') as f:
    synonyms = f.readlines()
    
# with open('synonyms.txt', 'r') as f:
#     # synonyms = synonyms + f.readlines()
#     synonyms = f.readlines()
    
# with open('synonym_answers2.txt', 'r') as f:
#     synonyms = synonyms + f.readlines()
    # synonyms = f.readlines()
    
# with open('compound_words_green.txt', 'r') as f:
#     synonyms = synonyms + f.readlines()

# # Load synonym clues from Dylans's file
# with open('synonym_answers2.txt', 'r') as f:
#     synonyms = synonyms + f.readlines()
    
# process them into a dict
# # The code you provided is creating a dictionary called `synonyms_dict` by processing the lines read from the file `nico_hints.txt`.
# synonyms_dict = {}
# for line in synonyms:
#     line = line.strip().split(',')
#     synonyms_dict[line[1]] = []
#     for i in range(len(line)-2):
#         if line[i+2].strip() not in synonyms_dict[line[1]]:
#             synonyms_dict[line[1]].append(line[i+2].strip())
    
# i = 0
# for key in synonyms_dict:
#     i+=1
#     print(i, key, synonyms_dict[key])

# for line in synonyms_2:
#     line = line.strip().split(',')
#     synonyms_dict[line[1]] = line[2].strip().split(' ')

# homs_of_syms_dict = {}
# for key in synonyms_dict:
#     synonyms = synonyms_dict[key]
#     for syn in synonyms:
#         if syn in better_homophones_dict:
#             homs = better_homophones_dict[syn]
#             if key not in homs_of_syms_dict:
#                 homs_of_syms_dict[key] = set()
#             for hom in homs:
#                 homs_of_syms_dict[key].add(hom)
                
# for key in homs_of_syms_dict:
#     print(key, homs_of_syms_dict[key])

homs_of_syms = ''
for line in synonyms:
    line = line.strip().split(',')
    hom_line = ''
    synonyms_list = []
    for i in range(2, len(line)):
        synonyms_list.append(line[i].strip())
    #print(hom_line, str(synonyms_list))
    homs_list = []
    for syn in synonyms_list:
        if syn in better_homophones_dict.keys():
            #print(syn, better_homophones_dict[syn])
            for i in range(len(better_homophones_dict[syn])):
                homs_list.append(better_homophones_dict[syn][i])
    #print(homs_list)
    if len(homs_list) >= 4:
        #print(homs_list)
        for hom in homs_list:
            hom_line += ', ' + hom
        hom_line += '\n'
    if hom_line != '':
        hom_line = 'purple' + ',' + ' Homonyms for'+line[1].lower() + hom_line
        if hom_line not in homs_of_syms:
            homs_of_syms += hom_line
    
print(homs_of_syms)

with open('savino_purple.txt', 'w') as f:
    f.write(homs_of_syms)