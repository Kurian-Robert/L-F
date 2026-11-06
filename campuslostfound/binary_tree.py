class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        new_node = TreeNode(data)
        if self.root is None:
            self.root = new_node
            return

        current = self.root
        while True:
            if data < current.data:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right

    def search(self, value):
        current = self.root
        while current:
            if current.data == value:
                return True
            elif value < current.data:
                current = current.left
            else:
                current = current.right
        return False

    # --- NEW: Deletion Logic for UI Synchronization ---
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return node

        if value < node.data:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.data:
            node.right = self._delete_recursive(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._get_min_value_node(node.right)
            node.data = temp.data
            node.right = self._delete_recursive(node.right, temp.data)

        return node

    def _get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # --- NEW: Phase 2 Required Traversals ---
    def inorder_traversal(self, node, result_list):
        if node:
            self.inorder_traversal(node.left, result_list)
            result_list.append(node.data)
            self.inorder_traversal(node.right, result_list)
        return result_list

    def preorder_traversal(self, node, result_list):
        if node:
            result_list.append(node.data)
            self.preorder_traversal(node.left, result_list)
            self.preorder_traversal(node.right, result_list)
        return result_list

    def postorder_traversal(self, node, result_list):
        if node:
            self.postorder_traversal(node.left, result_list)
            self.postorder_traversal(node.right, result_list)
            result_list.append(node.data)
        return result_list