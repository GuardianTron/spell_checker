from abc import ABC

class Screen(ABC):
    '''
        Base class for Screens.
        Each screen will represent 
        the entire output of the application
        for a signle section and will
        act as the controller for a given 
        application function.
        Override this this class to create new screens.

    '''
    def __init__(self,window_stack,stdscr):
        '''
            Handles initialization of the Screen.
            Takes a copy of the window stack
            to allow class to screens to 
            be drawn by the calling applicaton.
            Note: Call super before attempting to 
            register and deregister windows.
        '''
        self._windows = []
        self._window_stack = window_stack
        self._stdscr = stdscr

    def register_window(self,window):
        '''Add a window to be drawn.'''
        self._windows.append(window)

    def deregister_window(self,window):
        '''Remove window from drawing.'''
        try:
            self._windows.remove(window)
        except ValueError:
            #already removed so no need to worry
            pass 

    def process_input(self,character):
        '''Override this to create the controller for the screen.'''
        pass
    
    def draw(self,stdscr):
        '''
            Called by application to draw the windows.
            Takes standard screen curses object as a parameter so 
            that subclasses can use it for clean up operations such
            as fixing the cursor. 
            Not used here but docmuneted for consistency in caller
            which will pass this to all instances.
        '''
        for window in self._windows:
            window.draw()

    def handle_resize(self):
        '''Mark all windows to be redrawn in case terminal is resized.'''
        for window in self._windows:
            window.flag_for_redraw()
    
    def enter(self):
        pass

    def exit(self):
        pass


class Window(ABC):

    '''
        Base class for all window elements.  
        Provides methods for drawing and managing redrawing of 
        windows.
    '''

    def __init__(self,curses_window):
        '''
            Takes an ncurses window object to operate on.
            Subclasses should create this window themselves.
        '''
        self._window = curses_window
        self._draw_this_cycle = False

    def flag_for_redraw(self):
        ''' Will force redraw of window in event of resize.'''
        self._draw_this_cycle = True

    def draw(self):
        '''Called by screen class to draw the element. Override _draw_element to implement acutal draw'''
        if(self._draw_this_cycle):
            self._window.clear()
            self._draw_element()
            self._window.refresh()
            self._draw_this_cycle = False

    

    def _draw_element(self):
        '''Override this method in subclass to handle window drawing'''
        pass

class ScreenStack:

    def __init__(self):
        self._stack = []

    def _check_len_or_error(self):
        if len(self._stack) < 1:
            raise LookupError('Stack is empty.')
   
    def empty(self):
        return len(self._stack) == 0

    def __len__(self):
        return len(self._stack)

    def peek(self):
        self._check_len_or_error()            
        return self._stack[-1]
    
    def pop(self):
        self._check_len_or_error()
        top = self._stack.pop()
        top.exit()
        return top

    def append(self,screen:Screen):
        screen.enter()
        self._stack.append(screen)

