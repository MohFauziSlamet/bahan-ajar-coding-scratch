#!/usr/bin/env python3
"""Render markdown juknis/modul -> HTML A4 siap di-print Chrome headless.

Dipakai lewat _build_pdf.sh. Diagram ```mermaid dirender jadi SVG memakai
mermaid UMD lokal (vendor/mermaid.min.js), bukan CDN, agar hasilnya deterministik.
"""
import html
import pathlib
import re
import sys

from markdown_it import MarkdownIt

SRC = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else SRC / "_build").resolve()

CSS = """
:root { --ink:#1a1a1a; --muted:#5a5a5a; --line:#c9ccd1; --accent:#0f4c81; --band:#eef2f7; }
@page { size: A4; margin: 16mm 14mm 16mm 14mm; }
* { box-sizing: border-box; }
body {
  margin: 0; color: var(--ink); background: #fff;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 10.5pt; line-height: 1.5;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}
h1, h2, h3, h4 { break-after: avoid; page-break-after: avoid; color: var(--accent); line-height: 1.25; }
h1 { font-size: 19pt; margin: 0 0 6px; letter-spacing: -.2px; }
h2 { font-size: 13.5pt; margin: 18px 0 8px; padding: 5px 9px;
     background: var(--band); border-left: 4px solid var(--accent); border-radius: 2px; }
h3 { font-size: 11.5pt; margin: 14px 0 6px; color: #17324d; }
h4 { font-size: 10.5pt; margin: 12px 0 5px; color: #17324d; }
p { margin: 6px 0; orphans: 2; widows: 2; }
strong { color: #10233a; }
em { color: #33415c; }
hr { border: 0; border-top: 1px solid var(--line); margin: 12px 0; }
a { color: var(--accent); text-decoration: none; }

ul, ol { margin: 6px 0 6px 0; padding-left: 20px; }
li { margin: 3px 0; break-inside: avoid; }

blockquote {
  margin: 8px 0; padding: 7px 11px; background: #fbf7e8;
  border-left: 4px solid #e0b53a; border-radius: 2px; break-inside: avoid;
}
blockquote p { margin: 3px 0; }

table { width: 100%; border-collapse: collapse; margin: 9px 0; font-size: 9pt; }
th, td { border: 1px solid var(--line); padding: 5px 7px; text-align: left; vertical-align: top; }
th { background: var(--band); color: #10233a; font-weight: 600; }
tbody tr:nth-child(even) { background: #fafbfc; }
tr { break-inside: avoid; }

code { font-family: Menlo, "DejaVu Sans Mono", Consolas, monospace; font-size: .88em;
       background: #f1f3f5; padding: 1px 4px; border-radius: 3px; color: #b02a37; }

pre { margin: 9px 0; padding: 8px 10px; background: #fbfcfd;
      border: 1px solid var(--line); border-radius: 3px; break-inside: avoid; }
pre code { background: none; padding: 0; color: var(--ink); border-radius: 0; }
/* blok tanpa bahasa = ASCII art -> JANGAN dibungkus baris */
/* line-height HARUS 1.0: glyph box-drawing Menlo tepat setinggi 1em,
   lebih dari itu garis vertikal ┃ putus-putus antar baris. */
pre.ascii { white-space: pre; overflow: hidden; }
pre.ascii code { font-size: 8.4pt; line-height: 1.0; display: block; }
/* blok ```text = prosa panjang (prompt AI) -> boleh membungkus */
pre.prose { white-space: pre-wrap; overflow-wrap: anywhere; }
pre.prose code { font-size: 8.6pt; line-height: 1.45; }

img { max-width: 100%; max-height: 218mm; display: block; margin: 8px auto; }
p:has(img) { break-inside: avoid; text-align: center; }

pre.mermaid { background: none; border: 0; padding: 0; text-align: center;
              break-inside: avoid; white-space: pre; }
/* mermaid menaruh max-width inline pada <svg>; tanpa !important diagram tinggi
   meluber keluar halaman dan terpotong saat dicetak. */
pre.mermaid svg { width: auto !important; height: auto !important;
                  max-width: 100% !important; max-height: 240mm !important; }

.doc-foot { margin-top: 20px; padding-top: 7px; border-top: 1px solid var(--line);
            font-size: 8pt; color: var(--muted); text-align: center; }
"""

MERMAID = """
<script src="file://{vendor}/mermaid.min.js"></script>
<script>
  mermaid.initialize({{ startOnLoad: false, theme: 'neutral',
                       flowchart: {{ useMaxWidth: true, htmlLabels: true, curve: 'basis' }},
                       themeVariables: {{ fontFamily: 'Helvetica Neue, Helvetica, Arial, sans-serif',
                                         fontSize: '15px' }} }});
  window.mermaidDone = false;
  mermaid.run({{ querySelector: 'pre.mermaid' }})
    .then(function () {{ window.mermaidDone = true; document.title += ' [MERMAID-OK]'; }})
    .catch(function (e) {{ window.mermaidDone = 'error'; document.title += ' [MERMAID-FAIL]'; }});
</script>
"""

TEMPLATE = """<!doctype html>
<html lang="id"><head>
<meta charset="utf-8">
<base href="file://{base}/">
<title>{title}</title>
<style>{css}</style>
</head><body>
{body}
<div class="doc-foot">{foot}</div>
{mermaid}
</body></html>
"""


# Emoji yang secara default berpresentasi TEKS. Tanpa U+FE0F sebagian tak punya glyph
# di font teks macOS dan tercetak sebagai kotak kosong (mis. 🖱 di diagram Babak 4).
TEXT_DEFAULT_EMOJI = "\u2764\u2694\U0001F6E1\u2708\U0001F5B1\u2601\u23F1"


def pre_transform(src: str) -> str:
    """Normalisasi yang TIDAK menghapus konten, hanya mengganti notasi agar tampil benar."""
    # Fence verbatim (ASCII-art & ```text) HARUS dibiarkan apa adanya: emoji lebar ganda
    # merusak perataan kolom kotak, dan contoh sintaks yang dikutip untuk siswa tidak
    # boleh ikut ditulis ulang. Fence ```mermaid ikut dinormalisasi (jadi SVG, bukan teks).
    parts = re.split(r"(?ms)(^```.*?^```)", src)
    for i, part in enumerate(parts):
        is_verbatim_fence = part.startswith("```") and not part.startswith("```mermaid")
        if is_verbatim_fence:
            continue
        part = re.sub(f"([{TEXT_DEFAULT_EMOJI}])(?!\ufe0f)", "\\1\ufe0f", part)
        # LaTeX inline dari sumber -> panah unicode
        part = part.replace(r"$\rightarrow$", "→")
        # GFM task list (tak ada plugin tasklist) -> kotak centang cetak
        part = re.sub(r"^(\s*)-\s\[ \]\s", r"\1- ☐ ", part, flags=re.M)
        parts[i] = re.sub(r"^(\s*)-\s\[[xX]\]\s", r"\1- ☑ ", part, flags=re.M)
    return "".join(parts)


def render(md_path: pathlib.Path) -> str:
    src = pre_transform(md_path.read_text(encoding="utf-8"))
    md = MarkdownIt("gfm-like", {"html": False, "linkify": False, "typographer": False})

    def fence(self, tokens, idx, options, env):
        tok = tokens[idx]
        info = (tok.info or "").strip().lower()
        if info == "mermaid":
            return f'<pre class="mermaid">{html.escape(tok.content)}</pre>\n'
        cls = "prose" if info else "ascii"
        return f'<pre class="{cls}"><code>{html.escape(tok.content)}</code></pre>\n'

    md.add_render_rule("fence", fence)
    body = md.render(src)
    title = re.search(r"^#\s+(.+)$", src, re.M)
    return TEMPLATE.format(
        base=html.escape(str(SRC)),
        css=CSS,
        title=html.escape(title.group(1) if title else md_path.stem),
        body=body,
        mermaid=MERMAID.format(vendor=str(OUT.parent / "vendor")) if "mermaid" in body else "",
        foot=html.escape(f"{md_path.name} · OISEN 2026 · MGMP Informatika & KKA SMP Kab. Malang"),
    )


def selftest() -> None:
    """python3 _md2pdf.py --selftest — isi fence harus lolos dari semua substitusi."""
    kasus = (
        "```text\nContoh sintaks: - [ ] centang, panah $\\rightarrow$ begini\n```\n\n"
        "- [ ] Tugas nyata di luar fence $\\rightarrow$ 2\n"
    )
    hasil = pre_transform(kasus)
    dalam, luar = hasil.split("```")[1], hasil.split("```")[2]
    assert "- [ ]" in dalam and r"$\rightarrow$" in dalam, "isi fence ikut diubah"
    assert "- ☐ " in luar and "→" in luar, "teks di luar fence tidak dikonversi"
    # emoji default-teks: dapat U+FE0F di teks biasa, TIDAK di dalam fence
    assert pre_transform("Klik \U0001F5B1 di sini") == "Klik \U0001F5B1️ di sini"
    assert pre_transform("```\n│ \U0001F5B1 │\n```") == "```\n│ \U0001F5B1 │\n```"
    print("selftest OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        raise SystemExit(0)
    OUT.mkdir(parents=True, exist_ok=True)
    for p in sorted(SRC.glob("*.md")):
        dest = OUT / (p.stem + ".html")
        dest.write_text(render(p), encoding="utf-8")
        print("wrote", dest)
