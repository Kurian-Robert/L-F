import subprocess
import os
import re

# Script to generate both SVGs and the viewer HTML

def generate_flowcharts():
    # 1. Mermaid code for Diagram 1: Classic BST Lookup Flowchart (Exact Figure 7.1)
    mermaid_diag1 = """flowchart TD
    classDef default fill:#FFFFFF,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef terminator fill:#FFFFFF,stroke:#000000,stroke-width:2px,rx:20px,ry:20px;
    classDef decision fill:#FFFFFF,stroke:#000000,stroke-width:2px;
    classDef process fill:#FFFFFF,stroke:#000000,stroke-width:1.8px;
    classDef connector fill:#000000,stroke:#000000,stroke-width:1.5px;

    Start(["Start BST Search / Lookup<br/><b>Input: Target ID, Root Node</b>"]):::terminator
    
    LoopEntry((" ")):::connector

    CheckNull{"Current == NULL?"}:::decision
    NotFound(["<b>Item Not Found</b><br/>Return False"]):::terminator
    
    CheckMatch{"Target == Current.Data?"}:::decision
    MatchFound(["<b>Match Found!</b><br/>Return Record / Node"]):::terminator
    
    CheckLess{"Target < Current.Data?"}:::decision
    
    TraverseLeft["Traverse Left Subtree<br/><b>Current = Current.Left</b>"]:::process
    TraverseRight["Traverse Right Subtree<br/><b>Current = Current.Right</b>"]:::process
    
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
    
    LoopExit -->|"Repeat Loop (Next Iteration)"| LoopEntry
"""

    # 2. Mermaid code for Diagram 2: Complete BST Lookup & Deletion Algorithm
    mermaid_diag2 = """flowchart TD
    classDef default fill:#FFFFFF,stroke:#000000,stroke-width:1.5px,color:#000000;
    classDef terminator fill:#FFFFFF,stroke:#000000,stroke-width:2px,rx:20px,ry:20px;
    classDef decision fill:#FFFFFF,stroke:#000000,stroke-width:2px;
    classDef process fill:#FFFFFF,stroke:#000000,stroke-width:1.8px;
    classDef subcase fill:#F8FAFC,stroke:#000000,stroke-width:1.5px;
    classDef connector fill:#000000,stroke:#000000,stroke-width:1.5px;

    Start(["Start BST Operation<br/><b>Input: Target ID, Root, Operation Type</b>"]):::terminator
    LoopEntry((" ")):::connector

    CheckNull{"Current == NULL?"}:::decision
    NotFound(["<b>Item Not Found</b><br/>Return False / NULL"]):::terminator

    CheckMatch{"Target == Current.Data?"}:::decision

    CheckOp{"Operation == SEARCH?"}:::decision
    SearchSuccess(["<b>Search Success</b><br/>Return Found Node Record"]):::terminator

    CheckChildren{"Evaluate Node Degree<br/><b>Number of Children?</b>"}:::decision

    Case0["<b>Case 1: Leaf Node (0 Children)</b><br/>Delete node cleanly<br/>Set parent branch pointer = NULL"]:::subcase
    Case1["<b>Case 2: Single Child (1 Child)</b><br/>Bypass deleted node<br/>Link parent pointer directly to child"]:::subcase
    Case2["<b>Case 3: Two Children (2 Children)</b><br/>Find Inorder Successor S = min_node(Current.Right)<br/>Copy S.Data into Current.Data<br/>Recursively delete S from Right Subtree"]:::subcase

    DeleteDone(["<b>Deletion Complete</b><br/>Return Balanced Subtree Root"]):::terminator

    CheckLess{"Target < Current.Data?"}:::decision
    TraverseLeft["Traverse Left Subtree<br/><b>Current = Current.Left</b>"]:::process
    TraverseRight["Traverse Right Subtree<br/><b>Current = Current.Right</b>"]:::process
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
    LoopExit -->|"Repeat Loop"| LoopEntry
"""

    # Create HTML generator that Chrome can load to export both pure SVGs
    html_exporter = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SVG Exporter</title>
    <script src="mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: false,
            theme: 'base',
            themeVariables: {{
                fontFamily: 'Times New Roman, serif',
                fontSize: '13px',
                primaryColor: '#FFFFFF',
                primaryBorderColor: '#000000',
                primaryTextColor: '#000000',
                lineColor: '#000000',
                edgeLabelBackground: '#FFFFFF'
            }},
            flowchart: {{
                curve: 'linear',
                nodeSpacing: 50,
                rankSpacing: 55,
                htmlLabels: false
            }}
        }});

        window.addEventListener('DOMContentLoaded', async () => {{
            try {{
                const def1 = `{mermaid_diag1}`;
                const res1 = await mermaid.render('svg_diag1', def1);
                document.getElementById('container1').innerHTML = res1.svg;

                const def2 = `{mermaid_diag2}`;
                const res2 = await mermaid.render('svg_diag2', def2);
                document.getElementById('container2').innerHTML = res2.svg;

                document.getElementById('status').innerText = 'EXPORTS_READY';
            }} catch (e) {{
                document.getElementById('status').innerText = 'ERROR: ' + e.message;
            }}
        }});
    </script>
</head>
<body>
    <div id="status">LOADING</div>
    <div id="container1"></div>
    <div id="container2"></div>
</body>
</html>
"""

    with open("exporter_runner.html", "w", encoding="utf-8") as f:
        f.write(html_exporter)

    abs_html = os.path.abspath("exporter_runner.html").replace(os.sep, '/')
    cmd = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=4000",
        "--dump-dom",
        f"file:///{abs_html}"
    ]
    res = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")
    
    if "EXPORTS_READY" in res.stdout:
        print("DOM rendered successfully!")
        
        # Extract SVG 1
        m1 = re.search(r'<div id="container1">([\s\S]*?)</div>', res.stdout)
        if m1:
            svg1 = m1.group(1).strip()
            # Wrap properly with standard xml declaration and clean styling
            with open("Figure_7_1_BST_Lookup_Flowchart.svg", "w", encoding="utf-8") as f:
                f.write(svg1)
            print("Generated Figure_7_1_BST_Lookup_Flowchart.svg (Bytes:", len(svg1), ")")
            
        # Extract SVG 2
        m2 = re.search(r'<div id="container2">([\s\S]*?)</div>', res.stdout)
        if m2:
            svg2 = m2.group(1).strip()
            with open("Figure_7_1_BST_Lookup_and_Deletion_Complete.svg", "w", encoding="utf-8") as f:
                f.write(svg2)
            print("Generated Figure_7_1_BST_Lookup_and_Deletion_Complete.svg (Bytes:", len(svg2), ")")
    else:
        print("Export failed! Output preview:", res.stdout[:500])

if __name__ == "__main__":
    generate_flowcharts()
