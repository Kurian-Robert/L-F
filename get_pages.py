import subprocess
import sys
import os

def get_word_page_count(docx_path):
    abs_path = os.path.abspath(docx_path)
    ps_script = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open('{abs_path}')
    $pages = $doc.ComputeStatistics(2)
    Write-Output "PAGE_COUNT: $pages"
    $doc.Close([ref]$false)
}} finally {{
    $word.Quit()
}}
"""
    ps_file = os.path.abspath("temp_count.ps1")
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_script)

    try:
        res = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file], capture_output=True, text=True, timeout=30)
        os.remove(ps_file)
        for line in res.stdout.splitlines():
            if "PAGE_COUNT:" in line:
                return int(line.split("PAGE_COUNT:")[1].strip())
    except Exception as e:
        print(f"Error checking pages: {e}")
        if os.path.exists(ps_file):
            os.remove(ps_file)
    return None

if __name__ == "__main__":
    test_path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\kuria\OneDrive\Documents\kurianminiprojdoc..docx"
    print("Checking:", test_path)
    pages = get_word_page_count(test_path)
    print("Computed pages:", pages)
