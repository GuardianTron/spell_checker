import curses
from curses import ascii
from .base import Window

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