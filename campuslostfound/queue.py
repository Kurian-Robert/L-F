# queue.py

class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:

    def __init__(self):
        self.front = None
        self.rear = None

    # Add claim
    def enqueue(self, data):

        new_node = QueueNode(data)

        if self.rear is None:
            self.front = self.rear = new_node
            return

        self.rear.next = new_node
        self.rear = new_node

    # Process claim
    def dequeue(self):

        if self.front is None:
            print("No claims available.")
            return None

        data = self.front.data

        self.front = self.front.next

        if self.front is None:
            self.rear = None

        return data

    # Display claims
    def display(self):

        if self.front is None:
            print("No pending claims.")
            return

        current = self.front

        print("\nPending Claims:")

        while current:
            print("-", current.data)
            current = current.next