from queue import PriorityQueue

class PriorityQueueUpdateable(PriorityQueue):
    
    def __init__(self,*args,**kwargs):
        self._last_update = 0
        self._latest_result = None
        super().__init__(*args,**kwargs)

    def has_new_results(self):
        if not self.empty():
            result = self.get()
            update_time = result.priority
            self._latest_result = result.item
            if self._last_update > update_time:
                self._last_update = update_time
                while not self.empty():
                    result = self.get()
                    if result.priority < self._last_update:
                        self._last_update = result.priority
                        self._latest_result = result.item
            return True
        return False

    def get_latest_result(self):
        return self._latest_result
