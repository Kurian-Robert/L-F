import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set Times New Roman as standard font for all academic diagrams
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Times', 'serif']
plt.rcParams['mathtext.fontset'] = 'stix'

doc_images = os.path.abspath("doc_images")
os.makedirs(doc_images, exist_ok=True)

# -------------------------------------------------------------
# TRADITIONAL BLACK & WHITE ACADEMIC FLOWCHART PRIMITIVES
# -------------------------------------------------------------
COLOR_BLACK = "#000000"
COLOR_WHITE = "#FFFFFF"
COLOR_GRAY_BG = "#F4F4F4"   # Very subtle academic shading for headers
COLOR_TEXT = "#000000"
LINE_WIDTH = 1.4

def draw_terminator(ax, x, y, w, h, text, subtext=""):
    """Traditional Flowchart Terminator (Oval / Stadium) for Start/End"""
    pill = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={h/2}",
                                  facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=LINE_WIDTH, zorder=3)
    ax.add_patch(pill)
    if subtext:
        ax.text(x + w/2, y + h*0.64, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color=COLOR_TEXT, zorder=4)
        ax.text(x + w/2, y + h*0.32, subtext, ha='center', va='center', fontsize=8, color=COLOR_TEXT, zorder=4)
    else:
        ax.text(x + w/2, y + h*0.5, text, ha='center', va='center', fontsize=10, fontweight='bold', color=COLOR_TEXT, zorder=4)

def draw_process(ax, x, y, w, h, text, subtext="", bg=COLOR_WHITE):
    """Traditional Flowchart Process (Sharp Rectangle with crisp black border)"""
    rect = patches.Rectangle((x, y), w, h, facecolor=bg, edgecolor=COLOR_BLACK, linewidth=LINE_WIDTH, zorder=3)
    ax.add_patch(rect)
    if subtext:
        ax.text(x + w/2, y + h*0.66, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color=COLOR_TEXT, zorder=4)
        ax.text(x + w/2, y + h*0.32, subtext, ha='center', va='center', fontsize=8, color=COLOR_TEXT, zorder=4)
    else:
        ax.text(x + w/2, y + h*0.5, text, ha='center', va='center', fontsize=9.5, fontweight='bold', color=COLOR_TEXT, zorder=4)

def draw_decision(ax, x, y, w, h, text):
    """Traditional Flowchart Decision (Diamond / Rhombus)"""
    pts = [[x, y + h/2], [x + w/2, y + h], [x + w, y + h/2], [x + w/2, y]]
    diamond = patches.Polygon(pts, closed=True, facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=LINE_WIDTH, zorder=3)
    ax.add_patch(diamond)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color=COLOR_TEXT, zorder=4)

def draw_io(ax, x, y, w, h, text, subtext="", slant=2.5):
    """Traditional Flowchart Data Input/Output (Parallelogram)"""
    pts = [[x + slant, y + h], [x + w, y + h], [x + w - slant, y], [x, y]]
    poly = patches.Polygon(pts, closed=True, facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=LINE_WIDTH, zorder=3)
    ax.add_patch(poly)
    if subtext:
        ax.text(x + w/2, y + h*0.64, text, ha='center', va='center', fontsize=9, fontweight='bold', color=COLOR_TEXT, zorder=4)
        ax.text(x + w/2, y + h*0.32, subtext, ha='center', va='center', fontsize=7.8, color=COLOR_TEXT, zorder=4)
    else:
        ax.text(x + w/2, y + h*0.5, text, ha='center', va='center', fontsize=9, fontweight='bold', color=COLOR_TEXT, zorder=4)

def draw_arrow(ax, x1, y1, x2, y2, label="", lw=LINE_WIDTH, rad=0.0):
    """Draw traditional crisp black directional arrow with optional centered label"""
    conn = "arc3,rad=0.0" if rad == 0.0 else f"arc3,rad={rad}"
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=COLOR_BLACK, lw=lw, shrinkA=1, shrinkB=1, connectionstyle=conn), zorder=5)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        ax.text(mx, my + 1.2, label, ha='center', va='bottom', fontsize=8, fontweight='bold', color=COLOR_BLACK,
                bbox=dict(boxstyle="square,pad=0.15", facecolor=COLOR_WHITE, edgecolor="none", alpha=0.95), zorder=6)

# -------------------------------------------------------------
# 1. 3-TIER SYSTEM ARCHITECTURE DIAGRAM (TRADITIONAL B&W)
# -------------------------------------------------------------
def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(10.5, 7.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)

    # Title Banner
    ax.text(50, 96.5, "Figure 6.1: 3-Tier Layered System Architecture", ha='center', va='center',
            fontsize=13, fontweight='bold', color=COLOR_BLACK)
    ax.text(50, 93.5, "Presentation, Core Algorithmic Logic, and Relational Database Persistence Layers",
            ha='center', va='center', fontsize=9, color=COLOR_BLACK)

    # Layer 1: Presentation Tier
    rect1 = patches.Rectangle((4, 68), 92, 22, facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=LINE_WIDTH, zorder=1)
    ax.add_patch(rect1)
    ax.text(6, 87, "TIER 1: PRESENTATION & CLIENT INTERFACE LAYER", fontsize=9.5, fontweight='bold', color=COLOR_BLACK)
    
    draw_process(ax, 7, 71, 26, 13, "Student / Public Web", "HTML5, CSS3 Responsive Form\nSearch & Filter Lost Catalog")
    draw_process(ax, 37, 71, 26, 13, "Admin Management Portal", "Role-Based Dispatch & Auth\nPriority Queue Dashboard & Undo")
    draw_process(ax, 67, 71, 26, 13, "Desktop DSA Demonstrator", "Tkinter Desktop Native GUI\nReal-time Pointer & BST Inspector")

    # Layer 2: Algorithmic Core Tier
    rect2 = patches.Rectangle((4, 34), 92, 30, facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=LINE_WIDTH, zorder=1)
    ax.add_patch(rect2)
    ax.text(6, 61, "TIER 2: CORE APPLICATION LOGIC & ALGORITHMIC ENGINE LAYER", fontsize=9.5, fontweight='bold', color=COLOR_BLACK)

    draw_process(ax, 7, 37, 20, 20, "Phase 1: Linear DS", "• Singly Linked List\n• LIFO Activity Stack\n• FIFO Claim Queue")
    draw_process(ax, 30, 37, 20, 20, "Phase 2: Tree & Graph", "• BST Lookup O(log n)\n• In/Pre/Post Traversal\n• Campus Graph BFS")
    draw_process(ax, 53, 37, 20, 20, "Phase 3: Sort/Search", "• Linked List Merge Sort\n  O(n log n) Fast Pointer\n• Linear Scan Compare")
    draw_process(ax, 76, 37, 19, 20, "Phase 4: Optimization", "• DP Levenshtein Matrix\n  Typo-Tolerant Match\n• Greedy Min-Heap PQ")

    # Layer 3: Persistence Tier
    rect3 = patches.Rectangle((4, 4), 92, 26, facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=LINE_WIDTH, zorder=1)
    ax.add_patch(rect3)
    ax.text(6, 27, "TIER 3: DATA PERSISTENCE & MEMORY MANAGEMENT LAYER", fontsize=9.5, fontweight='bold', color=COLOR_BLACK)

    draw_process(ax, 7, 7, 26, 16, "Django ORM & Models", "• lost_items & found_items\n• claim_processing / done\n• activity_logs Table")
    draw_process(ax, 37, 7, 26, 16, "MySQL 8.0 RDBMS", "• Schema: data_structure\n• InnoDB ACID Transactions\n• Strict Foreign Keys (3NF)")
    draw_process(ax, 67, 7, 26, 16, "In-Memory Pointers", "• Dynamic Linked Nodes\n• Binary Tree Heap Objects\n• Adjacency List Hash Map")

    # Inter-Tier Flow Arrows
    draw_arrow(ax, 20, 71, 20, 58, "HTTP Request")
    draw_arrow(ax, 50, 71, 50, 58, "Claim Dispatch")
    draw_arrow(ax, 80, 71, 80, 58, "Direct Memory Call")

    draw_arrow(ax, 20, 37, 20, 24, "ORM Query")
    draw_arrow(ax, 50, 37, 50, 24, "SQL Persistence")
    draw_arrow(ax, 80, 37, 80, 24, "Heap References")

    out_path = os.path.join(doc_images, "arch_system_architecture.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=COLOR_WHITE, edgecolor='none')
    plt.close()
    print("Generated arch_system_architecture.png (Traditional B&W)")

# -------------------------------------------------------------
# 2. MASTER SYSTEM WORKFLOW FLOWCHART (TRADITIONAL B&W)
# -------------------------------------------------------------
def generate_master_flowchart():
    fig, ax = plt.subplots(figsize=(9.5, 9.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)

    ax.text(50, 97.5, "Figure 6.2: Master System Workflow & Claim Processing Pipeline", ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_BLACK)

    # 1. Start Terminator
    draw_terminator(ax, 38, 91, 24, 4.8, "START", "Student / Staff Access")

    # 2. Input Item Details
    draw_io(ax, 28, 81.5, 44, 6.2, "Report Item / Submit Query", "Name, Category, Location, Priority")

    # 3. Decision: Search Query or New Registration?
    draw_decision(ax, 33, 68, 34, 9.5, "Is Search Query?")

    # 4. Search Path - Branch Left: Levenshtein DP & Campus BFS
    draw_process(ax, 4, 53, 38, 9.5, "Typo-Tolerant Search (DP)", "Wagner-Fischer Matrix (dist <= 4)\nCampus Adjacency BFS for Nearby Areas")

    # 5. Register Path - Branch Right: Insert into Data Structures
    draw_process(ax, 58, 53, 38, 9.5, "Store & Index Property", "Append Singly Linked List\nInsert into BST (O(log n))\nPush Action to LIFO Stack")

    # 6. Claim Submission
    draw_process(ax, 28, 38, 44, 9, "Claim Submission & Scheduling", "Enqueue into FIFO Queue\nPush into Greedy Min-Heap Priority Queue\n(Priority 1: ID/Keys, 2: Academic, 3: General)")

    # 7. Decision: Admin Verification
    draw_decision(ax, 33, 23.5, 34, 9.5, "Ownership Verified?")

    # 8. Resolution and Reversal
    draw_process(ax, 58, 10, 38, 9, "Handover & Archive", "Move to claim_done\nRecord LIFO Log for Undo")
    draw_process(ax, 4, 10, 38, 9, "Reject Claim / Retain in Queue", "Alert Student / Keep in Custody")

    # 9. End Terminator
    draw_terminator(ax, 38, 1.5, 24, 4.8, "END", "Record Audited")

    # Connectors
    draw_arrow(ax, 50, 91, 50, 87.7)
    draw_arrow(ax, 50, 81.5, 50, 77.5)

    # From Decision "Is Search Query?"
    draw_arrow(ax, 33, 72.7, 23, 72.7)
    draw_arrow(ax, 23, 72.7, 23, 62.5, "Yes")
    
    draw_arrow(ax, 67, 72.7, 77, 72.7)
    draw_arrow(ax, 77, 72.7, 77, 62.5, "No")

    # Merge into Claim Submission
    draw_arrow(ax, 23, 53, 40, 47)
    draw_arrow(ax, 77, 53, 60, 47)

    # From Claim Submission to Decision "Ownership Verified?"
    draw_arrow(ax, 50, 38, 50, 33)

    # Branches from "Ownership Verified?"
    draw_arrow(ax, 67, 28.2, 77, 28.2)
    draw_arrow(ax, 77, 28.2, 77, 19, "Yes")

    draw_arrow(ax, 33, 28.2, 23, 28.2)
    draw_arrow(ax, 23, 28.2, 23, 19, "No")

    # To End Terminator
    draw_arrow(ax, 77, 10, 58, 4)
    draw_arrow(ax, 23, 10, 42, 4)

    out_path = os.path.join(doc_images, "flowchart_system_workflow.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=COLOR_WHITE, edgecolor='none')
    plt.close()
    print("Generated flowchart_system_workflow.png (Traditional B&W)")

# -------------------------------------------------------------
# 3. DFD LEVEL 0 (CONTEXT DIAGRAM - TRADITIONAL B&W)
# -------------------------------------------------------------
def generate_dfd_level0():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)

    ax.text(50, 96, "Figure 7.5: Data Flow Diagram (DFD) - Level 0 Context Diagram", ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_BLACK)
    ax.text(50, 92.5, "Boundary Interactions between Campus Stakeholders and Central System", ha='center', va='center',
            fontsize=9, color=COLOR_BLACK)

    # Central System Process (Circle / Oval)
    circle = patches.FancyBboxPatch((35, 36), 30, 26, boxstyle="round,pad=0,rounding_size=13",
                                    facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=1.8, zorder=3)
    ax.add_patch(circle)
    ax.text(50, 52, "0.0", ha='center', va='center', fontsize=12, fontweight='bold', color=COLOR_BLACK, zorder=4)
    ax.text(50, 46, "CAMPUS LOST & FOUND\nMANAGEMENT SYSTEM", ha='center', va='center', fontsize=9.5, fontweight='bold', color=COLOR_BLACK, zorder=4)

    # External Entities (Standard Sharp Rectangles with crisp double line or single border)
    draw_process(ax, 4, 39, 21, 20, "Student / Claimant", "• Submit Loss Reports\n• Query Found Catalog\n• Claim Missing Items")
    draw_process(ax, 40, 75, 20, 15, "Finder / Samaritan", "• Surrender Found Items\n• Specify Location & Date")
    draw_process(ax, 75, 39, 21, 20, "System Administrator", "• Verify Claim Proof\n• Dispatch Min-Heap PQ\n• Execute LIFO Undo")
    draw_process(ax, 40, 7, 20, 15, "Campus Security Office", "• Custody Handover\n• Sign Release Receipts")

    # Directed Data Flows
    draw_arrow(ax, 25, 52, 35, 52, "Loss Report / Claim")
    draw_arrow(ax, 35, 44, 25, 44, "Search Results / Status")

    draw_arrow(ax, 50, 75, 50, 62, "Found Property Details")
    draw_arrow(ax, 75, 52, 65, 52, "Claim Actions / Undo")
    draw_arrow(ax, 65, 44, 75, 44, "Priority Queue & Logs")

    draw_arrow(ax, 50, 36, 50, 22, "Handover Authorization")

    out_path = os.path.join(doc_images, "dfd_level0_context.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=COLOR_WHITE, edgecolor='none')
    plt.close()
    print("Generated dfd_level0_context.png (Traditional B&W)")

# -------------------------------------------------------------
# 4. DFD LEVEL 1 (SUBSYSTEM PROCESS DECOMPOSITION - TRADITIONAL B&W)
# -------------------------------------------------------------
def generate_dfd_level1():
    fig, ax = plt.subplots(figsize=(10.5, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)

    ax.text(50, 97.5, "Figure 7.6: Data Flow Diagram (DFD) - Level 1 Subsystem Decomposition", ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_BLACK)

    # External Entities
    draw_process(ax, 4, 76, 18, 12, "Student Entity", "Loss reports, claims,\nsearch keywords")
    draw_process(ax, 78, 76, 18, 12, "Admin Entity", "Claim verification,\npriority dispatch, undo")

    # Sub-processes (Standard Rounded Rectangles with ID)
    def draw_dfd_proc(ax, x, y, w, h, pid, name, details):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=2",
                                      facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=LINE_WIDTH, zorder=3)
        ax.add_patch(rect)
        # Process header line
        ax.plot([x, x+w], [y+h-3.5, y+h-3.5], color=COLOR_BLACK, lw=1.2, zorder=4)
        ax.text(x + w/2, y + h - 1.8, f"PROCESS {pid}: {name}", ha='center', va='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK, zorder=5)
        ax.text(x + w/2, y + (h-3.5)/2, details, ha='center', va='center', fontsize=7.8, color=COLOR_TEXT, zorder=5)

    draw_dfd_proc(ax, 38, 83, 24, 11, "1.0", "Authentication", "Validate Session & Roles\n(Student, Faculty, Admin)")
    draw_dfd_proc(ax, 8, 54, 24, 12, "2.0", "Item Registration", "Validate Fields, Assign Priority\n& Store in Active Tables")
    draw_dfd_proc(ax, 38, 54, 24, 12, "3.0", "Algorithmic Search", "BST ID Lookup & Merge Sort\nDP Levenshtein & Campus BFS")
    draw_dfd_proc(ax, 68, 54, 24, 12, "4.0", "Claim Scheduling", "FIFO Queue Enqueue\nGreedy Min-Heap Priority Order")
    draw_dfd_proc(ax, 38, 25, 24, 12, "5.0", "Activity Auditing", "LIFO Activity Stack Logging\nAdministrative State Reversal")

    # Data Stores (Standard Open Parallel Lines D1, D2, D3)
    def draw_store(ax, x, y, w, h, ds_id, ds_name):
        ax.plot([x, x+w], [y+h, y+h], color=COLOR_BLACK, lw=1.5, zorder=3)
        ax.plot([x, x+w], [y, y], color=COLOR_BLACK, lw=1.5, zorder=3)
        ax.plot([x+w*0.22, x+w*0.22], [y, y+h], color=COLOR_BLACK, lw=1.2, zorder=3)
        ax.fill_between([x, x+w], [y, y], [y+h, y+h], color=COLOR_WHITE, zorder=2)
        ax.text(x+w*0.11, y+h/2, ds_id, ha='center', va='center', fontsize=8.5, fontweight='bold', color=COLOR_BLACK, zorder=4)
        ax.text(x+w*0.61, y+h/2, ds_name, ha='center', va='center', fontsize=8, fontweight='semibold', color=COLOR_BLACK, zorder=4)

    draw_store(ax, 6, 8, 26, 7.5, "D1", "lost_items / found_items")
    draw_store(ax, 37, 8, 26, 7.5, "D2", "claim_processing / done")
    draw_store(ax, 68, 8, 26, 7.5, "D3", "activity_logs (LIFO Stack)")

    # Data flow connections
    draw_arrow(ax, 13, 76, 17, 66, "Item Info")
    draw_arrow(ax, 20, 54, 19, 15.5, "Write Record")
    draw_arrow(ax, 32, 60, 38, 60, "Keywords")
    draw_arrow(ax, 62, 60, 68, 60, "Matched Item")
    draw_arrow(ax, 87, 76, 80, 66, "Dispatch Request")
    draw_arrow(ax, 80, 54, 55, 15.5, "Update Claim Status")
    draw_arrow(ax, 50, 54, 50, 37, "Audit Event")
    draw_arrow(ax, 50, 25, 78, 15.5, "Persist Log")
    draw_arrow(ax, 87, 76, 62, 33, "Undo Command")

    out_path = os.path.join(doc_images, "dfd_level1_system.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=COLOR_WHITE, edgecolor='none')
    plt.close()
    print("Generated dfd_level1_system.png (Traditional B&W)")

# -------------------------------------------------------------
# 5. RELATIONAL DATABASE SCHEMA & ER DIAGRAM (TRADITIONAL B&W)
# -------------------------------------------------------------
def generate_db_er_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 7.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)

    ax.text(50, 96.5, "Figure 7.7: Relational Database Schema & Entity-Relationship (ER) Diagram", ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_BLACK)
    ax.text(50, 93.5, "3NF Normalized MySQL Tables with Primary/Foreign Keys and Relational Cardinality",
            ha='center', va='center', fontsize=9, color=COLOR_BLACK)

    def draw_er_table(ax, x, y, w, h, table_name, columns):
        # Header banner with black outline and subtle shading
        hdr = patches.Rectangle((x, y + h - 5), w, 5, facecolor=COLOR_GRAY_BG, edgecolor=COLOR_BLACK, linewidth=1.3, zorder=3)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 2.5, table_name, ha='center', va='center', fontsize=9, fontweight='bold', color=COLOR_BLACK, zorder=4)

        # Body rectangle
        body = patches.Rectangle((x, y), w, h - 5, facecolor=COLOR_WHITE, edgecolor=COLOR_BLACK, linewidth=1.3, zorder=3)
        ax.add_patch(body)
        step = (h - 6) / len(columns)
        for idx, (col, ctype, key) in enumerate(columns):
            cy = y + h - 7 - (idx * step)
            ax.text(x + 1.5, cy, col, ha='left', va='center', fontsize=7.5, fontweight='semibold', color=COLOR_BLACK, zorder=4)
            key_suffix = f" [{key}]" if key else ""
            ax.text(x + w - 1.5, cy, f"{ctype}{key_suffix}", ha='right', va='center', fontsize=7, color=COLOR_BLACK, zorder=4)

    # Table 1: lost_items
    draw_er_table(ax, 5, 52, 26, 32, "lost_items", [
        ("id", "INT AUTO_INC", "PK"),
        ("student_name", "VARCHAR(100)", ""),
        ("item_name", "VARCHAR(100)", ""),
        ("location", "VARCHAR(100)", ""),
        ("priority", "INT (1-3)", ""),
        ("is_resolved", "TINYINT(1)", ""),
        ("created_at", "DATETIME", "")
    ])

    # Table 2: found_items
    draw_er_table(ax, 69, 52, 26, 32, "found_items", [
        ("id", "INT AUTO_INC", "PK"),
        ("student_name", "VARCHAR(100)", ""),
        ("item_name", "VARCHAR(100)", ""),
        ("location", "VARCHAR(100)", ""),
        ("priority", "INT (1-3)", ""),
        ("is_resolved", "TINYINT(1)", ""),
        ("created_at", "DATETIME", "")
    ])

    # Table 3: claim_processing
    draw_er_table(ax, 5, 8, 26, 32, "claim_processing", [
        ("id", "INT AUTO_INC", "PK"),
        ("student_name", "VARCHAR(100)", ""),
        ("item_name", "VARCHAR(100)", ""),
        ("location", "VARCHAR(100)", ""),
        ("priority", "INT", ""),
        ("lost_item_id", "INT", "FK"),
        ("created_at", "DATETIME", "")
    ])

    # Table 4: claim_done
    draw_er_table(ax, 37, 8, 26, 32, "claim_done", [
        ("id", "INT AUTO_INC", "PK"),
        ("student_name", "VARCHAR(100)", ""),
        ("item_name", "VARCHAR(100)", ""),
        ("location", "VARCHAR(100)", ""),
        ("priority", "INT", ""),
        ("lost_item_id", "INT", "FK"),
        ("claimed_at", "DATETIME", "")
    ])

    # Table 5: activity_logs
    draw_er_table(ax, 69, 8, 26, 32, "activity_logs", [
        ("id", "INT AUTO_INC", "PK"),
        ("action_type", "VARCHAR(20)", ""),
        ("category", "VARCHAR(10)", ""),
        ("item_id", "INT", ""),
        ("description", "VARCHAR(200)", ""),
        ("created_at", "DATETIME", "")
    ])

    # Relationships in solid black
    draw_arrow(ax, 18, 52, 18, 40, "1 : N (CASCADE)")
    draw_arrow(ax, 28, 52, 45, 40, "1 : 1 (SET_NULL)")

    out_path = os.path.join(doc_images, "db_er_diagram.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=COLOR_WHITE, edgecolor='none')
    plt.close()
    print("Generated db_er_diagram.png (Traditional B&W)")

# -------------------------------------------------------------
# 6. BST FLOWCHART (TRADITIONAL B&W)
# -------------------------------------------------------------
def generate_bst_flowchart():
    fig, ax = plt.subplots(figsize=(9.5, 7.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)

    ax.text(50, 97, "Figure 7.1: Binary Search Tree (BST) Lookup & Deletion Algorithm Flowchart", ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_BLACK)

    # 1. Start Terminator
    draw_terminator(ax, 38, 89, 24, 5, "Start BST Search", "Target ID, Root Node")

    # 2. Decision 1: Node is NULL?
    draw_decision(ax, 35, 74, 30, 9, "Current == NULL?")

    # 3. Not Found Terminator
    draw_terminator(ax, 74, 75.5, 22, 6, "Not Found", "Return False")

    # 4. Decision 2: Target equals Current?
    draw_decision(ax, 33, 56, 34, 9.5, "Target == Current.Data?")

    # 5. Found Terminator
    draw_terminator(ax, 74, 57.5, 22, 6.5, "Match Found", "Return Record / Node")

    # 6. Decision 3: Target less than Current?
    draw_decision(ax, 33, 37, 34, 9.5, "Target < Current.Data?")

    # 7. Left / Right Branches
    draw_process(ax, 8, 20, 34, 8.5, "Traverse Left Subtree", "Current = Current.Left")
    draw_process(ax, 58, 20, 34, 8.5, "Traverse Right Subtree", "Current = Current.Right")

    # Arrows
    draw_arrow(ax, 50, 89, 50, 83)
    draw_arrow(ax, 65, 78.5, 74, 78.5, "Yes")
    draw_arrow(ax, 50, 74, 50, 65.5, "No")

    draw_arrow(ax, 67, 60.7, 74, 60.7, "Yes")
    draw_arrow(ax, 50, 56, 50, 46.5, "No")

    draw_arrow(ax, 33, 41.7, 25, 28.5, "Yes (Go Left)")
    draw_arrow(ax, 67, 41.7, 75, 28.5, "No (Go Right)")

    # Loop back arrows
    draw_arrow(ax, 25, 20, 42, 70, "Loop")
    draw_arrow(ax, 75, 20, 58, 70, "Loop")

    out_path = os.path.join(doc_images, "flowchart_phase2_bst.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=COLOR_WHITE, edgecolor='none')
    plt.close()
    print("Generated flowchart_phase2_bst.png (Traditional B&W)")

# -------------------------------------------------------------
# 7. CAMPUS BFS GRAPH FLOWCHART (TRADITIONAL B&W)
# -------------------------------------------------------------
def generate_bfs_flowchart():
    fig, ax = plt.subplots(figsize=(9.5, 7.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)

    ax.text(50, 97, "Figure 7.2: Campus Adjacency Graph BFS Proximity Flowchart", ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_BLACK)

    # 1. Start Terminator
    draw_terminator(ax, 36, 88.5, 28, 5.5, "Initialize BFS Traversal", "Queue = [Start], Visited = {Start}")

    # 2. Decision: Is Queue Empty?
    draw_decision(ax, 34, 72, 32, 9.5, "Is Queue Empty?")

    # 3. Traversal Complete Terminator
    draw_terminator(ax, 73, 73.5, 23, 6.5, "Traversal Complete", "Return Search Order List")

    # 4. Dequeue Vertex
    draw_process(ax, 32, 53, 36, 8.5, "Dequeue Vertex V", "V = queue.pop(0)\nAppend V to search_order")

    # 5. Inspect Neighbors
    draw_process(ax, 32, 35, 36, 9.5, "Inspect Neighbors of V", "Iterate over Adjacency List\ngraph[V] = [N1, N2, ...]")

    # 6. Decision: Neighbor in Visited?
    draw_decision(ax, 33, 17, 34, 9.5, "Neighbor in Visited?")

    # 7. Action: Enqueue neighbor
    draw_process(ax, 72, 17, 24, 9.5, "Enqueue Neighbor", "visited.add(N)\nqueue.append(N)")

    # Connectors
    draw_arrow(ax, 50, 88.5, 50, 81.5)
    draw_arrow(ax, 66, 76.7, 73, 76.7, "Yes")
    draw_arrow(ax, 50, 72, 50, 61.5, "No")
    draw_arrow(ax, 50, 53, 50, 44.5)
    draw_arrow(ax, 50, 35, 50, 26.5)

    draw_arrow(ax, 67, 21.7, 72, 21.7, "No")
    draw_arrow(ax, 84, 26.5, 84, 68, "Next")
    draw_arrow(ax, 33, 21.7, 20, 21.7)
    draw_arrow(ax, 20, 21.7, 20, 76.7, "Yes (Skip)")
    draw_arrow(ax, 20, 76.7, 34, 76.7)

    out_path = os.path.join(doc_images, "flowchart_phase2_bfs_graph.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=COLOR_WHITE, edgecolor='none')
    plt.close()
    print("Generated flowchart_phase2_bfs_graph.png (Traditional B&W)")

# -------------------------------------------------------------
# 8. MERGE SORT FLOWCHART (TRADITIONAL B&W)
# -------------------------------------------------------------
def generate_merge_sort_flowchart():
    fig, ax = plt.subplots(figsize=(9.5, 7.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)

    ax.text(50, 97, "Figure 7.3: Linked List Merge Sort Division & In-Place Merge Flowchart", ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_BLACK)

    # 1. Start / Base case decision
    draw_decision(ax, 33, 80, 34, 9.5, "head is None or\nhead.next is None?")

    # Base case exit
    draw_terminator(ax, 74, 81.5, 22, 6.5, "Return head", "Base Case: Already Sorted")

    # Two-pointer midpoint search
    draw_process(ax, 30, 63, 40, 9.5, "Find Midpoint (Fast & Slow)", "slow advances 1 step, fast advances 2 steps\nWhen fast hits end, slow is middle")

    # Sever list
    draw_process(ax, 30, 47, 40, 9, "Sever Link into Halves", "next_to_middle = middle.next\nmiddle.next = None (Divides List)")

    # Recursive sub-sorts
    draw_process(ax, 10, 29, 36, 9.5, "Recursively Sort Left Half", "left = merge_sort(head)")
    draw_process(ax, 54, 29, 36, 9.5, "Recursively Sort Right Half", "right = merge_sort(next_to_middle)")

    # In-place merge
    draw_process(ax, 28, 9, 44, 11, "In-Place Pointer Merge: sorted_merge(left, right)",
                 "Compare left.data['id'] <= right.data['id']\nSplice node.next pointers directly (O(1) extra space)")

    # Connectors
    draw_arrow(ax, 67, 84.7, 74, 84.7, "Yes")
    draw_arrow(ax, 50, 80, 50, 72.5, "No")
    draw_arrow(ax, 50, 63, 50, 56)
    draw_arrow(ax, 40, 47, 28, 38.5)
    draw_arrow(ax, 60, 47, 72, 38.5)
    draw_arrow(ax, 28, 29, 42, 20)
    draw_arrow(ax, 72, 29, 58, 20)

    out_path = os.path.join(doc_images, "flowchart_phase3_merge_sort.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=COLOR_WHITE, edgecolor='none')
    plt.close()
    print("Generated flowchart_phase3_merge_sort.png (Traditional B&W)")

# -------------------------------------------------------------
# 9. LEVENSHTEIN DP MATRIX FLOWCHART (TRADITIONAL B&W)
# -------------------------------------------------------------
def generate_levenshtein_flowchart():
    fig, ax = plt.subplots(figsize=(9.5, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_WHITE)
    ax.set_facecolor(COLOR_WHITE)

    ax.text(50, 97, "Figure 7.4: Dynamic Programming Levenshtein Distance Matrix Flowchart", ha='center', va='center',
            fontsize=12, fontweight='bold', color=COLOR_BLACK)

    # 1. Initialize matrix
    draw_process(ax, 30, 85, 40, 7.5, "Initialize 2D DP Matrix", "DP[0..m][0..n], where m=len(str1), n=len(str2)")

    # 2. Base conditions
    draw_process(ax, 30, 71, 40, 8, "Set Base Boundary Conditions", "DP[i][0] = i (Deletions), DP[0][j] = j (Insertions)")

    # 3. Decision: Character match?
    draw_decision(ax, 33, 53, 34, 10, "str1[i-1] == str2[j-1]?")

    # 4. Match cost 0
    draw_process(ax, 6, 36, 40, 9.5, "Characters Match (Cost = 0)", "DP[i][j] = DP[i-1][j-1]\nCopy diagonal previous state")

    # 5. Mismatch min cost
    draw_process(ax, 54, 36, 42, 9.5, "Characters Mismatch (Cost = 1 + min)", "DP[i][j] = 1 + min(Insert, Delete, Replace)\nmin(DP[i][j-1], DP[i-1][j], DP[i-1][j-1])")

    # 6. Smart Match Threshold Decision
    draw_decision(ax, 33, 19, 34, 9.5, "Edit Distance <= 4?")

    # 7. Outputs
    draw_terminator(ax, 6, 4, 38, 7.5, "Output Smart Match", "'Did you mean: [Matched Item]?'")
    draw_terminator(ax, 56, 4, 38, 7.5, "Reject Distant Query", "'No close matches found'")

    # Connectors
    draw_arrow(ax, 50, 85, 50, 79)
    draw_arrow(ax, 50, 71, 50, 63)
    draw_arrow(ax, 33, 58, 26, 45.5, "Yes")
    draw_arrow(ax, 67, 58, 75, 45.5, "No")
    draw_arrow(ax, 26, 36, 42, 28.5)
    draw_arrow(ax, 75, 36, 58, 28.5)
    draw_arrow(ax, 33, 23.7, 25, 11.5, "Yes")
    draw_arrow(ax, 67, 23.7, 75, 11.5, "No")

    out_path = os.path.join(doc_images, "flowchart_phase4_levenshtein.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=COLOR_WHITE, edgecolor='none')
    plt.close()
    print("Generated flowchart_phase4_levenshtein.png (Traditional B&W)")

if __name__ == "__main__":
    generate_system_architecture()
    generate_master_flowchart()
    generate_dfd_level0()
    generate_dfd_level1()
    generate_db_er_diagram()
    generate_bst_flowchart()
    generate_bfs_flowchart()
    generate_merge_sort_flowchart()
    generate_levenshtein_flowchart()
    print("All traditional black & white academic format visuals successfully generated!")
