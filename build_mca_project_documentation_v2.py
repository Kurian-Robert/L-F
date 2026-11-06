import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_mca_documentation():
    doc = docx.Document()

    # 1. Page Setup: Standard A4 Margins (1.0 inch all around) - Matching University Template
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)   # A4 Width (210 mm)
        section.page_height = Inches(11.69) # A4 Height (297 mm)

    # 2. Color Palette: Standard Academic Formal Palette (Black / Dark Slate / Subtle Grays)
    COLOR_TEXT = RGBColor(17, 24, 39)         # Deep Charcoal/Black #111827
    COLOR_MUTED = RGBColor(75, 85, 99)        # Academic Gray #4B5563
    COLOR_HEADING = RGBColor(15, 23, 42)      # Primary Dark #0F172A
    COLOR_SUBHEADING = RGBColor(30, 41, 59)   # Slate 800 #1E293B
    
    HEX_BORDER = "94A3B8"                     # Standard thin gray border #94A3B8
    HEX_LIGHT_BORDER = "CBD5E1"               # Subtle border #CBD5E1
    HEX_TABLE_HDR = "F1F5F9"                  # Neutral academic light gray #F1F5F9
    HEX_TABLE_ALT = "F8FAFC"                  # Alternating row fill #F8FAFC
    HEX_CODE_BG = "F8FAFC"                    # Code background
    HEX_NOTE_BG = "F1F5F9"                    # Note background

    def set_cell_shading(cell, color_hex):
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shading)

    def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def add_h1(text, page_break=True):
        if page_break:
            doc.add_page_break()
        h = doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.LEFT
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = COLOR_HEADING
        return h

    def add_h2(text):
        h = doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.LEFT
        h.paragraph_format.space_before = Pt(9)
        h.paragraph_format.space_after = Pt(3)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_SUBHEADING
        return h

    def add_h3(text):
        h = doc.add_paragraph()
        h.alignment = WD_ALIGN_PARAGRAPH.LEFT
        h.paragraph_format.space_before = Pt(7)
        h.paragraph_format.space_after = Pt(2)
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = COLOR_HEADING
        return h

    def add_p(text, space_after=3.8):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.color.rgb = COLOR_TEXT
        return p

    def add_bullet(bold_prefix, text, space_after=2.5):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        
        run_bold = p.add_run(bold_prefix)
        run_bold.font.name = "Times New Roman"
        run_bold.font.size = Pt(11)
        run_bold.font.bold = True
        run_bold.font.color.rgb = COLOR_HEADING

        run_text = p.add_run(" " + text)
        run_text.font.name = "Times New Roman"
        run_text.font.size = Pt(11)
        run_text.font.color.rgb = COLOR_TEXT
        return p

    def add_image_figure(image_path, caption_text, width_inches=4.8):
        if not os.path.exists(image_path):
            print(f"Warning: Image {image_path} does not exist!")
            return

        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(image_path, width=Inches(width_inches))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(5)
        p_cap.paragraph_format.keep_with_next = True
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = "Times New Roman"
        run_cap.font.size = Pt(9)
        run_cap.font.bold = True
        run_cap.font.italic = True
        run_cap.font.color.rgb = COLOR_MUTED

    def add_code_block(file_title, code_string, max_lines=None):
        lines = code_string.strip().splitlines()
        if max_lines and len(lines) > max_lines:
            code_display = "\n".join(lines[:max_lines]) + f"\n\n# ... [Artifact continued: {len(lines) - max_lines} operational lines in source repository] ..."
        else:
            code_display = "\n".join(lines)

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_shading(cell, HEX_CODE_BG)
        set_cell_margins(cell, top=60, bottom=60, left=90, right=90)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'''
            <w:tcBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_LIGHT_BORDER}"/>
                <w:left w:val="single" w:sz="14" w:space="0" w:color="{COLOR_SUBHEADING}"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_LIGHT_BORDER}"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_LIGHT_BORDER}"/>
            </w:tcBorders>
        ''')
        tcPr.append(borders)

        cp = cell.paragraphs[0]
        cp.paragraph_format.space_before = Pt(0)
        cp.paragraph_format.space_after = Pt(2)
        r_head = cp.add_run(f"Source Code Artifact: {file_title}\n")
        r_head.font.name = "Consolas"
        r_head.font.size = Pt(8.5)
        r_head.font.bold = True
        r_head.font.color.rgb = COLOR_HEADING

        r_code = cp.add_run(code_display)
        r_code.font.name = "Consolas"
        r_code.font.size = Pt(7.8)
        r_code.font.color.rgb = COLOR_TEXT

        p_spacer = doc.add_paragraph()
        p_spacer.paragraph_format.space_before = Pt(0)
        p_spacer.paragraph_format.space_after = Pt(3)

    def add_table_data(headers, data_rows, col_widths=None, col_alignments=None):
        """Creates a standard academic normal-type table with clean neutral headers and subtle borders"""
        table = doc.add_table(rows=len(data_rows) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Header Row
        hdr_cells = table.rows[0].cells
        for i, h_text in enumerate(headers):
            hdr_cells[i].text = h_text
            set_cell_shading(hdr_cells[i], HEX_TABLE_HDR)
            set_cell_margins(hdr_cells[i], top=65, bottom=65, left=80, right=80)
            p = hdr_cells[i].paragraphs[0]
            align = col_alignments[i] if col_alignments else WD_ALIGN_PARAGRAPH.CENTER
            p.alignment = align
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9.5)
                r.font.bold = True
                r.font.color.rgb = COLOR_HEADING

        # Data Rows
        for r_idx, row in enumerate(data_rows):
            row_cells = table.rows[r_idx + 1].cells
            shd_hex = HEX_TABLE_ALT if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row):
                row_cells[c_idx].text = str(val)
                set_cell_shading(row_cells[c_idx], shd_hex)
                set_cell_margins(row_cells[c_idx], top=45, bottom=45, left=70, right=70)
                p = row_cells[c_idx].paragraphs[0]
                align = col_alignments[c_idx] if col_alignments else WD_ALIGN_PARAGRAPH.LEFT
                p.alignment = align
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(8.8)
                    r.font.color.rgb = COLOR_TEXT

        # Standard clean thin borders
        for r in table.rows:
            for c in r.cells:
                tcPr = c._tc.get_or_add_tcPr()
                borders = parse_xml(f'''
                    <w:tcBorders {nsdecls("w")}>
                        <w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
                        <w:left w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
                        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
                        <w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
                    </w:tcBorders>
                ''')
                tcPr.append(borders)

        if col_widths:
            for row in table.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Inches(w)

        p_spacer = doc.add_paragraph()
        p_spacer.paragraph_format.space_before = Pt(0)
        p_spacer.paragraph_format.space_after = Pt(4)

    doc_img_dir = os.path.abspath("doc_images")
    logo_path = os.path.join(doc_img_dir, "kristu_jayanti_logo.jpeg")

    # =========================================================
    # PAGE 1: TITLE PAGE (OFFICIAL KRISTU JAYANTI UNIVERSITY FORMAT)
    # =========================================================
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(28)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(4.1))

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(12)
    p_rep.paragraph_format.space_after = Pt(8)
    r1 = p_rep.add_run("Project-based Practical Report on\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(15)
    r1.font.bold = False
    r1.font.color.rgb = COLOR_TEXT

    r2 = p_rep.add_run("“Campus Lost and Found Management System”")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(16)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_HEADING

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(24)
    p_sub.paragraph_format.space_after = Pt(24)
    r3 = p_sub.add_run("Submitted in partial fulfilment of the requirements for\n“Data Structures and Algorithms” for the 1st Semester\n\nMaster of Computer Applications (MCA)")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(12.5)
    r3.font.bold = False
    r3.font.color.rgb = COLOR_TEXT

    p_by_label = doc.add_paragraph()
    p_by_label.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by_label.paragraph_format.space_before = Pt(16)
    p_by_label.paragraph_format.space_after = Pt(6)
    r4 = p_by_label.add_run("Submitted by")
    r4.font.name = "Times New Roman"
    r4.font.size = Pt(12)
    r4.font.bold = False
    r4.font.color.rgb = COLOR_TEXT

    p_by_name = doc.add_paragraph()
    p_by_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by_name.paragraph_format.space_after = Pt(28)
    r5 = p_by_name.add_run("<KURIAN ROBERT>          <26MCAC28>")
    r5.font.name = "Times New Roman"
    r5.font.size = Pt(13)
    r5.font.bold = True
    r5.font.color.rgb = COLOR_HEADING

    p_guide_label = doc.add_paragraph()
    p_guide_label.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide_label.paragraph_format.space_after = Pt(6)
    r6 = p_guide_label.add_run("Under the guidance of")
    r6.font.name = "Times New Roman"
    r6.font.size = Pt(12)
    r6.font.bold = False
    r6.font.color.rgb = COLOR_TEXT

    p_guide_name = doc.add_paragraph()
    p_guide_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide_name.paragraph_format.space_after = Pt(10)
    r7 = p_guide_name.add_run("<Dr.SubramaniaKumar>")
    r7.font.name = "Times New Roman"
    r7.font.size = Pt(13)
    r7.font.bold = True
    r7.font.color.rgb = COLOR_HEADING

    # =========================================================
    # PAGE 2: CERTIFICATE OF AUTHENTICITY & CANDIDATE DECLARATION
    # =========================================================
    doc.add_page_break()
    h_cert = doc.add_paragraph()
    h_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h_cert.paragraph_format.space_before = Pt(20)
    h_cert.paragraph_format.space_after = Pt(16)
    r_c = h_cert.add_run("CERTIFICATE")
    r_c.font.name = "Times New Roman"
    r_c.font.size = Pt(16)
    r_c.font.bold = True
    r_c.font.color.rgb = COLOR_HEADING

    add_p("This is to certify that the project-based practical report entitled “Campus Lost and Found Management System with Priority Claim Scheduling” is a bona fide record of work carried out by KURIAN ROBERT (Reg. No. 26MCAC28) in partial fulfilment of the requirements for the award of the degree of Master of Computer Applications (MCA) for the 1st Semester in the course “Data Structures and Algorithms” during the academic year 2025–2026.")
    add_p("The project has been executed under my supervision and guidance, satisfying the prescribed academic curriculum guidelines. The algorithms, data structure designs, and software implementations documented herein are authentic and represent the candidate's original technical contribution.")
    
    # Signature Table
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(24)
    p_sig.paragraph_format.space_after = Pt(8)
    
    sig_data = [
        ["\n\n___________________________\nDr. Subramania Kumar\nFaculty Guide\nDepartment of Computer Science",
         "\n\n___________________________\nHead of the Department\nDepartment of Computer Science\nKristu Jayanti University"]
    ]
    add_table_data(["FACULTY GUIDE", "HEAD OF DEPARTMENT"], sig_data, [3.2, 3.2], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER])

    h_decl = doc.add_paragraph()
    h_decl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h_decl.paragraph_format.space_before = Pt(20)
    h_decl.paragraph_format.space_after = Pt(10)
    r_d = h_decl.add_run("DECLARATION")
    r_d.font.name = "Times New Roman"
    r_d.font.size = Pt(14)
    r_d.font.bold = True
    r_d.font.color.rgb = COLOR_HEADING

    add_p("I, KURIAN ROBERT, hereby declare that the practical project report entitled “Campus Lost and Found Management System with Priority Claim Scheduling” submitted to Kristu Jayanti University, Bengaluru, is an original work done by me under the supervision of Dr. Subramania Kumar. This work has not formed the basis for the award of any degree, diploma, or fellowship in this or any other institution.")
    
    p_cand = doc.add_paragraph()
    p_cand.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_cand.paragraph_format.space_before = Pt(18)
    p_cand.paragraph_format.space_after = Pt(0)
    r_cand = p_cand.add_run("KURIAN ROBERT\nReg. No: 26MCAC28\nBengaluru\nDate: 27-10-2026")
    r_cand.font.name = "Times New Roman"
    r_cand.font.size = Pt(10.5)
    r_cand.font.bold = True
    r_cand.font.color.rgb = COLOR_TEXT

    # =========================================================
    # PAGES 3, 4, 5: CONTENTS TABLE
    # =========================================================
    doc.add_page_break()
    h_cnt = doc.add_paragraph()
    h_cnt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h_cnt.paragraph_format.space_before = Pt(10)
    h_cnt.paragraph_format.space_after = Pt(8)
    r_cnt = h_cnt.add_run("Contents")
    r_cnt.font.name = "Times New Roman"
    r_cnt.font.size = Pt(16)
    r_cnt.font.bold = True
    r_cnt.font.color.rgb = COLOR_HEADING

    mca_toc = [
        ("1. Title of the Project", "6"),
        ("2. Introduction", "7"),
        ("   2.1 Operational Context & Existing System Challenges", "7"),
        ("   2.2 Problem Formulation & System Comparison", "8"),
        ("3. Objective of the Project", "9"),
        ("4. Scope of the Project", "10"),
        ("5. Software Specifications", "11"),
        ("6. Workflow of the Project", "12"),
        ("   6.1 Sequential Workflow Nodes & Execution Pipeline", "12"),
        ("   6.2 Layered System Architecture Diagram (Figure 6.1)", "13"),
        ("   6.3 Master Workflow Flowchart (Figure 6.2)", "14"),
        ("7. Modules of the Project - Phase-wise Explanation of Design & Execution", "15"),
        ("   7.1 Phase 1: Linear Data Structures Module (Linked List, Stack, Queue)", "15"),
        ("   7.2 Phase 2: Hierarchical & Graph Structures Module (BST & Campus BFS)", "16"),
        ("       7.2.1 Binary Search Tree Lookup & Deletion Flowchart (Figure 7.1)", "17"),
        ("       7.2.2 Campus Adjacency Graph BFS Proximity Flowchart (Figure 7.2)", "18"),
        ("   7.3 Phase 3: Searching & Sorting Operations Module (Merge Sort O(n log n))", "18"),
        ("       7.3.1 Linked List Merge Sort Division & In-Place Merge Flowchart (Figure 7.3)", "19"),
        ("   7.4 Phase 4: Algorithmic Problem Solving Module (DP Levenshtein & Min-Heap)", "19"),
        ("       7.4.1 Dynamic Programming Levenshtein Distance Matrix Flowchart (Figure 7.4)", "20"),
        ("   7.5 Comprehensive Algorithmic Complexity & Space-Time Trade-Offs (Table 7.1)", "21"),
        ("   7.6 Data Flow Diagram (DFD) Models", "21"),
        ("       7.6.1 DFD Level 0: Context Diagram (Figure 7.5)", "22"),
        ("       7.6.2 DFD Level 1: Subsystem Process Decomposition (Figure 7.6)", "23"),
        ("   7.7 Database Design, Relational Schema & Normalization Analysis (3NF)", "23"),
        ("       7.7.1 Relational Database Schema & ER Diagram (Figure 7.7)", "23"),
        ("       7.7.2 Table Definitions (lost_items, found_items, claims, activity)", "24"),
        ("       7.7.3 Formal Database Normalization Proof (1NF, 2NF, 3NF)", "26"),
        ("8. Source Code (Functional Code Structure)", "27"),
        ("   8.1 Data Structures Core Engine (campuslostfound)", "27"),
        ("   8.2 Desktop GUI Interface Implementation (main_ui.py)", "37"),
        ("   8.3 Django Web Application Controllers (models.py, views.py, urls.py)", "39"),
        ("   8.4 Front-End Presentation Templates (index.html, login.html)", "46"),
        ("9. Features of the Project", "57"),
        ("   9.1 System Features & Verification Test Cases (Table 9.1)", "57"),
        ("   9.2 User Interface Walkthrough & Live System Screenshots", "58"),
        ("       9.2.1 Web Dashboard & Priority Queue Interface (Figure 9.1)", "59"),
        ("       9.2.2 Authentication & Location Search Interfaces (Figures 9.2 & 9.3)", "60"),
        ("       9.2.3 Desktop Tkinter Demonstrator Layout (Figure 9.4)", "61"),
        ("10. Future Enhancements", "62"),
        ("11. Conclusion & Technical Defense", "63"),
        ("   11.1 Project Conclusion & Core Deliverables", "63"),
        ("   11.2 Viva-Voce Architectural Defense Q&A", "63"),
        ("   11.3 Academic References & Bibliography", "63")
    ]
    add_table_data(["Module / Chapter Section Title", "Page"], mca_toc, [5.3, 1.1], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER])

    # =========================================================
    # PAGE 6: 1. TITLE OF THE PROJECT
    # =========================================================
    add_h1("1. Title of the Project")
    add_h2("Campus Lost and Found Management System with Priority Claim Scheduling (CLFS-PCS)")
    add_p("The project is entitled 'Campus Lost and Found Management System with Priority Claim Scheduling'. It represents a full-stack Data Structures and Algorithms (DSA) software solution engineered to address real-world property tracking and retrieval challenges within university campus environments.")
    add_p("The software architecture bridges academic algorithm design with modern software engineering by integrating two complementary execution environments:")
    add_bullet("1. Standalone Core DSA Engine (`campuslostfound`):", "A pure Python implementation of foundational data structures developed entirely without external third-party collections. It encapsulates custom pointer-managed Singly Linked Lists, Last-In-First-Out (LIFO) Activity Stacks for administrative undo, First-In-First-Out (FIFO) Claim Queues, a Binary Search Tree (BST) for logarithmic key lookups, an undirected Campus Adjacency Graph evaluated through Breadth-First Search (BFS), an in-place Linked List Merge Sort, and a Wagner-Fischer Dynamic Programming Levenshtein Distance matrix for fuzzy matching.")
    add_bullet("2. Enterprise Web Application (`scheduler`):", "A full-featured web platform built using the Django framework and backed by a MySQL 8.0 relational database. It features secure session authentication, role-based controls for students, faculty, and administrative officers, and a Greedy Min-Heap Priority Queue (`heapq`) that automatically orders claims based on urgency level, ensuring time-critical articles like examination hall tickets and identification cards are resolved first.")
    add_bullet("3. Desktop Demonstrator (`main_ui.py`):", "A native desktop graphical user interface developed with Tkinter that allows students and instructors to interactively visualize and test memory structures, run BFS location expansions, search the BST, and verify in-memory sort routines in real time.")

    # =========================================================
    # PAGE 7: 2. INTRODUCTION
    # =========================================================
    add_h1("2. Introduction")
    add_p("Across higher education campuses with multiple academic blocks, central libraries, computing centers, cafeterias, and athletic facilities, students and faculty frequently misplace personal belongings. These items range from essential credentials—such as university smart cards, examination hall tickets, room keys, and prescription eyewear—to everyday academic tools including scientific calculators, course textbooks, lab records, backpacks, and water bottles.")
    add_p("Historically, university property tracking has relied on physical paper logbooks kept at security gates or informal word-of-mouth inquiries. In practice, these manual approaches create severe operational bottlenecks:")
    add_bullet("Manual Logbook Overhead:", "Paper registers record items sequentially by date. Searching for an item requires scanning through hundreds of handwritten rows, which is slow, labor-intensive, and prone to human error.")
    add_bullet("Zero Support for Typographical Errors:", "Standard manual searches and simple database string lookups require exact spelling matches. If a student searches for 'calclator', 'airpod', or 'idcard', conventional systems return no results even if the item is physically present in the storage locker.")
    add_bullet("Lack of Spatial Campus Awareness:", "Campuses consist of interconnected buildings. An article misplaced in the Central Library is often carried to or discovered in adjacent blocks such as the Computer Lab or Main Block. Traditional tracking records locations as isolated text strings without any spatial context.")
    add_bullet("Unranked Claim Processing:", "Conventional systems process claims on a simple first-come-first-served basis. Consequently, a student needing an urgent examination hall ticket or room key must wait behind routine claims for common utility items.")
    add_p("The Campus Lost and Found Management System addresses these challenges by replacing manual paper workflows with an algorithmically optimized digital repository. By combining linear structures, hierarchical search trees, topological graph traversals, and dynamic programming with enterprise web technologies, the platform provides automated, reliable, and fair property management.")

    # =========================================================
    # PAGE 8: 2.2 PROBLEM FORMULATION & SYSTEM COMPARISON
    # =========================================================
    add_h1("2.2 Problem Formulation & System Comparison", page_break=True)
    add_p("To clearly distinguish the advantages of the proposed algorithmically driven platform over traditional approaches, the operational characteristics of manual security logbooks, unindexed communication channels (such as notice boards and group chats), and the proposed automated DSA system are evaluated below.")
    
    comp_headers = ["Evaluation Metric", "Manual Security Registers", "Social / Notice Board Posts", "Proposed CLFS-PCS Platform"]
    comp_rows = [
        ["Record Ingestion", "Handwritten physical logbook entry; slow and non-standardized", "Unstructured text messages; easily buried or deleted", "Structured web and desktop forms with field validation"],
        ["Search & Retrieval", "Linear manual page scan: O(n) worst-case time (15–30 min)", "Keyword search limited to exact post text; unindexed", "Dual mode: O(log n) BST search and DP typo-tolerant matching"],
        ["Spelling Error Handling", "Impossible; requires human visual scanning of all pages", "None; misspellings cause searches to fail completely", "2D Levenshtein Matrix automatically suggests close matches (dist <= 4)"],
        ["Campus Proximity", "None; locations are isolated text entries", "None; no spatial or geographic relationship tracked", "Graph BFS traverses connected buildings to guide physical searches"],
        ["Claim Scheduling", "Arbitrary or basic first-come-first-served queueing", "Unregulated; prone to claim conflicts and false claims", "Greedy Min-Heap orders claims by strict urgency (Priority 1 to 3)"],
        ["Administrative Audit", "Physical cross-outs and manual corrections; no undo trail", "No historical trail; difficult to verify true claimant", "Immutable LIFO Activity Stack with instantaneous undo command"],
        ["Data Security & ACID", "Zero backup; prone to physical book loss or damage", "No privacy; personal contact details exposed publicly", "MySQL 8.0 with InnoDB foreign key constraints, CSRF & auth security"]
    ]
    add_table_data(comp_headers, comp_rows, [1.4, 1.8, 1.7, 1.7], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    add_p("As evidenced by the comparative matrix, the automated DSA-driven architecture resolves every major operational weakness of traditional tracking methods, providing measurable efficiency gains in retrieval time, search accuracy, and claim integrity.")

    # =========================================================
    # PAGE 9: 3. OBJECTIVE OF THE PROJECT
    # =========================================================
    add_h1("3. Objective of the Project")
    add_p("The primary objective of this project is to develop, test, and benchmark an automated lost-and-found management system that replaces manual registers with structured digital workflows powered by fundamental computer science data structures and algorithms. Specific measurable objectives include:")
    add_bullet("1. Implement Foundational Linear Structures (Phase 1):", "Construct custom dynamic Singly Linked Lists for property storage without fixed array pre-allocation, Last-In-First-Out (LIFO) Linked Stacks for audit history and administrative undo operations, and First-In-First-Out (FIFO) Linked Queues for chronological claim intake.")
    add_bullet("2. Optimize Hierarchical Lookup & Spatial Navigation (Phase 2):", "Build a Binary Search Tree (BST) supporting average O(log n) search, insertion, and three-case node deletion along with Inorder, Preorder, and Postorder traversals; and model campus buildings as an undirected adjacency graph evaluated through Breadth-First Search (BFS) to identify neighboring transit corridors.")
    add_bullet("3. Benchmark In-Place Sorting & Search Efficiency (Phase 3):", "Implement an in-place Linked List Merge Sort running in guaranteed O(n log n) time and O(1) auxiliary pointer memory using fast/slow two-pointer bisection, and empirically benchmark its lookup performance against linear scanning.")
    add_bullet("4. Solve Typo Tolerance & Urgency Scheduling (Phase 4):", "Construct a 2D Dynamic Programming Levenshtein Distance matrix ('Smart Match') to resolve misspelled item names within an edit distance of 4, and integrate a Greedy Min-Heap Priority Queue to order claims strictly by urgency (Priority 1: ID cards & valuables; Priority 2: Academic essentials; Priority 3: General articles).")
    add_bullet("5. Deliver Full-Stack Web & Desktop Interfaces:", "Integrate the algorithmic core into a multi-role Django web application with MySQL relational persistence and CSRF security, accompanied by an interactive desktop Tkinter demonstrator for laboratory presentation.")

    # =========================================================
    # PAGE 10: 4. SCOPE OF THE PROJECT
    # =========================================================
    add_h1("4. Scope of the Project")
    add_p("The operational scope of the platform is designed specifically for academic institutions, colleges, and university campuses. Key boundaries include:")
    add_bullet("Functional Boundaries:", "The application covers online submission of lost and found item reports, category-based and location-based indexing, fuzzy string searching for misspelled queries, campus building proximity suggestions, priority-based claim queueing, administrative claim verification and handover recording, and reversible audit logging.")
    add_bullet("User Roles & Permissions:", "The system supports three user roles: (1) Public Student/Guest Users, who can browse found items, search records, and submit ownership claims; (2) Faculty Members, who can report found property and view status boards; and (3) System Administrators, who possess exclusive rights to process priority claims, authorize handovers, and execute LIFO stack undo operations.")
    add_bullet("Deployment Boundaries:", "The application is optimized for campus intranet and web server deployment using standard web browsers (Chrome, Edge, Firefox) on desktop and mobile devices, alongside a desktop Tkinter interface for standalone laboratory demonstrations.")
    add_bullet("Exclusions & Future Scope:", "Hardware-level RFID automated locker lockers and direct SMS/WhatsApp carrier gateway integrations are excluded from the current practical release and designated for future enhancements.")

    # =========================================================
    # PAGE 11: 5. SOFTWARE SPECIFICATIONS
    # =========================================================
    add_h1("5. Software Specifications")
    add_p("The platform is developed using standard open-source tools and modular libraries, ensuring cross-platform stability and maintainability:")
    add_bullet("Programming Language:", "Python (v3.12 / v3.14 64-bit runtime) — utilized for custom data structure implementations, pointer manipulation, graph traversals, dynamic programming routines, and web controller logic.")
    add_bullet("Web Framework:", "Django Web Framework (v5.0+) — Model-View-Template (MVT) architecture providing automated ORM mapping, secure session authentication, CSRF protection, and administrative controls.")
    add_bullet("Relational Database Management System:", "MySQL 8.0+ / MariaDB (Database Schema: `data_structure`, InnoDB storage engine with strict foreign key constraints and ACID transaction compliance; SQLite3 configured as a portable development fallback).")
    add_bullet("Desktop GUI Framework:", "Tkinter (Tcl/Tk 8.6 native toolkit bundled with Python standard library) — powers the standalone educational DSA demonstrator.")
    add_bullet("Presentation Stack:", "HTML5 semantic markup, CSS3 (Modern Flexbox, CSS Grid, responsive media queries, card layouts), and Vanilla JavaScript for instant client-side filtering.")
    add_bullet("Development Tools & OS:", "Visual Studio Code / Antigravity IDE running on Microsoft Windows 11 Professional (64-bit kernel).")

    # =========================================================
    # PAGE 12: 6. WORKFLOW OF THE PROJECT
    # =========================================================
    add_h1("6. Workflow of the Project")
    add_h2("6.1 Sequential Workflow Nodes & Execution Pipeline")
    add_p("The application processes lost and found events through an integrated request-response pipeline coordinating the presentation front-end, Django controllers, the custom DSA algorithmic engine, and the MySQL database:")
    add_bullet("1. Reporting & Validation:", "A user registers a lost or found article through the web form. The request is validated by Django views, categorized, and assigned an urgency priority level (1=High, 2=Medium, 3=Low).")
    add_bullet("2. Dual Storage & Indexing:", "The record is committed to MySQL tables (`lost_items` or `found_items`) and simultaneously added to the in-memory Singly Linked List and Binary Search Tree.")
    add_bullet("3. Proximity Mapping via BFS:", "When a location is entered, the Campus Adjacency Graph executes a Breadth-First Search (BFS) to identify all immediately connected buildings, helping students focus their physical search.")
    add_bullet("4. Typo-Tolerant Search:", "Search queries trigger the 2D Dynamic Programming Levenshtein Distance matrix, comparing query terms against registered names to provide 'Smart Match' suggestions when edit distance <= 4.")
    add_bullet("5. Priority Claim Scheduling:", "Submitted claims enter `claim_processing` and are pushed into a Greedy Min-Heap (`heapq`). The administrator processes claims in logarithmic time, ensuring high-priority items are resolved first.")
    add_bullet("6. Resolution & LIFO Audit:", "Upon verified handover, the record moves to `claim_done`, and an action entry is pushed onto the LIFO Activity Stack, enabling instant administrative undo if needed.")

    # =========================================================
    # PAGE 13: 6.2 SYSTEM ARCHITECTURE DIAGRAM
    # =========================================================
    add_h1("6.2 Layered System Architecture Diagram", page_break=True)
    add_p("Figure 6.1 illustrates the 3-Tier Layered Architecture of the system, clearly separating the client presentation tier, the application and algorithmic tier, and the persistence storage tier.")
    add_image_figure(os.path.join(doc_img_dir, "arch_system_architecture.png"),
                     "Figure 6.1: 3-Tier Layered System Architecture of Campus Lost & Found System", width_inches=4.8)

    # =========================================================
    # PAGE 14: 6.3 MASTER WORKFLOW FLOWCHART
    # =========================================================
    add_h1("6.3 Master Workflow Flowchart", page_break=True)
    add_p("Figure 6.2 provides the comprehensive flowchart tracing the end-to-end execution path from initial loss reporting to final handover and audit logging.")
    add_image_figure(os.path.join(doc_img_dir, "flowchart_system_workflow.png"),
                     "Figure 6.2: Master System Workflow and Claim Processing Pipeline Flowchart", width_inches=4.6)

    # =========================================================
    # PAGE 15: 7. MODULES OF THE PROJECT - PHASE 1
    # =========================================================
    add_h1("7. Modules of the Project - Phase-wise Explanation")
    add_p("The project is structured into four sequential, mathematically grounded computer science phases, linking foundational data structures with enterprise software implementation.")
    
    add_h2("7.1 Phase 1: Linear Data Structures Module")
    add_p("Phase 1 establishes core memory management by developing linear data structures from scratch in pure Python without reliance on high-level container libraries.")
    
    add_h3("7.1.1 Dynamic Singly Linked List (campuslostfound/linked_list.py)")
    add_p("Unlike contiguous arrays which require static memory pre-allocation and costly O(n) array-shifting during deletions, the custom Singly Linked List manages memory dynamically through discrete `Node` objects. Each node stores a data dictionary (`id`, `name`, `type`, `location`) and a reference pointer `next` to the succeeding node.")
    add_bullet("Insertion Operation (O(n) / O(1)):", "Traverses to the terminal node where `current.next is None` and attaches the new node. In a head-pointer variant, insertion achieves constant O(1) time.")
    add_bullet("Deletion by ID (O(n)):", "Maintains dual pointers (`previous` and `current`) to find the target node and updates `previous.next = current.next`, cleanly bypassing the deleted node.")
    add_bullet("Sequential Traversal (O(n)):", "Iterates from `head` through `next` pointers to display or process all active records.")
    add_p("Memory Efficiency Analysis: In Python, standard dynamic lists pre-allocate contiguous memory buffers. For a system tracking sporadic, unpredictable lost-and-found entries, pre-allocated buffers consume excess memory. The linked node design allocates memory strictly on demand: each `Node(data)` allocates exactly one payload reference and one pointer, maximizing heap efficiency.")

    add_h3("7.1.2 Last-In-First-Out (LIFO) Stack (campuslostfound/stack.py)")
    add_p("The Stack structure enforces a strict LIFO operational sequence using linked `StackNode` elements. In the lost-and-found system, it maintains an auditable history of recent operations (registrations, claim resolutions, deletions).")
    add_bullet("Push Operation (O(1)):", "Sets `new_node.next = self.top` and updates `self.top = new_node` in constant time.")

    # =========================================================
    # PAGE 16: 7.1.3 QUEUE & 7.2 PHASE 2: TREE & GRAPH
    # =========================================================
    add_h1("7.1.3 First-In-First-Out (FIFO) Queue & Phase 2 Architecture", page_break=True)
    add_bullet("Pop Operation (O(1)):", "Retrieves the top action payload and advances `self.top = self.top.next`. In the Django application, this powers the administrative 'Undo Last Action' feature, reconstructing previous states with precision.")
    add_p("Administrative Reversal Mechanics: When an administrator accidentally finalizes a claim or records an erroneous lost item, standard systems require manual database rollbacks. By recording each transaction in an `ActivityLog` object and pushing it onto the LIFO Stack, an administrator can trigger an 'Undo' request. The stack pops the most recent action, inspects its type ('ADD' or 'PROCESS'), and executes the inverse operation (e.g., reverting `is_resolved=False` and restoring the claim).")

    add_h3("7.1.3 First-In-First-Out (FIFO) Queue (campuslostfound/queue.py)")
    add_p("The Queue structure enforces a FIFO operational order using dual pointers: `front` and `rear`.")
    add_bullet("Enqueue Operation (O(1)):", "Appends new claim inquiries to `self.rear` in constant time.")
    add_bullet("Dequeue Operation (O(1)):", "Removes the oldest pending claim from `self.front`, guaranteeing fair chronological intake.")
    add_bullet("Queue Boundary Management:", "Includes underflow checks. When `front` equals `None`, `dequeue()` catches the condition gracefully without throwing null-pointer exceptions.")

    add_h2("7.2 Phase 2: Hierarchical & Graph Structures Module")
    add_p("Phase 2 expands the platform into non-linear, hierarchical and networked topological structures:")
    
    add_h3("7.2.1 Binary Search Tree Architecture (campuslostfound/binary_tree.py)")
    add_p("To eliminate linear search overhead, item records are organized into a custom Binary Search Tree keyed on unique numerical `id` values. Each `TreeNode` encapsulates `data`, `left`, and `right` child pointers, maintaining the BST invariant: for any node N, all keys in N.left < N.data and all keys in N.right >= N.data.")
    add_bullet("BST Search (O(log n) average):", "Compares the target ID against the current node. If `target < current.data`, it branches left; if `target > current.data`, it branches right, halving the search space at each step.")
    add_bullet("BST Node Deletion (O(log n)):", "Handles three distinct topological scenarios: (1) Leaf node deletion; (2) Single-child node deletion; (3) Two-child node deletion (locates the in-order successor—minimum value node in the right subtree, replaces node data, and recursively deletes the successor).")

    # =========================================================
    # PAGE 17: BST TRAVERSALS & CAMPUS GRAPH BFS
    # =========================================================
    add_h1("7.2.1 BST Traversals & Figure 7.1 Flowchart", page_break=True)
    add_bullet("Tree Traversals:", "Implements Inorder (Left -> Root -> Right) returning sorted IDs; Preorder (Root -> Left -> Right) for structural cloning; and Postorder (Left -> Right -> Root) for node deallocation.")
    add_image_figure(os.path.join(doc_img_dir, "flowchart_phase2_bst.png"),
                     "Figure 7.1: Phase 2: Binary Search Tree Lookup and Deletion Flowchart", width_inches=4.7)

    add_h3("7.2.2 Campus Adjacency Graph & BFS Traversal (campuslostfound/graph.py)")
    add_p("College landmarks are modeled as an undirected topological graph G = (V, E), where vertices V represent physical buildings and edges E represent connecting pathways.")
    add_bullet("Adjacency List Mapping:", "Implemented as: `{'Main Block': ['Library', 'Cafeteria'], 'Library': ['Main Block', 'Computer Lab'], 'Cafeteria': ['Main Block', 'Sports Ground'], ...}`.")
    add_bullet("Breadth-First Search (BFS):", "When an item is reported missing in a building (e.g., 'Library'), BFS explores surrounding landmarks layer-by-layer using a FIFO queue and a `visited` set. This outputs a prioritized sequence of adjacent structures where the student is advised to search.")

    # =========================================================
    # PAGE 18: BFS WALKTHROUGH & PHASE 3 MERGE SORT
    # =========================================================
    add_h1("7.2.2 Campus BFS Walkthrough & Phase 3 Introduction", page_break=True)
    add_p("Algorithmic Walkthrough of BFS: Suppose an item is lost at the 'Library'. The algorithm initializes `queue = ['Library']` and `visited = {'Library'}`. It dequeues 'Library' and appends it to `search_order`. Next, it queries `graph['Library']`, discovering neighbors ['Main Block', 'Computer Lab']. Since neither has been visited, both are marked visited and enqueued. In subsequent iterations, 'Main Block' is dequeued, discovering 'Cafeteria'. The resulting output order `['Library', 'Main Block', 'Computer Lab', 'Cafeteria', 'Sports Ground']` provides an exact, radially expanding search path for campus security.")
    add_image_figure(os.path.join(doc_img_dir, "flowchart_phase2_bfs_graph.png"),
                     "Figure 7.2: Phase 2: Campus Adjacency Graph Breadth-First Search (BFS) Flowchart", width_inches=4.6)

    add_h2("7.3 Phase 3: Searching & Sorting Operations Module")
    add_p("Phase 3 addresses record ordering and algorithmic optimization:")
    
    add_h3("7.3.1 Linked List Merge Sort (campuslostfound/merge_sort.py)")
    add_p("Sorting a singly linked list presents unique algorithmic constraints: random memory indexing is impossible, preventing standard QuickSort or HeapSort from operating in O(1) space. Merge Sort is mathematically optimal for linked lists, operating in guaranteed O(n log n) time and O(1) auxiliary pointer space.")
    add_bullet("1. Fast & Slow Pointer Bisection:", "A `slow` pointer advances one step while a `fast` pointer advances two steps. When `fast` reaches the end, `slow` is precisely at the midpoint. Setting `middle.next = None` severs the list into two halves.")
    add_bullet("2. Recursive Division:", "Recursively sorts both left and right halves down to individual base nodes.")
    add_bullet("3. In-Place Sorted Merge:", "Compares `left.data['id']` against `right.data['id']` and splices pointers directly without allocating array copies.")

    # =========================================================
    # PAGE 19: MERGE SORT FLOWCHART & PHASE 4 LEVENSHTEIN
    # =========================================================
    add_h1("7.3.1 Merge Sort Flowchart & Phase 4 Introduction", page_break=True)
    add_image_figure(os.path.join(doc_img_dir, "flowchart_phase3_merge_sort.png"),
                     "Figure 7.3: Phase 3: Linked List Merge Sort In-Place Division and Merge Flowchart", width_inches=4.6)

    add_h3("7.3.2 Linear vs. Hierarchical Search Benchmarking")
    add_p("Linear scanning through an unsorted linked list requires O(n) comparisons in the worst case (e.g., inspecting 10,000 nodes for an absent key). By contrast, querying the Binary Search Tree requires at most 14 comparisons (since log2(10000) ≈ 13.3). Phase 3 empirically demonstrates this asymptotic advantage.")

    add_h2("7.4 Phase 4: Algorithmic Problem Solving Module")
    add_p("Phase 4 incorporates advanced algorithmic paradigms to solve fuzzy string matching and priority scheduling:")
    
    add_h3("7.4.1 Dynamic Programming Levenshtein Distance Matrix (campuslostfound/smart_match.py)")
    add_p("When students search for lost items, phonetic and typing errors routinely prevent exact database matches. Phase 4 implements the Wagner-Fischer Dynamic Programming algorithm to compute the minimal edit distance (insertions, deletions, and substitutions) between two arbitrary strings.")
    add_p("The recurrence relation is defined over a 2D matrix DP[0..m][0..n]:")
    add_bullet("Base Conditions:", "DP[i][0] = i (cost of deleting i characters); DP[0][j] = j (cost of inserting j characters).")

    # =========================================================
    # PAGE 20: LEVENSHTEIN WALKTHROUGH & PHASE 4 MIN-HEAP
    # =========================================================
    add_h1("7.4.1 Levenshtein Matrix Flowchart & Min-Heap PQ", page_break=True)
    add_bullet("Transition Equation:", "If `str1[i-1] == str2[j-1]`, then `DP[i][j] = DP[i-1][j-1]` (cost is 0). Otherwise, `DP[i][j] = 1 + min(DP[i][j-1], DP[i-1][j], DP[i-1][j-1])` representing minimum cost among insertion, deletion, and substitution.")
    add_bullet("Smart Match Decision Rule:", "The system iterates over all active records in the linked list, computing edit distance. If the minimal distance is <= 4, the system outputs: `Did you mean: '[Matched Item]'? (Edit distance: k)`. This bridges human spelling errors with exact database records.")
    add_p("Illustrative Walkthrough: Suppose a student enters query 'calclator' and the database holds 'Calculator'. The 2D DP matrix computes: string length m=9, n=10. The letters match sequentially except for the missing 'u' at index 4. The algorithm calculates minimal cost = 1 insertion. Since 1 <= 4, the Smart Match engine instantly returns: 'Did you mean: Calculator? (Edit distance: 1)', converting an otherwise failed query into a successful recovery.")
    add_image_figure(os.path.join(doc_img_dir, "flowchart_phase4_levenshtein.png"),
                     "Figure 7.4: Phase 4: Dynamic Programming Levenshtein Distance Matrix Flowchart", width_inches=4.6)

    add_h3("7.4.2 Greedy Min-Heap Priority Queue Claim Scheduler (scheduler/views.py)")
    add_p("In Phase 4, the web application elevates FIFO claim handling into an urgency-ranked Priority Queue. Utilizing Python's binary min-heap implementation (`heapq`), pending claims are scheduled based on an integer priority tuple `(priority, id, object)`:")

    # =========================================================
    # PAGE 21: MIN-HEAP PRIORITIES, TABLE 7.1 & DFD INTRO
    # =========================================================
    add_h1("7.5 Algorithmic Complexity Table & DFD Models", page_break=True)
    add_bullet("Priority 1 (High Urgency):", "Identity cards, room keys, examination tickets, laptops, prescription eyewear.")
    add_bullet("Priority 2 (Medium Urgency):", "Scientific calculators, wristwatches, course textbooks, backpacks.")
    add_bullet("Priority 3 (Low Urgency):", "Water bottles, stationery, notebooks, umbrellas.")
    add_p("By maintaining the min-heap property in O(log n) time during `heappush` and `heappop`, high-priority claims automatically rise to the top of the processing queue, ensuring vital student belongings are resolved before non-essential items.")

    add_h2("7.5 Comprehensive Algorithmic Complexity & Space-Time Trade-Offs")
    add_p("Table 7.1 details the formal space-time complexity bounds across all four project phases:")

    comp_table = [
        ("Data Structure / Algorithm", "Phase", "Time (Best)", "Time (Average)", "Time (Worst)", "Space Complexity"),
        ("Singly Linked List (Insert)", "Phase 1", "O(1)", "O(n)", "O(n)", "O(1) auxiliary"),
        ("Singly Linked List (Delete)", "Phase 1", "O(1)", "O(n)", "O(n)", "O(1) auxiliary"),
        ("Linked Stack (Push / Pop)", "Phase 1", "O(1)", "O(1)", "O(1)", "O(n) storage"),
        ("Linked Queue (Enqueue / Dequeue)", "Phase 1", "O(1)", "O(1)", "O(1)", "O(n) storage"),
        ("Binary Search Tree (Search)", "Phase 2", "O(1)", "O(log n)", "O(n) skewed", "O(h) call stack"),
        ("Binary Search Tree (Delete)", "Phase 2", "O(1)", "O(log n)", "O(n) skewed", "O(h) call stack"),
        ("Campus Graph BFS Traversal", "Phase 2", "O(V + E)", "O(V + E)", "O(V + E)", "O(V) queue & visited"),
        ("Linked List Merge Sort", "Phase 3", "O(n log n)", "O(n log n)", "O(n log n)", "O(log n) stack / O(1) mem"),
        ("DP Levenshtein Distance Matrix", "Phase 4", "O(m * n)", "O(m * n)", "O(m * n)", "O(m * n) 2D matrix"),
        ("Min-Heap Priority Queue (Push/Pop)", "Phase 4", "O(1)", "O(log n)", "O(log n)", "O(n) heap array")
    ]
    add_table_data(comp_table[0], comp_table[1:], [1.6, 0.7, 0.9, 1.0, 1.0, 1.3], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT])

    add_h2("7.6 Data Flow Diagram (DFD) Models")
    add_p("Data Flow Diagrams visualize the systemic movement, transformation, and storage of data between external entities and internal processes:")

    # =========================================================
    # PAGE 22: 7.6.1 DFD LEVEL 0 & FIGURE 7.5
    # =========================================================
    add_h1("7.6.1 DFD Level 0 Context Diagram", page_break=True)
    add_p("The Level 0 Context Diagram establishes the global boundary of the system. Four external entities interact with Process 0.0 (Campus Lost & Found System): Students (submitting loss reports and claims), Finders (registering found items), System Administrators (verifying claims and auditing logs), and the Campus Security Office (authorizing asset handovers).")
    add_image_figure(os.path.join(doc_img_dir, "dfd_level0_context.png"),
                     "Figure 7.5: Data Flow Diagram (DFD) - Level 0 Context Diagram", width_inches=4.7)

    add_h2("7.6.2 DFD Level 1: Subsystem Process Decomposition")
    add_p("The Level 1 DFD decomposes Process 0.0 into five discrete operational processes: Process 1.0 (User Authentication & Role Validation), Process 2.0 (Lost/Found Item Registration), Process 3.0 (Algorithmic Search & Smart Matching), Process 4.0 (Claim Priority Scheduling), and Process 5.0 (Activity Auditing & LIFO Stack Undo). These processes interact with three data stores: D1 (`lost_items` / `found_items`), D2 (`claim_processing` / `claim_done`), and D3 (`activity_logs`).")

    # =========================================================
    # PAGE 23: FIGURE 7.6 DFD LEVEL 1 & 7.7 DATABASE DESIGN
    # =========================================================
    add_h1("7.6.2 DFD Level 1 Diagram & Database Design", page_break=True)
    add_image_figure(os.path.join(doc_img_dir, "dfd_level1_system.png"),
                     "Figure 7.6: Data Flow Diagram (DFD) - Level 1 Subsystem Process Decomposition", width_inches=4.7)

    add_h2("7.7 Database Design, Relational Schema & Normalization Analysis (3NF)")
    add_p("The relational database schema is configured under the `data_structure` MySQL database. It consists of five interrelated tables designed according to rigorous Third Normal Form (3NF) relational principles.")
    add_image_figure(os.path.join(doc_img_dir, "db_er_diagram.png"),
                     "Figure 7.7: Relational Database Schema and Entity-Relationship (ER) Diagram", width_inches=4.7)

    # =========================================================
    # PAGE 24: DATABASE TABLE SPECIFICATIONS (PART 1)
    # =========================================================
    add_h1("7.7.2 Detailed Relational Table Specifications", page_break=True)
    add_h3("Table 1: lost_items (Lost Property Registry)")
    tbl_lost = [
        ("Field Name", "Data Type", "Constraint", "Description / Purpose"),
        ("id", "INT AUTO_INCREMENT", "PRIMARY KEY", "Unique numerical surrogate key for lost item record"),
        ("student_name", "VARCHAR(100)", "NOT NULL", "Student identification or register number (e.g. 26MCAC28)"),
        ("item_name", "VARCHAR(100)", "NOT NULL", "Description of lost property (e.g. Student ID Card)"),
        ("location", "VARCHAR(100)", "NOT NULL", "Last known campus location where item was lost"),
        ("priority", "INT", "DEFAULT 2", "Urgency level: 1 = High, 2 = Medium, 3 = Low"),
        ("is_resolved", "TINYINT(1)", "DEFAULT 0", "Boolean flag indicating whether item has been recovered"),
        ("created_at", "DATETIME", "AUTO_NOW_ADD", "Timestamp of loss report submission")
    ]
    add_table_data(tbl_lost[0], tbl_lost[1:], [1.2, 1.4, 1.4, 2.5], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT])

    add_h3("Table 2: found_items (Found Property Inventory)")
    tbl_found = [
        ("Field Name", "Data Type", "Constraint", "Description / Purpose"),
        ("id", "INT AUTO_INCREMENT", "PRIMARY KEY", "Unique numerical surrogate key for found item record"),
        ("student_name", "VARCHAR(100)", "NOT NULL", "Name or identifier of person who discovered the item"),
        ("item_name", "VARCHAR(100)", "NOT NULL", "Title / description of the found article"),
        ("location", "VARCHAR(100)", "NOT NULL", "Campus physical location where item was recovered"),
        ("priority", "INT", "DEFAULT 2", "Calculated item urgency priority (1=High, 2=Med, 3=Low)"),
        ("is_resolved", "TINYINT(1)", "DEFAULT 0", "Boolean flag: 1 if returned to owner, 0 if still in inventory"),
        ("created_at", "DATETIME", "AUTO_NOW_ADD", "System timestamp when item was logged into custody")
    ]
    add_table_data(tbl_found[0], tbl_found[1:], [1.2, 1.4, 1.4, 2.5], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT])

    # =========================================================
    # PAGE 25: DATABASE TABLE SPECIFICATIONS (PART 2)
    # =========================================================
    add_h1("7.7.2 Relational Specifications (Claims Management)", page_break=True)
    add_h3("Table 3: claim_processing (Active Claims Queue)")
    tbl_cp = [
        ("Field Name", "Data Type", "Constraint", "Description / Purpose"),
        ("id", "INT AUTO_INCREMENT", "PRIMARY KEY", "Unique numerical claim queue identifier"),
        ("student_name", "VARCHAR(100)", "NOT NULL", "Claimant student ID or register number"),
        ("item_name", "VARCHAR(100)", "NOT NULL", "Name of the target item being claimed"),
        ("location", "VARCHAR(100)", "NOT NULL", "Location where loss occurred"),
        ("priority", "INT", "DEFAULT 2", "Priority weighting used by Min-Heap queue scheduler"),
        ("lost_item_id", "INT", "FOREIGN KEY", "References lost_items(id) with CASCADE deletion rule"),
        ("created_at", "DATETIME", "AUTO_NOW_ADD", "Timestamp when claim entered active processing queue")
    ]
    add_table_data(tbl_cp[0], tbl_cp[1:], [1.2, 1.4, 1.4, 2.5], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT])

    add_h3("Table 4: claim_done (Historical Claim Archive)")
    tbl_cd = [
        ("Field Name", "Data Type", "Constraint", "Description / Purpose"),
        ("id", "INT AUTO_INCREMENT", "PRIMARY KEY", "Unique historical archive record key"),
        ("student_name", "VARCHAR(100)", "NOT NULL", "Name of claimant who received the item"),
        ("item_name", "VARCHAR(100)", "NOT NULL", "Name of resolved article"),
        ("location", "VARCHAR(100)", "NOT NULL", "Location record of item"),
        ("priority", "INT", "DEFAULT 2", "Urgency level of the fulfilled claim"),
        ("lost_item_id", "INT", "FOREIGN KEY", "References lost_items(id) with SET_NULL rule on delete"),
        ("claimed_at", "DATETIME", "AUTO_NOW_ADD", "Verification timestamp when handover was finalized")
    ]
    add_table_data(tbl_cd[0], tbl_cd[1:], [1.2, 1.4, 1.4, 2.5], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT])

    # =========================================================
    # PAGE 26: DATABASE TABLE SPECIFICATIONS (PART 3) & NORMALIZATION
    # =========================================================
    add_h1("7.7.3 Database Normalization Proof (1NF, 2NF, 3NF)", page_break=True)
    add_h3("Table 5: activity_logs (Audit Trail & Undo Log)")
    tbl_act = [
        ("Field Name", "Data Type", "Constraint", "Description / Purpose"),
        ("id", "INT AUTO_INCREMENT", "PRIMARY KEY", "Sequential audit log entry key"),
        ("action_type", "VARCHAR(20)", "NOT NULL", "Operation type: 'ADD', 'PROCESS', or 'DELETE'"),
        ("category", "VARCHAR(10)", "DEFAULT 'Lost'", "Category of item affected ('Lost' or 'Found')"),
        ("item_id", "INT", "NOT NULL", "Surrogate ID of the target record modified"),
        ("description", "VARCHAR(200)", "NOT NULL", "Human-readable activity summary for auditing"),
        ("created_at", "DATETIME", "AUTO_NOW_ADD", "Exact system timestamp when action transpired")
    ]
    add_table_data(tbl_act[0], tbl_act[1:], [1.2, 1.4, 1.4, 2.5], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT])

    add_h3("Formal Normalization Proof (1NF, 2NF, 3NF)")
    add_p("To eliminate update, insertion, and deletion anomalies, the relational schema was normalized through 1NF, 2NF, and 3NF:")
    add_bullet("First Normal Form (1NF):", "All table attributes contain atomic, indivisible values. Repeating groups and multi-valued comma-separated lists were eliminated. Every record possesses a unique primary key (`id`).")
    add_bullet("Second Normal Form (2NF):", "The schema satisfies 1NF and contains zero partial functional dependencies. All non-prime attributes (`student_name`, `item_name`, `location`, `priority`) depend entirely on the entire primary key.")
    add_bullet("Third Normal Form (3NF):", "The schema satisfies 2NF and contains zero transitive dependencies. In previous designs, resolving a claim updated fields in `lost_items` while storing resolution metadata in the same table, creating transitive reliance. By isolating active claims into `claim_processing` and archived handovers into `claim_done`, non-key attributes depend strictly and directly on the primary key alone (X -> Y where X is a superkey).")

    # =========================================================
    # PAGES 27 TO 56: 8. SOURCE CODE (FUNCTIONAL CODE STRUCTURE)
    # =========================================================
    add_h1("8. Source Code (Functional Code Structure)")
    add_p("In accordance with project documentation standards, structural and functional source code excerpts representing the core data structures, desktop UI, and Django web controllers are presented below.")

    add_h2("8.1 Data Structures Core Engine (campuslostfound/)")
    
    # 1. linked_list.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/campuslostfound/linked_list.py", "r", encoding="utf-8") as f:
        code_ll = f.read()
    add_code_block("campuslostfound/linked_list.py (Phase 1: Dynamic Singly Linked List)", code_ll)

    # 2. stack.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/campuslostfound/stack.py", "r", encoding="utf-8") as f:
        code_st = f.read()
    add_code_block("campuslostfound/stack.py (Phase 1: LIFO Linked Stack for Activity History)", code_st)

    # 3. queue.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/campuslostfound/queue.py", "r", encoding="utf-8") as f:
        code_qu = f.read()
    add_code_block("campuslostfound/queue.py (Phase 1: FIFO Linked Queue for Claim Inquiries)", code_qu)

    # 4. binary_tree.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/campuslostfound/binary_tree.py", "r", encoding="utf-8") as f:
        code_bt = f.read()
    add_code_block("campuslostfound/binary_tree.py (Phase 2: BST Insertion, Search, Deletion & Traversals)", code_bt)

    # 5. graph.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/campuslostfound/graph.py", "r", encoding="utf-8") as f:
        code_gr = f.read()
    add_code_block("campuslostfound/graph.py (Phase 2: Campus Adjacency Graph & BFS Traversal)", code_gr)

    # 6. merge_sort.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/campuslostfound/merge_sort.py", "r", encoding="utf-8") as f:
        code_ms = f.read()
    add_code_block("campuslostfound/merge_sort.py (Phase 3: Linked List Merge Sort In-Place)", code_ms)

    # 7. smart_match.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/campuslostfound/smart_match.py", "r", encoding="utf-8") as f:
        code_sm = f.read()
    add_code_block("campuslostfound/smart_match.py (Phase 4: Dynamic Programming Levenshtein Distance)", code_sm)

    add_h2("8.2 Desktop GUI Interface Implementation (main_ui.py)")
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/campuslostfound/main_ui.py", "r", encoding="utf-8") as f:
        code_ui = f.read()
    add_code_block("campuslostfound/main_ui.py (Desktop Tkinter Multi-Phase Demonstrator)", code_ui, max_lines=180)

    add_h2("8.3 Django Web Application Controllers (scheduler/)")
    
    # models.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/scheduler/models.py", "r", encoding="utf-8") as f:
        code_mod = f.read()
    add_code_block("scheduler/models.py (Django ORM Models & Relational Schemas)", code_mod)

    # views.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/scheduler/views.py", "r", encoding="utf-8") as f:
        code_vw = f.read()
    add_code_block("scheduler/views.py (Django Application Views & Min-Heap Priority Queue)", code_vw, max_lines=250)

    # urls.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/scheduler/urls.py", "r", encoding="utf-8") as f:
        code_url = f.read()
    add_code_block("scheduler/urls.py (URL Routing Configurations)", code_url)

    # admin.py
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/scheduler/admin.py", "r", encoding="utf-8") as f:
        code_adm = f.read()
    add_code_block("scheduler/admin.py (Django Administrative Dashboard Configurations)", code_adm)

    add_h2("8.4 Front-End Presentation Templates (scheduler/templates/)")
    
    # index.html
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/scheduler/templates/index.html", "r", encoding="utf-8") as f:
        code_idx = f.read()
    add_code_block("scheduler/templates/index.html (Main Dashboard, Priority Queue & Activity UI)", code_idx, max_lines=240)

    # login.html
    with open("c:/Users/kuria/OneDrive/Desktop/L & F/scheduler/templates/login.html", "r", encoding="utf-8") as f:
        code_log = f.read()
    add_code_block("scheduler/templates/login.html (Multi-Role Authentication Interface)", code_log, max_lines=210)

    # =========================================================
    # PAGES 57 & 58: 9. FEATURES OF THE PROJECT & TEST CASES
    # =========================================================
    add_h1("9. Features of the Project")
    add_p("The Campus Lost and Found Management System delivers powerful, distinctive engineering features that bridge academic algorithms with institutional utility:")
    add_bullet("1. Urgency-Ranked Min-Heap Scheduling:", "Prioritizes vital assets (Identity cards, fee receipts, room keys, electronics) ahead of non-essential articles in O(log n) time.")
    add_bullet("2. Typo-Tolerant Dynamic Programming Fuzzy Match:", "Reconciles spelling variations within 4 edit distance operations, ensuring students locate misplaced property even when descriptions are misspelled.")
    add_bullet("3. Topological Campus Proximity Guidance:", "Evaluates contiguous campus buildings via Breadth-First Search (BFS), providing spatial suggestions on nearby transit corridors.")
    add_bullet("4. Guaranteed O(n log n) Linked List Sorting:", "Sorts dynamic linked nodes in-place using two-pointer bisection without array copying.")
    add_bullet("5. LIFO Audit Trail & State Reversal (Undo):", "Maintains an immutable stack history, enabling administrators to reverse mistaken handovers or accidental deletions with mathematical certainty.")
    add_bullet("6. ACID Relational Integrity:", "Enforces strict MySQL foreign key constraints across `lost_items`, `found_items`, `claim_processing`, `claim_done`, and `activity_logs`.")

    add_h2("9.1 Verification Test Cases & Algorithmic Outcomes")
    add_p("Table 9.1 documents the comprehensive verification test suites executed across all four algorithmic phases:")

    test_cases = [
        ("Test ID", "Component / Phase", "Test Scenario & Input Data", "Expected Output / Behavior", "Actual Output", "Status"),
        ("TC-01", "Phase 1: Linked List", "Insert Node (ID: 101, 'Student ID Card')", "Node appended at tail; traverse() displays 101", "Node successfully inserted", "PASSED"),
        ("TC-02", "Phase 1: Linked List", "Delete existing head node (ID: 101)", "Head pointer advances to node 102; 101 removed", "Head node excised cleanly", "PASSED"),
        ("TC-03", "Phase 1: Stack", "Push 3 activity logs; invoke pop()", "Last logged activity returned (LIFO order)", "Returned 3rd activity", "PASSED"),
        ("TC-04", "Phase 1: Queue", "Enqueue claims C1, C2; invoke dequeue()", "C1 returned first (FIFO operational order)", "C1 dispatched first", "PASSED"),
        ("TC-05", "Phase 2: BST", "Insert IDs [105, 102, 108]; search(108)", "search(108) returns True; branches right", "Returned True in O(log n)", "PASSED"),
        ("TC-06", "Phase 2: BST", "Delete node with 2 children (ID: 105)", "In-order successor replaces 105; invariant intact", "Successor swapped correctly", "PASSED"),
        ("TC-07", "Phase 2: Campus Graph", "Run BFS starting from 'Main Block'", "Returns: ['Main Block', 'Library', 'Cafeteria', ...]", "Full BFS order matched", "PASSED"),
        ("TC-08", "Phase 3: Merge Sort", "Sort unsorted list: [105, 101, 104, 102]", "Pointers re-linked to ascending: [101, 102, 104, 105]", "Sorted ascending O(n log n)", "PASSED"),
        ("TC-09", "Phase 4: Smart Match", "Fuzzy search 'calclator' vs 'Calculator'", "Distance = 1; outputs: 'Did you mean: Calculator?'", "Smart Match triggered", "PASSED"),
        ("TC-10", "Phase 4: Smart Match", "Fuzzy search 'xyz999' vs 'Calculator'", "Distance > 4; outputs 'No close matches found'", "Rejected distant match", "PASSED"),
        ("TC-11", "Phase 4: Min-Heap", "Enqueue Priority 3, then Priority 1", "Min-heap schedules Priority 1 item at front of queue", "Priority 1 popped first", "PASSED"),
        ("TC-12", "Django Web: Undo", "Admin triggers 'Undo Last Action'", "Stack pop restores previous record in MySQL", "Database state rolled back", "PASSED"),
        ("TC-13", "Security: Access", "Student attempts admin undo action", "Access Denied: Administrative permission required", "Unauthorized request blocked", "PASSED")
    ]
    add_table_data(test_cases[0], test_cases[1:], [0.7, 1.2, 1.6, 1.4, 1.1, 0.6], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER])

    add_h2("9.2 User Interface Walkthrough & Live System Screenshots")
    add_p("The user interface walkthrough illustrates the responsive web platform and companion desktop demonstrator captured from the active application:")

    # =========================================================
    # PAGES 59, 60, 61: LIVE APPLICATION SCREENSHOTS
    # =========================================================
    doc.add_page_break()
    add_image_figure(os.path.join(doc_img_dir, "ui_web_dashboard.png"),
                     "Figure 9.1: Web Application Dashboard: Public Item Catalog, Priority Queue & Activity Log", width_inches=4.8)

    doc.add_page_break()
    add_image_figure(os.path.join(doc_img_dir, "ui_web_login.png"),
                     "Figure 9.2: Web Application Multi-Role User Authentication Screen", width_inches=4.8)

    doc.add_page_break()
    add_image_figure(os.path.join(doc_img_dir, "ui_web_search.png"),
                     "Figure 9.3: Web Application Location Proximity & Keyword Filtering Results", width_inches=4.5)
    add_image_figure(os.path.join(doc_img_dir, "ui_desktop_mockup.png"),
                     "Figure 9.4: Desktop DSA Demonstrator: Tkinter Native Interface & Algorithmic Console", width_inches=4.1)

    # =========================================================
    # PAGE 62: 10. FUTURE ENHANCEMENTS
    # =========================================================
    add_h1("10. Future Enhancements")
    add_p("While the system fully meets its current academic and operational goals, future developmental iterations can introduce advanced capabilities:")
    add_bullet("1. Computer Vision Image Matching:", "Integrating Convolutional Neural Networks (CNNs) to automatically classify uploaded item photographs and compute visual feature similarity embeddings between lost and found articles.")
    add_bullet("2. Automated SMS & WhatsApp Notifications:", "Integrating institutional SMS gateways or the WhatsApp Business API to dispatch automated alerts the moment a matching article is surrendered.")
    add_bullet("3. Smart Locker RFID Integration:", "Connecting the software to physical smart locker compartments equipped with RFID card scanners for automated, 24/7 keycard-based property retrieval without manual staff intervention.")
    add_bullet("4. Geofenced Mobile Application:", "Developing a cross-platform mobile application with GPS geofencing that alerts students whenever they enter an academic block where their lost property was recovered.")

    # =========================================================
    # PAGES 63 & 64: 11. CONCLUSION, VIVA DEFENSE & REFERENCES
    # =========================================================
    add_h1("11. Conclusion & Technical Defense")
    add_h2("11.1 Project Conclusion & Core Deliverables")
    add_p("The 'Campus Lost and Found Management System with Priority Claim Scheduling' demonstrates the successful practical application of Data Structures and Algorithms to resolve real-world campus logistics challenges. By implementing all four project phases—Linear Data Structures, Hierarchical & Graph Structures, Search/Sort Optimizations, and Dynamic Programming with Priority Queues—the project bridges theoretical computer science with enterprise software engineering.")
    add_p("The platform successfully replaces manual paper registers with an automated, responsive digital repository, ensures fair and urgency-ranked claim settlements, empowers students through typo-tolerant fuzzy retrieval, and guarantees complete administrative accountability through a reversible LIFO audit trail.")

    add_h2("11.2 Viva-Voce Architectural Defense Q&A")
    add_p("To support final examination defense, key architectural questions and model answers are summarized below:")
    add_bullet("Q1: Why is Merge Sort preferred over QuickSort for Singly Linked Lists?", "Answer: QuickSort relies heavily on O(1) random memory indexing to select pivots and swap elements, which requires costly O(n) pointer scans on linked lists. Merge Sort divides lists in O(log n) stages using two-pointer bisection and merges them in-place with O(1) auxiliary pointer memory, guaranteeing strict O(n log n) worst-case time.")
    add_bullet("Q2: How does the Dynamic Programming Levenshtein Distance matrix avoid redundant calculation?", "Answer: It decomposes string comparison into overlapping subproblems. By storing previously computed transformation costs in a 2D matrix DP[i][j], optimal edit costs for prefixes are reused in O(1) time rather than re-evaluating exponentially in O(3^(m+n)) recursive calls.")
    add_bullet("Q3: Why use a Min-Heap instead of a sorted list for claim scheduling?", "Answer: Inserting a new claim into a sorted array requires O(n) shifting. A binary min-heap executes insertions (`heappush`) and extractions (`heappop`) in strict O(log n) time, ensuring constant-time access to the most urgent claim while scaling gracefully as campus reports grow.")

    doc.add_page_break()
    add_h2("11.3 Academic References & Bibliography")
    add_p("The design, algorithmic formulation, and implementation of this dissertation drew upon established textbooks, peer-reviewed research papers, and technical documentation:")
    
    bib_entries = [
        ("Ref ID", "Citation / Source Details", "Domain / Subject Relevance"),
        ("[1]", "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). Introduction to Algorithms (4th ed.). MIT Press.", "Theoretical foundation for Binary Search Trees, Merge Sort, and Min-Heap Priority Queues."),
        ("[2]", "Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. Soviet Physics Doklady, 10(8), 707-710.", "Original mathematical formulation of string edit distance dynamic programming recurrence."),
        ("[3]", "Goodrich, M. T., Tamassia, R., & Goldwasser, M. H. (2013). Data Structures and Algorithms in Python. John Wiley & Sons.", "Implementation patterns for linked lists, stacks, queues, and graph traversals in Python."),
        ("[4]", "Django Software Foundation. (2026). Django Documentation: Model-View-Template Architecture & ORM. https://docs.djangoproject.com/", "Official architectural specifications for Django models, views, and authentication."),
        ("[5]", "Elmasri, R., & Navathe, S. B. (2016). Fundamentals of Database Systems (7th ed.). Pearson.", "Relational database design, Third Normal Form (3NF) normalization, and ACID transaction rules."),
        ("[6]", "Lutz, M. (2013). Learning Python (5th ed.). O'Reilly Media.", "Comprehensive reference for Python object model, memory management, and Tkinter GUI architecture."),
        ("[7]", "Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.). Pearson.", "Heuristic search, priority queues, and graph traversal methodologies.")
    ]
    add_table_data(bib_entries[0], bib_entries[1:], [0.8, 3.8, 2.0], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    out_file = os.path.abspath("Campus_Lost_and_Found_Project_Documentation.docx")
    doc.save(out_file)
    print(f"Document saved to: {out_file}")
    return out_file

if __name__ == "__main__":
    generate_mca_documentation()
