"""Render REVIEW.md to REVIEW.pdf.

Pipeline: python-markdown (tables + smarty off, so the text stays
byte-faithful) -> styled HTML -> Chrome headless print-to-pdf.
Run from anywhere:  python3 masselot-review/make_pdf.py
"""

import os
import subprocess
import sys

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "REVIEW.md")
HTML = os.path.join(HERE, "out", "REVIEW.html")
PDF = os.path.join(HERE, "REVIEW.pdf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

CSS = """
@page { size: A4; margin: 22mm 20mm; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt;
       line-height: 1.45; color: #111; max-width: 100%; }
h1 { font-size: 15pt; line-height: 1.3; margin: 0 0 10pt 0; }
h2 { font-size: 12pt; margin: 16pt 0 6pt 0;
     border-bottom: 0.5pt solid #999; padding-bottom: 2pt; }
p { margin: 6pt 0; text-align: justify; }
ol, ul { margin: 6pt 0; padding-left: 18pt; }
li { margin: 4pt 0; text-align: justify; }
code { font-family: Menlo, 'Courier New', monospace; font-size: 9pt;
       background: #f2f2f2; padding: 0 2pt; }
pre { font-family: Menlo, 'Courier New', monospace; font-size: 9pt;
      background: #f5f5f5; border: 0.5pt solid #ccc; padding: 6pt 8pt;
      white-space: pre-wrap; }
table { border-collapse: collapse; width: 100%; font-size: 8.7pt;
        margin: 8pt 0; page-break-inside: auto; }
th, td { border: 0.5pt solid #888; padding: 4pt 5pt; vertical-align: top;
         text-align: left; overflow-wrap: break-word; }
th { background: #eee; }
tr { page-break-inside: avoid; }
"""


def main():
    with open(SRC) as f:
        text = f.read()
    body = markdown.markdown(text, extensions=["tables"])
    os.makedirs(os.path.dirname(HTML), exist_ok=True)
    with open(HTML, "w") as f:
        f.write(
            "<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{CSS}</style></head><body>{body}</body></html>"
        )
    r = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu",
         "--no-pdf-header-footer", f"--print-to-pdf={PDF}", HTML],
        capture_output=True, text=True, timeout=120)
    if not os.path.exists(PDF):
        print(r.stdout, r.stderr)
        sys.exit(1)
    print(f"wrote {PDF} ({os.path.getsize(PDF)} bytes)")


if __name__ == "__main__":
    main()
