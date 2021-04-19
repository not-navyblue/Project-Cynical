from typing import Any, Iterable, Union

class Queue:
    def __init__(self, items: Union[Iterable, Any] = None):
        if isinstance(items, Iterable) and not isinstance(items, str):
            self.items = list(items)
        elif not items is None:
            self.items = [items]
        else:
            self.items = []
    
    def is_empty(self):
        return self.items == []
    
    def enqueue(self, items):
        self.items.append(items)
        
    def dequeue(self):
        if self.items == []:
            raise EmptyQueue()
        
        return self.items.pop(0)
    
    def get_item_index(self, item):
        try:
            return self.items.index(item)
        except ValueError:
            return None
    
    def size(self):
        return len(self.items)

class Stack:
    def __init__(self, items: Union[Iterable, Any] = None):
        if isinstance(items, Iterable) and not isinstance(items, str):
            self.items = list(items)
        elif not items is None:
            self.items = [items]
        else:
            self.items = []
    
    def is_empty(self):
        return self.items == []
    
    def push(self, items):
        self.items.append(items)
        
    def pop(self):
        if self.items == []:
            raise EmptyStack()
        
        return self.items.pop()
    
    def size(self):
        return len(self.items)

class EmptyQueue(KeyError):
    def __init__(self, message = None):
        super().__init__(message or "Queue is empty")
        
class EmptyStack(KeyError):
    def __init__(self, message = None):
        super().__init__(message or "Stack is empty")