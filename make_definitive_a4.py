import subprocess
import os
import re
import shutil

def build_definitive_orthogonal_a4():
    # 1. Mermaid code: strictly horizontal and vertical lines, compact text, traditional ANSI styling
    mermaid_ortho = """flowchart TD
    classDef default fill:#FFFFFF,stroke:#000000,stroke-width:1.2px,color:#000000;
    classDef term fill:#FFFFFF,stroke:#000000,stroke-width:1.5px,rx:15px,ry:15px;
    classDef dec fill:#FFFFFF,stroke:#000000,stroke-width:1.5px;
    classDef proc fill:#FFFFFF,stroke:#000000,stroke-width:1.2px;
    classDef conn fill:#000000,stroke:#000000,stroke-width:1px;

    Start(["Start BST Search\\nTarget, Root"]):::term
    TopEntry((" ")):::conn

    CheckNull{"Current == NULL?"}:::dec
    NotFound(["Not Found\\nReturn False"]):::term

    CheckMatch{"Target == Node.Data?"}:::dec
    MatchFound(["Match Found\\nReturn Node"]):::term

    CheckLess{"Target < Node.Data?"}:::dec
    GoLeft["Go Left\\nCurr = Curr.Left"]:::proc
    GoRight["Go Right\\nCurr = Curr.Right"]:::proc

    BotRail((" ")):::conn

    Start --> TopEntry
    TopEntry --> CheckNull

    CheckNull -->|"Yes"| NotFound
    CheckNull -->|"No"| CheckMatch

    CheckMatch -->|"Yes"| MatchFound
    CheckMatch -->|"No"| CheckLess

    CheckLess -->|"Yes"| GoLeft
    CheckLess -->|"No"| GoRight

    GoLeft --> BotRail
    GoRight --> BotRail

    BotRail -->|"Loop"| TopEntry
"""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="mermaid.min.js"></script>
    <script>
        window.addEventListener('DOMContentLoaded', async () => {{
            mermaid.initialize({{
                startOnLoad: false,
                theme: 'base',
                themeVariables: {{
                    fontFamily: 'Times New Roman, serif',
                    fontSize: '11px',
                    primaryColor: '#FFFFFF',
                    primaryBorderColor: '#000000',
                    primaryTextColor: '#000000',
                    lineColor: '#000000'
                }},
                flowchart: {{
                    curve: 'stepAfter',
                    nodeSpacing: 45,
                    rankSpacing: 45,
                    htmlLabels: false
                }}
            }});

            const def = `{mermaid_ortho}`;
            const res = await mermaid.render('render_ortho_a4', def);
            document.getElementById('out').innerHTML = res.svg;
            document.getElementById('status').innerText = 'READY';
        }});
    </script>
</head>
<body>
    <div id="status">INIT</div>
    <div id="out"></div>
</body>
</html>
"""

    tmp_html = "build_ortho_temp.html"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(html)

    abs_html = os.path.abspath(tmp_html).replace(os.sep, '/')
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
        m = re.search(r'<div id="out">([\s\S]*?)</div>', res.stdout)
        if m:
            svg = m.group(1).strip()
            svg = svg.replace('&amp;lt;', '&lt;')
            header = '<?xml version="1.0" encoding="UTF-8"?>\n<!-- Figure 7.1: Phase 2: Binary Search Tree (BST) Lookup Flowchart (Orthogonal Lines & A4 Fit) -->\n'
            full_svg = header + svg

            # Write Figure_7_1_BST_Orthogonal_A4.svg
            with open("Figure_7_1_BST_Orthogonal_A4.svg", "w", encoding="utf-8") as f:
                f.write(full_svg)
            # Also update Figure_7_1_BST_Lookup_Flowchart.svg so the main file name is updated
            with open("Figure_7_1_BST_Lookup_Flowchart.svg", "w", encoding="utf-8") as f:
                f.write(full_svg)
            print("Successfully written Figure_7_1_BST_Orthogonal_A4.svg & Figure_7_1_BST_Lookup_Flowchart.svg")

            # Capture High-Res PNG (300 DPI layout on A4 aspect ratio)
            standalone_html = f"""<!DOCTYPE html>
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
    font-size: 16px;
    font-weight: bold;
    color: #000000;
    margin-bottom: 15px;
    text-align: center;
    border-bottom: 2px solid #000000;
    padding-bottom: 5px;
    width: 90%;
  }}
  .svg-wrap {{
    display: flex;
    justify-content: center;
    width: 100%;
  }}
  svg {{
    max-width: 95%;
    height: auto;
  }}
</style>
</head>
<body>
  <div class="title-header">Figure 7.1: Binary Search Tree (BST) Lookup Algorithm Flowchart</div>
  <div class="svg-wrap">{svg}</div>
</body>
</html>"""
            tmp_shot_html = "build_ortho_shot.html"
            with open(tmp_shot_html, "w", encoding="utf-8") as f:
                f.write(standalone_html)

            abs_shot_html = os.path.abspath(tmp_shot_html).replace(os.sep, '/')
            abs_png = os.path.abspath("Figure_7_1_BST_Orthogonal_A4.png")
            cmd_shot = [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "--headless=new",
                "--disable-gpu",
                "--virtual-time-budget=2000",
                "--window-size=1000,1200",
                f"--screenshot={abs_png}",
                f"file:///{abs_shot_html}"
            ]
            subprocess.run(cmd_shot, capture_output=True)
            print(f"Captured {abs_png}")

            # Also update Figure_7_1_BST_Lookup_Flowchart.png and doc_images/flowchart_phase2_bst.png
            shutil.copyfile(abs_png, os.path.abspath("Figure_7_1_BST_Lookup_Flowchart.png"))
            shutil.copyfile(abs_png, os.path.abspath("doc_images/flowchart_phase2_bst.png"))
            print("Updated Figure_7_1_BST_Lookup_Flowchart.png and doc_images/flowchart_phase2_bst.png")

    # Clean up temp runner files
    for f_del in [tmp_html, "build_ortho_shot.html"]:
        if os.path.exists(f_del):
            os.remove(f_del)

if __name__ == "__main__":
    build_definitive_orthogonal_a4()

