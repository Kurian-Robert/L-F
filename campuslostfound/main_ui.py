import tkinter as tk
from tkinter import messagebox
import sys
import io

# Import your custom data structures
from linked_list import LinkedList
from stack import Stack
from queue import Queue 
from binary_tree import BinarySearchTree
from graph import CampusGraph
from merge_sort import merge_sort_linked_list
from smart_match import find_best_match

# Initialize data structures
items = LinkedList()
activities = Stack()
claims = Queue()
item_tree = BinarySearchTree()
campus_map = CampusGraph()  # <-- Fixed: This was missing

def add_item_ui():
    try:
        item_id = int(entry_id.get())
        name = entry_name.get()
        item_type = entry_type.get()
        location = entry_loc.get()
        
        # Insert into structures
        items.insert({"id": item_id, "name": name, "type": item_type, "location": location})
        activities.push(f"Added item: {name}")
        item_tree.insert(item_id)
        
        messagebox.showinfo("Success", "Item Added Successfully!")
        
        # Clear inputs
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_type.delete(0, tk.END)
        entry_loc.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Item ID must be an integer.")

def find_nearby_ui():
    location = entry_loc.get()
    if not location:
        messagebox.showwarning("Warning", "Please enter a location in the Add Item section to search nearby.")
        return
        
    # Run the O(V+E) BFS traversal
    nearby = campus_map.get_nearby_locations(location)
    activities.push(f"Ran BFS traversal from: {location}")
    
    messagebox.showinfo("BFS Traversal Result", f"If item is missing from {location}, check these connected areas:\n\n{', '.join(nearby)}")

def search_item_ui():
    try:
        item_id = int(entry_search_id.get())
        
        # O(log N) search using the Binary Search Tree
        if item_tree.search(item_id):
            messagebox.showinfo("Search Result", f"Item ID {item_id} FOUND in the system!")
        else:
            messagebox.showwarning("Search Result", f"Item ID {item_id} NOT FOUND.")
            
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric ID.")

def delete_item_ui():
    try:
        item_id = int(entry_search_id.get())
        
        # Synchronized deletion: Remove from both Linked List and BST
        items.delete(item_id)
        item_tree.delete(item_id)
        activities.push(f"Deleted item ID: {item_id}")
        
        messagebox.showinfo("Success", f"Attempted to delete Item ID {item_id}.")
        entry_search_id.delete(0, tk.END)
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric ID.")

def add_claim_ui():
    name = entry_claim_name.get()
    item_id = entry_claim_id.get()
    if name and item_id:
        claims.enqueue(f"{name} claimed item {item_id}")
        activities.push("New claim added")
        messagebox.showinfo("Success", "Claim Added to Queue!")
        entry_claim_name.delete(0, tk.END)
        entry_claim_id.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter both name and item ID.")

def process_claim_ui():
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    claims.dequeue()
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    output_box.delete('1.0', tk.END)
    output_box.insert(tk.END, f"Processed Claim:\n{output}" if output else "No claims available.")

def sort_items_ui():
    if items.head is None:
        messagebox.showinfo("Notice", "No items to sort.")
        return
        
    items.head = merge_sort_linked_list(items.head)
    activities.push("Sorted items by ID using Merge Sort")
    messagebox.showinfo("Success", "Linked List sorted by Item ID!")
    display_items_ui()

def smart_match_ui():
    search_term = entry_smart_search.get()
    if not search_term:
        messagebox.showwarning("Warning", "Please enter an item name to match.")
        return
        
    result = find_best_match(search_term, items.head)
    activities.push(f"Ran smart match for: {search_term}")
    messagebox.showinfo("Smart Match (Levenshtein)", result)

def display_items_ui():
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    items.traverse()
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    output_box.delete('1.0', tk.END)
    output_box.insert(tk.END, output if output else "No items in list.")

# --- UI Layout ---
window = tk.Tk()
window.title("Campus Lost & Found System")
window.geometry("500x850") # Taller window to fit all phases

# --- Add Item Section ---
tk.Label(window, text="--- Add New Item ---", font=('Helvetica', 10, 'bold')).pack(pady=(5,2))
tk.Label(window, text="Item ID:").pack()
entry_id = tk.Entry(window)
entry_id.pack()

tk.Label(window, text="Item Name:").pack()
entry_name = tk.Entry(window)
entry_name.pack()

tk.Label(window, text="Type (Lost/Found):").pack()
entry_type = tk.Entry(window)
entry_type.pack()

tk.Label(window, text="Location:").pack()
entry_loc = tk.Entry(window)
entry_loc.pack()

frame_add_btns = tk.Frame(window)
frame_add_btns.pack(pady=5)
tk.Button(frame_add_btns, text="Add Item", bg="lightblue", command=add_item_ui).pack(side=tk.LEFT, padx=5)
tk.Button(frame_add_btns, text="Find Nearby (BFS)", bg="thistle", command=find_nearby_ui).pack(side=tk.LEFT, padx=5)

# --- Manage Claims Section ---
tk.Label(window, text="--- Manage Claims ---", font=('Helvetica', 10, 'bold')).pack(pady=(5,2))
tk.Label(window, text="Claimant Name:").pack()
entry_claim_name = tk.Entry(window)
entry_claim_name.pack()

tk.Label(window, text="Target Item ID:").pack()
entry_claim_id = tk.Entry(window)
entry_claim_id.pack()

frame_btns = tk.Frame(window)
frame_btns.pack(pady=5)
tk.Button(frame_btns, text="Enqueue Claim", bg="lightgreen", command=add_claim_ui).pack(side=tk.LEFT, padx=5)
tk.Button(frame_btns, text="Process Claim", bg="salmon", command=process_claim_ui).pack(side=tk.LEFT, padx=5)

# --- Phase 2: BST Search & Delete ---
tk.Label(window, text="--- Search & Delete (BST) ---", font=('Helvetica', 10, 'bold')).pack(pady=(5,2))
entry_search_id = tk.Entry(window)
entry_search_id.pack()

frame_sd_btns = tk.Frame(window)
frame_sd_btns.pack(pady=5)
tk.Button(frame_sd_btns, text="Search ID", bg="khaki", command=search_item_ui).pack(side=tk.LEFT, padx=5)
tk.Button(frame_sd_btns, text="Delete Item", bg="tomato", command=delete_item_ui).pack(side=tk.LEFT, padx=5)

# --- Phase 4: Smart Match (DP) ---
tk.Label(window, text="--- Smart Match (Levenshtein) ---", font=('Helvetica', 10, 'bold')).pack(pady=(5,2))
entry_smart_search = tk.Entry(window)
entry_smart_search.pack()
tk.Button(window, text="Fuzzy Search Name", bg="lightcyan", command=smart_match_ui).pack(pady=5)

# --- Phase 3 & Display Section ---
frame_disp_btns = tk.Frame(window)
frame_disp_btns.pack(pady=5)
tk.Button(frame_disp_btns, text="Display All Items", bg="lightgrey", command=display_items_ui).pack(side=tk.LEFT, padx=5)
tk.Button(frame_disp_btns, text="Sort by ID (Merge)", bg="plum", command=sort_items_ui).pack(side=tk.LEFT, padx=5)

# Output Box
output_box = tk.Text(window, height=10, width=50, bg="black", fg="white")
output_box.pack(pady=10)

window.mainloop()