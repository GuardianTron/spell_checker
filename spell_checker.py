from datastructures.bk_tree import BKTree
from edit_distance import levenshtein_distance
import random
import sys
import curses
from curses import ascii
import pickle

'''
Developer: Anthony Feeney
Email: feeney.anthony.l@gmail.com

This script implements a basic spellchecker utilizing a
memory optimized version of Wagner-Fischer algorithm to 
calculate the edit distance for words and a BK Tree to 
limit comparisons. 
Lists up to 25 words that are the closest match to the 
supplied string.

Usage:
Pass string to be checked as parameter.
'''

def load_dictionary(filename='usa.txt'):
    '''
    Loads the dictionary from file and stores in BKTree

    This function will load dictionary database from a 
    pickled BK tree if found.
    If not found, a text file consisting of words separated by \\n 
    newline characters will loaded and and processed into a BK tree
    which will then be pickled.   

    Keyword arguments:
    filename --- Name of the text file containing the dictionary

    Return: BKTree
    '''
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

def c_main(stdscr):
    word_window = curses.newwin(1,curses.COLS,0,0)
    results_window_height = curses.LINES - 1
    results_window = curses.newwin(results_window_height,40,2,5)
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    results_window.bkgd(' ',curses.color_pair(1))
    dictionary = load_dictionary()
    word = ''
    while True:
        character = stdscr.getch()
        word_changed = False
        if curses.ascii.iscntrl(character):
            if character == curses.ascii.ESC:
                break
            elif character in (curses.KEY_ENTER,10,13):
                pass
               
            elif character in (curses.KEY_BACKSPACE,127): #backaspce
                word = word[:-1]
                word_changed = True
        elif curses.ascii.isprint(character):
            character_to_s = chr(character)
            word_changed = True
            if len(word) < curses.COLS:
                word += character_to_s
            else:
                  word = word[1:] + character_to_s
            
        #update spell check list if word has changed  
        if word_changed:
            results = dictionary.search(word,3,[])  
            results.sort(key=lambda results: results[1])
            results_max = results_window_height if len(results) > results_window_height else len(results)
            results_window.clear()
            results_window.addstr(0,1,word)
            for i in range(0,results_max -1):
                results_window.addstr(i+1,1,results[i][0])
                results_window.border()
                results_window.refresh()
                

        word_window.clear()
        
       
        word_window.addstr(word)
        
        word_window.refresh()
    return 0

def main():
    return curses.wrapper(c_main)

if __name__ == "__main__":
    exit(main())
'''
    search_string = sys.argv[1].strip()
    dictionary = load_dictionary()
    results = dictionary.search(search_string,4)

    results.sort(key= lambda result_tuple: result_tuple[1])
    print(f'Search String: {search_string}')
    print(f'Number dictionary results: {len(results)}')
    print(f'{"-"*20}')
    num_results_to_display = min(25,len(results))
    for i in range(0,num_results_to_display):
        word,score = results[i]
        word = word.strip()
        print(f"{word:15}  {score} ")

'''
