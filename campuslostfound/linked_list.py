# linked_list.py

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # Insert a new item
    def insert(self, data):

        new_node = Node(data)

        if self.head is None:
            self.head = new_node
        else:
            current = self.head

            while current.next:
                current = current.next

            current.next = new_node

        print("Item inserted successfully.")

    # Delete an item using ID
    def delete(self, item_id):

        current = self.head
        previous = None

        while current:

            if current.data["id"] == item_id:

                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next

                print("Item deleted successfully.")
                return

            previous = current
            current = current.next

        print("Item not found.")

    # Display all items
    def traverse(self):

        if self.head is None:
            print("No items available.")
            return

        current = self.head

        while current:

            print("----------------------")
            print("ID       :", current.data["id"])
            print("Item     :", current.data["name"])
            print("Type     :", current.data["type"])
            print("Location :", current.data["location"])

            current = current.next