import subprocess
import os
import re

def build_all_flowcharts():
    # 1. Mermaid code for Figure 7.1 Classic BST Lookup Flowchart
    mermaid_classic = """flowchart TD
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

    LoopExit -->|"Repeat Loop (Next Iteration)"| LoopEntry
"""

    # 2. Mermaid code for Figure 7.1 Extended Complete BST Lookup & Deletion Algorithm
    mermaid_extended = """flowchart TD
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
    LoopExit -->|"Repeat Loop"| LoopEntry
"""

    # HTML builder to execute in Chrome headless
    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Generator</title>
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
                rankSpacing: 50,
                htmlLabels: false
            }}
        }});

        window.addEventListener('DOMContentLoaded', async () => {{
            try {{
                const def1 = `{mermaid_classic}`;
                const res1 = await mermaid.render('svg_classic', def1);
                document.getElementById('c1').innerHTML = res1.svg;

                const def2 = `{mermaid_extended}`;
                const res2 = await mermaid.render('svg_extended', def2);
                document.getElementById('c2').innerHTML = res2.svg;

                document.getElementById('status').innerText = 'READY';
            }} catch(err) {{
                document.getElementById('status').innerText = 'ERR: ' + err.message;
            }}
        }});
    </script>
</head>
<body>
    <div id="status">INIT</div>
    <div id="c1"></div>
    <div id="c2"></div>
</body>
</html>
"""
    with open("temp_generator.html", "w", encoding="utf-8") as f:
        f.write(html_template)

    abs_html = os.path.abspath("temp_generator.html").replace(os.sep, '/')
    cmd = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "--headless=new",
        "--disable-gpu",
        "--virtual-time-budget=3000",
        "--dump-dom",
        f"file:///{abs_html}"
    ]
    res = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    if "READY" in res.stdout:
        print("DOM parsed successfully!")
        
        # 1. Save Classic SVG
        m1 = re.search(r'<div id="c1">([\s\S]*?)</div>', res.stdout)
        if m1:
            svg1 = m1.group(1).strip()
            svg1 = svg1.replace('&amp;lt;', '&lt;')
            # Add XML header if not present
            header = '<?xml version="1.0" encoding="UTF-8"?>\n<!-- Figure 7.1: Phase 2: Binary Search Tree (BST) Lookup Flowchart -->\n'
            full_svg1 = header + svg1
            with open("Figure_7_1_BST_Lookup_Flowchart.svg", "w", encoding="utf-8") as f:
                f.write(full_svg1)
            print("Successfully written Figure_7_1_BST_Lookup_Flowchart.svg")

        # 2. Save Extended SVG
        m2 = re.search(r'<div id="c2">([\s\S]*?)</div>', res.stdout)
        if m2:
            svg2 = m2.group(1).strip()
            svg2 = svg2.replace('&amp;lt;', '&lt;')
            header = '<?xml version="1.0" encoding="UTF-8"?>\n<!-- Figure 7.1: Phase 2: Binary Search Tree (BST) Lookup & Deletion Algorithm Flowchart -->\n'
            full_svg2 = header + svg2
            with open("Figure_7_1_BST_Lookup_and_Deletion_Complete.svg", "w", encoding="utf-8") as f:
                f.write(full_svg2)
            print("Successfully written Figure_7_1_BST_Lookup_and_Deletion_Complete.svg")

        # 3. Generate PNG previews for both
        for svg_file, png_file in [
            ("Figure_7_1_BST_Lookup_Flowchart.svg", "Figure_7_1_BST_Lookup_Flowchart.png"),
            ("Figure_7_1_BST_Lookup_and_Deletion_Complete.svg", "Figure_7_1_BST_Lookup_and_Deletion_Complete.png")
        ]:
            svg_content = open(svg_file, "r", encoding="utf-8").read()
            # Title banner for academic documentation
            fig_title = "Figure 7.1: Binary Search Tree (BST) Lookup Algorithm Flowchart" if "Lookup_Flowchart" in svg_file else "Figure 7.1: Binary Search Tree (BST) Lookup & Deletion Algorithm Flowchart"
            preview_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    margin: 0;
    padding: 30px;
    background: #FFFFFF;
    font-family: 'Times New Roman', serif;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .title-header {{
    font-size: 18px;
    font-weight: bold;
    color: #000000;
    margin-bottom: 20px;
    text-align: center;
    border-bottom: 2px solid #000000;
    padding-bottom: 6px;
    width: 90%;
  }}
  .svg-wrap {{
    display: flex;
    justify-content: center;
    width: 100%;
  }}
  svg {{
    max-width: 100%;
    height: auto;
  }}
</style>
</head>
<body>
  <div class="title-header">{fig_title}</div>
  <div class="svg-wrap">{svg_content}</div>
</body>
</html>"""
            tmp_preview = f"tmp_{png_file}.html"
            with open(tmp_preview, "w", encoding="utf-8") as f:
                f.write(preview_html)

            h_size = "1300" if "Lookup_Flowchart" in svg_file else "1750"
            cmd_shot = [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "--headless=new",
                "--disable-gpu",
                "--virtual-time-budget=2000",
                f"--window-size=1200,{h_size}",
                f"--screenshot={os.path.abspath(png_file)}",
                f"file:///{os.path.abspath(tmp_preview).replace(os.sep, '/')}"
            ]
            subprocess.run(cmd_shot, capture_output=True)
            print(f"Captured {png_file}")

        # Also copy Figure_7_1_BST_Lookup_Flowchart.png to doc_images/flowchart_phase2_bst.png
        import shutil
        target_doc_img = os.path.abspath("doc_images/flowchart_phase2_bst.png")
        shutil.copyfile(os.path.abspath("Figure_7_1_BST_Lookup_Flowchart.png"), target_doc_img)
        print(f"Updated {target_doc_img} with clean traditional visual!")

if __name__ == "__main__":
    build_all_flowcharts()

