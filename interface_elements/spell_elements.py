import curses
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
