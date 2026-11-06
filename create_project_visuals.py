import os
import subprocess
import tempfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

doc_images = os.path.abspath("doc_images")
os.makedirs(doc_images, exist_ok=True)

# -------------------------------------------------------------
# 1. CAPTURE WEB SCREENSHOTS
# -------------------------------------------------------------
def capture_web_screenshots():
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dsa_scheduler.settings')
    django.setup()
    from django.template.loader import render_to_string
    from scheduler.models import LostItem, FoundItem, ClaimProcessing, ClaimDone, ActivityLog

    lost_pending = list(ClaimProcessing.objects.all())
    found_pending = list(FoundItem.objects.filter(is_resolved=False))
    lost_resolved = list(ClaimDone.objects.order_by('-id')[:5])
    found_resolved = list(FoundItem.objects.filter(is_resolved=True).order_by('-id')[:5])
    activities = list(ActivityLog.objects.order_by('-id')[:6])

    # 1. Dashboard
    ctx_dash = {
        'lost_pending': lost_pending,
        'found_pending': found_pending,
        'lost_resolved': lost_resolved,
        'found_resolved': found_resolved,
        'items': [],
        'resolved_items': [],
        'activities': activities,
        'message': 'Welcome to Campus Lost & Found System - Academic Edition',
        'db_info': 'MySQL Database: data_structure (Tables: lost_items, found_items, claim_processing, claim_done)',
        'is_admin': True,
        'is_faculty': False,
        'search_q': '',
        'search_loc': '',
        'search_performed': False,
        'found_search_results': [],
        'unique_locations': ['Library', 'Lab 2', 'Classroom', 'Main Block', 'Cafeteria', 'Sports Ground'],
    }
    dash_html = render_to_string('index.html', ctx_dash)
    with open(os.path.join(doc_images, 'page_dashboard.html'), 'w', encoding='utf-8') as f:
        f.write(dash_html)

    # 2. Login
    login_html = render_to_string('login.html', {'message': ''})
    with open(os.path.join(doc_images, 'page_login.html'), 'w', encoding='utf-8') as f:
        f.write(login_html)

    # 3. Search Results
    found_search = list(FoundItem.objects.filter(location__icontains='Lab'))
    ctx_search = dict(ctx_dash)
    ctx_search.update({
        'search_q': 'Calculator',
        'search_loc': 'Lab',
        'search_performed': True,
        'found_search_results': found_search,
    })
    search_html = render_to_string('index.html', ctx_search)
    with open(os.path.join(doc_images, 'page_search.html'), 'w', encoding='utf-8') as f:
        f.write(search_html)

    edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    temp_profile = os.path.join(tempfile.gettempdir(), 'edge_lf_doc_profile')

    pages = [
        ('page_dashboard.html', 'ui_web_dashboard.png', 1280, 1050),
        ('page_login.html', 'ui_web_login.png', 1280, 850),
        ('page_search.html', 'ui_web_search.png', 1280, 950),
    ]

    for html_file, out_name, w, h in pages:
        in_path = os.path.join(doc_images, html_file)
        out_path = os.path.join(doc_images, out_name)
        url = 'file:///' + in_path.replace('\\', '/')
        try:
            subprocess.run([
                edge_exe,
                '--headless=new',
                '--disable-gpu',
                f'--user-data-dir={temp_profile}',
                f'--screenshot={out_path}',
                f'--window-size={w},{h}',
                url
            ], capture_output=True, timeout=15)
            print(f"Captured {out_name}: {os.path.getsize(out_path)} bytes")
        except Exception as e:
            print(f"Error capturing {html_file}: {e}")

# -------------------------------------------------------------
# 2. GENERATE DIAGRAM UTILITIES
# -------------------------------------------------------------
def draw_rounded_box(ax, x, y, w, h, title, subtitle="", bg="#FFFFFF", border="#1B365D", lw=1.5, title_color="#1B365D", sub_color="#475569", title_fontsize=10, sub_fontsize=8):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.2",
                                facecolor=bg, edgecolor=border, linewidth=lw, zorder=2)
    ax.add_patch(box)
    if subtitle:
        ax.text(x + w/2, y + h*0.62, title, ha='center', va='center', fontsize=title_fontsize, fontweight='bold', color=title_color, zorder=3)
        ax.text(x + w/2, y + h*0.30, subtitle, ha='center', va='center', fontsize=sub_fontsize, color=sub_color, zorder=3)
    else:
        ax.text(x + w/2, y + h*0.5, title, ha='center', va='center', fontsize=title_fontsize, fontweight='bold', color=title_color, zorder=3)

def draw_arrow(ax, x1, y1, x2, y2, label="", color="#1E293B", lw=1.5, style="->"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, shrinkA=3, shrinkB=3), zorder=4)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        ax.text(mx, my + 1.2, label, ha='center', va='bottom', fontsize=7.5, fontweight='semibold', color=color,
                bbox=dict(boxstyle="square,pad=0.15", facecolor="#FFFFFF", edgecolor="none", alpha=0.85), zorder=5)

# -------------------------------------------------------------
# 3. SYSTEM ARCHITECTURE DIAGRAM
# -------------------------------------------------------------
def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Main Title
    ax.text(50, 96, "Campus Lost & Found System - Architectural Design", ha='center', va='center',
            fontsize=15, fontweight='bold', color="#1B365D")
    ax.text(50, 92.5, "Tiered Integration: Desktop DSA Engine, Django Web Framework & MySQL Relational Store",
            ha='center', va='center', fontsize=9.5, color="#64748B")

    # Layer 1: Presentation Layer
    draw_rounded_box(ax, 3, 67, 94, 21, "", bg="#EFF6FF", border="#93C5FD", lw=1.2)
    ax.text(6, 85, "1. PRESENTATION & CLIENT LAYER", fontsize=10, fontweight='bold', color="#1E40AF")
    draw_rounded_box(ax, 6, 70, 26, 12, "Student / Public Web", "HTML5, CSS3, Responsive Portal\nSearch, Filter & Browse Found Items", bg="#FFFFFF", border="#2563EB")
    draw_rounded_box(ax, 37, 70, 26, 12, "Faculty / Admin Portal", "Role-Based Claim Dispatch\nQueue Inspection & LIFO Stack Undo", bg="#FFFFFF", border="#2563EB")
    draw_rounded_box(ax, 68, 70, 26, 12, "Desktop DSA Demonstrator", "Tkinter Native Python GUI\nDirect Pointer & Tree Visualizer", bg="#FFFFFF", border="#2563EB")

    # Layer 2: Application Logic & Algorithms
    draw_rounded_box(ax, 3, 33, 94, 29, "", bg="#F0FDF4", border="#86EFAC", lw=1.2)
    ax.text(6, 59, "2. CORE APPLICATION LOGIC & ALGORITHMIC LAYER", fontsize=10, fontweight='bold', color="#15803D")

    draw_rounded_box(ax, 6, 36, 20, 19, "Phase 1: Linear DS", "• Singly Linked List (Items)\n• Stack (Audit Logs & Undo)\n• Queue (FIFO Claims)", bg="#FFFFFF", border="#16A34A", sub_fontsize=7.5)
    draw_rounded_box(ax, 29, 36, 20, 19, "Phase 2: Tree & Graph", "• BST (O(log n) Search/Del)\n• In/Pre/Post Traversals\n• Campus Graph BFS Spatial", bg="#FFFFFF", border="#16A34A", sub_fontsize=7.5)
    draw_rounded_box(ax, 52, 36, 20, 19, "Phase 3: Search/Sort", "• Linked List Merge Sort\n  O(n log n) Fast Pointer\n• Linear vs Tree Search", bg="#FFFFFF", border="#16A34A", sub_fontsize=7.5)
    draw_rounded_box(ax, 75, 36, 20, 19, "Phase 4: Optimization", "• Dynamic Programming\n  Levenshtein Smart Match\n• Greedy Min-Heap PQ", bg="#FFFFFF", border="#16A34A", sub_fontsize=7.5)

    # Layer 3: Persistence Layer
    draw_rounded_box(ax, 3, 4, 94, 24, "", bg="#FEF3C7", border="#FDE68A", lw=1.2)
    ax.text(6, 25, "3. PERSISTENCE & DATA STORAGE LAYER", fontsize=10, fontweight='bold', color="#B45309")

    draw_rounded_box(ax, 6, 7, 26, 14, "Django ORM & Models", "• LostItem & FoundItem\n• ClaimProcessing & ClaimDone\n• ActivityLog Auditing", bg="#FFFFFF", border="#D97706", sub_fontsize=7.5)
    draw_rounded_box(ax, 37, 7, 26, 14, "MySQL RDBMS", "Schema: data_structure\nInnoDB Engine, Foreign Keys\nACID Transaction Safety", bg="#FFFFFF", border="#D97706", sub_fontsize=7.5)
    draw_rounded_box(ax, 68, 7, 26, 14, "In-Memory Pointers", "Python Heap Nodes\nDynamic Pointer Chaining\nBST Tree Nodes & Adjacency Map", bg="#FFFFFF", border="#D97706", sub_fontsize=7.5)

    # Connecting Arrows
    draw_arrow(ax, 19, 70, 19, 56, "HTTP / Views", color="#2563EB")
    draw_arrow(ax, 50, 70, 50, 56, "Claims / Auth", color="#2563EB")
    draw_arrow(ax, 81, 70, 81, 56, "In-Memory Direct", color="#2563EB")

    draw_arrow(ax, 19, 36, 19, 22, "CRUD / Log", color="#16A34A")
    draw_arrow(ax, 50, 36, 50, 22, "Heap / ORM", color="#16A34A")
    draw_arrow(ax, 81, 36, 81, 22, "Pointer State", color="#16A34A")

    out_path = os.path.join(doc_images, "arch_system_architecture.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated arch_system_architecture.png")

# -------------------------------------------------------------
# 4. SYSTEM MASTER WORKFLOW FLOWCHART
# -------------------------------------------------------------
def generate_master_flowchart():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    ax.text(50, 96, "Master System Workflow - Campus Lost & Found System", ha='center', va='center',
            fontsize=14, fontweight='bold', color="#1B365D")

    # Flowchart Nodes
    draw_rounded_box(ax, 38, 88, 24, 6, "START", "User / Admin Access", bg="#DBEAFE", border="#1D4ED8")
    draw_rounded_box(ax, 35, 76, 30, 8, "Item Reporting / Discovery", "Capture: Name, Type, Location, Priority", bg="#FFFFFF", border="#1B365D")
    draw_rounded_box(ax, 10, 62, 35, 9, "Typo-Tolerant Query (Phase 4)", "Run DP Levenshtein Distance Matrix\nCalculate Distance <= 4 (Smart Match)", bg="#FEF3C7", border="#D97706")
    draw_rounded_box(ax, 55, 62, 35, 9, "Spatial Proximity (Phase 2)", "Run Campus Graph BFS Traversal\nSuggest Adjacent Search Locations", bg="#E0E7FF", border="#4338CA")

    draw_rounded_box(ax, 33, 47, 34, 10, "Record Insertion & Indexing", "• Singly Linked List Append (Phase 1)\n• Binary Search Tree Insertion (Phase 2)\n• Push Action to Activity Stack (Undo)", bg="#DCFCE7", border="#15803D")

    draw_rounded_box(ax, 33, 31, 34, 10, "Claim Submission & Scheduling", "• Enqueue Claim Request (Phase 1 FIFO)\n• Push to Min-Heap Priority Queue (Phase 4)\n  (Priority: 1=High, 2=Med, 3=Low)", bg="#FCE7F3", border="#BE185D")

    draw_rounded_box(ax, 33, 16, 34, 9, "Claim Resolution & Verification", "• Dequeue Min-Heap Top Item\n• Match Student Proof & Handover\n• Move to ClaimDone & Update Log", bg="#FFFFFF", border="#1B365D")

    draw_rounded_box(ax, 38, 4, 24, 6, "END", "Record Audited & Archived", bg="#DBEAFE", border="#1D4ED8")

    # Connecting Arrows
    draw_arrow(ax, 50, 88, 50, 84)
    draw_arrow(ax, 43, 76, 27, 71, "Search Query")
    draw_arrow(ax, 57, 76, 72, 71, "Proximity Help")
    draw_arrow(ax, 27, 62, 45, 57)
    draw_arrow(ax, 72, 62, 55, 57)
    draw_arrow(ax, 50, 47, 50, 41, "Claims Arrive")
    draw_arrow(ax, 50, 31, 50, 25, "Scheduler Dispatch")
    draw_arrow(ax, 50, 16, 50, 10, "Finalized")

    out_path = os.path.join(doc_images, "flowchart_system_workflow.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated flowchart_system_workflow.png")

# -------------------------------------------------------------
# 5. DFD DIAGRAMS (LEVEL 0, LEVEL 1, LEVEL 2)
# -------------------------------------------------------------
def generate_dfd_diagrams():
    # --- DFD LEVEL 0 (Context Diagram) ---
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    ax.text(50, 94, "Data Flow Diagram (DFD) - Level 0 Context Diagram", ha='center', va='center',
            fontsize=14, fontweight='bold', color="#1B365D")
    ax.text(50, 90, "Interactions between External Campus Entities and the Central System", ha='center', va='center',
            fontsize=9, color="#64748B")

    # Central Process Circle/Box
    p0 = patches.Ellipse((50, 50), 32, 26, facecolor="#DBEAFE", edgecolor="#1D4ED8", linewidth=2, zorder=2)
    ax.add_patch(p0)
    ax.text(50, 53, "0.0", ha='center', va='center', fontsize=12, fontweight='bold', color="#1E40AF", zorder=3)
    ax.text(50, 48, "CAMPUS LOST & FOUND\nMANAGEMENT SYSTEM", ha='center', va='center', fontsize=10, fontweight='bold', color="#1B365D", zorder=3)

    # External Entities
    # Entity 1: Student / Claimant
    draw_rounded_box(ax, 5, 43, 20, 14, "Student / Claimant", "Reports Lost Items\nSubmits Ownership Claims\nSearches Found Catalog", bg="#FFFFFF", border="#1B365D", lw=1.5, sub_fontsize=7)
    # Entity 2: Finder / Reporter
    draw_rounded_box(ax, 50, 78, 22, 12, "Finder / Good Samaritan", "Surrenders Found Property\nSpecifies Drop Location", bg="#FFFFFF", border="#1B365D", lw=1.5, sub_fontsize=7)
    # Entity 3: System Administrator / Faculty
    draw_rounded_box(ax, 75, 43, 20, 14, "System Administrator", "Verifies Ownership Proof\nDispatches Claims via Heap\nPerforms Stack LIFO Undo", bg="#FFFFFF", border="#1B365D", lw=1.5, sub_fontsize=7)
    # Entity 4: Campus Security / Department
    draw_rounded_box(ax, 39, 10, 22, 12, "Campus Security Office", "Safekeeps High-Value Assets\nSigns Handover Vouchers", bg="#FFFFFF", border="#1B365D", lw=1.5, sub_fontsize=7)

    # Data Flow Arrows
    draw_arrow(ax, 25, 53, 34, 53, "Lost Item / Claim Data")
    draw_arrow(ax, 34, 47, 25, 47, "Search Matches & Status")

    draw_arrow(ax, 61, 78, 54, 63, "Found Item Details")
    draw_arrow(ax, 48, 63, 56, 78, "Receipt Acknowledgment")

    draw_arrow(ax, 75, 53, 66, 53, "Claim Resolution / Undo")
    draw_arrow(ax, 66, 47, 75, 47, "Priority Claims / Logs")

    draw_arrow(ax, 50, 37, 50, 22, "Handover Authorization")

    out_path = os.path.join(doc_images, "dfd_level0_context.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated dfd_level0_context.png")

    # --- DFD LEVEL 1 ---
    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    ax.text(50, 97, "Data Flow Diagram (DFD) - Level 1 Detailed Processes", ha='center', va='center',
            fontsize=14, fontweight='bold', color="#1B365D")

    # External Entities
    draw_rounded_box(ax, 3, 76, 18, 11, "Student Entity", "Submits loss report &\nclaims ownership", bg="#FFFFFF", border="#1B365D")
    draw_rounded_box(ax, 79, 76, 18, 11, "Admin Entity", "Dispatches claims &\naudits activities", bg="#FFFFFF", border="#1B365D")

    # Process 1.0: Authentication
    draw_rounded_box(ax, 40, 84, 20, 10, "1.0 User Auth", "Session & Role Validation\n(Student/Faculty/Admin)", bg="#EFF6FF", border="#2563EB")

    # Process 2.0: Item Registration
    draw_rounded_box(ax, 12, 54, 22, 11, "2.0 Item Registration", "Validate ID, Category,\nLocation & Priority Level", bg="#DCFCE7", border="#16A34A")

    # Process 3.0: DSA Search & Matching
    draw_rounded_box(ax, 40, 54, 20, 11, "3.0 Algorithmic Search", "• BST Search & Merge Sort\n• DP Levenshtein Smart Match\n• Campus Graph BFS Proximity", bg="#FEF3C7", border="#D97706", sub_fontsize=7)

    # Process 4.0: Claim Priority Scheduling
    draw_rounded_box(ax, 68, 54, 22, 11, "4.0 Claim Scheduling", "• FIFO Queue Enqueue\n• Min-Heap Priority Ordering\n• Claim Verification & Handover", bg="#FCE7F3", border="#DB2777", sub_fontsize=7)

    # Process 5.0: Audit Logging & Undo
    draw_rounded_box(ax, 40, 24, 20, 11, "5.0 Activity Audit", "• Push to LIFO Stack\n• Administrative Reversal\n• State Synchronization", bg="#E0E7FF", border="#4F46E5", sub_fontsize=7)

    # Data Stores (D1, D2, D3, D4)
    # Open-ended rectangle for data stores
    def draw_datastore(ax, x, y, w, h, id_str, name_str):
        ax.plot([x, x+w], [y+h, y+h], color="#1E293B", lw=1.5)
        ax.plot([x, x+w], [y, y], color="#1E293B", lw=1.5)
        ax.plot([x+w*0.22, x+w*0.22], [y, y+h], color="#1E293B", lw=1.2)
        ax.fill_between([x, x+w], [y, y], [y+h, y+h], color="#F1F5F9", zorder=1)
        ax.text(x+w*0.11, y+h/2, id_str, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#0F172A", zorder=2)
        ax.text(x+w*0.61, y+h/2, name_str, ha='center', va='center', fontsize=8, fontweight='semibold', color="#0F172A", zorder=2)

    draw_datastore(ax, 8, 8, 24, 8, "D1", "lost_items / found_items")
    draw_datastore(ax, 38, 8, 24, 8, "D2", "claim_processing / done")
    draw_datastore(ax, 68, 8, 24, 8, "D3", "activity_logs / Stack")

    # Connectors
    draw_arrow(ax, 12, 76, 20, 65, "Item Info")
    draw_arrow(ax, 23, 54, 20, 16, "Store Record")
    draw_arrow(ax, 34, 59, 40, 59, "Query Terms")
    draw_arrow(ax, 60, 59, 68, 59, "Match Identified")
    draw_arrow(ax, 79, 76, 79, 65, "Process Dispatch")
    draw_arrow(ax, 79, 54, 50, 16, "Update Claim Status")
    draw_arrow(ax, 50, 54, 50, 35, "Log Operation")
    draw_arrow(ax, 50, 24, 75, 16, "Write Audit Log")
    draw_arrow(ax, 85, 76, 55, 33, "Undo Request")

    out_path = os.path.join(doc_images, "dfd_level1_system.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated dfd_level1_system.png")

# -------------------------------------------------------------
# 6. RELATIONAL DATABASE SCHEMA & ER DIAGRAM
# -------------------------------------------------------------
def generate_db_schema_diagram():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    ax.text(50, 96, "Relational Database Schema & Entity Relationships", ha='center', va='center',
            fontsize=14, fontweight='bold', color="#1B365D")
    ax.text(50, 92.5, "Normalized MySQL Tables with Primary/Foreign Keys and Cardinalities", ha='center', va='center',
            fontsize=9, color="#64748B")

    def draw_schema_table(ax, x, y, w, h, table_name, columns, header_bg="#1E3A8A"):
        # Header
        hdr = patches.FancyBboxPatch((x, y + h - 5), w, 5, boxstyle="square,pad=0",
                                     facecolor=header_bg, edgecolor="#0F172A", linewidth=1.2, zorder=2)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 2.5, table_name, ha='center', va='center', fontsize=9, fontweight='bold', color="#FFFFFF", zorder=3)

        # Body
        body = patches.FancyBboxPatch((x, y), w, h - 5, boxstyle="square,pad=0",
                                      facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2, zorder=2)
        ax.add_patch(body)
        step = (h - 6) / len(columns)
        for idx, (col, ctype, key) in enumerate(columns):
            cy = y + h - 7 - (idx * step)
            k_color = "#DC2626" if "PK" in key else ("#2563EB" if "FK" in key else "#64748B")
            ax.text(x + 1.5, cy, col, ha='left', va='center', fontsize=7.5, fontweight='semibold', color="#1E293B", zorder=3)
            ax.text(x + w - 1.5, cy, f"{ctype} [{key}]", ha='right', va='center', fontsize=7, color=k_color, zorder=3)

    # Table 1: lost_items
    draw_schema_table(ax, 5, 52, 26, 32, "lost_items", [
        ("id", "INT AUTO_INC", "PK"),
        ("student_name", "VARCHAR(100)", ""),
        ("item_name", "VARCHAR(100)", ""),
        ("location", "VARCHAR(100)", ""),
        ("priority", "INT (1-3)", ""),
        ("is_resolved", "TINYINT(1)", ""),
        ("created_at", "DATETIME", "")
    ], header_bg="#1E40AF")

    # Table 2: found_items
    draw_schema_table(ax, 69, 52, 26, 32, "found_items", [
        ("id", "INT AUTO_INC", "PK"),
        ("student_name", "VARCHAR(100)", ""),
        ("item_name", "VARCHAR(100)", ""),
        ("location", "VARCHAR(100)", ""),
        ("priority", "INT (1-3)", ""),
        ("is_resolved", "TINYINT(1)", ""),
        ("created_at", "DATETIME", "")
    ], header_bg="#0D9488")

    # Table 3: claim_processing
    draw_schema_table(ax, 5, 8, 26, 32, "claim_processing", [
        ("id", "INT AUTO_INC", "PK"),
        ("student_name", "VARCHAR(100)", ""),
        ("item_name", "VARCHAR(100)", ""),
        ("location", "VARCHAR(100)", ""),
        ("priority", "INT", ""),
        ("lost_item_id", "INT", "FK"),
        ("created_at", "DATETIME", "")
    ], header_bg="#7C3AED")

    # Table 4: claim_done
    draw_schema_table(ax, 37, 8, 26, 32, "claim_done", [
        ("id", "INT AUTO_INC", "PK"),
        ("student_name", "VARCHAR(100)", ""),
        ("item_name", "VARCHAR(100)", ""),
        ("location", "VARCHAR(100)", ""),
        ("priority", "INT", ""),
        ("lost_item_id", "INT", "FK"),
        ("claimed_at", "DATETIME", "")
    ], header_bg="#16A34A")

    # Table 5: activity_logs
    draw_schema_table(ax, 69, 8, 26, 32, "activity_logs", [
        ("id", "INT AUTO_INC", "PK"),
        ("action_type", "VARCHAR(20)", ""),
        ("category", "VARCHAR(10)", ""),
        ("item_id", "INT", ""),
        ("description", "VARCHAR(200)", ""),
        ("created_at", "DATETIME", "")
    ], header_bg="#B45309")

    # Relationships (Arrows)
    draw_arrow(ax, 18, 52, 18, 40, "1 : N (CASCADE)", color="#7C3AED")
    draw_arrow(ax, 28, 52, 45, 40, "1 : 1 (SET_NULL)", color="#16A34A")

    out_path = os.path.join(doc_images, "db_er_diagram.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated db_er_diagram.png")

# -------------------------------------------------------------
# 7. PHASE-SPECIFIC ALGORITHMIC FLOWCHARTS
# -------------------------------------------------------------
def generate_phase_flowcharts():
    # --- PHASE 2: BST INSERTION & SEARCH FLOWCHART ---
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    ax.text(50, 96, "Phase 2: Binary Search Tree (BST) Lookup & Deletion Algorithm", ha='center', va='center',
            fontsize=13, fontweight='bold', color="#1B365D")

    draw_rounded_box(ax, 38, 86, 24, 7, "Start BST Search", "Input: Target ID, Root", bg="#EFF6FF", border="#2563EB")
    draw_rounded_box(ax, 35, 71, 30, 8, "Current == NULL?", "Decision Node", bg="#FEF3C7", border="#D97706")
    draw_rounded_box(ax, 72, 71, 22, 8, "Item Not Found", "Return False", bg="#FEE2E2", border="#DC2626")

    draw_rounded_box(ax, 33, 53, 34, 9, "Target == Current.Data?", "Equality Evaluation", bg="#FEF3C7", border="#D97706")
    draw_rounded_box(ax, 72, 53, 22, 9, "Match Confirmed!", "Return Node Record", bg="#DCFCE7", border="#16A34A")

    draw_rounded_box(ax, 33, 34, 34, 9, "Target < Current.Data?", "Branching Decision", bg="#FEF3C7", border="#D97706")

    draw_rounded_box(ax, 10, 18, 32, 9, "Traverse Left Branch", "Current = Current.Left", bg="#E0E7FF", border="#4338CA")
    draw_rounded_box(ax, 58, 18, 32, 9, "Traverse Right Branch", "Current = Current.Right", bg="#E0E7FF", border="#4338CA")

    draw_arrow(ax, 50, 86, 50, 79)
    draw_arrow(ax, 65, 75, 72, 75, "Yes")
    draw_arrow(ax, 50, 71, 50, 62, "No")
    draw_arrow(ax, 67, 57, 72, 57, "Yes")
    draw_arrow(ax, 50, 53, 50, 43, "No")
    draw_arrow(ax, 33, 38, 26, 27, "Yes (Go Left)")
    draw_arrow(ax, 67, 38, 74, 27, "No (Go Right)")
    draw_arrow(ax, 26, 18, 45, 68, "Loop", style="->")
    draw_arrow(ax, 74, 18, 55, 68, "Loop", style="->")

    out_path = os.path.join(doc_images, "flowchart_phase2_bst.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated flowchart_phase2_bst.png")

    # --- PHASE 2: CAMPUS GRAPH BFS FLOWCHART ---
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    ax.text(50, 96, "Phase 2: Campus Adjacency Graph Breadth-First Search (BFS)", ha='center', va='center',
            fontsize=13, fontweight='bold', color="#1B365D")

    draw_rounded_box(ax, 36, 86, 28, 7, "Initialize BFS Traversal", "Queue = [Start], Visited = {Start}", bg="#EFF6FF", border="#2563EB")
    draw_rounded_box(ax, 35, 70, 30, 8, "Is Queue Empty?", "Decision Loop", bg="#FEF3C7", border="#D97706")
    draw_rounded_box(ax, 72, 70, 22, 8, "Traversal Complete", "Return Search Order List", bg="#DCFCE7", border="#16A34A")

    draw_rounded_box(ax, 33, 52, 34, 9, "Dequeue Vertex: V = pop(0)", "Append V to Search Order", bg="#FFFFFF", border="#1B365D")
    draw_rounded_box(ax, 33, 33, 34, 10, "Inspect Neighbors of V in Graph", "Iterate over Adjacency List\nGraph[V] = [N1, N2, ...]", bg="#E0E7FF", border="#4338CA")

    draw_rounded_box(ax, 33, 15, 34, 10, "Neighbor in Visited Set?", "If Not Visited: Add to Visited\nEnqueue Neighbor: queue.append(N)", bg="#FEF3C7", border="#D97706")

    draw_arrow(ax, 50, 86, 50, 78)
    draw_arrow(ax, 65, 74, 72, 74, "Yes")
    draw_arrow(ax, 50, 70, 50, 61, "No")
    draw_arrow(ax, 50, 52, 50, 43)
    draw_arrow(ax, 50, 33, 50, 25)
    draw_arrow(ax, 33, 20, 15, 74, "Loop next vertex", style="->")
    draw_arrow(ax, 15, 74, 35, 74)

    out_path = os.path.join(doc_images, "flowchart_phase2_bfs_graph.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated flowchart_phase2_bfs_graph.png")

    # --- PHASE 3: LINKED LIST MERGE SORT FLOWCHART ---
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    ax.text(50, 96, "Phase 3: Linked List Merge Sort - O(n log n) Divide & Conquer", ha='center', va='center',
            fontsize=13, fontweight='bold', color="#1B365D")

    draw_rounded_box(ax, 35, 86, 30, 7, "merge_sort(head)", "Base Case: head is None or head.next is None", bg="#EFF6FF", border="#2563EB")
    draw_rounded_box(ax, 72, 86, 22, 7, "Return head", "List already sorted", bg="#DCFCE7", border="#16A34A")

    draw_rounded_box(ax, 32, 69, 36, 10, "Find Middle Node (Two Pointers)", "Slow pointer (1 step), Fast pointer (2 steps)\nWhen Fast reaches end, Slow is at middle", bg="#FEF3C7", border="#D97706")

    draw_rounded_box(ax, 32, 51, 36, 10, "Sever Link & Divide List", "next_to_middle = middle.next\nmiddle.next = None (Two distinct lists)", bg="#FEE2E2", border="#DC2626")

    draw_rounded_box(ax, 20, 32, 28, 10, "Recursive Sort Left", "left = merge_sort(head)", bg="#E0E7FF", border="#4338CA")
    draw_rounded_box(ax, 52, 32, 28, 10, "Recursive Sort Right", "right = merge_sort(next_to_middle)", bg="#E0E7FF", border="#4338CA")

    draw_rounded_box(ax, 32, 12, 36, 11, "In-Place Sorted Merge", "sorted_merge(left, right)\nCompare left.id <= right.id\nRe-link pointers without array copying", bg="#DCFCE7", border="#16A34A")

    draw_arrow(ax, 50, 86, 50, 79)
    draw_arrow(ax, 65, 89.5, 72, 89.5, "Base Case")
    draw_arrow(ax, 50, 69, 50, 61)
    draw_arrow(ax, 42, 51, 34, 42)
    draw_arrow(ax, 58, 51, 66, 42)
    draw_arrow(ax, 34, 32, 43, 23)
    draw_arrow(ax, 66, 32, 57, 23)

    out_path = os.path.join(doc_images, "flowchart_phase3_merge_sort.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated flowchart_phase3_merge_sort.png")

    # --- PHASE 4: DYNAMIC PROGRAMMING LEVENSHTEIN DISTANCE ---
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    ax.text(50, 96, "Phase 4: Dynamic Programming Levenshtein Distance (Smart Match)", ha='center', va='center',
            fontsize=13, fontweight='bold', color="#1B365D")

    draw_rounded_box(ax, 30, 86, 40, 7, "Initialize 2D Matrix DP[m+1][n+1]", "m = len(str1), n = len(str2)", bg="#EFF6FF", border="#2563EB")
    draw_rounded_box(ax, 30, 71, 40, 8, "Set Base Conditions (i=0 or j=0)", "DP[i][0] = i (Deletions), DP[0][j] = j (Insertions)", bg="#FEF3C7", border="#D97706")

    draw_rounded_box(ax, 28, 53, 44, 10, "Iterate Over Characters: i=1..m, j=1..n", "Are characters equal: str1[i-1] == str2[j-1]?", bg="#FFFFFF", border="#1B365D")

    draw_rounded_box(ax, 8, 34, 38, 10, "Cost is 0 (No Operation Needed)", "DP[i][j] = DP[i-1][j-1]\nCopy diagonal previous state", bg="#DCFCE7", border="#16A34A")

    draw_rounded_box(ax, 54, 34, 38, 10, "Cost is 1 + min(Operations)", "1 + min(DP[i][j-1], DP[i-1][j], DP[i-1][j-1])\n(Insert, Delete, or Substitute)", bg="#FEE2E2", border="#DC2626")

    draw_rounded_box(ax, 28, 14, 44, 11, "Evaluation & Smart Match Threshold", "Total Distance = DP[m][n]\nIf Distance <= 4: Output 'Did you mean: [Item]?'\nElse: No close match found", bg="#E0E7FF", border="#4338CA")

    draw_arrow(ax, 50, 86, 50, 79)
    draw_arrow(ax, 50, 71, 50, 63)
    draw_arrow(ax, 40, 53, 27, 44, "Equal (Cost 0)")
    draw_arrow(ax, 60, 53, 73, 44, "Mismatch (Cost 1)")
    draw_arrow(ax, 27, 34, 42, 25)
    draw_arrow(ax, 73, 34, 58, 25)

    out_path = os.path.join(doc_images, "flowchart_phase4_levenshtein.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated flowchart_phase4_levenshtein.png")

# -------------------------------------------------------------
# 8. DESKTOP GUI MOCKUP / LAYOUT
# -------------------------------------------------------------
def generate_desktop_ui_layout():
    fig, ax = plt.subplots(figsize=(8, 10.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#E2E8F0')
    ax.set_facecolor('#E2E8F0')

    # Window Frame
    win = patches.FancyBboxPatch((5, 3), 90, 94, boxstyle="round,pad=0.2,rounding_size=1.5",
                                facecolor="#F8FAFC", edgecolor="#475569", linewidth=2, zorder=2)
    ax.add_patch(win)

    # Title Bar
    title_bar = patches.FancyBboxPatch((5, 93), 90, 4, boxstyle="square,pad=0",
                                      facecolor="#1E293B", edgecolor="#1E293B", linewidth=1, zorder=3)
    ax.add_patch(title_bar)
    ax.text(8, 95, "Campus Lost & Found System (DSA Engine)", fontsize=9, fontweight='bold', color="#FFFFFF", zorder=4)
    ax.text(90, 95, "―  □  ✕", fontsize=9, fontweight='bold', color="#94A3B8", zorder=4)

    # Section 1: Add New Item
    ax.text(50, 89, "--- Add New Item ---", ha='center', fontsize=9.5, fontweight='bold', color="#0F172A", zorder=4)
    y_pos = 85
    for label, val in [("Item ID:", "101"), ("Item Name:", "Calculater"), ("Type (Lost/Found):", "Lost"), ("Location:", "Library")]:
        ax.text(20, y_pos, label, ha='right', fontsize=8, color="#334155", zorder=4)
        box = patches.Rectangle((22, y_pos-1.5), 56, 3, facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=1, zorder=3)
        ax.add_patch(box)
        ax.text(24, y_pos, val, ha='left', va='center', fontsize=7.5, color="#0F172A", zorder=4)
        y_pos -= 4.2

    draw_rounded_box(ax, 22, 67, 26, 4, "Add Item", bg="#BAE6FD", border="#0284C7", title_fontsize=8)
    draw_rounded_box(ax, 52, 67, 26, 4, "Find Nearby (BFS)", bg="#E9D5FF", border="#9333EA", title_fontsize=8)

    # Section 2: Manage Claims
    ax.text(50, 62, "--- Manage Claims ---", ha='center', fontsize=9.5, fontweight='bold', color="#0F172A", zorder=4)
    ax.text(20, 58, "Claimant Name:", ha='right', fontsize=8, color="#334155", zorder=4)
    ax.add_patch(patches.Rectangle((22, 56.5), 56, 3, facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=1, zorder=3))
    ax.text(24, 58, "Kurian Robert (26MCAC28)", ha='left', va='center', fontsize=7.5, color="#0F172A", zorder=4)

    ax.text(20, 53, "Target Item ID:", ha='right', fontsize=8, color="#334155", zorder=4)
    ax.add_patch(patches.Rectangle((22, 51.5), 56, 3, facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=1, zorder=3))
    ax.text(24, 53, "101", ha='left', va='center', fontsize=7.5, color="#0F172A", zorder=4)

    draw_rounded_box(ax, 22, 46, 26, 4, "Enqueue Claim", bg="#BBF7D0", border="#16A34A", title_fontsize=8)
    draw_rounded_box(ax, 52, 46, 26, 4, "Process Claim", bg="#FECDD3", border="#E11D48", title_fontsize=8)

    # Section 3: BST Search & Delete
    ax.text(50, 41, "--- Search & Delete (BST) ---", ha='center', fontsize=9.5, fontweight='bold', color="#0F172A", zorder=4)
    ax.add_patch(patches.Rectangle((32, 36.5), 36, 3, facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=1, zorder=3))
    ax.text(34, 38, "101", ha='left', va='center', fontsize=7.5, color="#0F172A", zorder=4)

    draw_rounded_box(ax, 22, 31, 26, 4, "Search ID", bg="#FEF08A", border="#CA8A04", title_fontsize=8)
    draw_rounded_box(ax, 52, 31, 26, 4, "Delete Item", bg="#FFEDD5", border="#EA580C", title_fontsize=8)

    # Section 4: Smart Match (DP)
    ax.text(50, 26, "--- Smart Match (Levenshtein) ---", ha='center', fontsize=9.5, fontweight='bold', color="#0F172A", zorder=4)
    ax.add_patch(patches.Rectangle((32, 21.5), 36, 3, facecolor="#FFFFFF", edgecolor="#CBD5E1", lw=1, zorder=3))
    ax.text(34, 23, "Calculater", ha='left', va='center', fontsize=7.5, color="#0F172A", zorder=4)
    draw_rounded_box(ax, 35, 16, 30, 4, "Fuzzy Search Name", bg="#CFFAFE", border="#0891B2", title_fontsize=8)

    # Terminal Output Box
    term_box = patches.Rectangle((12, 5), 76, 9.5, facecolor="#0F172A", edgecolor="#334155", lw=1.2, zorder=3)
    ax.add_patch(term_box)
    ax.text(14, 12.5, "CONSOLE OUTPUT / ALGORITHMIC RESULTS:", fontsize=6.5, fontweight='bold', color="#38BDF8", zorder=4)
    ax.text(14, 10.2, "> BFS from Library: ['Library', 'Main Block', 'Computer Lab', 'Cafeteria']", fontsize=6, color="#4ADE80", zorder=4)
    ax.text(14, 8.2, "> Smart Match: Did you mean: 'Calculator'? (Edit distance: 1)", fontsize=6, color="#FBBF24", zorder=4)
    ax.text(14, 6.2, "> BST Search(101): Node Found! Inorder: [101, 102, 105, 108]", fontsize=6, color="#E2E8F0", zorder=4)

    out_path = os.path.join(doc_images, "ui_desktop_mockup.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Generated ui_desktop_mockup.png")

if __name__ == "__main__":
    print("=== Generating Visual Assets for Campus Lost & Found System ===")
    capture_web_screenshots()
    generate_system_architecture()
    generate_master_flowchart()
    generate_dfd_diagrams()
    generate_db_schema_diagram()
    generate_phase_flowcharts()
    generate_desktop_ui_layout()
    print("=== All Visual Assets Generated Successfully! ===")
