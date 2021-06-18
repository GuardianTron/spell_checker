from datastructures.bk_tree import BKTree
from edit_distance import levenshtein_distance
import random
import sys
import timeit
import pickle



search_string = sys.argv[1].strip()
with open('usa.txt','r') as words_file:
    words = words_file.readlines()
random.shuffle(words)
try:
    dictionary_handle = open('dictionary','rb')
    dictionary = pickle.load(dictionary_handle)
    dictionary_handle.close()
except:
    dictionary = BKTree(levenshtein_distance)

    for word in words:
        dictionary.add_element(word.strip())
    dictionary_handle = open('dictionary','wb')
    pickle.dump(dictionary,dictionary_handle)
    dictionary_handle.close()
results_dict = []

dictionary.search(search_string,4,results_dict)



results_bute = [(word,levenshtein_distance(search_string,word.strip())) for word in words]



results_dict.sort(key= lambda result_tuple: result_tuple[1])
results_bute.sort(key= lambda result_tuple: result_tuple[1])
print(f'Search String: {search_string}')
for i in range(0,20):
    word_dict,score_dict = results_dict[i]
    word_brute,score_brute = results_bute[i]
    print(f"{word_dict.strip()}: \t {score_dict} \t\t {word_brute.strip()}: \t {score_brute}")