from datastructures.bk_tree import BKTreeThreaded
from edit_distance import levenshtein_distance
from threading import Lock
import random
import sys
import curses
from curses import ascii
from queue import PriorityQueue
from threaded_search_runner import SearchRunner
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
        dictionary = BKTreeThreaded(levenshtein_distance)

        for word in words:
            dictionary.add_element(word.strip())
        dictionary_handle = open('dictionary','wb')
        pickle.dump(dictionary,dictionary_handle)
        dictionary_handle.close()
    return dictionary



def c_main(stdscr):
    stdscr.nodelay(1)
    word_window = curses.newwin(2,curses.COLS,0,0)
    results_window_height = curses.LINES - 2
    results_window = curses.newwin(results_window_height,40,2,5)
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    results_window.bkgd(' ',curses.color_pair(1))
    dictionary = load_dictionary()
    word = ''
    results_pqueue = PriorityQueue()
    threads = []
    last_update = 0
    while True:
        character = stdscr.getch()
        word_changed = False
        list_updated = False
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
            search = SearchRunner(dictionary,word,results_pqueue,daemon=True)
            threads.append(search)
            search.start()
            #results = dictionary.search(word,3,[])  
            
                
        if not results_pqueue.empty():
            result = results_pqueue.get()
            update_time = result.priority
            results = result.item
            if last_update > update_time:
                last_update = update_time
                while not results_pqueue.empty():
                    result = results_pqueue.get()
                    if result.priority < last_update:
                        last_update = result.priority
                        results = result.item

                results.sort(key=lambda results: results[1])
                results_max = results_window_height if len(results) > results_window_height else len(results)
                results_window.clear()
                results_window.addstr(0,1,word)
                for i in range(0,results_max -1):
                    results_window.addstr(i+1,1,results[i][0])
                    results_window.border()
                    results_window.refresh()
            
            
        if list_updated or word_changed:
            word_window.clear()
        
       
            word_window.addstr(0,0,word)
 
        
            word_window.refresh()
    return 0

def main():
    return curses.wrapper(c_main)

if __name__ == "__main__":
    exit(main())

