from datastructures.bk_tree import BKTreeThreaded
from datastructures.priority_queue_updatedable import PriorityQueueUpdateable
from interface_elements.spell_elements import SpellCheckerScreen
from edit_distance import levenshtein_distance
from threading import Lock
import random
import sys
import curses
from curses import ascii
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

def load_dictionary(filename=None):
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
    if filename is not None:
        return create_dictionary_from_file(filename)
    else:
        with open('dictionary.pbk','rb') as dict_file:
            return pickle.load(dict_file)

def create_dictionary_from_file(filename:str):
    with open(filename,'r') as word_file:
        words = word_file.readlines()
    #prevent recursion depth overflow
    random.shuffle(words)
    dictionary = BKTreeThreaded(levenshtein_distance)
    for word in words:
        dictionary.add_element(word.strip())
    with open('dictionary.pbk','wb') as dict_file:
        pickle.dump(dictionary,dict_file)
    return dictionary


def c_main(stdscr):
    stdscr.nodelay(1)

    
    new_text_file_path = sys.argv[1] if len(sys.argv) > 1 else None
   
    dictionary = load_dictionary(new_text_file_path)
    screen_stack = []
    spell_screen = SpellCheckerScreen(screen_stack,dictionary)
    screen_stack.append(spell_screen)
    while True:
        character = stdscr.getch()
        if curses.ascii.iscntrl(character):
            if character == curses.ascii.ESC:
                break
        
        screen_stack[-1].process_input(character)
        screen_stack[-1].draw(stdscr)
            
       

        # 
    return 0

def main():
    try:
        return curses.wrapper(c_main)
    except FileNotFoundError:
        if len(sys.argv) > 1:
            print('The text file you attempted to upload could not be found.')
        else:
            print('The dictionary could not be found. Please select file to upload.')
if __name__ == "__main__":
    exit(main())


