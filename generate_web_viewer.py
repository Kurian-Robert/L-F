import os

def create_web_viewer():
    svg1_path = "Figure_7_1_BST_Lookup_Flowchart.svg"
    svg2_path = "Figure_7_1_BST_Lookup_and_Deletion_Complete.svg"

    with open(svg1_path, "r", encoding="utf-8") as f:
        svg1_raw = f.read()
    with open(svg2_path, "r", encoding="utf-8") as f:
        svg2_raw = f.read()

    # Clean XML declaration from embedded strings if present
    svg1_clean = svg1_raw.split("?>")[-1].strip() if "?>" in svg1_raw else svg1_raw
    svg2_clean = svg2_raw.split("?>")[-1].strip() if "?>" in svg2_raw else svg2_raw

    mermaid_code1 = """flowchart TD
    classDef default fill:#FFFFFF,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef terminator fill:#FFFFFF,stroke:#000000,stroke-width:2px,rx:20px,ry:20px;
    classDef decision fill:#FFFFFF,stroke:#000000,stroke-width:2px;
    classDef process fill:#FFFFFF,stroke:#000000,stroke-width:1.8px;
    classDef connector fill:#000000,stroke:#000000,stroke-width:1.5px;

    Start(["Start BST Search\\nTarget ID, Root Node"]):::terminator
    LoopEntry((" ")):::connector

    CheckNull{"Current == NULL?"}:::decision
    NotFound(["Not Found\\nReturn False"]):::terminator

    CheckMatch{"Target == Current.Data?"}:::decision
    MatchFound(["Match Found\\nReturn Record / Node"]):::terminator

    CheckLess{"Target < Current.Data?"}:::decision
    TraverseLeft["Traverse Left Subtree\\nCurrent = Current.Left"]:::process
    TraverseRight["Traverse Right Subtree\\nCurrent = Current.Right"]:::process

    LoopExit((" ")):::connector

    Start --> LoopEntry
    LoopEntry --> CheckNull

    CheckNull -->|"Yes"| NotFound
    CheckNull -->|"No"| CheckMatch

    CheckMatch -->|"Yes"| MatchFound
    CheckMatch -->|"No"| CheckLess

    CheckLess -->|"Yes (Go Left)"| TraverseLeft
    CheckLess -->|"No (Go Right)"| TraverseRight

    TraverseLeft --> LoopExit
    TraverseRight --> LoopExit

    LoopExit -->|"Repeat Loop (Next Iteration)"| LoopEntry"""

    mermaid_code2 = """flowchart TD
    classDef default fill:#FFFFFF,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef terminator fill:#FFFFFF,stroke:#000000,stroke-width:2px,rx:20px,ry:20px;
    classDef decision fill:#FFFFFF,stroke:#000000,stroke-width:2px;
    classDef process fill:#FFFFFF,stroke:#000000,stroke-width:1.8px;
    classDef subcase fill:#FFFFFF,stroke:#000000,stroke-width:1.8px;
    classDef connector fill:#000000,stroke:#000000,stroke-width:1.5px;

    Start(["Start BST Operation\\nInput: Target ID, Root, Operation Type"]):::terminator
    LoopEntry((" ")):::connector

    CheckNull{"Current == NULL?"}:::decision
    NotFound(["Item Not Found\\nReturn False / NULL"]):::terminator

    CheckMatch{"Target == Current.Data?"}:::decision

    CheckOp{"Operation == SEARCH?"}:::decision
    SearchSuccess(["Search Success\\nReturn Found Node Record"]):::terminator

    CheckChildren{"Evaluate Node Degree\\nNumber of Children?"}:::decision

    Case0["Case 1: Leaf Node (0 Children)\\nDelete node cleanly\\nSet parent branch pointer = NULL"]:::subcase
    Case1["Case 2: Single Child (1 Child)\\nBypass deleted node\\nLink parent pointer directly to child"]:::subcase
    Case2["Case 3: Two Children (2 Children)\\nFind Inorder Successor S = min_node(Current.Right)\\nCopy S.Data into Current.Data\\nRecursively delete S from Right Subtree"]:::subcase

    DeleteDone(["Deletion Complete\\nReturn Balanced Subtree Root"]):::terminator

    CheckLess{"Target < Current.Data?"}:::decision
    TraverseLeft["Traverse Left Subtree\\nCurrent = Current.Left"]:::process
    TraverseRight["Traverse Right Subtree\\nCurrent = Current.Right"]:::process
    LoopExit((" ")):::connector

    Start --> LoopEntry
    LoopEntry --> CheckNull

    CheckNull -->|"Yes"| NotFound
    CheckNull -->|"No"| CheckMatch

    CheckMatch -->|"Yes (Match Found)"| CheckOp
    CheckOp -->|"Yes"| SearchSuccess
    CheckOp -->|"No (Execute Deletion)"| CheckChildren

    CheckChildren -->|"0 Children"| Case0
    CheckChildren -->|"1 Child"| Case1
    CheckChildren -->|"2 Children"| Case2

    Case0 --> DeleteDone
    Case1 --> DeleteDone
    Case2 --> DeleteDone

    CheckMatch -->|"No"| CheckLess
    CheckLess -->|"Yes (Go Left)"| TraverseLeft
    CheckLess -->|"No (Go Right)"| TraverseRight

    TraverseLeft --> LoopExit
    TraverseRight --> LoopExit
    LoopExit -->|"Repeat Loop"| LoopEntry"""

    viewer_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Figure 7.1: Binary Search Tree Flowchart | Campus Lost & Found System</title>
    <style>
        :root {{
            --bg-color: #F8FAFC;
            --surface-color: #FFFFFF;
            --primary-color: #0F172A;
            --accent-blue: #2563EB;
            --accent-hover: #1D4ED8;
            --border-color: #E2E8F0;
            --text-dark: #1E293B;
            --text-muted: #64748B;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-dark);
            line-height: 1.5;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }}

        /* Header */
        header {{
            background-color: var(--surface-color);
            border-bottom: 1px solid var(--border-color);
            padding: 16px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}

        .brand {{
            display: flex;
            flex-direction: column;
        }}

        .brand h1 {{
            font-size: 19px;
            font-weight: 700;
            color: var(--primary-color);
            letter-spacing: -0.3px;
        }}

        .brand p {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        .badge-bar {{
            display: flex;
            gap: 10px;
        }}

        .badge {{
            background: #EEF2F6;
            color: #334155;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid #CBD5E1;
        }}

        /* Main Workspace */
        main {{
            display: flex;
            flex: 1;
            overflow: hidden;
            height: calc(100vh - 75px);
        }}

        /* Left Canvas Viewport */
        .canvas-area {{
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #FFFFFF;
            position: relative;
            overflow: hidden;
        }}

        /* Viewport Toolbar */
        .toolbar {{
            background: #F1F5F9;
            border-bottom: 1px solid var(--border-color);
            padding: 10px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 10;
        }}

        .tab-group {{
            display: flex;
            gap: 6px;
            background: #E2E8F0;
            padding: 3px;
            border-radius: 8px;
        }}

        .tab-btn {{
            border: none;
            background: transparent;
            padding: 7px 16px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            color: #475569;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .tab-btn.active {{
            background: #FFFFFF;
            color: #0F172A;
            box-shadow: 0 1px 2px rgba(0,0,0,0.08);
        }}

        .controls-group {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 7px 14px;
            font-size: 13px;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
            text-decoration: none;
            border: 1px solid var(--border-color);
            background: #FFFFFF;
            color: var(--text-dark);
        }}

        .btn:hover {{
            background: #F8FAFC;
            border-color: #CBD5E1;
        }}

        .btn-primary {{
            background: var(--accent-blue);
            color: #FFFFFF;
            border-color: var(--accent-blue);
        }}

        .btn-primary:hover {{
            background: var(--accent-hover);
        }}

        /* Interactive SVG Container */
        .viewport-wrapper {{
            flex: 1;
            position: relative;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            cursor: grab;
            overflow: auto;
            background-image: radial-gradient(#E2E8F0 1px, transparent 1px);
            background-size: 20px 20px;
        }}

        .viewport-wrapper:active {{
            cursor: grabbing;
        }}

        .svg-canvas {{
            transform-origin: center center;
            transition: transform 0.08s ease-out;
            padding: 40px;
            display: flex;
            justify-content: center;
        }}

        .svg-canvas svg {{
            filter: drop-shadow(0 4px 12px rgba(0,0,0,0.06));
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 30px;
        }}

        /* Right Side Sidebar */
        aside {{
            width: 380px;
            background: var(--surface-color);
            border-left: 1px solid var(--border-color);
            padding: 24px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        .card {{
            background: #F8FAFC;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
        }}

        .card h3 {{
            font-size: 14px;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .card p, .card li {{
            font-size: 13px;
            color: #334155;
            line-height: 1.6;
        }}

        .card ul {{
            margin-left: 18px;
            margin-top: 6px;
        }}

        .complexity-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-top: 8px;
        }}

        .complexity-table th, .complexity-table td {{
            border: 1px solid #CBD5E1;
            padding: 6px 8px;
            text-align: left;
        }}

        .complexity-table th {{
            background: #F1F5F9;
            font-weight: 700;
        }}

        pre code {{
            display: block;
            background: #0F172A;
            color: #F8FAFC;
            font-family: Consolas, "Courier New", monospace;
            font-size: 11.5px;
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
            margin-top: 8px;
        }}

        .toast {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #0F172A;
            color: #FFFFFF;
            padding: 10px 18px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 500;
            opacity: 0;
            transition: opacity 0.2s ease;
            pointer-events: none;
            z-index: 1000;
        }}

        .toast.show {{
            opacity: 1;
        }}
    </style>
</head>
<body>

    <header>
        <div class="brand">
            <h1>Campus Lost & Found Management System</h1>
            <p>Figure 7.1: Phase 2 Binary Search Tree (BST) Lookup & Deletion Algorithm Flowchart</p>
        </div>
        <div class="badge-bar">
            <span class="badge">MCA Semester 1</span>
            <span class="badge">DSA (26MCD1L211)</span>
            <span class="badge">Kurian Robert (26MCAC28)</span>
        </div>
    </header>

    <main>
        <!-- Canvas Area -->
        <section class="canvas-area">
            <div class="toolbar">
                <div class="tab-group">
                    <button class="tab-btn active" id="tab1-btn" onclick="switchView('diag1')">
                        Figure 7.1: BST Lookup (Standard)
                    </button>
                    <button class="tab-btn" id="tab2-btn" onclick="switchView('diag2')">
                        Figure 7.1 Extended: Lookup & Deletion
                    </button>
                </div>

                <div class="controls-group">
                    <button class="btn" onclick="zoomIn()" title="Zoom In (+)">➕</button>
                    <button class="btn" onclick="zoomOut()" title="Zoom Out (-)">➖</button>
                    <button class="btn" onclick="resetZoom()" title="Reset Zoom">🔄 Reset (100%)</button>
                    <button class="btn btn-primary" onclick="downloadCurrentSVG()">⬇ Download SVG</button>
                    <button class="btn" onclick="copyMermaid()">📋 Copy Mermaid</button>
                </div>
            </div>

            <div class="viewport-wrapper" id="viewport" onwheel="handleWheel(event)" onmousedown="startPan(event)">
                <div class="svg-canvas" id="canvas">
                    <div id="view-diag1" style="display: block;">
                        {svg1_clean}
                    </div>
                    <div id="view-diag2" style="display: none;">
                        {svg2_clean}
                    </div>
                </div>
            </div>
        </section>

        <!-- Technical Sidebar -->
        <aside>
            <div class="card">
                <h3>📐 Traditional Flowchart Standards</h3>
                <p>Constructed in strict accordance with ANSI/ISO computer science flowcharting standards:</p>
                <ul>
                    <li><strong>Stadium (Pill):</strong> Terminal boundaries (<code>Start</code>, <code>Not Found</code>, <code>Match Found</code>).</li>
                    <li><strong>Rhombus (Diamond):</strong> Branching decisions (<code>Current == NULL?</code>, <code>Target &lt; Current.Data?</code>).</li>
                    <li><strong>Rectangle:</strong> Sequential processes (<code>Current = Current.Left</code>).</li>
                    <li><strong>Non-Crossing Outer Bus:</strong> Loopback arrows route cleanly along the outer perimeter with zero line-crossing.</li>
                </ul>
            </div>

            <div class="card">
                <h3>⚡ Space & Time Complexity</h3>
                <table class="complexity-table">
                    <thead>
                        <tr>
                            <th>Operation</th>
                            <th>Time (Avg)</th>
                            <th>Time (Worst)</th>
                            <th>Space</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>BST Lookup</td>
                            <td><strong>O(log n)</strong></td>
                            <td>O(n)</td>
                            <td>O(1) aux</td>
                        </tr>
                        <tr>
                            <td>BST Deletion</td>
                            <td><strong>O(log n)</strong></td>
                            <td>O(n)</td>
                            <td>O(h) stack</td>
                        </tr>
                        <tr>
                            <td>Traversals</td>
                            <td>O(n)</td>
                            <td>O(n)</td>
                            <td>O(n) output</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="card">
                <h3>✂️ Three Deletion Cases Handled</h3>
                <p>When the target node is located, three structural cases are resolved in <code>binary_tree.py</code>:</p>
                <ul>
                    <li><strong>Case 1 (Leaf Node):</strong> 0 children &rarr; Remove node and set parent pointer to <code>NULL</code>.</li>
                    <li><strong>Case 2 (Single Child):</strong> 1 child &rarr; Replace node directly with its active child pointer.</li>
                    <li><strong>Case 3 (Two Children):</strong> 2 children &rarr; Find Inorder Successor (minimum node in right subtree), copy value, and recursively excise successor.</li>
                </ul>
            </div>

            <div class="card">
                <h3>🐍 Python Implementation Excerpt</h3>
                <p>Corresponds to <code>campuslostfound/binary_tree.py</code>:</p>
                <pre><code>def search(self, value):
    current = self.root
    while current:
        if current.data == value:
            return True
        elif value < current.data:
            current = current.left
        else:
            current = current.right
    return False</code></pre>
            </div>
        </aside>
    </main>

    <div class="toast" id="toast">Copied to clipboard!</div>

    <script>
        let currentView = 'diag1';
        let scale = 1.0;
        let panX = 0;
        let panY = 0;
        let isDragging = false;
        let startX, startY;

        const canvas = document.getElementById('canvas');
        const viewport = document.getElementById('viewport');

        const mermaid1 = `{mermaid_code1.replace('`', '\\`')}`;
        const mermaid2 = `{mermaid_code2.replace('`', '\\`')}`;

        function switchView(viewName) {{
            currentView = viewName;
            document.getElementById('view-diag1').style.display = viewName === 'diag1' ? 'block' : 'none';
            document.getElementById('view-diag2').style.display = viewName === 'diag2' ? 'block' : 'none';

            document.getElementById('tab1-btn').classList.toggle('active', viewName === 'diag1');
            document.getElementById('tab2-btn').classList.toggle('active', viewName === 'diag2');

            resetZoom();
        }}

        function updateTransform() {{
            canvas.style.transform = `translate(${{panX}}px, ${{panY}}px) scale(${{scale}})`;
        }}

        function zoomIn() {{
            scale = Math.min(scale * 1.2, 3.0);
            updateTransform();
        }}

        function zoomOut() {{
            scale = Math.max(scale / 1.2, 0.4);
            updateTransform();
        }}

        function resetZoom() {{
            scale = 1.0;
            panX = 0;
            panY = 0;
            updateTransform();
        }}

        function handleWheel(e) {{
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            scale = Math.min(Math.max(scale * delta, 0.4), 3.0);
            updateTransform();
        }}

        function startPan(e) {{
            if (e.target.tagName === 'BUTTON' || e.target.closest('button')) return;
            isDragging = true;
            startX = e.clientX - panX;
            startY = e.clientY - panY;

            window.addEventListener('mousemove', onPan);
            window.addEventListener('mouseup', endPan);
        }}

        function onPan(e) {{
            if (!isDragging) return;
            panX = e.clientX - startX;
            panY = e.clientY - startY;
            updateTransform();
        }}

        function endPan() {{
            isDragging = false;
            window.removeEventListener('mousemove', onPan);
            window.removeEventListener('mouseup', endPan);
        }}

        function downloadCurrentSVG() {{
            const svgElement = currentView === 'diag1' 
                ? document.querySelector('#view-diag1 svg') 
                : document.querySelector('#view-diag2 svg');

            const serializer = new XMLSerializer();
            const svgStr = '<?xml version="1.0" encoding="UTF-8"?>\\n' + serializer.serializeToString(svgElement);
            const blob = new Blob([svgStr], {{ type: 'image/svg+xml;charset=utf-8' }});
            const url = URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = currentView === 'diag1' 
                ? 'Figure_7_1_BST_Lookup_Flowchart.svg' 
                : 'Figure_7_1_BST_Lookup_and_Deletion_Complete.svg';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast('SVG Download initiated!');
        }}

        function copyMermaid() {{
            const textToCopy = currentView === 'diag1' ? mermaid1 : mermaid2;
            navigator.clipboard.writeText(textToCopy).then(() => {{
                showToast('Mermaid code copied to clipboard!');
            }}).catch(() => {{
                showToast('Failed to copy code.');
            }});
        }}

        function showToast(msg) {{
            const toast = document.getElementById('toast');
            toast.innerText = msg;
            toast.classList.add('show');
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, 2200);
        }}
    </script>
</body>
</html>
"""

    viewer_path = "Figure_7_1_BST_Flowchart_Viewer.html"
    with open(viewer_path, "w", encoding="utf-8") as f:
        f.write(viewer_html)
    print(f"Successfully generated {viewer_path} ({os.path.getsize(viewer_path)} bytes)")

if __name__ == "__main__":
    create_web_viewer()
