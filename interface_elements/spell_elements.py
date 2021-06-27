import curses
from curses import ascii
from .base import Window,Screen
from datastructures.bk_tree import BKTreeThreaded
from datastructures.priority_queue_updatedable import PriorityQueueUpdateable
from threaded_search_runner import SearchRunner
class ResultsWindow(Window):

    def __init__(self,height:int,width:int,y:int,x:int,color_pair:int = None):
        self._height = height
        self._width = width
        self._results = []
        super().__init__(curses.newwin(height,width,y,x))
        if color_pair is not None:
            self._window.bkgd(' ',curses.color_pair(color_pair))

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self,results_list):
        self._results = results_list
        self.flag_for_redraw()

    def _draw_element(self):
        num_lines_to_draw = self._height if len(self._results) > self._height else len(self._results)
        for i in range(0,num_lines_to_draw - 1):
            self._window.addstr(i+1,1,self._results[i])
        self._window.border()

class InputWindow(Window):

    def __init__(self,y:int,x:int,color_pair:int = None):
        super().__init__(curses.newwin(2,curses.COLS,y,x))
        self._y = y
        if color_pair is not None:
            self._window.bkgd(' ',curses.color_pair(color_pair))
        self._word = ''

    def process_input(self,character):
        word_changed = False
        if ascii.iscntrl(character) and character in (curses.KEY_BACKSPACE,127):
            self._word = self._word[:-1]
            self.flag_for_redraw()
        elif ascii.isprint(character):
            self.flag_for_redraw()
            character_to_s = chr(character)
            if len(self._word) < curses.COLS:
                self._word += character_to_s
            else:
                self._word = self._word[1:] + character_to_s
    

    @property
    def text(self):
        return self._word

    def _draw_element(self):
        self._window.addstr(0,0,self._word)

    def capture_cursor(self,stdscr):
        cursor_x = len(self._word) if len(self._word) < curses.COLS - 1 else curses.COLS - 1
        stdscr.move(self._y,cursor_x)


class MenuWindow(Window):
    
    def __init__(self,height:int,width:int,y:int,x:int,color_pair_standard:int,color_pair_highlight:int):
        self._height = height
        self._width = width
        super().__init__(curses.newwin(height,width,y,x))

        self._base_color = curses.color_pair(color_pair_standard)
        self._highlight_color = curses.color_pair(color_pair_highlight)

        self._menu_options = []
        self._selected_option = 0

    @property
    def selected(self):
        return self._selected_option

    @selected.setter
    def selected(self,option:int):
        if option > len(self._menu_options):
            raise ValueError('The selected option exceeds the number set within the menu.')
        self._selected_option = option

    def add_menu_option(self,text:str,position:int = None):
        if position is None:
            self._menu_options.append(text)
        else:
            self._menu_options[position] = text 
    
    def remove_menu_option(self,position:int=None,text:str=None):
        if position is None and text is None:
            raise ValueError('Must set either a position or text to be removed.')
        elif position is not None:
            self._menu_options.pop(position)
        else:
            self._menu_options.remove(text)

    def __len__(self):
        return len(self._menu_options)        

    def _draw_element(self):
        num_lines_to_draw = self._height if len(self._menu_options) > self._height else len(self._menu_options)
        bottom_line_number = num_lines_to_draw - 1
        #determine the range to draw in the menu
        if self._selected_option > bottom_line_number: #selected option below visible area, draw at bottom
            draw_range = range(self._selected_option - bottom_line_number,self._selected_option)
        else: #draw options 0 - bottom_line_number
            draw_range = range(0,bottom_line_number)
        
        for option in draw_range:
            if option == self._selected_option:
                self._window.bkgd(' ',self._highlight_color)
            else:
                self._window.bkgd(' ',self._base_color)
            self._window.addstr(option,0,self._menu_options[option])
        
        #reset color and draw border
        self._window.bkgd(' ',self._base_color)
        self._window.border()

    
class SpellCheckerScreen(Screen):

    def __init__(self,window_stack:list,dictionary:BKTreeThreaded):
        super().__init__(window_stack)
        self._input_window = InputWindow(0,0)
        self.register_window(self._input_window)
        curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
        results_window_height = curses.LINES - 2
        self._results_window = ResultsWindow(results_window_height,40,2,5,1)
        self.register_window(self._results_window)
        self._dictionary = dictionary
        self._results_pqueue = PriorityQueueUpdateable()

        self._current_word = ''

    def process_input(self, character):
                   

        self._input_window.process_input(character)
        if self._current_word != self._input_window.text:
            self._current_word = self._input_window.text
            search = SearchRunner(self._dictionary,self._current_word,self._results_pqueue,daemon=True)
            search.start()

        if self._results_pqueue.has_new_results():
            results = self._results_pqueue.get_latest_result()
            results.sort(key=lambda results: results[1])
            self._results_window.results = [result[0] for result in results]

    def draw(self,stdscr):
        super().draw(stdscr)
        self._input_window.capture_cursor(stdscr)