# stack.py

class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:

    def __init__(self):
        self.top = None

    # Push
    def push(self, data):

        new_node = StackNode(data)

        new_node.next = self.top
        self.top = new_node

        print("Activity added to stack.")

    # Pop
    def pop(self):

        if self.top is None:
            print("Stack is empty.")
            return None

        data = self.top.data
        self.top = self.top.next

        return data

    # Display stack
    def display(self):

        if self.top is None:
            print("Stack is empty.")
            return

        current = self.top

        print("\nRecent Activities:")

        while current:
            print("-", current.data)
            current = current.next