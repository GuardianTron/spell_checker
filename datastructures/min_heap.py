class MinHeap:

    def __init__(self):
        self._heap = []

    def peek(self):
        if len(self) <= 0:
            raise LookupError('The heap is empty.')
        return self._heap[0]

    def pop(self):
        if len(self) <= 0:
            raise LookupError("The heap is empty.")
        top_value = self._heap[0]
        #replace top with last child in heap and swim 
        last_child = self._heap.pop()
        if len(self) > 0:
            self._heap[0] = last_child
            self._sink(0)
        return top_value
    
    def insert(self,value):
        self._heap.append(value)
        self._swim(len(self) - 1)

    
    def _sink(self,index):
        if index < len(self):
            left_child_index,right_child_index = self._get_children_indices(index)

            #swap node with smallest child to sink it
            if left_child_index and right_child_index:
                current_value = self._heap[index]
                left_child_value = self._heap[left_child_index]
                right_child_value = self._heap[right_child_index]
                #swap with left child
                if left_child_value <= right_child_value and left_child_value < current_value:
                    self._swap_values(index,left_child_index)
                    self._sink(left_child_index)
                elif right_child_value < left_child_value and right_child_value < current_value:
                    self._swap_values(index,right_child_index)
                    self._sink(right_child_index)
            elif left_child_index and self._heap[left_child_index] < self._heap[index]:
                self._swap_values(index,left_child_index)
                self._sink(left_child_index)

     

    
    def _swim(self,index): 
        if index > 0:
            parent_index = self._get_parent_index(index)
            current_value = self._heap[index]
            parent_value = self._heap[parent_index]
            #not heap ordered so swap values
            #and just keep swimming
            if current_value < parent_value:
                self._heap[index] = parent_value
                self._heap[parent_index] = current_value
                self._swim(parent_index)

    def _swap_values(self,index1,index2):
        temp = self._heap[index1]
        self._heap[index1] = self._heap[index2]
        self._heap[index2] = temp

    def _get_children_indices(self,index):
        if index < 0:
            raise ValueError(f"{index} must be zero or greater.")
        elif int(index) != index:
            raise ValueError(f"Index {index} is not an integer")

        left_child = 2*index+1
        right_child = 2*index+2
        #make sure indices don't exceed heap size
        if left_child >= len(self):
            left_child = None
        if right_child >= len(self):
            right_child = None

        return (left_child,right_child)

    def _get_parent_index(self,index):
        if index <= 0: 
            raise ValueError(f"Index {index} parent.")
        return int((index-1)/2)


    def __len__(self):
        return len(self._heap)

    
#testing
if __name__ == "__main__":
    print('Testing Heap...')
    heap = MinHeap()
    try:
        heap.pop()
    except LookupError:
        print("Attempt to pop empty heap successfully caused error.")

    print("Testing min heap with sorting...\n")

    from random import randint
    sorts_attempted = 10
    failed_sorts = 0
    for i in range(10):
        unsorted_list = [randint(0,100) for i in range(10)]
        print(f"Unsorted: \t {unsorted_list}")
        for i in unsorted_list:
            heap.insert(i)
        #sort by putting new values into list
        sorted_list = []
        while len(heap):
            sorted_list.append(heap.pop())
        #make sure lists are sorted in ascending order
        is_sorted = True
        for i in range(1,len(sorted_list)):
            if sorted_list[i-1] > sorted_list[i]: 
                is_sorted = False
                failed_sorts += 1
        print_label = "Sorted" if is_sorted else "Failed"
        print(f"{print_label}: \t {sorted_list}")

        print(" ")
    
    print(f'Total Sorts: \t {sorts_attempted}')
    print(f'Succesful: \t {sorts_attempted - failed_sorts}')
    print(f'Failed: \t {failed_sorts}')