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