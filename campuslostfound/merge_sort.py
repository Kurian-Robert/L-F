def merge_sort_linked_list(head):
    # Base case: if head is empty or there is only one element
    if head is None or head.next is None:
        return head

    # Find the middle of the linked list
    middle = get_middle(head)
    next_to_middle = middle.next
    
    # Sever the link to split the list in two
    middle.next = None

    # Recursively sort both halves
    left = merge_sort_linked_list(head)
    right = merge_sort_linked_list(next_to_middle)

    # Merge the sorted halves
    return sorted_merge(left, right)

def get_middle(head):
    if head is None:
        return head
    slow = head
    fast = head
    # Fast pointer moves two nodes, slow pointer moves one node
    while fast.next is not None and fast.next.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow

def sorted_merge(a, b):
    result = None
    
    # Base cases
    if a is None:
        return b
    if b is None:
        return a

    # Sort numerically by Item ID
    if a.data["id"] <= b.data["id"]:
        result = a
        result.next = sorted_merge(a.next, b)
    else:
        result = b
        result.next = sorted_merge(a, b.next)
        
    return result