from typing import Dict
from datastructures.bk_tree import BKTreeThreaded
from interface_elements.spell_elements import SpellCheckerScreen,SelectLanguageScreen
from edit_distance import levenshtein_distance
from dictionary_loader import DictionaryLoader
import sys
import curses
from curses import ascii


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




def c_main(stdscr):
    stdscr.nodelay(1)

    
    new_text_file_path = sys.argv[1] if len(sys.argv) > 1 else None
    dictionary_loader = DictionaryLoader()
    if new_text_file_path:
        dictionary = dictionary_loader.create_dictionary(new_text_file_path)
    else:
        dictionaries = dictionary_loader.get_dictionary_list()
        dictionary = dictionary_loader.load_dictionary(dictionaries[0])
    screen_stack = []
    #spell_screen = SpellCheckerScreen(screen_stack,dictionary)
    spell_screen = SelectLanguageScreen(screen_stack)
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


