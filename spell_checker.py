from datastructures.bk_tree import BKTree
from edit_distance import levenshtein_distance
import random
import sys
import timeit
import pickle

def load_dictionary(filename='usa.txt'):
    #load the dictionary if cached, otherwise build from text file
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
    return dictionary


search_string = sys.argv[1].strip()
dictionary = load_dictionary()


results = dictionary.search(search_string,4)



results.sort(key= lambda result_tuple: result_tuple[1])
print(f'Search String: {search_string}')
print(f'Number dictionary results: {len(results)}')
print(f'{"-"*20}')
for i in range(0,len(results)):
    word,score = results[i]
    word = word.strip()
    print(f"{word:15}  {score} ")


