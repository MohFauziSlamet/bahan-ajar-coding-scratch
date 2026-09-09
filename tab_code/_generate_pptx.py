#!/usr/bin/env python3
"""
Generator PPTX bahan ajar Scratch — tab Code.

Menghasilkan satu berkas .pptx untuk tiap berkas .md di folder ini
(nama berkas sama, hanya beda ekstensi).

Jalankan:  python3 _generate_pptx.py
Butuh   :  pip install python-pptx
"""

import json
import struct
from itertools import combinations
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

OUT_DIR = Path(__file__).resolve().parent
ASSETS = OUT_DIR / "assets"          # gambar blok, dibuat oleh _gen_block_assets.py
ASSET_DPI = 360                      # scratchblocks skala 1, dirender Chrome 3x
MAX_IMG_H, MAX_IMG_W = 1.85, 4.60    # batas tampil gambar blok (inci)
EMU_IN = 914400
MAX_ZOOM = 2.2                       # batas pembesaran gambar contoh
LEFT_W = Inches(6.05)                # kolom keterangan + catatan
COL_GAP = Inches(0.45)               # jarak ke kolom contoh

# ---------------------------------------------------------------- tema

W, H = Inches(13.333), Inches(7.5)          # 16:9
MARGIN = Inches(0.6)
BODY_W = W - 2 * MARGIN

INK = RGBColor(0x1F, 0x24, 0x33)            # teks utama
MUTED = RGBColor(0x62, 0x6B, 0x7A)          # teks sekunder
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CODE_BG = RGBColor(0xF3, 0xF4, 0xF7)
NOTE_BG = RGBColor(0xFF, 0xF8, 0xE1)
WARN_BG = RGBColor(0xFF, 0xEB, 0xEE)
ROW_ALT = RGBColor(0xF7, 0xF8, 0xFA)

FONT = "Arial"
MONO = "Courier New"


def rgb(hexstr):
    return RGBColor(int(hexstr[0:2], 16), int(hexstr[2:4], 16), int(hexstr[4:6], 16))


def tint(color, factor):
    """Campur warna dengan putih. factor 0..1 (1 = putih)."""
    return RGBColor(
        int(color[0] + (255 - color[0]) * factor),
        int(color[1] + (255 - color[1]) * factor),
        int(color[2] + (255 - color[2]) * factor),
    )


# ------------------------------------------------------------- helper

def _txbox(slide, x, y, w, h):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    return tf


def _para(tf, text, size, bold=False, color=INK, font=FONT, space_after=6,
          first=False, align=PP_ALIGN.LEFT, italic=False, line_spacing=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.space_after = Pt(space_after)
    p.space_before = Pt(0)
    if line_spacing:
        p.line_spacing = line_spacing
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    return p


def _rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, line=None):
    sh = slide.shapes.add_shape(shape, x, y, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(1)
    sh.shadow.inherit = False
    try:
        sh.adjustments[0] = 0.06
    except (IndexError, KeyError):
        pass
    return sh


def _tinggi_teks(teks, lebar, ukuran, jeda=0.0):
    """Perkiraan tinggi sebuah blok teks (Emu).

    Lebar rata-rata huruf Arial ~0.50 em. Perkiraan lama memakai 0.075 in/huruf
    untuk SEMUA ukuran font, sehingga teks 13-14 pt dikira muat satu baris
    padahal membungkus jadi dua — dan baris berikutnya menimpanya.
    """
    per_huruf = ukuran * 0.50 / 72
    per_baris = max(1, int((lebar / EMU_IN) / per_huruf))
    n = max(1, -(-len(teks) // per_baris))
    return Inches(n * ukuran * 1.26 / 72 + jeda)


def _block_png(cat_key, idx):
    """Gambar blok ke-idx untuk sebuah kategori, bila asetnya sudah dirender."""
    d = ASSETS / cat_key
    hits = sorted(d.glob(f"{idx:02d}-*.png")) if d.is_dir() else []
    return hits[0] if hits else None


def _block_image(slide, cat_key, idx, x, y, max_w=None):
    """Tempel gambar blok. Kembalikan (lebar, tinggi) dalam EMU; (0,0) bila tak ada."""
    p = _block_png(cat_key, idx)
    if p is None:
        return 0, 0
    px_w, px_h = struct.unpack(">II", p.read_bytes()[16:24])
    w, h = px_w / ASSET_DPI, px_h / ASSET_DPI
    lim_w = (max_w / EMU_IN * 0.80) if max_w else MAX_IMG_W
    k = min(MAX_IMG_H / h, lim_w / w, 1.9)       # boleh diperbesar; blok C tetap dibatasi
    w, h = Inches(w * k), Inches(h * k)
    slide.shapes.add_picture(str(p), x, y, width=w, height=h)
    return w, h


def _contoh_images(cat_key, idx):
    """Potongan contoh versi blok puzzle: [(png, judul), ...]."""
    d = ASSETS / "contoh" / cat_key
    if not d.is_dir():
        return []
    judul = {}
    ix = d / "index.json"
    if ix.exists():
        judul = json.loads(ix.read_text(encoding="utf-8"))
    return [(p, judul.get(p.name, "")) for p in sorted(d.glob(f"{idx:02d}-*.png"))]


def _png_size(p):
    return struct.unpack(">II", p.read_bytes()[16:24])


CAP_H, GAP_Y, GAP_X = 0.24, 0.18, 0.30       # judul, jarak tegak, jarak antar kolom


def _bagi(n, k):
    """Semua cara memotong n potongan berurutan jadi k kelompok tak-kosong."""
    for cut in combinations(range(1, n), k - 1):
        batas = (0,) + cut + (n,)
        yield [list(range(batas[i], batas[i + 1])) for i in range(k)]


def _pak_gambar(slide, items, x, y, w, h, cap_h, cap_pt, cap_color,
                gap_x=GAP_X, gap_y=GAP_Y):
    """Susun pasangan (png, judul) ke dalam 1..n kolom, dipilih susunan yang
    memberi gambar TERBESAR.

    Yang biasanya membatasi bukan tinggi melainkan LEBAR kolom — script
    Scratch yang memuat syarat boolean itu lebar. Karena itu jumlah kolom
    tidak dipatok: memaksa 3 kolom pada script lebar membuat gambarnya
    menyusut di bawah ukuran asli dan menyisakan ruang kosong besar.
    """
    xi, yi0 = x / EMU_IN, y / EMU_IN
    wi, hi = w / EMU_IN, h / EMU_IN
    nat = [(pw / ASSET_DPI, ph / ASSET_DPI)
           for pw, ph in (_png_size(p) for p, _ in items)]
    n = len(items)

    def skala(kolom, cw):
        k = MAX_ZOOM
        for kol in kolom:
            tinggi = sum(nat[i][1] for i in kol) or 1e-9
            sisa = hi - len(kol) * cap_h - (len(kol) - 1) * gap_y
            k = min(k, sisa / tinggi, cw / max(nat[i][0] for i in kol))
        return k

    best_k, best = -1, None
    for nk in range(1, n + 1):
        cw = (wi - gap_x * (nk - 1)) / nk
        for kolom in _bagi(n, nk):
            k = skala(kolom, cw)
            if k > best_k:
                best_k, best = k, (kolom, cw)
    kolom, cw = best

    for j, kol in enumerate(kolom):
        cx, cy = xi + j * (cw + gap_x), yi0
        for i in kol:
            p, judul = items[i]
            pw, ph = nat[i]
            if judul:
                _para(_txbox(slide, Inches(cx), Inches(cy), Inches(cw), Inches(cap_h)),
                      judul, cap_pt, bold=True, color=cap_color, first=True,
                      space_after=0)
            cy += cap_h
            slide.shapes.add_picture(str(p), Inches(cx), Inches(cy),
                                     width=Inches(pw * best_k),
                                     height=Inches(ph * best_k))
            cy += ph * best_k + gap_y


def _contoh_puzzle(slide, blk, items, x, y, w, h):
    """Contoh sebagai blok puzzle di kolom kanan slide blok."""
    _para(_txbox(slide, x, y, w, Inches(0.24)), "CONTOH", 10, bold=True,
          color=MUTED, first=True, space_after=0)
    _pak_gambar(slide, items, x, y + Inches(0.32), w, h - Inches(0.32),
                CAP_H, 11, INK)


def _banding_strip(slide, pasangan, x, y, w, h):
    """Sandingkan pasangan blok yang sering tertukar, berdampingan.

    Mengisi ruang kosong di bawah tabel 'Yang Sering Tertukar' — pasangan
    seperti repeat vs forever jauh lebih cepat dipahami bila bloknya
    dilihat berdampingan, bukan sekadar dibaca.
    """
    _para(_txbox(slide, x, y, w, Inches(0.24)), "LIHAT BEDANYA", 10, bold=True,
          color=MUTED, first=True, space_after=0)

    xi, yi = x / EMU_IN, (y + Inches(0.34)) / EMU_IN
    wi, hi = w / EMU_IN, (h - Inches(0.34)) / EMU_IN
    n = len(pasangan)
    gw = (wi - GAP_X * (n - 1)) / n              # lebar tiap grup pasangan
    sw = (gw - 0.16) / 2                         # lebar slot bila berdampingan
    jud_h, ket_h = 0.26, 0.42                    # tinggi judul grup & keterangan

    nat = [[(pw / ASSET_DPI, ph / ASSET_DPI)
            for pw, ph in (_png_size(ASSETS.parent / f) for f, _ in sisi)]
           for _, sisi in pasangan]

    # Dua susunan mungkin, dan mana yang lebih besar berbeda per kategori:
    # berdampingan hemat tinggi tapi slotnya cuma separuh grup, bertumpuk
    # memakai lebar grup penuh. Blok Scratch itu lebar, jadi untuk kebanyakan
    # kategori bertumpuk menang telak — dipilih otomatis, bukan dipatok.
    k_samping = min([MAX_ZOOM] +
                    [sw / pw for grup in nat for pw, _ in grup] +
                    [(hi - jud_h - ket_h) / max(ph for _, ph in grup) for grup in nat])
    k_tumpuk = min([MAX_ZOOM] +
                   [gw / pw for grup in nat for pw, _ in grup] +
                   [(hi - jud_h - 2 * ket_h - 0.08) / sum(ph for _, ph in grup)
                    for grup in nat])

    for j, ((judul, sisi), grup) in enumerate(zip(pasangan, nat)):
        gx = xi + j * (gw + GAP_X)
        _para(_txbox(slide, Inches(gx), Inches(yi), Inches(gw), Inches(jud_h)),
              judul, 12, bold=True, color=INK, first=True, space_after=0)

        if k_tumpuk > k_samping:                 # blok A di atas blok B
            k, cy = k_tumpuk, yi + jud_h
            for (f, ket), (pw, ph) in zip(sisi, grup):
                slide.shapes.add_picture(str(ASSETS.parent / f), Inches(gx),
                                         Inches(cy), Inches(pw * k), Inches(ph * k))
                cy += ph * k + 0.04
                _para(_txbox(slide, Inches(gx), Inches(cy), Inches(gw), Inches(ket_h)),
                      ket, 10, color=MUTED, first=True, space_after=0)
                cy += ket_h
        else:                                    # berdampingan, satu garis dasar
            k = k_samping
            ty = yi + jud_h + max(ph for grup2 in nat
                                  for _, ph in grup2) * k + 0.06
            for i, ((f, ket), (pw, ph)) in enumerate(zip(sisi, grup)):
                sx = gx + i * (sw + 0.16)
                slide.shapes.add_picture(str(ASSETS.parent / f), Inches(sx),
                                         Inches(yi + jud_h), Inches(pw * k),
                                         Inches(ph * k))
                _para(_txbox(slide, Inches(sx), Inches(ty), Inches(sw), Inches(ket_h)),
                      ket, 10, color=MUTED, first=True, space_after=0)


def _contoh_teks(slide, blk, _items, x, y, w, h):
    """Contoh versi lama (teks monospace) — untuk kategori yang belum dikonversi."""
    _para(_txbox(slide, x, y, w, Inches(0.24)), "CONTOH", 10, bold=True,
          color=MUTED, first=True, space_after=0)
    y += Inches(0.30)
    lines = blk["contoh"].strip("\n").split("\n")
    ch = min(Inches(0.34) + Inches(0.235) * len(lines), h - Inches(0.30))
    _rect(slide, x, y, w, ch, CODE_BG)
    tfk = _txbox(slide, x + Inches(0.22), y + Inches(0.17),
                 w - Inches(0.44), ch - Inches(0.34))
    for i, line in enumerate(lines):
        _para(tfk, line if line else " ", 12, color=INK, font=MONO,
              first=(i == 0), space_after=1)


def _blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def _footer(slide, cat, page):
    tf = _txbox(slide, MARGIN, H - Inches(0.55), BODY_W, Inches(0.3))
    p = tf.paragraphs[0]
    p.space_after = 0
    r = p.add_run()
    r.text = cat
    r.font.size = Pt(10)
    r.font.color.rgb = MUTED
    r.font.name = FONT
    tf2 = _txbox(slide, W - MARGIN - Inches(1.0), H - Inches(0.55), Inches(1.0), Inches(0.3))
    p2 = tf2.paragraphs[0]
    p2.alignment = PP_ALIGN.RIGHT
    p2.space_after = 0
    r2 = p2.add_run()
    r2.text = str(page)
    r2.font.size = Pt(10)
    r2.font.color.rgb = MUTED
    r2.font.name = FONT


def _header(slide, color, title, kicker=None):
    """Pita warna di atas slide + judul.

    Kicker dan judul sengaja ditaruh di KOTAK TEKS TERPISAH dengan koordinat
    tetap. Bila keduanya digabung dalam satu text frame, sebagian renderer
    (PowerPoint/Keynote) menghitung tinggi baris berbeda dari Quick Look
    sehingga teks bisa tumpang tindih.
    """
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(1.15))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    bar.shadow.inherit = False

    if kicker:
        tk = _txbox(slide, MARGIN, Inches(0.17), BODY_W, Inches(0.24))
        _para(tk, kicker, 11, bold=True, color=tint(color, 0.72), first=True,
              space_after=0, line_spacing=1.0)
        tt = _txbox(slide, MARGIN, Inches(0.47), BODY_W, Inches(0.52))
        _para(tt, title, 26, bold=True, color=WHITE, first=True,
              space_after=0, line_spacing=1.0)
    else:
        tt = _txbox(slide, MARGIN, Inches(0.32), BODY_W, Inches(0.55))
        _para(tt, title, 28, bold=True, color=WHITE, first=True,
              space_after=0, line_spacing=1.0)


# -------------------------------------------------------- jenis slide

def slide_title(prs, cat):
    s = _blank(prs)
    color = cat["color"]

    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(4.5))
    band.fill.solid()
    band.fill.fore_color.rgb = color
    band.line.fill.background()
    band.shadow.inherit = False

    # tiap baris = kotak teks sendiri agar tidak pernah tumpang tindih
    tk = _txbox(s, MARGIN, Inches(1.35), BODY_W, Inches(0.3))
    _para(tk, "BAHAN AJAR SCRATCH  |  TAB CODE", 13, bold=True,
          color=tint(color, 0.78), first=True, space_after=0, line_spacing=1.0)

    tt = _txbox(s, MARGIN, Inches(1.90), BODY_W, Inches(0.95))
    _para(tt, cat["name"], 42, bold=True, color=WHITE, first=True,
          space_after=0, line_spacing=1.0)

    ts = _txbox(s, MARGIN, Inches(3.05), BODY_W, Inches(0.45))
    _para(ts, cat["subtitle"], 20, color=tint(color, 0.85), first=True,
          space_after=0, line_spacing=1.0)

    t1 = _txbox(s, MARGIN, Inches(5.05), BODY_W, Inches(0.55))
    _para(t1, cat["tagline"], 17, color=INK, first=True, space_after=0, line_spacing=1.1)

    t2 = _txbox(s, MARGIN, Inches(5.85), BODY_W, Inches(0.7))
    _para(t2, cat["scope"], 13, color=MUTED, first=True, space_after=0, line_spacing=1.1)
    return s


def slide_overview(prs, cat, page):
    s = _blank(prs)
    color = cat["color"]
    _header(s, color, "Peta Kategori", cat["name"].upper())

    y = Inches(1.55)
    col_w = (BODY_W - Inches(0.4)) / 2
    baris = (len(cat["overview"]) + 1) // 2
    # jarak antar baris dihitung dari ruang yang tersedia; sebelumnya dipatok
    # 1.25in sehingga kategori berisi 7 kelompok (4 baris) mendorong kotak
    # "Bekal wajib" keluar slide
    sisa = H - Inches(0.72) - y - (Inches(0.95) if cat.get("prasyarat") else 0)
    pitch = min(Inches(1.25), sisa / max(baris, 1))
    kartu = pitch - Inches(0.20)
    for i, (group, items) in enumerate(cat["overview"]):
        cx = MARGIN + (col_w + Inches(0.4)) * (i % 2)
        cy = y + pitch * (i // 2)
        _rect(s, cx, cy, col_w, kartu, tint(color, 0.90))
        tf = _txbox(s, cx + Inches(0.18), cy + Inches(0.11), col_w - Inches(0.36),
                    kartu - Inches(0.22))
        _para(tf, group, 14, bold=True, color=color, first=True, space_after=4)
        _para(tf, items, 12, color=INK, space_after=0)

    if cat.get("prasyarat"):
        by = y + pitch * baris + Inches(0.1)
        _rect(s, MARGIN, by, BODY_W, Inches(0.85), NOTE_BG)
        tf = _txbox(s, MARGIN + Inches(0.25), by + Inches(0.14), BODY_W - Inches(0.5), Inches(0.6))
        _para(tf, "Bekal wajib", 11, bold=True, color=rgb("B26A00"), first=True, space_after=3)
        _para(tf, cat["prasyarat"], 12, color=INK, space_after=0)

    _footer(s, cat["name"], page)
    return s


SHAPE_LABEL = {
    "Hat": ("Hat  (pemicu, paling atas)", "8C6D1F"),
    "Stack": ("Stack  (perintah bertumpuk)", "3B4252"),
    "C": ("C-Block  (membungkus blok lain)", "8A5000"),
    "Cap": ("Cap  (penutup, tak bisa disambung)", "8A2D2D"),
    "Reporter": ("Reporter  (masuk lubang oval)", "1F6B4A"),
    "Boolean": ("Boolean  (masuk lubang segi enam)", "1F4F8B"),
}


def slide_block(prs, cat, blk, page, idx):
    s = _blank(prs)
    color = cat["color"]
    _header(s, color, blk["n"], f'{cat["short"].upper()}  ·  BLOK {idx}')

    y = Inches(1.45)

    # label bentuk
    label, lcol = SHAPE_LABEL[blk["shape"]]
    chip = _rect(s, MARGIN, y, Inches(3.6), Inches(0.36), tint(color, 0.86))
    tfc = chip.text_frame
    tfc.word_wrap = True
    tfc.margin_left = Inches(0.14)
    tfc.margin_top = tfc.margin_bottom = 0
    tfc.vertical_anchor = MSO_ANCHOR.MIDDLE
    _para(tfc, label, 11, bold=True, color=rgb(lcol), first=True, space_after=0)

    puzzle = _contoh_images(cat["key"], idx)
    has_code = bool(puzzle) or bool(blk.get("contoh"))

    # dua kolom: keterangan di kiri, contoh di kanan
    left_w = LEFT_W if has_code else BODY_W
    rx = MARGIN + LEFT_W + COL_GAP
    rw = MARGIN + BODY_W - rx
    bottom = H - Inches(0.72)          # batas bawah, tepat di atas footer

    if has_code:
        (_contoh_puzzle if puzzle else _contoh_teks)(
            s, blk, puzzle, rx, Inches(1.45), rw, bottom - Inches(1.45))

    y += Inches(0.52)

    # gambar blok asli, lalu kalimat sederhana DI BAWAHNYA (kolom kiri sempit)
    iw, ih = _block_image(s, cat["key"], idx, MARGIN, y, max_w=left_w)
    if ih:
        y += ih + Inches(0.12)
    if blk.get("mudah"):
        arti = "Artinya:  " + blk["mudah"]
        th = _tinggi_teks(arti, left_w, 13)
        tfm = _txbox(s, MARGIN, y, left_w, th)
        _para(tfm, arti, 13, color=MUTED, first=True, space_after=0)
        y += th
    y += Inches(0.18)

    tf = _txbox(s, MARGIN, y, left_w, Inches(2.0))
    _para(tf, "FUNGSI", 10, bold=True, color=MUTED, first=True, space_after=4)
    _para(tf, blk["fungsi"], 14, color=INK, space_after=9)
    y += Inches(0.26) + _tinggi_teks(blk["fungsi"], left_w, 14, 0.12)
    if blk.get("param"):
        _para(tf, "PARAMETER", 10, bold=True, color=MUTED, space_after=4)
        for line in blk["param"]:
            _para(tf, "•  " + line, 12, color=INK, space_after=3)
        y += Inches(0.26) + sum(_tinggi_teks("•  " + q, left_w, 12, 0.04)
                                for q in blk["param"])

    # CATATAN mengisi sisa ruang kosong di bawah keterangan
    if blk.get("catatan"):
        ny = y + Inches(0.16)
        nh = max(bottom - ny, Inches(0.8))
        warn = blk.get("warn", False)
        _rect(s, MARGIN, ny, left_w, nh, WARN_BG if warn else NOTE_BG)
        tfn = _txbox(s, MARGIN + Inches(0.24), ny + Inches(0.16),
                     left_w - Inches(0.48), nh - Inches(0.32))
        if nh > Inches(1.7):                 # kotak tinggi -> teks di tengah & lebih besar
            tfn.vertical_anchor = MSO_ANCHOR.MIDDLE
        _para(tfn, "PERHATIAN" if warn else "CATATAN", 10, bold=True,
              color=rgb("B3261E") if warn else rgb("B26A00"), first=True,
              space_after=5)
        _para(tfn, blk["catatan"], 14 if nh > Inches(1.7) else 13,
              color=INK, space_after=0)

    _footer(s, cat["name"], page)
    return s


def slide_table(prs, cat, page, title, kicker, headers, rows, widths=None,
                font_size=12, head_size=12, isi_penuh=True):
    s = _blank(prs)
    color = cat["color"]
    _header(s, color, title, kicker)

    top = Inches(1.5)
    n_baris = len(rows) + 1
    height = min(Inches(5.2), Inches(0.42) * n_baris + Inches(0.15))
    if isi_penuh:
        # memanjangkan tabel sampai memenuhi ruang kosong di bawahnya,
        # dengan batas tinggi per baris agar tidak terlihat melar
        height = max(height, min(H - Inches(0.72) - top,
                                 Inches(0.72) * n_baris))
    shape = s.shapes.add_table(len(rows) + 1, len(headers), MARGIN, top, BODY_W, height)
    table = shape.table
    table.first_row = True

    if widths:
        total = sum(widths)
        for i, wgt in enumerate(widths):
            table.columns[i].width = Emu(int(BODY_W * wgt / total))

    for c, head in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = ""
        cell.fill.solid()
        cell.fill.fore_color.rgb = color
        cell.margin_left = cell.margin_right = Inches(0.12)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        _para(cell.text_frame, head, head_size, bold=True, color=WHITE, first=True, space_after=0)

    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = ""
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r % 2 else ROW_ALT
            cell.margin_left = cell.margin_right = Inches(0.12)
            cell.margin_top = cell.margin_bottom = Inches(0.05)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            mono = val.startswith("`")
            _para(cell.text_frame, val.strip("`"), font_size, color=INK,
                  font=MONO if mono else FONT, first=True, space_after=0)

    _footer(s, cat["name"], page)
    return s


def slide_pattern(prs, cat, page, title, kicker, items):
    """Slide berisi 1-3 potongan script."""
    s = _blank(prs)
    color = cat["color"]
    _header(s, color, title, kicker)

    n = len(items)
    gap = Inches(0.35)
    col_w = (BODY_W - gap * (n - 1)) / n
    y = Inches(1.5)

    # versi blok puzzle bila asetnya sudah dirender (assets/pola/<kategori>/)
    d = ASSETS / "pola" / cat["key"]
    pola = sorted(d.glob("*.png")) if d.is_dir() else []

    if len(pola) == n:
        _pak_gambar(s, list(zip(pola, [lab for lab, _ in items])),
                    MARGIN, y, BODY_W, H - Inches(0.72) - y,
                    cap_h=0.50, cap_pt=14, cap_color=color,
                    gap_x=gap / EMU_IN, gap_y=0.30)
    else:
        for i, (label, code) in enumerate(items):
            cx = MARGIN + (col_w + gap) * i
            tf = _txbox(s, cx, y, col_w, Inches(0.5))
            _para(tf, label, 14, bold=True, color=color, first=True, space_after=0)
            lines = code.strip("\n").split("\n")
            ch = Inches(0.36) + Inches(0.245) * len(lines)
            _rect(s, cx, y + Inches(0.45), col_w, ch, CODE_BG)
            tfk = _txbox(s, cx + Inches(0.2), y + Inches(0.62),
                         col_w - Inches(0.4), ch - Inches(0.34))
            for j, line in enumerate(lines):
                _para(tfk, line if line else " ", 12, color=INK, font=MONO,
                      first=(j == 0), space_after=1)

    _footer(s, cat["name"], page)
    return s


def slide_bullets(prs, cat, page, title, kicker, bullets, note=None):
    s = _blank(prs)
    color = cat["color"]
    _header(s, color, title, kicker)

    # ukuran & jarak menyesuaikan banyaknya butir agar ruang terpakai penuh
    ruang = 4.4 if note else 5.0
    ukuran = max(15, min(24, int(ruang * 62 / max(len(bullets), 1))))
    jarak = max(10, min(34, int(ruang * 74 / max(len(bullets), 1)) - ukuran))
    tf = _txbox(s, MARGIN, Inches(1.6), BODY_W, Inches(ruang))
    for i, b in enumerate(bullets):
        _para(tf, f"{i + 1}.  {b}", ukuran, color=INK, first=(i == 0),
              space_after=jarak)

    if note:
        _rect(s, MARGIN, H - Inches(1.55), BODY_W, Inches(0.8), NOTE_BG)
        tfn = _txbox(s, MARGIN + Inches(0.25), H - Inches(1.42), BODY_W - Inches(0.5), Inches(0.55))
        _para(tfn, note, 13, color=INK, first=True, space_after=0)

    _footer(s, cat["name"], page)
    return s


def slide_answers(prs, cat, page, answers):
    s = _blank(prs)
    color = cat["color"]
    _header(s, color, "Kunci Jawaban", cat["short"].upper())

    ukuran = max(13, min(19, int(5.0 * 52 / max(len(answers), 1))))
    jarak = max(9, min(26, int(5.0 * 66 / max(len(answers), 1)) - ukuran))
    tf = _txbox(s, MARGIN, Inches(1.6), BODY_W, Inches(5.0))
    for i, a in enumerate(answers):
        _para(tf, f"{i + 1}.  {a}", ukuran, color=INK, first=(i == 0),
              space_after=jarak)

    _footer(s, cat["name"], page)
    return s


def slide_closing(prs, cat):
    s = _blank(prs)
    color = cat["color"]
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    band.fill.solid()
    band.fill.fore_color.rgb = color
    band.line.fill.background()
    band.shadow.inherit = False

    th = _txbox(s, MARGIN, Inches(2.35), BODY_W, Inches(0.35))
    _para(th, "RANGKUMAN", 15, bold=True, color=tint(color, 0.78), first=True,
          space_after=0, line_spacing=1.0)

    tf = _txbox(s, MARGIN, Inches(3.0), BODY_W, Inches(2.6))
    for i, line in enumerate(cat["takeaways"]):
        _para(tf, "•  " + line, 19, color=WHITE, first=(i == 0), space_after=16,
              line_spacing=1.15)
    return s


# ------------------------------------------------------------ perakit

def build(cat):
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H

    slide_title(prs, cat)
    page = 2
    slide_overview(prs, cat, page)
    page += 1

    for i, blk in enumerate(cat["blocks"], start=1):
        slide_block(prs, cat, blk, page, i)
        page += 1

    if cat.get("compare"):
        st = slide_table(prs, cat, page, "Yang Sering Tertukar", cat["short"].upper(),
                         ["Pasangan blok", "Beda utama"], cat["compare"],
                         widths=[38, 62], isi_penuh=not cat.get("banding"))
        if cat.get("banding"):
            tb = max((sh.top + sh.height for sh in st.shapes if sh.has_table),
                     default=Inches(4.2))
            _banding_strip(st, cat["banding"], MARGIN, tb + Inches(0.34),
                           BODY_W, H - Inches(0.72) - tb - Inches(0.34))
        page += 1

    if cat.get("patterns"):
        slide_pattern(prs, cat, page, "Pola yang Sering Dipakai", cat["short"].upper(),
                      cat["patterns"])
        page += 1

    slide_table(prs, cat, page, "Kesalahan Umum di Kelas", cat["short"].upper(),
                ["Kesalahan", "Gejala", "Perbaikan"], cat["mistakes"], widths=[34, 33, 33])
    page += 1

    slide_table(prs, cat, page, "Latihan Bertingkat", cat["short"].upper(),
                ["Level", "Tantangan", "Blok kunci"], cat["practice"], widths=[12, 50, 38])
    page += 1

    slide_bullets(prs, cat, page, "Cek Pemahaman", cat["short"].upper(), cat["quiz"])
    page += 1

    slide_answers(prs, cat, page, cat["answers"])
    page += 1

    slide_closing(prs, cat)

    out = OUT_DIR / f'tab_code_{cat["key"]}.pptx'
    prs.save(out)
    return out, len(prs.slides.__iter__.__self__._sldIdLst)


# ----------------------------------------------------------- dek index

def build_index(cats):
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    accent = rgb("855CD6")

    # sampul
    s = _blank(prs)
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    band.fill.solid()
    band.fill.fore_color.rgb = accent
    band.line.fill.background()
    band.shadow.inherit = False
    tk = _txbox(s, MARGIN, Inches(2.45), BODY_W, Inches(0.32))
    _para(tk, "BAHAN AJAR INFORMATIKA  ·  SD-SMP", 14, bold=True,
          color=tint(accent, 0.78), first=True, space_after=0, line_spacing=1.0)
    tt = _txbox(s, MARGIN, Inches(3.05), BODY_W, Inches(1.1))
    _para(tt, "Tab Code Scratch", 48, bold=True, color=WHITE, first=True,
          space_after=0, line_spacing=1.0)
    ts = _txbox(s, MARGIN, Inches(4.35), BODY_W, Inches(0.45))
    _para(ts, "Penjelasan lengkap 9 kategori blok  ·  125 blok inti", 20,
          color=tint(accent, 0.86), first=True, space_after=0, line_spacing=1.0)

    idx = {"name": "Index Tab Code", "short": "INDEX", "color": accent}

    # daftar dek
    rows = [[c["short"], c["subtitle"], c["level"]] for c in cats]
    slide_table(prs, idx, 2, "Sembilan Kategori Blok", "DAFTAR DEK",
                ["Kategori", "Jumlah blok", "Tingkat"], rows, widths=[38, 32, 30], font_size=14)

    # bentuk blok
    shapes = [
        ["Hat", "Atas melengkung", "Hanya di paling atas script", "when green flag clicked"],
        ["Stack", "Takik atas & bawah", "Ditumpuk atas–bawah", "move (10) steps"],
        ["C-Block", "Huruf C", "Membungkus blok lain", "repeat (10)"],
        ["Reporter", "Oval", "Masuk ke lubang oval", "(x position)"],
        ["Boolean", "Segi enam", "Masuk ke lubang segi enam", "<touching (edge)?>"],
        ["Cap", "Bawah rata", "Penutup, tak bisa disambung", "stop (all)"],
    ]
    slide_table(prs, idx, 3, "Enam Bentuk Blok = Tata Bahasa Scratch", "KONSEP DASAR",
                ["Bentuk", "Ciri fisik", "Aturan pemasangan", "Contoh"],
                shapes, widths=[15, 22, 33, 30], font_size=12)

    # urutan mengajar
    order = [
        ["1", "Events (when green flag clicked)", "Pemicu"],
        ["2", "Motion", "Urutan (sequence), koordinat"],
        ["3", "Looks", "Animasi, kostum"],
        ["4", "Sound", "Media & sinkronisasi"],
        ["5", "Control (repeat, forever, wait)", "Perulangan"],
        ["6", "Sensing", "Input & deteksi"],
        ["7", "Control (if / if-else) + Operators", "Percabangan & logika"],
        ["8", "Variables", "Penyimpanan data, skor"],
        ["9", "Events (broadcast)", "Komunikasi antar objek"],
        ["10", "Control (klon)", "Objek dinamis"],
        ["11", "Variables (List)", "Struktur data"],
        ["12", "My Blocks", "Prosedur & abstraksi"],
    ]
    slide_table(prs, idx, 4, "Urutan Mengajar yang Disarankan", "BUKAN URUT KATEGORI",
                ["Tahap", "Kategori", "Fokus konsep"], order, widths=[10, 48, 42],
                font_size=11, head_size=12)

    # aturan umum
    slide_bullets(prs, idx, 5, "Enam Aturan yang Berlaku di Semua Kategori", "PEGANGAN GURU", [
        "Klik blok di palet = uji coba sekali jalan, tidak menambah kode ke proyek.",
        "Blok menempel pada sprite yang sedang dipilih — ganti sprite, area kode ikut berganti.",
        "Blok Motion tidak tersedia untuk Stage karena panggung tidak bisa bergerak.",
        "Lubang angka bisa diisi blok reporter: move (pick random 1 to 10) steps.",
        "Perbandingan teks tidak membedakan huruf besar-kecil: [Halo] = [halo] bernilai benar.",
        "Semua penomoran di Scratch (item list, huruf, kostum) dimulai dari 1, bukan 0.",
    ])

    out = OUT_DIR / "tab_code_index.pptx"
    prs.save(out)
    return out


# =================================================================== DATA

M = {
    "key": "motion", "short": "Motion", "name": "Motion (Gerak)", "subtitle": "18 blok",
    "color": rgb("4C97FF"),
    "tagline": "Menggerakkan dan menempatkan sprite di panggung.",
    "scope": "Hanya untuk Sprite. Bila Stage dipilih, kategori ini kosong — panggung tidak bisa bergerak.",
    "level": "Dasar",
    "prasyarat": "Panggung 480x360.  x: -240 s.d. 240,  y: -180 s.d. 180, pusat (0,0).  "
                 "Arah: 90 = kanan, 0 = atas, 180 = bawah, -90 = kiri.",
    "overview": [
        ("Gerak relatif (dari posisi sekarang)", "move, turn right, turn left, change x by, change y by"),
        ("Gerak absolut (ke tempat tertentu)", "go to, go to x y, set x to, set y to, point in direction"),
        ("Gerak halus berdurasi", "glide to, glide to x y"),
        ("Mengikuti target", "point towards"),
        ("Pengaturan", "if on edge bounce, set rotation style"),
        ("Pelapor nilai", "x position, y position, direction"),
    ],
    "blocks": [
        {"n": "move (10) steps", "mudah": "maju ke depan sejauh 10 titik, mengikuti ke mana sprite sedang menghadap.", "shape": "Stack",
         "fungsi": "Memajukan sprite sesuai ARAH HADAPNYA sejauh N piksel.",
         "param": ["10 = jumlah piksel", "Boleh negatif (mundur), boleh desimal"],
         "contoh": "when green flag clicked\nmove (100) steps",
         "catatan": "\"steps\" berarti PIKSEL, bukan langkah kaki. Arahnya mengikuti nilai direction — "
                    "kalau sprite menghadap 0 (atas), move 100 membuatnya naik, bukan ke kanan."},
        {"n": "turn right (15) degrees", "mudah": "memutar badan sprite ke kanan sebesar 15 derajat.", "shape": "Stack",
         "fungsi": "Memutar sprite searah jarum jam.",
         "param": ["15 = besar sudut", "Nilai negatif memutar ke arah sebaliknya"],
         "contoh": "repeat (4)\n  move (100) steps\n  turn right (90) degrees",
         "catatan": "Rumus menggambar segi-n:  repeat (n) + turn right (360/n) degrees."},
        {"n": "turn left (15) degrees", "mudah": "memutar badan sprite ke kiri sebesar 15 derajat.", "shape": "Stack",
         "fungsi": "Memutar sprite berlawanan arah jarum jam.",
         "contoh": "turn left (90) degrees",
         "catatan": "Sama dengan blok sebelumnya, arah berlawanan.  turn left 90 = turn right -90."},
        {"n": "go to (random position)", "mudah": "pindah kedip ke tempat yang dipilih — langsung sampai, tanpa terlihat berjalan.", "shape": "Stack",
         "fungsi": "Memindahkan sprite SEKETIKA (tanpa animasi) ke lokasi pilihan.",
         "param": ["random position = tempat acak", "mouse-pointer = posisi kursor",
                   "(nama sprite lain) = posisi sprite itu"],
         "contoh": "forever\n  go to (mouse-pointer)",
         "catatan": "Perpindahan instan. Untuk gerak halus gunakan glide."},
        {"n": "go to x: (0) y: (0)", "mudah": "pindah kedip ke titik koordinat tertentu di panggung.", "shape": "Stack",
         "fungsi": "Memindahkan sprite seketika ke koordinat tertentu.",
         "contoh": "when green flag clicked\ngo to x: (0) y: (0)",
         "catatan": "BLOK PALING PENTING UNTUK SCRIPT RESET. Tanpa ini, sprite mulai dari posisi "
                    "terakhir sesi sebelumnya sehingga proyek terasa \"tidak konsisten\"."},
        {"n": "glide (1) secs to (random position)", "mudah": "meluncur pelan ke tempat pilihan selama 1 detik, gerakannya terlihat.", "shape": "Stack",
         "fungsi": "Meluncur HALUS ke lokasi pilihan selama N detik.",
         "param": ["1 = durasi dalam detik", "Dropdown sama dengan blok go to"],
         "catatan": "Script BERHENTI MENUNGGU sampai luncuran selesai (blocking). Jangan dipakai di "
                    "dalam forever bila sprite harus tetap responsif terhadap tombol.", "warn": True},
        {"n": "glide (1) secs to x: (0) y: (0)", "mudah": "meluncur pelan ke titik koordinat selama 1 detik.", "shape": "Stack",
         "fungsi": "Meluncur halus ke koordinat tertentu. Kecepatan dihitung otomatis: jarak dibagi durasi.",
         "contoh": "when green flag clicked\ngo to x: (-200) y: (0)\nglide (3) secs to x: (200) y: (0)",
         "catatan": "Pilihan terbaik untuk animasi cerita dan perpindahan adegan."},
        {"n": "point in direction (90)", "mudah": "mengatur sprite mau menghadap ke mana. 90 = kanan, 0 = atas.", "shape": "Stack",
         "fungsi": "Menetapkan arah hadap sprite (nilai absolut, bukan menambah).",
         "param": ["90 = kanan (bawaan)", "0 = atas", "180 = bawah", "-90 = kiri"],
         "catatan": "Klik kolomnya untuk memunculkan piringan pemutar (dial). "
                    "Blok ini wajib ada di script reset."},
        {"n": "point towards (mouse-pointer)", "mudah": "memutar sprite supaya menghadap ke sasaran, misalnya kursor mouse.", "shape": "Stack",
         "fungsi": "Menghadapkan sprite ke arah target.",
         "param": ["mouse-pointer", "random direction", "(nama sprite lain)"],
         "contoh": "forever\n  point towards (Pemain)\n  move (2) steps",
         "catatan": "Kombinasi point towards + move adalah resep dasar AI musuh pengejar."},
        {"n": "change x by (10)", "mudah": "menggeser sprite 10 titik ke kanan. Selalu mendatar, tak peduli arah hadapnya.", "shape": "Stack",
         "fungsi": "Menggeser sprite MENDATAR sejauh N piksel, tanpa memedulikan arah hadap.",
         "contoh": "when green flag clicked\nforever\n  if <key (right arrow)\n     pressed?> then\n    change x by (10)",
         "catatan": "Berbeda dari move — blok ini SELALU mendatar. Inilah blok yang benar untuk "
                    "kontrol tombol panah."},
        {"n": "set x to (0)", "mudah": "menaruh sprite di posisi kiri-kanan tertentu; ketinggiannya tidak berubah.", "shape": "Stack",
         "fungsi": "Menetapkan koordinat X; nilai Y tidak berubah.",
         "contoh": "set x to (-240)",
         "catatan": "Dipakai untuk memindahkan sprite ke tepi tanpa mengubah ketinggiannya."},
        {"n": "change y by (10)", "mudah": "menggeser sprite 10 titik ke atas. Angka positif = naik, negatif = turun.", "shape": "Stack",
         "fungsi": "Menggeser sprite TEGAK sejauh N piksel. Nilai positif = naik.",
         "contoh": "forever\n  change y by (kecepatan)\n  change (kecepatan) by (-1)",
         "catatan": "Y positif berarti NAIK. Ini sering membingungkan siswa yang terbiasa koordinat "
                    "layar komputer, di mana Y positif justru turun."},
        {"n": "set y to (0)", "mudah": "menaruh sprite di ketinggian tertentu; posisi kiri-kanannya tidak berubah.", "shape": "Stack",
         "fungsi": "Menetapkan koordinat Y; nilai X tidak berubah.",
         "contoh": "set y to (-100)",
         "catatan": "Sering dipakai untuk mengembalikan tokoh ke permukaan tanah."},
        {"n": "if on edge, bounce", "mudah": "kalau sprite kena pinggir panggung, ia langsung memantul balik.", "shape": "Stack",
         "fungsi": "Bila sprite menyentuh tepi panggung, arah hadapnya dibalik sehingga memantul.",
         "contoh": "when green flag clicked\nforever\n  move (10) steps\n  if on edge, bounce",
         "catatan": "Hampir selalu dipasangkan dengan set rotation style [left-right]; tanpa itu "
                    "sprite akan tampak jungkir balik saat memantul."},
        {"n": "set rotation style (left-right)", "mudah": "mengatur cara gambar sprite berubah saat ia berputar.", "shape": "Stack",
         "fungsi": "Mengatur BAGAIMANA TAMPILAN sprite berubah saat arah hadapnya berubah.",
         "param": ["all around = gambar ikut berputar penuh (roket, panah)",
                   "left-right = cermin kiri/kanan saja (tokoh berjalan)",
                   "don't rotate = gambar tidak pernah berubah (ikon, tombol)"],
         "catatan": "JAWABAN KELUHAN PALING SERING: \"kucingnya jalan terbalik!\" Blok ini mengubah "
                    "tampilan saja; nilai direction tetap berubah seperti biasa."},
        {"n": "(x position)", "mudah": "memberi tahu angka posisi kiri-kanan sprite saat ini.", "shape": "Reporter",
         "fungsi": "Melaporkan koordinat X sprite saat ini.",
         "contoh": "if <(x position) > (200)> then\n  say [Aku di tepi kanan!]",
         "catatan": "Ada kotak centang di palet — centang untuk menampilkan monitor di panggung. "
                    "Alat debugging terbaik untuk pemula."},
        {"n": "(y position)", "mudah": "memberi tahu angka posisi atas-bawah sprite saat ini.", "shape": "Reporter",
         "fungsi": "Melaporkan koordinat Y sprite saat ini.",
         "contoh": "if <(y position) < (-170)> then\n  say [Game Over]",
         "catatan": "Sering dipakai untuk mendeteksi tokoh jatuh ke dasar panggung."},
        {"n": "(direction)", "mudah": "memberi tahu sprite sekarang menghadap ke arah berapa derajat.", "shape": "Reporter",
         "fungsi": "Melaporkan arah hadap sprite dalam derajat.",
         "catatan": "Nilainya selalu dalam rentang -179 sampai 180. Setelah turn right 200 derajat "
                    "dari arah 90, hasilnya dilaporkan -70, bukan 290."},
    ],
    "compare": [
        ["move  vs  change x by", "move mengikuti ARAH HADAP; change x by SELALU mendatar"],
        ["go to x y  vs  glide to x y", "go to INSTAN; glide BERDURASI dan menunggu selesai"],
        ["change x by  vs  set x to", "change MENAMBAH dari posisi sekarang; set MENETAPKAN nilai baru"],
        ["turn  vs  point in direction", "turn memutar RELATIF; point menetapkan arah ABSOLUT"],
        ["direction  vs  rotation style", "direction = arah sesungguhnya; rotation style = cara menampilkannya"],
    ],
    "banding": [
        ("move  vs  change x by",
         [("assets/motion/01-move-steps.png", "maju MENGIKUTI arah hadap"),
          ("assets/motion/10-change-x-by.png", "geser mendatar, arah diabaikan")]),
        ("go to x y  vs  glide to x y",
         [("assets/motion/05-go-to-x-y.png", "pindah seketika"),
          ("assets/motion/07-glide-secs-to-x-y.png", "bergerak halus, butuh waktu")]),
        ("change x by  vs  set x to",
         [("assets/motion/10-change-x-by.png", "menambah dari posisi sekarang"),
          ("assets/motion/11-set-x-to.png", "langsung ke angka itu")]),
    ],
    "patterns": [
        ("Script reset (wajib)", "when green flag clicked\ngo to x: (0) y: (0)\npoint in direction (90)\nset rotation style\n  [left-right]"),
        ("Kontrol tombol panah", "forever\n  if <key (right arrow)\n     pressed?> then\n    change x by (10)\n  if <key (left arrow)\n     pressed?> then\n    change x by (-10)"),
        ("Bola memantul", "when green flag clicked\nset rotation style\n  [left-right]\nforever\n  move (10) steps\n  if on edge, bounce"),
    ],
    "mistakes": [
        ["Memakai move untuk kontrol tombol panah", "Sprite bergerak menyerong / arah aneh", "Ganti ke change x by / change y by"],
        ["Lupa script reset", "Posisi awal berbeda tiap kali dijalankan", "Tambah go to x y + point in direction (90)"],
        ["if on edge bounce tanpa rotation style", "Sprite jungkir balik saat memantul", "Tambah set rotation style [left-right]"],
        ["Mengira \"steps\" = langkah kaki", "Salah memperkirakan jarak", "1 step = 1 piksel; lebar panggung hanya 480"],
        ["glide di dalam forever untuk kontrol", "Kontrol terasa lambat / macet", "Pakai change x by; glide hanya untuk animasi"],
    ],
    "practice": [
        ["*", "Kucing berjalan 100 langkah lalu berhenti", "move"],
        ["*", "Kucing menggambar persegi", "repeat, move, turn"],
        ["**", "Kucing bergerak dengan 4 tombol panah", "change x by, change y by"],
        ["**", "Bola memantul tanpa henti dan tidak terbalik", "forever, if on edge bounce, rotation style"],
        ["***", "Musuh mengejar pemain", "point towards, move"],
        ["***", "Sprite melompat lalu jatuh (gravitasi)", "change y by + variabel kecepatan"],
    ],
    "quiz": [
        "Apa beda move (10) steps dengan change x by (10)?",
        "Sprite menghadap arah 0. Ke mana ia bergerak bila diberi move (50) steps?",
        "Blok apa yang harus ditambahkan agar sprite tidak jungkir balik saat memantul?",
        "Tuliskan script agar sprite selalu mengikuti kursor mouse.",
    ],
    "answers": [
        "move bergerak mengikuti arah hadap sprite; change x by selalu mendatar tanpa memedulikan arah hadap.",
        "Ke ATAS, karena arah 0 berarti menghadap ke atas.",
        "set rotation style [left-right].",
        "when green flag clicked / forever / go to (mouse-pointer). Alternatif lebih halus: point towards (mouse-pointer) + move (5) steps.",
    ],
    "takeaways": [
        "\"Steps\" = piksel, dan arahnya mengikuti direction — bukan selalu ke kanan.",
        "Kontrol tombol panah memakai change x by / change y by, bukan move.",
        "Setiap proyek diawali script reset: posisi, arah, dan rotation style.",
    ],
}

L = {
    "key": "looks", "short": "Looks", "name": "Looks (Tampilan)", "subtitle": "21 blok",
    "color": rgb("9966FF"),
    "tagline": "Mengatur rupa sprite dan latar panggung.",
    "scope": "Sebagian khusus Sprite, sebagian khusus Stage, sebagian bisa keduanya.",
    "level": "Dasar",
    "prasyarat": "Kostum milik Sprite, backdrop milik Stage. Setiap sprite wajib punya minimal satu kostum.",
    "overview": [
        ("Berbicara (Sprite)", "say, say for secs, think, think for secs"),
        ("Kostum (Sprite)", "switch costume to, next costume, (costume)"),
        ("Backdrop (Stage)", "switch backdrop to, ... and wait, next backdrop, (backdrop)"),
        ("Ukuran (Sprite)", "change size by, set size to, (size)"),
        ("Terlihat (Sprite)", "show, hide"),
        ("Lapisan (Sprite)", "go to layer, go layers"),
        ("Efek grafis (Sprite & Stage)", "change effect by, set effect to, clear graphic effects"),
    ],
    "blocks": [
        {"n": "say [Hello!] for (2) seconds", "mudah": "sprite memunculkan balon bicara selama 2 detik, lalu balonnya hilang sendiri.", "shape": "Stack",
         "fungsi": "Menampilkan balon bicara selama N detik, lalu balon hilang sendiri.",
         "contoh": "when green flag clicked\nsay [Selamat datang!]\n  for (2) seconds\nsay [Ayo mulai!]\n  for (2) seconds",
         "catatan": "Script MENUNGGU sampai durasi habis (blocking) — cocok untuk dialog berurutan."},
        {"n": "say [Hello!]", "mudah": "sprite memunculkan balon bicara yang menempel terus sampai diganti.", "shape": "Stack",
         "fungsi": "Menampilkan balon bicara TANPA batas waktu; balon tetap ada sampai diganti.",
         "contoh": "forever\n  say (join [Skor: ]\n       (skor))",
         "catatan": "Cara menghapus balon: say [] dengan kolom DIKOSONGKAN. Ini pertanyaan langganan "
                    "siswa: \"Pak, balonnya nggak mau hilang!\""},
        {"n": "think [Hmm...] for (2) seconds", "mudah": "balon berpikir (bulat-bulat kecil) muncul selama 2 detik lalu hilang.", "shape": "Stack",
         "fungsi": "Sama seperti say for seconds, tetapi berbentuk balon pikiran (bulatan-bulatan).",
         "catatan": "Bagus untuk menunjukkan tokoh sedang berpikir atau ragu dalam cerita."},
        {"n": "think [Hmm...]", "mudah": "balon berpikir muncul dan menempel terus sampai diganti.", "shape": "Stack",
         "fungsi": "Balon pikiran tanpa batas waktu. Dihapus dengan think [] kosong.",
        "catatan": "Bedanya dengan say cuma bentuk balonnya. Balon ini menetap sampai diganti atau dikosongkan dengan think [] — bukan hilang sendiri."},
        {"n": "switch costume to (costume2)", "mudah": "mengganti 'baju' atau gambar sprite ke kostum yang dipilih.", "shape": "Stack",
         "fungsi": "Mengganti tampilan sprite ke kostum tertentu.",
         "contoh": "forever\n  switch costume to\n    (costume1)\n  wait (0.2) seconds\n  switch costume to\n    (costume2)\n  wait (0.2) seconds",
         "catatan": "Kolomnya juga bisa diisi angka atau blok reporter, mis. "
                    "switch costume to (pick random (1) to (4))."},
        {"n": "next costume", "mudah": "ganti ke kostum berikutnya. Kalau diulang cepat, sprite terlihat bergerak seperti animasi.", "shape": "Stack",
         "fungsi": "Berpindah ke kostum berikutnya; setelah yang terakhir kembali ke yang pertama.",
         "contoh": "forever\n  next costume\n  move (10) steps\n  wait (0.1) seconds",
         "catatan": "BLOK PALING PENTING UNTUK ANIMASI. Kecepatan animasi diatur lewat wait, bukan "
                    "lewat blok ini. Tanpa wait, animasi terlihat bergetar."},
        {"n": "(costume [number])", "mudah": "memberi tahu sprite sedang memakai kostum nomor berapa (atau namanya apa).", "shape": "Reporter",
         "fungsi": "Melaporkan nomor atau nama kostum yang sedang dipakai.",
         "param": ["number = angka urut, mulai dari 1", "name = nama kostum"],
         "contoh": "if <(costume [name])\n   = [terluka]> then\n  change (nyawa) by (-1)",
        "catatan": "Pilih [number] bila mau dibandingkan dengan angka, [name] bila mau dibandingkan dengan teks. Membandingkan number dengan teks nama akan selalu bernilai salah."},
        {"n": "switch backdrop to (Blue Sky)", "mudah": "mengganti gambar latar panggung ke backdrop yang dipilih.", "shape": "Stack",
         "fungsi": "Mengganti latar belakang panggung.",
         "catatan": "Meski milik Stage, blok ini JUGA bisa dipakai dari sprite. Sering dipakai untuk "
                    "berpindah level."},
        {"n": "switch backdrop to (...) and wait", "mudah": "ganti latar, lalu tunggu dulu sampai semua reaksi latar itu selesai jalan.", "shape": "Stack",
         "fungsi": "Mengganti latar, lalu MENUNGGU semua script \"when backdrop switches to\" selesai.",
         "catatan": "Versi lanjutan; berguna agar urutan cerita tidak saling mendahului."},
        {"n": "next backdrop", "mudah": "ganti ke gambar latar berikutnya.", "shape": "Stack",
         "fungsi": "Berpindah ke backdrop berikutnya, berputar kembali ke awal setelah yang terakhir.",
         "contoh": "when green flag clicked\nforever\n  next backdrop\n  wait (3) seconds",
        "catatan": "Setelah backdrop terakhir ia kembali ke yang pertama. Untuk pindah ke latar tertentu jangan pakai ini — pakai switch backdrop to."},
        {"n": "(backdrop [number])", "mudah": "memberi tahu panggung sedang memakai latar nomor berapa (atau namanya apa).", "shape": "Reporter",
         "fungsi": "Melaporkan nomor atau nama backdrop yang sedang tampil.",
         "contoh": "if <(backdrop [name])\n   = [Level3]> then\n  set (kesulitan) to (3)",
        "catatan": "Milik Stage, tetapi bisa dibaca dari sprite mana pun. Berguna untuk mengatur tingkat kesulitan mengikuti level yang sedang tampil."},
        {"n": "change size by (10)", "mudah": "memperbesar sprite 10 persen dari ukuran sekarang. Angka negatif memperkecil.", "shape": "Stack",
         "fungsi": "Menambah atau mengurangi ukuran sprite sebanyak N persen.",
         "contoh": "repeat (10)\n  change size by (5)\nrepeat (10)\n  change size by (-5)",
        "catatan": "Menumpuk dari ukuran sekarang, jadi dipanggil 10 kali akan membesar 10 kali pula. Batas Scratch: sprite tidak bisa lebih kecil atau lebih besar dari yang muat di panggung."},
        {"n": "set size to (100) %", "mudah": "menetapkan ukuran sprite. 100% = ukuran asli, 50% = separuhnya.", "shape": "Stack",
         "fungsi": "Menetapkan ukuran sprite dalam persen dari ukuran kostum aslinya.",
         "param": ["100 = ukuran asli", "50 = setengah", "200 = dua kali"],
         "catatan": "WAJIB ada di script reset. Tanpa ini, ukuran sisa dari percobaan sebelumnya "
                    "akan terbawa ke sesi berikutnya."},
        {"n": "(size)", "mudah": "memberi tahu ukuran sprite sekarang dalam persen.", "shape": "Reporter",
         "fungsi": "Melaporkan ukuran sprite saat ini dalam persen.",
         "contoh": "if <(size) < (200)> then\n  change size by (10)",
        "catatan": "Nilainya persen, bukan piksel — 100 berarti ukuran asli kostum. Pakai ini sebagai penjaga batas agar sprite tidak membesar tanpa henti."},
        {"n": "show", "mudah": "memunculkan sprite supaya terlihat lagi di panggung.", "shape": "Stack",
         "fungsi": "Menampilkan sprite di panggung.",
         "catatan": "Selalu taruh di awal script reset — ini penyelamat dari sprite yang \"hilang\"."},
        {"n": "hide", "mudah": "menyembunyikan sprite. Sprite tetap ada dan tetap bisa jalan, hanya tak terlihat.", "shape": "Stack",
         "fungsi": "Menyembunyikan sprite dari panggung.",
         "contoh": "when green flag clicked\nshow",
         "catatan": "Sprite tersembunyi TETAP menjalankan kodenya, tetapi TIDAK terdeteksi oleh blok "
                    "touching ()?. Jebakan klasik: siswa memakai hide lalu sprite \"hilang\" di sesi berikutnya.",
         "warn": True},
        {"n": "go to (front) layer", "mudah": "menaruh sprite di lapisan paling depan supaya tidak tertutup sprite lain.", "shape": "Stack",
         "fungsi": "Memindahkan sprite ke lapisan paling depan atau paling belakang.",
         "catatan": "Stage SELALU paling belakang dan tidak bisa diubah."},
        {"n": "go (forward) (1) layers", "mudah": "memindahkan sprite maju 1 lapisan ke depan (atau mundur ke belakang).", "shape": "Stack",
         "fungsi": "Menggeser sprite maju atau mundur sebanyak N lapisan.",
         "catatan": "Dipakai misalnya agar awan berada di belakang tokoh tetapi tetap di depan latar."},
        {"n": "change (color) effect by (25)", "mudah": "menambah efek warna sebanyak 25 dari nilai sekarang.", "shape": "Stack",
         "fungsi": "Menambah nilai salah satu dari 7 efek grafis.",
         "param": ["color 0-200 (berulang) | fisheye | whirl", "pixelate | mosaic 0-5105",
                   "brightness -100..100 | ghost 0-100"],
         "contoh": "set (ghost) effect to (100)\nshow\nrepeat (20)\n  change (ghost)\n    effect by (-5)",
        "catatan": "Efek color berputar: setelah 100 ia kembali ke 0. Efek ghost tidak berputar, 0 = terlihat penuh dan 100 = tidak terlihat sama sekali."},
        {"n": "set (color) effect to (0)", "mudah": "menetapkan nilai efek langsung. Angka 0 berarti kembali normal.", "shape": "Stack",
         "fungsi": "Menetapkan nilai efek grafis secara pasti.",
         "catatan": "Berbeda dari hide: sprite ber-ghost 100 tak terlihat tetapi MASIH TERDETEKSI oleh "
                    "touching ()?. Trik ini dipakai untuk membuat area tabrakan tak kasatmata."},
        {"n": "clear graphic effects", "mudah": "menghapus SEMUA efek sekaligus supaya sprite kembali normal.", "shape": "Stack",
         "fungsi": "Menghapus SEMUA efek grafis sekaligus, mengembalikan tampilan normal.",
         "catatan": "Wajib masuk script reset. Tanpa ini sprite bisa tetap buram atau aneh dari "
                    "percobaan sebelumnya."},
    ],
    "compare": [
        ["say  vs  say for () seconds", "Tanpa durasi balon menetap selamanya; dengan durasi hilang sendiri"],
        ["hide  vs  set ghost effect to 100", "hide TIDAK terdeteksi touching; ghost 100 MASIH terdeteksi"],
        ["costume  vs  backdrop", "Kostum milik Sprite; backdrop milik Stage"],
        ["change size by  vs  set size to", "change menambah dari ukuran sekarang; set menetapkan nilai"],
        ["next costume  vs  switch costume to", "next berurutan otomatis; switch memilih kostum tertentu"],
    ],
    "banding": [
        ("say  vs  say for () seconds",
         [("assets/looks/02-say.png", "balon menetap sampai diganti"),
          ("assets/looks/01-say-for-seconds.png", "balon hilang sendiri")]),
        ("next costume  vs  switch costume to",
         [("assets/looks/06-next-costume.png", "maju ke kostum berikutnya"),
          ("assets/looks/05-switch-costume-to.png", "langsung ke kostum pilihan")]),
        ("hide  vs  ghost 100",
         [("assets/looks/16-hide.png", "hilang, sentuhan tak terdeteksi"),
          ("assets/banding/looks/01-set-ghost-100.png", "tak terlihat, tapi masih bisa kena")]),
    ],
    "patterns": [
        ("Script reset lengkap", "when green flag clicked\nshow\nclear graphic effects\nset size to (100) %\nswitch costume to\n  (costume1)\ngo to x: (0) y: (0)\npoint in direction (90)"),
        ("Animasi berjalan", "forever\n  next costume\n  move (10) steps\n  wait (0.1) seconds"),
        ("Muncul perlahan", "set (ghost) effect\n  to (100)\nshow\nrepeat (20)\n  change (ghost)\n    effect by (-5)"),
    ],
    "mistakes": [
        ["Balon say tidak mau hilang", "Teks menempel selamanya", "Pakai say [] kosong, atau say ... for () seconds"],
        ["next costume tanpa wait", "Animasi bergetar terlalu cepat", "Tambah wait (0.1) seconds"],
        ["Lupa show di awal", "Sprite \"hilang\" saat proyek dijalankan", "Tambahkan script reset"],
        ["Efek ghost / mosaic tertinggal", "Sprite tampak aneh atau buram", "Tambah clear graphic effects"],
        ["Memakai hide untuk objek yang harus bisa ditabrak", "Deteksi tabrakan gagal", "Pakai set ghost effect to (100)"],
    ],
    "practice": [
        ["*", "Kucing menyapa namamu selama 3 detik", "say for seconds"],
        ["*", "Kucing berjalan dengan animasi kaki", "next costume + wait"],
        ["**", "Tokoh muncul perlahan dari transparan", "set / change ghost effect"],
        ["**", "Sprite membesar saat diklik", "when this sprite clicked, change size by"],
        ["***", "Cerita 3 babak dengan pergantian backdrop & dialog", "switch backdrop, say, broadcast"],
    ],
    "quiz": [
        "Bagaimana cara menghilangkan balon say yang tidak berbatas waktu?",
        "Apa beda hide dengan set ghost effect to (100)?",
        "Blok apa yang membuat animasi berjalan, dan blok apa yang mengatur kecepatannya?",
        "Sebutkan empat blok yang sebaiknya ada di script reset.",
    ],
    "answers": [
        "Gunakan blok say [] dengan kolom teks dikosongkan.",
        "hide membuat sprite tak terlihat DAN tidak terdeteksi touching ()?; ghost 100 tak terlihat tetapi MASIH terdeteksi.",
        "next costume membuat animasi; wait () seconds mengatur kecepatannya.",
        "show, clear graphic effects, set size to (100)%, switch costume to (...), ditambah go to x y dan point in direction (90).",
    ],
    "takeaways": [
        "Animasi = next costume + wait. Tanpa wait, gerakan bergetar.",
        "Balon say tanpa durasi harus dihapus manual dengan say [] kosong.",
        "Script reset wajib memuat show, clear graphic effects, dan set size.",
    ],
}

S = {
    "key": "sound", "short": "Sound", "name": "Sound (Suara)", "subtitle": "9 blok",
    "color": rgb("CF63CF"),
    "tagline": "Memainkan dan mengatur suara dalam proyek.",
    "scope": "Berlaku untuk Sprite dan Stage. Stage biasanya dipakai untuk musik latar.",
    "level": "Dasar",
    "prasyarat": "Suara harus sudah ada di tab Sounds. Cara menambah: pustaka Scratch, "
                 "rekam sendiri lewat mikrofon, atau unggah berkas.",
    "overview": [
        ("Memainkan", "play sound until done, start sound, stop all sounds"),
        ("Efek suara", "change effect by, set effect to, clear sound effects"),
        ("Volume", "change volume by, set volume to, (volume)"),
    ],
    "blocks": [
        {"n": "play sound (Meow) until done", "mudah": "memainkan suara sampai habis dulu, baru blok berikutnya jalan.", "shape": "Stack",
         "fungsi": "Memainkan suara dan MENUNGGU sampai suara habis sebelum melanjutkan.",
         "contoh": "when green flag clicked\nplay sound (Halo)\n  until done\nplay sound (ApaKabar)\n  until done",
         "catatan": "Sifatnya blocking. Inilah blok yang tepat untuk NARASI CERITA agar suara tidak "
                    "saling menimpa."},
        {"n": "start sound (Meow)", "mudah": "menyalakan suara lalu langsung lanjut ke blok berikutnya, tanpa menunggu.", "shape": "Stack",
         "fungsi": "Memainkan suara TANPA menunggu — script langsung lanjut ke blok berikutnya.",
         "contoh": "when (space) key pressed\nstart sound (Pop)\nchange y by (50)",
         "catatan": "Blok yang tepat untuk EFEK SUARA PERMAINAN (tembakan, lompat, koin) karena suara "
                    "dan gerakan terjadi bersamaan."},
        {"n": "stop all sounds", "mudah": "menghentikan seketika semua suara yang sedang berbunyi.", "shape": "Stack",
         "fungsi": "Menghentikan SELURUH suara yang sedang berbunyi, dari semua sprite sekaligus.",
         "contoh": "when I receive (game over)\nstop all sounds\nplay sound (Kalah)\n  until done",
         "catatan": "Wajib dipakai saat berganti level atau adegan agar musik latar lama tidak menumpuk."},
        {"n": "change (pitch) effect by (10)", "mudah": "menambah efek suara, misalnya nada makin tinggi seperti suara tupai.", "shape": "Stack",
         "fungsi": "Menambah nilai efek suara.",
         "param": ["pitch (-360..360) = nada naik/turun",
                   "pan left/right (-100..100) = arah speaker"],
         "contoh": "change (pitch)\n  effect by (20)\nstart sound (Koin)",
         "catatan": "pitch mengubah nada SEKALIGUS kecepatan suara, mirip memutar kaset lebih cepat. "
                    "Efek pan butuh headphone atau speaker stereo agar terasa."},
        {"n": "set (pitch) effect to (100)", "mudah": "menetapkan langsung nilai efek suara. Nilai 0 berarti suara normal.", "shape": "Stack",
         "fungsi": "Menetapkan nilai efek suara secara pasti. Nilai 0 berarti suara normal.",
         "contoh": "set (pitch)\n  effect to (-200)\nplay sound (Halo)\n  until done",
         "catatan": "Nilai pitch negatif besar menghasilkan suara tokoh raksasa; positif besar "
                    "menghasilkan suara tokoh kecil."},
        {"n": "clear sound effects", "mudah": "menghapus semua efek suara supaya kembali normal.", "shape": "Stack",
         "fungsi": "Menghapus semua efek suara (pitch dan pan) sekaligus.",
         "catatan": "Masukkan ke script reset, karena efek suara BERTAHAN meski proyek dihentikan."},
        {"n": "change volume by (-10)", "mudah": "mengurangi keras suara 10 persen dari yang sekarang.", "shape": "Stack",
         "fungsi": "Menambah atau mengurangi volume sprite ini sebanyak N persen.",
         "contoh": "repeat (10)\n  change volume by (-10)\n  wait (0.1) seconds\nstop all sounds",
         "catatan": "Pola di samping adalah cara membuat musik memudar (fade out) saat permainan berakhir."},
        {"n": "set volume to (100) %", "mudah": "menetapkan keras suara. 100% = paling keras, 0% = diam.", "shape": "Stack",
         "fungsi": "Menetapkan volume dalam persen (0 = diam, 100 = penuh).",
         "catatan": "Volume bersifat PER SPRITE. Menyetel volume di Sprite1 tidak memengaruhi Sprite2. "
                    "Untuk musik latar, atur volumenya di Stage."},
        {"n": "(volume)", "mudah": "memberi tahu keras suara sprite ini sekarang berapa persen.", "shape": "Reporter",
         "fungsi": "Melaporkan volume sprite ini saat ini (0-100).",
         "contoh": "if <(volume) > (0)> then\n  change volume by (-10)",
         "catatan": "Ada kotak centang di palet untuk menampilkan monitornya di panggung."},
    ],
    "compare": [
        ["play sound until done  vs  start sound", "Menunggu (blocking) vs jalan terus (non-blocking)"],
        ["stop all sounds  vs  set volume to 0", "Yang pertama menghentikan; yang kedua hanya membisukan"],
        ["change volume by  vs  set volume to", "change menambah; set menetapkan nilai pasti"],
    ],
    "banding": [
        ("play until done  vs  start sound",
         [("assets/sound/01-play-sound-until-done.png", "tunggu suara habis dulu"),
          ("assets/sound/02-start-sound.png", "langsung lanjut ke blok berikutnya")]),
        ("change volume  vs  set volume",
         [("assets/sound/07-change-volume-by.png", "menambah dari volume sekarang"),
          ("assets/sound/08-set-volume-to.png", "langsung ke angka itu")]),
        ("stop all sounds  vs  clear sound effects",
         [("assets/sound/03-stop-all-sounds.png", "suaranya yang dimatikan"),
          ("assets/sound/06-clear-sound-effects.png", "efeknya yang dinormalkan")]),
    ],
    "patterns": [
        ("Musik latar (di Stage)", "when green flag clicked\nset volume to (60) %\nforever\n  play sound (Musik)\n    until done"),
        ("Efek suara permainan", "when this sprite clicked\nstart sound (Pop)\nchange (skor) by (1)"),
        ("Reset suara", "when green flag clicked\nstop all sounds\nclear sound effects\nset volume to (100) %"),
    ],
    "mistakes": [
        ["start sound di dalam forever untuk musik latar", "Suara bertumpuk jadi berisik", "Ganti ke play sound until done"],
        ["play sound until done untuk efek lompat", "Gerakan tertunda menunggu suara", "Ganti ke start sound"],
        ["Efek pitch tertinggal dari percobaan", "Semua suara terdengar aneh", "Tambah clear sound effects di reset"],
        ["Suara ditaruh di sprite yang salah", "Dropdown tidak memuat suara yang dicari", "Cek tab Sounds pada sprite yang benar"],
        ["Rekaman terlalu panjang", "Proyek berat (batas 10 MB per aset)", "Potong di Sound Editor, cukup beberapa detik"],
    ],
    "practice": [
        ["*", "Kucing mengeong saat diklik", "when this sprite clicked, start sound"],
        ["*", "Rekam suaramu sendiri lalu mainkan", "tab Sounds > Record, play sound until done"],
        ["**", "Musik latar berulang tanpa putus", "forever + play sound until done"],
        ["**", "Musik memudar saat permainan berakhir", "change volume by, repeat"],
        ["***", "Nada naik tiap kali dapat poin", "change pitch effect by, variabel"],
    ],
    "quiz": [
        "Kamu ingin efek suara lompat berbunyi BERSAMAAN dengan gerakan. Blok mana yang dipakai?",
        "Mengapa musik latar dalam forever sebaiknya memakai play sound until done?",
        "Apakah set volume to (50)% di Sprite1 memengaruhi volume Sprite2?",
        "Blok apa yang mengembalikan suara ke normal setelah dipakai efek pitch?",
    ],
    "answers": [
        "start sound, karena sifatnya non-blocking sehingga script langsung lanjut.",
        "Agar lagu selesai dulu baru diulang; dengan start sound lagu akan ditumpuk berkali-kali sehingga berisik.",
        "Tidak. Volume bersifat per sprite.",
        "clear sound effects, atau set (pitch) effect to (0).",
    ],
    "takeaways": [
        "play sound until done = menunggu; start sound = jalan terus. Ini konsep blocking vs non-blocking.",
        "Musik latar: forever + play sound until done, diletakkan di Stage.",
        "Volume dan efek suara bersifat per sprite dan bertahan antar sesi — masukkan ke script reset.",
    ],
}

E = {
    "key": "events", "short": "Events", "name": "Events (Kejadian)", "subtitle": "9 blok",
    "color": rgb("FFBF00"),
    "tagline": "Menentukan KAPAN sebuah script mulai berjalan.",
    "scope": "Kategori paling penting untuk pemula. Aturan kelas: setiap script diawali blok kuning.",
    "level": "Dasar",
    "prasyarat": "Tanpa blok Events, script tidak akan pernah berjalan sendiri saat bendera hijau diklik.",
    "overview": [
        ("Pemicu pemain", "when green flag clicked, when key pressed, when this sprite clicked"),
        ("Pemicu panggung", "when stage clicked, when backdrop switches to"),
        ("Pemicu sensor", "when (loudness / timer) > ()"),
        ("Pesan siaran", "when I receive, broadcast, broadcast and wait"),
    ],
    "blocks": [
        {"n": "when green flag clicked", "mudah": "semua blok di bawahnya jalan begitu bendera hijau ditekan. Ini pintu masuk program.", "shape": "Hat",
         "fungsi": "Menjalankan script di bawahnya saat bendera hijau ditekan.",
         "contoh": "when green flag clicked\ngo to x: (0) y: (0)\nsay [Mulai!]\n  for (2) seconds",
         "catatan": "Boleh dipakai BERKALI-KALI dalam satu sprite; semuanya berjalan bersamaan (paralel). "
                    "Kalau siswa mengeluh \"tidak terjadi apa-apa\", 90% penyebabnya blok ini tidak ada."},
        {"n": "when (space) key pressed", "mudah": "blok di bawahnya jalan tiap kali tombol yang dipilih ditekan.", "shape": "Hat",
         "fungsi": "Menjalankan script saat tombol keyboard tertentu ditekan.",
         "param": ["space, panah, huruf a-z, angka 0-9", "any = tombol apa saja"],
         "contoh": "when (space) key pressed\nchange y by (50)",
         "catatan": "JEBAKAN GAME: blok ini punya jeda ulang seperti menahan tombol saat mengetik, "
                    "sehingga gerakan TERSENDAT. Untuk kontrol mulus gunakan forever + if <key () pressed?>.",
         "warn": True},
        {"n": "when this sprite clicked", "mudah": "blok di bawahnya jalan tiap sprite ini diklik. Cocok untuk membuat tombol.", "shape": "Hat",
         "fungsi": "Menjalankan script saat sprite tersebut diklik pemain.",
         "contoh": "when this sprite clicked\nstart sound (Pop)\nchange (skor) by (1)",
         "catatan": "Sprite yang sedang hide TIDAK bisa diklik. Klik hanya terdeteksi pada bagian "
                    "gambar yang tidak transparan."},
        {"n": "when stage clicked", "mudah": "blok di bawahnya jalan tiap panggungnya yang diklik, bukan spritenya.", "shape": "Hat",
         "fungsi": "Versi blok sebelumnya yang muncul saat Stage yang dipilih — dipicu saat latar diklik.",
         "catatan": "Blok ini menggantikan when this sprite clicked di palet Stage. Itulah sebabnya "
                    "jumlah blok Events kadang disebut 8, kadang 9."},
        {"n": "when backdrop switches to (Level2)", "mudah": "blok di bawahnya jalan tiap latar berganti ke backdrop itu. Berguna untuk pindah level.", "shape": "Hat",
         "fungsi": "Menjalankan script saat latar panggung berganti ke backdrop tertentu.",
         "contoh": "when backdrop switches\n  to (Level2)\nshow\ngo to x: (200) y: (0)",
         "catatan": "Cara paling rapi membuat permainan berlevel atau cerita berbabak. Tidak terpicu "
                    "bila backdrop diganti ke latar yang SUDAH aktif."},
        {"n": "when (loudness) > (10)", "mudah": "blok di bawahnya jalan kalau suara di sekitar melebihi angka itu. Perlu mikrofon.", "shape": "Hat",
         "fungsi": "Menjalankan script saat nilai sensor melampaui ambang batas.",
         "param": ["loudness = tingkat suara mikrofon (0-100)", "timer = waktu berjalan (detik)"],
         "contoh": "when (loudness) > (30)\nchange y by (50)",
         "catatan": "Perlu izin mikrofon dari browser. Sangat disukai siswa — cocok untuk demo "
                    "\"coding yang bisa mendengar\"."},
        {"n": "when I receive (mulai)", "mudah": "blok di bawahnya jalan begitu pesan itu disiarkan. Cara sprite saling memberi aba-aba.", "shape": "Hat",
         "fungsi": "Menjalankan script saat pesan siaran (broadcast) tertentu diterima.",
         "contoh": "when I receive\n  (game over)\nhide\nstop all sounds",
         "catatan": "Semua sprite DAN Stage bisa menerima pesan yang sama. Satu pesan bisa memicu "
                    "banyak script sekaligus."},
        {"n": "broadcast (mulai)", "mudah": "menyiarkan pesan ke semua sprite lalu langsung lanjut, tanpa menunggu.", "shape": "Stack",
         "fungsi": "Mengirim pesan siaran ke seluruh proyek, lalu LANGSUNG melanjutkan.",
         "contoh": "when green flag clicked\nsay [Bersiap...]\n  for (2) seconds\nbroadcast\n  (mulai permainan)",
         "catatan": "Mekanisme komunikasi antar-sprite. Sprite tidak bisa memerintah sprite lain "
                    "secara langsung — mereka \"berteriak\" lewat pesan."},
        {"n": "broadcast (mulai) and wait", "mudah": "menyiarkan pesan lalu menunggu sampai semua penerimanya selesai bekerja.", "shape": "Stack",
         "fungsi": "Mengirim pesan lalu MENUNGGU semua script penerima selesai, baru melanjutkan.",
         "contoh": "when green flag clicked\nbroadcast (babak1)\n  and wait\nbroadcast (babak2)\n  and wait\nbroadcast (tamat)\n  and wait",
         "catatan": "Inilah cara membuat urutan adegan yang tidak saling menyerobot. Tanpa \"and wait\", "
                    "semua babak berjalan bersamaan dan berantakan."},
    ],
    "compare": [
        ["when () key pressed  vs  if <key () pressed?>", "Hat block TERSENDAT; Sensing dalam forever MULUS — pakai untuk game"],
        ["broadcast  vs  broadcast and wait", "Yang pertama jalan terus; yang kedua menunggu penerima selesai"],
        ["when green flag clicked  vs  when I receive", "Bendera dipicu pemain; broadcast dipicu program"],
        ["when backdrop switches to  vs  when I receive", "Backdrop = pemicu visual (level); broadcast = pemicu logika (bebas)"],
    ],
    "banding": [
        ("broadcast  vs  broadcast and wait",
         [("assets/events/08-broadcast.png", "kirim lalu langsung lanjut"),
          ("assets/events/09-broadcast-and-wait.png", "tunggu penerima selesai")]),
        ("hat tombol  vs  boolean tombol",
         [("assets/events/02-when-key-pressed.png", "memulai script sendiri"),
          ("assets/sensing/07-key-pressed.png", "dipasang di dalam if")]),
        ("bendera hijau  vs  when I receive",
         [("assets/events/01-when-green-flag-clicked.png", "dipicu pemain"),
          ("assets/events/07-when-i-receive.png", "dipicu script lain")]),
    ],
    "patterns": [
        ("Dialog dua sprite", "[Kucing]\nwhen green flag clicked\nsay [Halo Beruang!]\n  for (2) seconds\nbroadcast (giliran beruang)\n\n[Beruang]\nwhen I receive\n  (giliran beruang)\nsay [Halo Kucing!]\n  for (2) seconds"),
        ("Cerita berurutan", "when green flag clicked\nbroadcast (babak1)\n  and wait\nbroadcast (babak2)\n  and wait\nbroadcast (tamat)\n  and wait"),
        ("Kontrol game yang benar", "when green flag clicked\nforever\n  if <key (right arrow)\n     pressed?> then\n    change x by (10)"),
    ],
    "mistakes": [
        ["Script tanpa hat block", "Bendera hijau diklik, tidak terjadi apa-apa", "Tambah when green flag clicked"],
        ["Kontrol game pakai when () key pressed", "Gerakan tersendat saat tombol ditahan", "Ganti ke forever + if <key () pressed?>"],
        ["broadcast padahal butuh urutan", "Adegan tumpang tindih", "Pakai broadcast () and wait"],
        ["Pesan diberi nama message1", "Proyek besar jadi tidak terbaca", "Beri nama bermakna: mulai, game over, level2"],
        ["when this sprite clicked pada sprite yang di-hide", "Klik tidak berfungsi", "Pastikan sprite dalam keadaan show"],
    ],
    "practice": [
        ["*", "Kucing menyapa saat bendera hijau diklik", "when green flag clicked"],
        ["*", "Kucing mengeong saat diklik", "when this sprite clicked"],
        ["**", "Kucing melompat saat spasi ditekan", "when (space) key pressed"],
        ["**", "Sprite melompat saat kamu bertepuk tangan", "when (loudness) > ()"],
        ["***", "Dua sprite berdialog bergantian rapi", "broadcast, when I receive"],
        ["***", "Cerita 3 babak berurutan", "broadcast () and wait"],
    ],
    "quiz": [
        "Mengapa kontrol permainan sebaiknya TIDAK memakai when () key pressed?",
        "Apa beda broadcast dengan broadcast and wait?",
        "Berapa sprite yang bisa menanggapi satu pesan broadcast?",
        "Sprite kamu tidak bereaksi saat diklik. Sebutkan dua kemungkinan penyebabnya.",
    ],
    "answers": [
        "Karena blok itu punya jeda ulang sehingga gerakan tersendat; gunakan forever + if <key () pressed?> dari Sensing.",
        "broadcast langsung lanjut tanpa menunggu; broadcast and wait menunggu semua script penerima selesai lebih dulu.",
        "Tidak terbatas — semua sprite dan Stage yang punya when I receive dengan pesan sama akan menanggapi.",
        "Sprite sedang hide; script tidak diawali when this sprite clicked; atau yang diklik adalah area transparan kostum.",
    ],
    "takeaways": [
        "Setiap script wajib diawali blok kuning, kalau tidak ia tidak akan pernah berjalan.",
        "Untuk kontrol permainan, pakai Sensing di dalam forever — bukan when () key pressed.",
        "broadcast = pengeras suara sekolah: pengirim tidak perlu tahu siapa yang mendengar.",
    ],
}

C = {
    "key": "control", "short": "Control", "name": "Control (Kontrol)", "subtitle": "11 blok",
    "color": rgb("FFAB19"),
    "tagline": "Mengatur ALUR program: perulangan, percabangan, jeda, dan klon.",
    "scope": "Berisi inti berpikir komputasional — loop dan conditional ada di semua bahasa pemrograman.",
    "level": "Menengah",
    "prasyarat": "Lubang segi enam pada if / repeat until / wait until hanya menerima blok Boolean "
                 "dari kategori Sensing atau Operators.",
    "overview": [
        ("Jeda", "wait () seconds, wait until <>"),
        ("Perulangan", "repeat (), forever, repeat until <>"),
        ("Percabangan", "if <> then, if <> then else"),
        ("Penghenti", "stop ()"),
        ("Klon", "create clone of, when I start as a clone, delete this clone"),
    ],
    "blocks": [
        {"n": "wait (1) seconds", "mudah": "menjeda program selama 1 detik sebelum lanjut ke blok berikutnya.", "shape": "Stack",
         "fungsi": "Menghentikan script ini selama N detik, lalu melanjutkan.",
         "contoh": "forever\n  hide\n  wait (0.5) seconds\n  show\n  wait (0.5) seconds",
         "catatan": "Hanya menjeda SCRIPT INI; script lain tetap berjalan. Nilai kecil seperti 0.1 "
                    "dipakai untuk mengatur kecepatan animasi."},
        {"n": "wait until <>", "mudah": "menahan program sampai syarat di dalamnya benar, baru lanjut.", "shape": "Stack",
         "fungsi": "Menghentikan script sampai kondisi di lubang segi enam menjadi BENAR.",
         "contoh": "say [Tekan spasi\n  untuk mulai]\nwait until\n  <key (space) pressed?>\nsay [Mulai!]\n  for (1) seconds",
         "catatan": "Lebih hemat daripada repeat until kosong. Bila kondisinya tidak pernah benar, "
                    "script menunggu selamanya — sering jadi penyebab program \"macet\"."},
        {"n": "repeat (10)", "mudah": "mengulang blok di dalam pelukannya tepat 10 kali, lalu berhenti.", "shape": "C",
         "fungsi": "Mengulang blok di dalamnya sebanyak N kali, lalu melanjutkan ke bawah.",
         "contoh": "repeat (4)\n  move (100) steps\n  turn right (90) degrees",
         "catatan": "Ini counted loop — jumlah pengulangan sudah diketahui sejak awal. "
                    "Rumus segi-n: repeat (n) + turn right (360/n) degrees."},
        {"n": "forever", "mudah": "mengulang blok di dalamnya terus-menerus dan tidak pernah berhenti sendiri.", "shape": "C",
         "fungsi": "Mengulang blok di dalamnya SELAMANYA, sampai proyek dihentikan.",
         "contoh": "when green flag clicked\nforever\n  move (5) steps\n  if on edge, bounce",
         "catatan": "Bawahnya sengaja dibuat RATA — tidak ada blok yang bisa dipasang setelah forever, "
                    "karena ia tidak akan pernah selesai. Pola forever + if adalah inti setiap permainan."},
        {"n": "repeat until <>", "mudah": "mengulang terus sampai syaratnya benar, baru berhenti.", "shape": "C",
         "fungsi": "Mengulang SELAMA kondisi masih salah; berhenti begitu kondisi menjadi benar.",
         "contoh": "repeat until\n  <touching (edge)?>\n  move (10) steps\nsay [Sampai!]",
         "catatan": "Logikanya TERBALIK dari while di bahasa lain. Di Scratch: mengulang SAMPAI benar, "
                    "bukan SELAMA benar. Ini sumber kebingungan yang perlu ditegaskan.", "warn": True},
        {"n": "if <> then", "mudah": "menjalankan blok di dalamnya HANYA kalau syaratnya benar.", "shape": "C",
         "fungsi": "Menjalankan blok di dalamnya HANYA BILA kondisi bernilai benar; bila salah dilewati.",
         "contoh": "forever\n  if <touching (Musuh)?>\n    then\n    change (nyawa)\n      by (-1)",
         "catatan": "Dicek satu kali saat blok dilewati. Untuk pengecekan terus-menerus, WAJIB "
                    "dibungkus forever."},
        {"n": "if <> then ... else ...", "mudah": "kalau syaratnya benar jalankan bagian atas; kalau salah, jalankan bagian bawah.", "shape": "C",
         "fungsi": "Menjalankan bagian pertama bila kondisi benar, bagian else bila salah.",
         "contoh": "ask [Berapa 5 + 3?]\n  and wait\nif <(answer) = (8)> then\n  say [Benar!]\nelse\n  say [Salah]",
         "catatan": "Salah satu bagian PASTI dijalankan. Untuk lebih dari dua pilihan, susun if-else "
                    "bersarang (nested)."},
        {"n": "stop (all)", "mudah": "menghentikan program. Bisa dipilih: semua script, script ini saja, atau script lain.", "shape": "Cap",
         "fungsi": "Menghentikan script. Berubah jadi blok Stack bila memilih \"other scripts in sprite\".",
         "param": ["all = seluruh script di semua sprite", "this script = hanya script ini",
                   "other scripts in sprite = script lain di sprite ini"],
         "contoh": "if <(nyawa) = (0)> then\n  say [Game Over]\n    for (2) seconds\n  stop (all)",
         "catatan": "Hanya opsi \"other scripts in sprite\" yang bisa disambung ke bawah, karena dua "
                    "opsi lain memang mengakhiri jalannya script."},
        {"n": "create clone of (myself)", "mudah": "membuat salinan sprite yang bisa jalan sendiri. Cocok untuk peluru atau musuh banyak.", "shape": "Stack",
         "fungsi": "Membuat satu klon baru saat proyek berjalan.",
         "contoh": "when green flag clicked\nhide\nforever\n  create clone of\n    (myself)\n  wait (0.5) seconds",
         "catatan": "Klon mewarisi posisi, arah, ukuran, kostum, efek, dan nilai variabel lokal dari "
                    "induknya PADA SAAT diklon."},
        {"n": "when I start as a clone", "mudah": "blok di bawahnya jalan tiap kali sebuah salinan baru lahir.", "shape": "Hat",
         "fungsi": "Script yang dijalankan oleh SETIAP KLON begitu klon itu lahir.",
         "contoh": "when I start as a clone\ngo to x: (pick random\n  (-240) to (240))\n  y: (180)\nshow\nrepeat until\n  <(y position) < (-170)>\n  change y by (-5)\ndelete this clone",
         "catatan": "Hanya berjalan pada KLON, tidak pernah pada sprite aslinya. Kunci membuat banyak "
                    "objek serupa (peluru, musuh, koin) tanpa menggandakan sprite manual."},
        {"n": "delete this clone", "mudah": "menghapus salinan ini supaya tidak menumpuk dan membuat proyek berat.", "shape": "Cap",
         "fungsi": "Menghapus klon yang sedang menjalankan blok ini. Tidak berpengaruh pada sprite asli.",
         "catatan": "WAJIB DIPAKAI. Batas Scratch adalah 300 KLON AKTIF; setelahnya create clone "
                    "diabaikan diam-diam sehingga permainan tampak rusak dan makin lambat.", "warn": True},
    ],
    "compare": [
        ["repeat ()  vs  forever", "repeat berhenti setelah N kali; forever tidak pernah berhenti sendiri"],
        ["repeat until  vs  while (bahasa lain)", "Scratch mengulang SAMPAI benar; while mengulang SELAMA benar"],
        ["if  vs  wait until", "if mengecek sekali lalu lanjut; wait until menahan script sampai benar"],
        ["stop (all)  vs  stop (this script)", "Menghentikan semuanya vs hanya script yang bersangkutan"],
        ["duplicate sprite  vs  create clone", "duplicate saat mengedit (permanen); clone saat berjalan (sementara)"],
    ],
        "banding": [
        ("repeat  vs  forever",
         [("assets/control/03-repeat.png", "berhenti setelah N kali"),
          ("assets/control/04-forever.png", "tidak pernah berhenti")]),
        ("if  vs  wait until",
         [("assets/control/06-if-then.png", "cek sekali, langsung lanjut"),
          ("assets/control/02-wait-until.png", "menahan sampai benar")]),
        ("stop: all  vs  this script",
         [("assets/control/08-stop-all.png", "semua script mati"),
          ("assets/banding/control/01-stop-this-script.png", "hanya script ini")]),
    ],
    "patterns": [
        ("Mesin permainan", "when green flag clicked\nforever\n  if <key (right arrow)\n     pressed?> then\n    change x by (10)\n  if <touching (Musuh)?>\n    then\n    broadcast\n      (game over)"),
        ("Peluru dengan klon", "when I receive (tembak)\ncreate clone of (myself)\n\nwhen I start as a clone\ngo to (Pemain)\nshow\nrepeat until\n  <touching (edge)?>\n  change y by (10)\ndelete this clone"),
        ("Percabangan bertingkat", "if <(nilai) > (85)> then\n  say [A]\nelse\n  if <(nilai) > (70)>\n    then\n    say [B]\n  else\n    say [C]"),
    ],
    "mistakes": [
        ["if tanpa dibungkus forever", "Tabrakan / tombol hanya dicek sekali", "Bungkus dengan forever"],
        ["Mencoba menyambung blok di bawah forever", "Blok tidak bisa menempel", "Taruh blok itu DI DALAM loop"],
        ["Lupa delete this clone", "Permainan melambat lalu klon berhenti muncul", "Selalu akhiri hidup klon (batas 300)"],
        ["Salah paham repeat until", "Loop berjalan terbalik dari harapan", "Tegaskan: mengulang SAMPAI benar"],
        ["Terlalu banyak wait di loop kontrol", "Kontrol pemain terasa berat", "Kurangi atau hilangkan wait di loop kontrol"],
    ],
    "practice": [
        ["*", "Kucing berkedip 10 kali", "repeat, show, hide, wait"],
        ["*", "Menggambar segitiga dan segi enam", "repeat, turn"],
        ["**", "Sprite bergerak terus dan memantul", "forever, if on edge bounce"],
        ["**", "Kuis benar / salah", "if-else, ask and wait"],
        ["**", "Bergerak sampai menyentuh garis finis", "repeat until"],
        ["***", "Hujan koin dengan klon", "create clone, when I start as a clone, delete this clone"],
        ["***", "Permainan tembak-tembakan", "ketiga blok klon + broadcast"],
    ],
    "quiz": [
        "Apa beda repeat (10) dengan forever?",
        "Mengapa tidak ada blok yang bisa dipasang di bawah forever?",
        "repeat until <touching (edge)?> — kapan loop ini BERHENTI?",
        "Apa akibatnya jika klon tidak pernah dihapus dengan delete this clone?",
        "Blok apa yang harus dipakai agar setiap klon menjalankan kodenya sendiri?",
    ],
    "answers": [
        "repeat (10) mengulang tepat 10 kali lalu berhenti; forever mengulang tanpa akhir sampai proyek dihentikan.",
        "Karena forever tidak pernah selesai, blok setelahnya tidak akan pernah dijalankan — bentuknya sengaja dibuat rata.",
        "Berhenti begitu sprite MENYENTUH TEPI, yaitu saat kondisinya menjadi benar.",
        "Klon menumpuk sampai batas 300; setelah itu klon baru tidak terbuat, permainan melambat dan tampak rusak.",
        "when I start as a clone.",
    ],
    "takeaways": [
        "forever + if adalah pola inti setiap permainan Scratch.",
        "repeat until berlogika terbalik dari while: mengulang SAMPAI benar.",
        "Setiap create clone harus punya pasangan delete this clone — batasnya 300 klon.",
    ],
}

SE = {
    "key": "sensing", "short": "Sensing", "name": "Sensing (Sensor)", "subtitle": "18 blok",
    "color": rgb("5CB1D6"),
    "tagline": "Membuat proyek MERASAKAN: tabrakan, tombol, mouse, mikrofon, waktu, dan jawaban pemain.",
    "scope": "Kategori yang mengubah proyek dari animasi menjadi interaktif. "
             "Hampir semua bloknya dipasangkan dengan if dari Control.",
    "level": "Menengah",
    "prasyarat": "Blok berbentuk Boolean (segi enam) hanya bisa dipasang di lubang segi enam: "
                 "if, repeat until, wait until, and / or / not.",
    "overview": [
        ("Deteksi tabrakan & jarak", "touching ()?, touching color ()?, color is touching ()?, distance to ()"),
        ("Input pemain", "ask and wait, (answer), key () pressed?, mouse down?, mouse x, mouse y, set drag mode"),
        ("Sensor perangkat", "(loudness)"),
        ("Waktu", "(timer), reset timer, current (), days since 2000"),
        ("Data objek lain", "([] of ()), (username)"),
    ],
    "blocks": [
        {"n": "<touching (mouse-pointer)?>", "mudah": "bertanya: apakah sprite sedang bersentuhan dengan sasaran itu? Jawabannya benar atau salah.", "shape": "Boolean",
         "fungsi": "Bernilai BENAR bila sprite sedang menyentuh target.",
         "param": ["mouse-pointer", "edge = tepi panggung", "(nama sprite lain)"],
         "contoh": "forever\n  if <touching (Musuh)?>\n    then\n    change (nyawa)\n      by (-1)\n    wait (1) seconds",
         "catatan": "Sprite yang sedang hide TIDAK terdeteksi. Beri wait setelah pengurangan nyawa, "
                    "kalau tidak nyawa berkurang puluhan kali dalam sekejap."},
        {"n": "<touching color [ ]?>", "mudah": "bertanya: apakah sprite sedang menyentuh warna tertentu?", "shape": "Boolean",
         "fungsi": "Bernilai benar bila sprite menyentuh WARNA tertentu apa pun di panggung.",
         "contoh": "forever\n  if <touching color\n     [hitam]?> then\n    go to x: (0) y: (0)",
         "catatan": "Warna harus PERSIS SAMA. Gunakan alat PIPET (eyedropper) untuk mengambil warna "
                    "langsung dari panggung — jangan menebak dari roda warna.", "warn": True},
        {"n": "<color [ ] is touching [ ]?>", "mudah": "bertanya: apakah bagian berwarna tertentu pada sprite menyentuh warna lain?", "shape": "Boolean",
         "fungsi": "Benar bila warna tertentu PADA SPRITE INI menyentuh warna tertentu di panggung.",
         "catatan": "Versi lebih presisi. Contoh: hanya bagian kaki tokoh (merah) yang menyentuh tanah "
                    "(hijau) — dipakai untuk deteksi pijakan pada game platformer."},
        {"n": "(distance to (mouse-pointer))", "mudah": "memberi tahu jarak sprite ke sasaran dalam satuan titik.", "shape": "Reporter",
         "fungsi": "Melaporkan jarak dalam piksel dari sprite ini ke target.",
         "param": ["mouse-pointer atau nama sprite lain", "TIDAK ada pilihan edge"],
         "contoh": "forever\n  if <(distance to\n     (Harta)) < (50)>\n    then\n    say [Panas!]\n  else\n    say [Dingin...]",
         "catatan": "Alternatif deteksi tabrakan yang lebih halus — bisa mendeteksi \"hampir kena\" "
                    "sebelum benar-benar bersentuhan."},
        {"n": "ask [Siapa namamu?] and wait", "mudah": "memunculkan kotak pertanyaan lalu menunggu pemain mengetik jawabannya.", "shape": "Stack",
         "fungsi": "Menampilkan kotak isian di bawah panggung dan MENUNGGU pemain mengetik lalu Enter.",
         "contoh": "ask [Siapa namamu?]\n  and wait\nsay (join [Halo, ]\n  (answer))\n  for (2) seconds",
         "catatan": "Bila dijalankan sprite yang terlihat, pertanyaan muncul dalam balon bicara; bila "
                    "oleh Stage atau sprite tersembunyi, muncul sebagai teks biasa."},
        {"n": "(answer)", "mudah": "menyimpan jawaban terakhir yang diketik pemain.", "shape": "Reporter",
         "fungsi": "Melaporkan jawaban terakhir yang diketik pemain.",
         "contoh": "ask [Siapa namamu?]\n  and wait\nset (nama) to (answer)",
         "catatan": "answer bersifat GLOBAL dan akan TERTIMPA oleh ask berikutnya. Bila jawaban masih "
                    "dibutuhkan, salin segera ke variabel.", "warn": True},
        {"n": "<key (space) pressed?>", "mudah": "bertanya: apakah tombol itu sedang ditekan sekarang?", "shape": "Boolean",
         "fungsi": "Bernilai benar SELAMA tombol ditekan.",
         "contoh": "when green flag clicked\nforever\n  if <key (right arrow)\n     pressed?> then\n    change x by (10)\n  if <key (left arrow)\n     pressed?> then\n    change x by (-10)",
         "catatan": "INILAH CARA YANG BENAR untuk kontrol permainan — tanpa jeda tersendat seperti "
                    "blok Events when () key pressed. Bandingkan keduanya di kelas."},
        {"n": "<mouse down?>", "mudah": "bertanya: apakah tombol mouse sedang ditekan?", "shape": "Boolean",
         "fungsi": "Bernilai benar selama tombol mouse ditekan.",
         "contoh": "forever\n  go to (mouse-pointer)\n  if <mouse down?> then\n    pen down\n  else\n    pen up",
         "catatan": "Contoh di samping memakai ekstensi Pen untuk membuat aplikasi menggambar sederhana."},
        {"n": "(mouse x)", "mudah": "memberi tahu posisi kiri-kanan kursor mouse.", "shape": "Reporter",
         "fungsi": "Melaporkan koordinat X kursor mouse, rentang -240 sampai 240.",
        "catatan": "Selalu tersedia walau mouse di luar panggung — nilainya berhenti di batas -240 dan 240. Pasangannya (mouse y) dengan rentang -180 sampai 180."},
        {"n": "(mouse y)", "mudah": "memberi tahu posisi atas-bawah kursor mouse.", "shape": "Reporter",
         "fungsi": "Melaporkan koordinat Y kursor mouse, rentang -180 sampai 180.",
         "contoh": "forever\n  set x to (mouse x)",
         "catatan": "Contoh di samping membuat papan pemantul (game Pong) yang mengikuti mouse hanya "
                    "secara mendatar."},
        {"n": "set drag mode (draggable)", "mudah": "mengatur boleh tidaknya sprite digeser pakai mouse saat proyek berjalan.", "shape": "Stack",
         "fungsi": "Menentukan apakah pemain boleh MENYERET sprite saat proyek berjalan penuh layar.",
         "param": ["draggable = boleh diseret", "not draggable = tidak boleh"],
         "catatan": "Di dalam editor sprite SELALU bisa diseret; pengaturan ini baru terasa pada mode "
                    "layar penuh. Berguna untuk permainan puzzle susun gambar."},
        {"n": "(loudness)", "mudah": "memberi tahu seberapa keras suara di sekitar, ditangkap lewat mikrofon.", "shape": "Reporter",
         "fungsi": "Melaporkan tingkat kekerasan suara dari mikrofon, rentang 0 sampai 100.",
         "contoh": "forever\n  set size to\n    ((loudness) + (50)) %",
         "catatan": "Perlu izin mikrofon dari browser. Nilai di kelas yang ramai biasanya 10-30; "
                    "tepuk tangan bisa 60 ke atas."},
        {"n": "(timer)", "mudah": "memberi tahu sudah berapa detik berjalan sejak penghitung waktu terakhir dinolkan.", "shape": "Reporter",
         "fungsi": "Melaporkan waktu berjalan dalam detik, dengan desimal.",
         "catatan": "Timer SELALU berjalan sejak proyek dimuat dan TIDAK otomatis nol saat bendera "
                    "hijau diklik — karena itu hampir selalu dipasangkan dengan reset timer.", "warn": True},
        {"n": "reset timer", "mudah": "mengembalikan penghitung waktu ke nol.", "shape": "Stack",
         "fungsi": "Mengembalikan timer ke nol.",
         "contoh": "when green flag clicked\nreset timer\nrepeat until\n  <(timer) > (30)>\n  change (skor) by (1)\nsay [Waktu habis!]",
        "catatan": "Timer berjalan sendiri sejak proyek dibuka dan TIDAK ikut nol saat bendera hijau diklik. Kalau butuh hitungan dari nol, blok ini wajib dipanggil sendiri."},
        {"n": "(current (year))", "mudah": "mengambil waktu sekarang dari jam komputer: tahun, bulan, jam, dan seterusnya.", "shape": "Reporter",
         "fungsi": "Melaporkan data waktu NYATA dari komputer pemain.",
         "param": ["year, month, date, day of week", "hour (format 24 jam), minute, second"],
         "contoh": "if <(current (hour))\n   < (12)> then\n  say [Selamat pagi!]\nelse\n  say [Selamat sore!]",
         "catatan": "day of week bernilai 1 untuk Minggu sampai 7 untuk Sabtu."},
        {"n": "(days since 2000)", "mudah": "memberi tahu sudah berapa hari sejak 1 Januari 2000. Sering dipakai membuat angka acak.", "shape": "Reporter",
         "fungsi": "Melaporkan jumlah hari sejak 1 Januari 2000, dalam bentuk desimal.",
         "catatan": "Dipakai untuk menghitung selisih waktu panjang, misalnya \"sudah berapa hari sejak "
                    "terakhir bermain\". Materi lanjutan."},
        {"n": "([x position] of (Sprite1))", "mudah": "mengintip nilai milik sprite lain, misalnya posisi atau ukurannya.", "shape": "Reporter",
         "fungsi": "Membaca PROPERTI sprite atau Stage lain.",
         "param": ["Sprite: x position, y position, direction, costume #/name, size, volume, variabel lokal",
                   "Stage: backdrop #/name, volume, variabel global"],
         "contoh": "forever\n  set x to\n    ([x position]\n     of (Pemain))",
         "catatan": "Satu-satunya cara sprite \"mengintip\" data sprite lain. Sangat berguna untuk AI "
                    "musuh dan efek kamera pengikut."},
        {"n": "(username)", "mudah": "memberi tahu nama akun Scratch pemain, bila proyek dibuka di situs Scratch.", "shape": "Reporter",
         "fungsi": "Melaporkan nama pengguna Scratch pemain yang sedang membuka proyek.",
         "contoh": "say (join [Halo, ]\n  (username))\n  for (2) seconds",
         "catatan": "Kosong bila pemain belum login atau proyek dijalankan di editor offline. "
                    "Sering dipakai bersama cloud variable untuk papan skor."},
    ],
    "compare": [
        ["<key () pressed?>  vs  when () key pressed", "Sensing di forever MULUS; Events TERSENDAT saat tombol ditahan"],
        ["touching ()?  vs  distance to ()", "touching = sudah bersentuhan; distance = seberapa dekat"],
        ["touching ()?  vs  touching color ()?", "Menyentuh objek vs menyentuh warna apa pun di panggung"],
        ["(timer)  vs  (current (second))", "timer = waktu berjalan proyek; current = jam nyata komputer"],
        ["(answer)  vs  variabel", "answer selalu tertimpa ask berikutnya; variabel tersimpan aman"],
    ],
    "banding": [
        ("touching?  vs  distance to",
         [("assets/sensing/01-touching.png", "sudah bersentuhan atau belum"),
          ("assets/sensing/04-distance-to.png", "berapa jauh, berupa angka")]),
        ("boolean tombol  vs  hat tombol",
         [("assets/sensing/07-key-pressed.png", "dipasang di dalam if"),
          ("assets/events/02-when-key-pressed.png", "memulai script sendiri")]),
        ("answer  vs  variabel",
         [("assets/sensing/06-answer.png", "tertimpa pertanyaan berikutnya"),
          ("assets/variables/02-variabel-reporter.png", "isinya bertahan sampai diganti")]),
    ],
    "patterns": [
        ("Kontrol pemain (wajib)", "when green flag clicked\nforever\n  if <key (right arrow)\n     pressed?> then\n    change x by (10)\n  if <key (left arrow)\n     pressed?> then\n    change x by (-10)"),
        ("Tabrakan dengan jeda aman", "forever\n  if <touching (Musuh)?>\n    then\n    change (nyawa)\n      by (-1)\n    start sound (Aduh)\n    wait (1) seconds"),
        ("Kuis dengan jawaban", "ask [Berapa 7 x 8?]\n  and wait\nif <(answer) = (56)>\n  then\n  change (skor) by (10)"),
    ],
    "mistakes": [
        ["Blok Sensing tidak dibungkus forever", "Hanya terdeteksi sekali", "Bungkus dengan forever"],
        ["Nyawa berkurang drastis saat bersentuhan", "Berkurang tiap frame", "Tambah wait (1) seconds setelahnya"],
        ["touching color diisi dengan menebak warna", "Tidak pernah terdeteksi", "Gunakan alat PIPET untuk mengambil warna asli"],
        ["Lupa reset timer", "Waktu sudah berjalan sebelum permainan mulai", "Tambah reset timer setelah bendera hijau"],
        ["answer dipakai jauh setelah ask", "Nilainya sudah tertimpa", "Simpan segera ke variabel"],
    ],
    "practice": [
        ["*", "Kucing menyapa dengan nama pemain", "ask and wait, answer, join"],
        ["*", "Sprite mengikuti mouse", "mouse x, mouse y"],
        ["**", "Kontrol 4 arah dengan tombol panah", "key () pressed?, forever, if"],
        ["**", "Permainan tangkap koin dengan skor", "touching ()?, variabel"],
        ["**", "Balon membesar saat ditiup", "loudness"],
        ["***", "Labirin: menyentuh dinding kembali ke awal", "touching color ()?"],
        ["***", "Musuh mengikuti posisi pemain", "([x position] of (Pemain))"],
    ],
    "quiz": [
        "Mengapa <key () pressed?> lebih baik daripada when () key pressed untuk kontrol permainan?",
        "Apa yang terjadi pada nilai (answer) setelah blok ask dijalankan lagi?",
        "Sprite tersembunyi tidak terdeteksi touching ()?. Apa alternatifnya?",
        "Blok apa yang dipakai agar sprite bisa membaca posisi X sprite lain?",
        "Mengapa reset timer hampir selalu dibutuhkan?",
    ],
    "answers": [
        "Karena di dalam forever tidak ada jeda ulang sehingga gerakan mulus; blok Events tersendat saat tombol ditahan.",
        "Nilainya TERTIMPA oleh jawaban baru. Simpan ke variabel bila masih dibutuhkan.",
        "Gunakan set (ghost) effect to (100) — sprite tak terlihat tetapi tetap terdeteksi.",
        "([x position] of (nama sprite)).",
        "Karena timer berjalan sejak proyek dimuat dan tidak otomatis nol saat bendera hijau diklik.",
    ],
    "takeaways": [
        "Kontrol permainan = forever + if <key () pressed?>, bukan hat block Events.",
        "Semua blok Sensing perlu dibungkus forever agar terus dipantau.",
        "answer selalu tertimpa ask berikutnya — segera salin ke variabel.",
    ],
}

O = {
    "key": "operators", "short": "Operators", "name": "Operators (Operator)", "subtitle": "18 blok",
    "color": rgb("59C059"),
    "tagline": "Menghitung, membandingkan, mengolah teks, dan menyusun logika.",
    "scope": "Semua blok di sini berbentuk Reporter atau Boolean — tidak bisa berdiri sendiri, "
             "harus dimasukkan ke lubang blok lain.",
    "level": "Menengah",
    "prasyarat": "Reporter (oval) masuk ke lubang oval; Boolean (segi enam) masuk ke lubang segi enam.",
    "overview": [
        ("Aritmetika", "+  -  *  /  mod  round  [abs] of ()"),
        ("Bilangan acak", "pick random () to ()"),
        ("Perbandingan", "<   =   >"),
        ("Logika", "and, or, not"),
        ("Pengolahan teks", "join, letter () of, length of, contains ()?"),
    ],
    "blocks": [
        {"n": "(() + ())   (() - ())", "mudah": "menjumlah dan mengurangi dua angka.", "shape": "Reporter",
         "fungsi": "Penjumlahan dan pengurangan dua nilai.",
         "contoh": "set (total) to\n  ((harga) + (pajak))\nset (sisa) to\n  ((nyawa) - (1))",
        "catatan": "Lubangnya boleh diisi blok lain, jadi rumus panjang dibuat dengan menyusun beberapa operator bersarang. Scratch tidak punya blok satu-baris untuk itu."},
        {"n": "(() * ())   (() / ())", "mudah": "mengalikan dan membagi dua angka.", "shape": "Reporter",
         "fungsi": "Perkalian dan pembagian dua nilai.",
         "contoh": "set (luas) to\n  ((panjang) * (lebar))",
         "catatan": "Pembagian dengan 0 menghasilkan Infinity, bukan pesan kesalahan. Hasilnya bisa "
                    "desimal panjang — bungkus dengan round bila perlu dirapikan."},
        {"n": "(() mod ())", "mudah": "memberi SISA pembagian. Berguna untuk mengecek angka genap atau ganjil.", "shape": "Reporter",
         "fungsi": "Melaporkan SISA pembagian. Contoh: (7) mod (2) = 1.",
         "param": ["Genap/ganjil: ((angka) mod (2)) = (0)",
                   "Muncul dari sisi seberang: ((x) + (10)) mod (480)",
                   "Setiap 5 detik: ((detik) mod (5)) = (0)"],
         "catatan": "Blok yang paling sering diabaikan padahal sangat berguna. Wajib diajarkan bersama "
                    "materi bilangan genap-ganjil di Matematika."},
        {"n": "(round ())", "mudah": "membulatkan angka ke bilangan bulat terdekat.", "shape": "Reporter",
         "fungsi": "Membulatkan ke bilangan bulat terdekat. Nilai tepat 0.5 dibulatkan KE ATAS.",
         "contoh": "say (round\n  ((skor) / (3)))",
         "catatan": "Wajib dipakai saat menampilkan hasil pembagian, agar tidak muncul angka seperti "
                    "3.3333333333 di layar."},
        {"n": "([abs] of ())", "mudah": "kumpulan fungsi matematika: nilai mutlak, akar, pembulatan ke bawah, dan lainnya.", "shape": "Reporter",
         "fungsi": "Menerapkan salah satu dari 14 fungsi matematika.",
         "param": ["abs, floor, ceiling, sqrt", "sin, cos, tan, asin, acos, atan (satuan DERAJAT)",
                   "ln, log, e^, 10^"],
         "contoh": "go to x: ((100) *\n  ([cos] of (sudut)))\n  y: ((100) *\n  ([sin] of (sudut)))",
         "catatan": "Scratch memakai DERAJAT, bukan radian — memudahkan siswa SMP. Tidak ada blok "
                    "pangkat umum; untuk kuadrat gunakan (x) * (x)."},
        {"n": "(pick random (1) to (10))", "mudah": "mengambil satu angka acak di antara dua batas itu.", "shape": "Reporter",
         "fungsi": "Menghasilkan bilangan acak antara dua nilai, termasuk kedua ujungnya.",
         "contoh": "go to x: (pick random\n  (-240) to (240))\n  y: (pick random\n  (-180) to (180))",
         "catatan": "Bila KEDUA input bilangan bulat, hasilnya bulat. Bila salah satu ditulis desimal "
                    "(mis. 1.0), hasilnya bisa desimal — ini kerap membingungkan siswa."},
        {"n": "(() < ())   (() = ())   (() > ())", "mudah": "membandingkan dua nilai. Hasilnya benar atau salah, dipakai di dalam blok if.", "shape": "Boolean",
         "fungsi": "Membandingkan dua nilai; menghasilkan benar atau salah.",
         "contoh": "if <(skor) > (100)>\n  then\n  say [Menang!]",
         "catatan": "TIDAK ADA blok >= atau <=. Solusinya: <not <(skor) < (10)>> untuk skor >= 10, "
                    "atau <(skor) > (9)> bila nilainya pasti bilangan bulat.", "warn": True},
        {"n": "(<> and <>)", "mudah": "hasilnya benar HANYA kalau kedua syarat benar.", "shape": "Boolean",
         "fungsi": "Bernilai benar HANYA BILA kedua kondisi benar.",
         "contoh": "if <<(skor) > (50)>\n   and\n   <(nyawa) > (0)>>\n  then\n  say [Lanjut level 2]",
        "catatan": "Kedua lubangnya berbentuk SEGI ENAM, jadi hanya bisa diisi blok kondisi — bukan angka dan bukan teks."},
        {"n": "(<> or <>)", "mudah": "hasilnya benar kalau SALAH SATU syarat saja sudah benar.", "shape": "Boolean",
         "fungsi": "Bernilai benar bila SALAH SATU (atau keduanya) benar.",
         "contoh": "if <<touching (Musuh)?>\n   or\n   <touching (Duri)?>>\n  then\n  change (nyawa)\n    by (-1)",
        "catatan": "Bila salah satu sudah benar, sisanya tidak lagi menentukan hasil. Gunakan and bila kedua syarat memang wajib terpenuhi."},
        {"n": "(not <>)", "mudah": "membalik jawaban: yang benar jadi salah, yang salah jadi benar.", "shape": "Boolean",
         "fungsi": "Membalik nilai: benar menjadi salah, salah menjadi benar.",
         "contoh": "wait until\n  <not <key (space)\n     pressed?>>",
         "catatan": "Contoh di samping menunggu sampai tombol spasi DILEPAS. not juga dipakai untuk "
                    "menyiasati blok >= dan <= yang tidak tersedia."},
        {"n": "(join [apple] [banana])", "mudah": "menyambung dua teks jadi satu, misalnya kata Skor ditambah angkanya.", "shape": "Reporter",
         "fungsi": "Menyambung dua teks menjadi satu.",
         "contoh": "say (join [Skor kamu: ]\n  (skor))\n\njoin [Halo, ]\n  (join (nama) [!])",
         "catatan": "Hanya menerima DUA masukan; untuk tiga bagian harus disarangkan. Blok WAJIB "
                    "untuk menampilkan kalimat yang memuat variabel."},
        {"n": "(letter (1) of [apple])", "mudah": "mengambil satu huruf pada urutan tertentu dari sebuah teks.", "shape": "Reporter",
         "fungsi": "Mengambil satu huruf pada posisi tertentu. letter (1) of [apple] = a.",
         "contoh": "set (i) to (1)\nrepeat (length of (kata))\n  say (letter (i)\n    of (kata))\n    for (0.5) seconds\n  change (i) by (1)",
         "catatan": "Penomoran dimulai dari 1, BUKAN 0 — berbeda dari kebanyakan bahasa pemrograman. "
                    "Sebutkan ini saat siswa nanti belajar Python."},
        {"n": "(length of [apple])", "mudah": "menghitung ada berapa huruf dalam sebuah teks.", "shape": "Reporter",
         "fungsi": "Menghitung jumlah KARAKTER dalam teks; spasi ikut dihitung. Hasilnya 5.",
         "catatan": "Jangan tertukar dengan length of (list) di kategori Variables yang menghitung "
                    "jumlah ITEM. Bedakan dari warnanya: hijau = teks, merah tua = list."},
        {"n": "<[apple] contains [a]?>", "mudah": "bertanya: apakah teks itu memuat huruf atau kata tertentu?", "shape": "Boolean",
         "fungsi": "Bernilai benar bila teks pertama memuat teks kedua.",
         "contoh": "if <(answer)\n   contains [jakarta]?>\n  then\n  say [Benar!]",
         "catatan": "Tidak membedakan huruf besar-kecil. Sangat berguna untuk kuis agar jawaban "
                    "\"Kota Jakarta\" tetap dianggap benar."},
    ],
    "compare": [
        ["=  pada teks", "TIDAK membedakan huruf besar-kecil: [Halo] = [halo] bernilai BENAR"],
        ["length of [teks]  vs  length of (list)", "Hijau menghitung HURUF; merah tua menghitung ITEM"],
        ["round  vs  floor  vs  ceiling", "Terdekat vs selalu ke bawah vs selalu ke atas"],
        ["and  vs  or", "and butuh keduanya benar; or cukup salah satu"],
        ["Tidak ada >= dan <=", "Pakai <not <a < b>> atau geser nilainya satu angka"],
    ],
    "banding": [
        ("and  vs  or",
         [("assets/operators/08-and.png", "dua-duanya harus benar"),
          ("assets/operators/09-or.png", "salah satu benar sudah cukup")]),
        ("=  vs  contains",
         [("assets/operators/tunggal/06-sama-dengan.png", "isinya harus persis sama"),
          ("assets/operators/14-contains.png", "cukup mengandung potongan itu")]),
        ("length teks  vs  length list",
         [("assets/operators/13-length-of.png", "jumlah HURUF dalam teks"),
          ("assets/variables/15-length-of-list.png", "jumlah ISI dalam daftar")]),
    ],
    "patterns": [
        ("Tabel kebenaran", "A     B    and  or  not A\nB     B     B    B    S\nB     S     S    B    S\nS     B     S    B    B\nS     S     S    S    B\n\n(B = Benar, S = Salah)"),
        ("Genap atau ganjil", "ask [Masukkan angka]\n  and wait\nif <((answer) mod (2))\n   = (0)> then\n  say [Genap]\nelse\n  say [Ganjil]"),
        ("Blok bersarang", "say (join\n  [Rata-rata: ]\n  (round\n    (((a) + (b))\n      / (2))))\n\nBaca dari DALAM\nke LUAR."),
    ],
    "mistakes": [
        ["Mencari blok >= atau <=", "Tidak ketemu di palet", "Pakai not, atau geser nilainya satu angka"],
        ["Menampilkan variabel tanpa join", "Hanya angka polos tanpa keterangan", "Bungkus dengan join"],
        ["Hasil pembagian panjang sekali", "Muncul 3.3333333333", "Bungkus dengan round"],
        ["Mengira letter mulai dari 0", "Huruf meleset satu posisi", "Penomoran Scratch mulai dari 1"],
        ["Tertukar and dan or", "Kondisi tidak pernah / selalu terpenuhi", "Gunakan tabel kebenaran"],
    ],
    "practice": [
        ["*", "Kalkulator penjumlahan dua bilangan", "ask, +, join"],
        ["*", "Lempar dadu", "pick random (1) to (6)"],
        ["**", "Tentukan bilangan genap atau ganjil", "mod, =, if-else"],
        ["**", "Kuis dengan skor dan pesan lulus / tidak", "=, >, and"],
        ["**", "Sprite bergerak ke posisi acak", "pick random"],
        ["***", "Mengeja kata satu huruf per detik", "letter () of, length of, repeat"],
        ["***", "Gerak melingkar mengelilingi titik pusat", "sin, cos"],
    ],
    "quiz": [
        "Blok apa yang dipakai untuk mengecek bilangan genap atau ganjil? Tuliskan kondisinya.",
        "Scratch tidak punya blok >=. Bagaimana menuliskan \"skor >= 10\"?",
        "Apa hasil letter (3) of [Scratch]?",
        "Kamu ingin menampilkan \"Skor: 25\". Blok apa yang dibutuhkan?",
        "Apakah [Jakarta] = [jakarta] bernilai benar atau salah?",
    ],
    "answers": [
        "mod — kondisinya <((angka) mod (2)) = (0)> untuk bilangan genap.",
        "<not <(skor) < (10)>>, atau untuk bilangan bulat cukup <(skor) > (9)>.",
        "Huruf r (penomoran mulai dari 1: S-c-r).",
        "say (join [Skor: ] (skor)).",
        "BENAR — perbandingan teks di Scratch tidak membedakan huruf besar-kecil.",
    ],
    "takeaways": [
        "Semua blok Operators harus dimasukkan ke lubang blok lain, tidak bisa berdiri sendiri.",
        "Tidak ada >= dan <= — siasati dengan not atau geser satu angka.",
        "join adalah blok wajib untuk menampilkan kalimat yang memuat variabel.",
    ],
}

V = {
    "key": "variables", "short": "Variables", "name": "Variables (Variabel & List)", "subtitle": "5 + 12 blok",
    "color": rgb("FF8C1A"),
    "tagline": "Menyimpan dan mengolah data yang berubah selama program berjalan.",
    "scope": "Berbeda dari kategori lain: bloknya BELUM ADA sampai kamu membuatnya sendiri. "
             "Palet hanya menampilkan tombol Make a Variable dan Make a List.",
    "level": "Menengah–Lanjut",
    "prasyarat": "Variabel = satu kotak berlabel berisi satu nilai. List = rak berisi banyak kotak bernomor, "
                 "penomoran mulai dari 1.",
    "overview": [
        ("Cakupan variabel", "For all sprites (global) | For this sprite only (lokal) | Cloud"),
        ("Blok variabel", "(variabel), set to, change by, show variable, hide variable"),
        ("List: menambah & menghapus", "add to, delete of, delete all of, insert at, replace item"),
        ("List: membaca", "(item () of), (item # of), (length of), contains ()?"),
        ("List: monitor", "show list, hide list"),
    ],
    "blocks": [
        {"n": "Membuat variabel: Make a Variable", "mudah": "tombol untuk membuat kotak penyimpan angka atau teks. Belum ada variabel, belum bisa menyimpan skor.", "shape": "Stack",
         "fungsi": "Menentukan nama dan CAKUPAN variabel sebelum bloknya muncul di palet.",
         "param": ["For all sprites = global, dibaca semua sprite (skor, level)",
                   "For this sprite only = lokal, tiap klon punya salinan sendiri",
                   "Cloud variable = disimpan di server Scratch"],
         "catatan": "Cloud variable hanya bisa berisi ANGKA, maksimal 10 per proyek, tidak tersedia "
                    "bagi New Scratcher maupun di editor offline."},
        {"n": "(nama variabel)", "mudah": "kotak penyimpan satu nilai. Isinya bisa dipakai di blok mana saja.", "shape": "Reporter",
         "fungsi": "Melaporkan nilai yang tersimpan di dalam variabel.",
         "contoh": "say (join [Skor: ]\n  (skor))",
         "catatan": "Ada kotak centang di palet untuk memunculkan MONITOR di panggung. Klik kanan "
                    "monitor untuk memilih tampilan: normal, besar, atau SLIDER yang bisa digeser pemain."},
        {"n": "set (skor) to (0)", "mudah": "mengisi variabel dengan nilai baru, menimpa isi lamanya.", "shape": "Stack",
         "fungsi": "MENGISI variabel dengan nilai baru, menimpa isi lama.",
         "contoh": "when green flag clicked\nset (skor) to (0)\nset (nyawa) to (3)",
         "catatan": "WAJIB ADA DI SCRIPT RESET. Tanpa ini skor melanjutkan dari permainan sebelumnya — "
                    "kesalahan nomor satu pada proyek permainan buatan siswa.", "warn": True},
        {"n": "change (skor) by (1)", "mudah": "menambah isi variabel sebanyak 1 dari nilai sekarang.", "shape": "Stack",
         "fungsi": "MENAMBAH nilai variabel; nilai negatif berarti mengurangi.",
         "contoh": "when this sprite clicked\nchange (skor) by (10)\nchange (nyawa) by (-1)",
         "catatan": "Hanya bekerja untuk ANGKA. set (skor) to (1) membuat skor menjadi tepat 1; "
                    "change (skor) by (1) menambah 1 dari nilai sekarang."},
        {"n": "show variable (skor)", "mudah": "menampilkan kotak nilai variabel di panggung supaya pemain bisa melihatnya.", "shape": "Stack",
         "fungsi": "Menampilkan monitor variabel di panggung lewat program.",
         "catatan": "Berguna untuk menampilkan skor hanya saat permainan berlangsung."},
        {"n": "hide variable (skor)", "mudah": "menyembunyikan kotak nilai variabel dari panggung.", "shape": "Stack",
         "fungsi": "Menyembunyikan monitor variabel dari panggung.",
         "contoh": "when I receive\n  (game over)\nhide variable (waktu)",
        "catatan": "Yang disembunyikan hanya tampilannya di panggung; isi variabelnya tetap ada dan tetap bisa dipakai script."},
        {"n": "(nama list)", "mudah": "list adalah kotak penyimpan yang memuat BANYAK nilai sekaligus, bernomor urut.", "shape": "Reporter",
         "fungsi": "Melaporkan SELURUH isi list, disambung dengan spasi.",
         "catatan": "Jarang dipakai langsung dalam perhitungan; lebih sering yang dipakai adalah "
                    "monitornya di panggung."},
        {"n": "add [thing] to (daftar)", "mudah": "menambah satu isi baru di urutan paling belakang list.", "shape": "Stack",
         "fungsi": "Menambahkan item baru di AKHIR list.",
         "contoh": "ask [Siapa namamu?]\n  and wait\nadd (answer) to\n  (daftar pemain)",
        "catatan": "Selalu masuk di urutan paling bawah. Untuk menyisipkan di posisi tertentu pakai insert at."},
        {"n": "delete (1) of (daftar)", "mudah": "menghapus isi list pada urutan tertentu.", "shape": "Stack",
         "fungsi": "Menghapus item pada posisi tertentu.",
         "catatan": "Setelah dihapus, item di bawahnya NAIK NOMOR. Bila menghapus di dalam loop, hapus "
                    "dari BELAKANG KE DEPAN agar penomorannya tidak kacau."},
        {"n": "delete all of (daftar)", "mudah": "mengosongkan seluruh isi list sekaligus.", "shape": "Stack",
         "fungsi": "Mengosongkan seluruh isi list.",
         "catatan": "WAJIB ada di script reset, kalau tidak isi list akan menumpuk berlipat setiap kali "
                    "proyek dijalankan.", "warn": True},
        {"n": "insert [thing] at (1) of (daftar)", "mudah": "menyisipkan isi baru di urutan tertentu; isi lain bergeser mundur.", "shape": "Stack",
         "fungsi": "Menyisipkan item di posisi tertentu; item lain bergeser turun.",
         "catatan": "Dipakai misalnya untuk menaruh pemenang baru di puncak papan skor."},
        {"n": "replace item (1) of (daftar) with [x]", "mudah": "mengganti isi pada urutan tertentu tanpa mengubah panjang list.", "shape": "Stack",
         "fungsi": "Mengganti isi item pada posisi tertentu tanpa mengubah panjang list.",
        "catatan": "Panjang list tidak berubah — isi lama pada posisi itu hilang tertimpa. Nomor di luar panjang list membuat blok ini tidak melakukan apa-apa."},
        {"n": "(item (1) of (daftar))", "mudah": "mengambil isi list pada urutan tertentu.", "shape": "Reporter",
         "fungsi": "Membaca isi item pada posisi tertentu.",
         "contoh": "set (nomor) to\n  (pick random (1) to\n   (length of (soal)))\nask (item (nomor)\n  of (soal)) and wait",
         "catatan": "Bila nomor melebihi panjang list, hasilnya KOSONG — bukan pesan kesalahan. "
                    "Ini membuat bug sulit terlihat."},
        {"n": "(item # of [thing] in (daftar))", "mudah": "mencari sebuah isi berada di urutan ke berapa dalam list.", "shape": "Reporter",
         "fungsi": "Mencari POSISI sebuah item di dalam list. Melaporkan 0 bila tidak ditemukan.",
         "contoh": "set (i) to (item # of\n  (soal terpilih) in\n  (daftar soal))\nif <(answer) =\n   (item (i) of\n    (daftar jawaban))>\n  then\n  say [Benar!]",
        "catatan": "Melaporkan 0 bila tidak ketemu, jadi 0 bisa dipakai sebagai penanda \"tidak ada\". Bila isinya kembar, yang dilaporkan posisi yang pertama."},
        {"n": "(length of (daftar))", "mudah": "menghitung ada berapa isi dalam list.", "shape": "Reporter",
         "fungsi": "Menghitung JUMLAH ITEM dalam list.",
         "catatan": "Jangan tertukar dengan length of [teks] berwarna hijau di kategori Operators yang "
                    "menghitung jumlah HURUF."},
        {"n": "<(daftar) contains [thing]?>", "mudah": "bertanya: apakah list itu memuat isi tertentu?", "shape": "Boolean",
         "fungsi": "Bernilai benar bila list memuat item tersebut.",
         "contoh": "if <not <(daftar pemain)\n   contains (answer)?>>\n  then\n  add (answer) to\n    (daftar pemain)",
         "catatan": "Contoh di samping mencegah nama ganda masuk ke dalam daftar."},
        {"n": "show list / hide list (daftar)", "mudah": "menampilkan atau menyembunyikan kotak list di panggung.", "shape": "Stack",
         "fungsi": "Menampilkan atau menyembunyikan monitor list di panggung.",
         "catatan": "Monitor list bisa diperbesar dengan menyeret sudut kanan bawahnya, dan pemain "
                    "bisa menambah atau mengubah isinya langsung lewat tombol +."},
    ],
    "compare": [
        ["set  vs  change", "set MENETAPKAN nilai baru; change MENAMBAH dari nilai sekarang"],
        ["Variabel  vs  List", "Satu nilai vs banyak nilai bernomor"],
        ["Global  vs  Lokal", "Dibaca semua sprite vs milik satu sprite (tiap klon punya salinan)"],
        ["length of [teks]  vs  length of (list)", "Jumlah huruf (hijau) vs jumlah item (merah tua)"],
        ["Variabel biasa  vs  Cloud variable", "Lokal di komputer vs disimpan di server, angka saja, maks 10"],
    ],
    "banding": [
        ("set  vs  change",
         [("assets/variables/03-set-to.png", "menetapkan nilai pasti"),
          ("assets/variables/04-change-by.png", "menambah dari nilai sekarang")]),
        ("variabel  vs  list",
         [("assets/variables/02-variabel-reporter.png", "satu kotak, satu isi"),
          ("assets/variables/07-list-reporter.png", "banyak kotak bernomor")]),
        ("add  vs  insert at",
         [("assets/variables/08-add-to.png", "selalu masuk paling bawah"),
          ("assets/variables/11-insert-at.png", "masuk di urutan yang kamu pilih")]),
    ],
    "patterns": [
        ("Skor & nyawa", "when green flag clicked\nset (skor) to (0)\nset (nyawa) to (3)\n\nwhen this sprite clicked\nchange (skor) by (1)"),
        ("Gravitasi", "when green flag clicked\nset (kecepatan) to (0)\nforever\n  change (kecepatan)\n    by (-1)\n  change y by\n    (kecepatan)\n  if <(y position)\n     < (-140)> then\n    set y to (-140)\n    set (kecepatan)\n      to (0)"),
        ("Kuis dari bank soal", "when green flag clicked\ndelete all of (soal)\nadd [Ibu kota RI?]\n  to (soal)\nadd [2 + 2 = ?]\n  to (soal)\nrepeat (length of (soal))\n  ask (item (1) of\n    (soal)) and wait\n  delete (1) of (soal)"),
    ],
    "mistakes": [
        ["Lupa set (skor) to (0) di awal", "Skor melanjutkan dari permainan sebelumnya", "Tambahkan ke script reset"],
        ["Lupa delete all of (list)", "Isi list menumpuk berlipat tiap dijalankan", "Tambahkan ke script reset"],
        ["Tertukar set dan change", "Skor melompat aneh atau tidak bertambah", "set = tetapkan, change = tambahkan"],
        ["Memakai variabel lokal untuk skor bersama", "Sprite lain tidak bisa membacanya", "Buat sebagai For all sprites"],
        ["Menghapus item dari depan di dalam loop", "Sebagian item terlewat", "Hapus dari belakang ke depan"],
    ],
    "practice": [
        ["*", "Penghitung klik", "set, change, monitor"],
        ["*", "Skor bertambah saat menangkap koin", "change (skor) by (1)"],
        ["**", "Nyawa berkurang & permainan berakhir saat 0", "change by (-1), if, stop"],
        ["**", "Timer mundur 30 detik", "set, repeat until, wait"],
        ["**", "Lompat dengan gravitasi", "variabel kecepatan"],
        ["***", "Kuis dari bank soal acak", "list + item () of + pick random"],
        ["***", "Papan skor 5 besar", "list + insert at + delete"],
    ],
    "quiz": [
        "Apa beda set (skor) to (5) dengan change (skor) by (5)?",
        "Kapan sebaiknya memakai variabel For this sprite only?",
        "Apa yang terjadi bila lupa memakai delete all of (list) di awal proyek?",
        "Berapa nomor item PERTAMA dalam sebuah list?",
        "Blok apa yang dipakai untuk mengecek apakah sebuah nama sudah ada di dalam list?",
    ],
    "answers": [
        "set menetapkan nilainya menjadi tepat 5; change menambahkan 5 ke nilai yang sudah ada.",
        "Bila tiap sprite atau klon perlu nilainya sendiri, misalnya kecepatan tiap peluru atau HP tiap musuh.",
        "Isi list menumpuk setiap kali proyek dijalankan sehingga datanya berlipat dan kacau.",
        "Nomor 1.",
        "<(nama list) contains [thing]?>.",
    ],
    "takeaways": [
        "set = tetapkan, change = tambahkan. Dua-duanya wajib dibedakan sejak awal.",
        "Script reset harus memuat set variabel dan delete all of list.",
        "Variabel = satu kotak; List = rak kotak bernomor mulai dari 1.",
    ],
}

MB = {
    "key": "my_blocks", "short": "My Blocks", "name": "My Blocks (Blok Buatan Sendiri)",
    "subtitle": "Dibuat sendiri oleh pengguna",
    "color": rgb("FF6680"),
    "tagline": "Membuat blok perintah sendiri — setara fungsi / prosedur di bahasa pemrograman lain.",
    "scope": "Materi lanjut. Ajarkan setelah siswa menguasai loop, kondisi, dan variabel.",
    "level": "Lanjut",
    "prasyarat": "Palet ini KOSONG saat pertama dibuka; hanya ada satu tombol: Make a Block.",
    "overview": [
        ("Konsep yang diajarkan", "Dekomposisi, abstraksi, dan DRY (Don't Repeat Yourself)"),
        ("Membuat", "Make a Block > beri nama > muncul blok di palet + blok define di area kode"),
        ("Tiga jenis input", "number or text, boolean, dan label text (teks hiasan)"),
        ("Opsi khusus", "Run without screen refresh"),
        ("Kemampuan lanjut", "Rekursi — blok memanggil dirinya sendiri"),
        ("Keterbatasan", "Belum ada custom reporter dan custom boolean block"),
    ],
    "blocks": [
        {"n": "Mengapa My Blocks penting?", "mudah": "My Blocks membuat kita bisa memberi NAMA pada sekumpulan blok, lalu memanggilnya berkali-kali.", "shape": "Stack",
         "fungsi": "Mengubah delapan blok berulang menjadi satu blok bernama.",
         "contoh": "TANPA My Blocks:\nmove (100) steps\nturn right (90) degrees\nmove (100) steps\nturn right (90) degrees\nmove (100) steps\nturn right (90) degrees\nmove (100) steps\nturn right (90) degrees\n\nDENGAN My Blocks:\ngambar persegi (100)",
         "catatan": "Mengajarkan tiga konsep besar sekaligus: DEKOMPOSISI (memecah masalah), "
                    "ABSTRAKSI (menyembunyikan detail), dan DRY (tidak menyalin kode berulang)."},
        {"n": "define (nama blok)", "mudah": "kepala blok buatan sendiri. Semua blok di bawahnya jalan tiap blok itu dipanggil.", "shape": "Hat",
         "fungsi": "Menampung ISI dari blok buatan sendiri. Di bawah blok inilah perintahnya disusun.",
         "contoh": "define gambar persegi\nrepeat (4)\n  move (100) steps\n  turn right (90) degrees",
         "catatan": "Blok define TIDAK BERJALAN SENDIRI. Ia hanya \"resep\". Yang berjalan adalah blok "
                    "pemanggilnya yang dipakai di script lain.", "warn": True},
        {"n": "Input: number or text", "mudah": "menambah kolom isian supaya blok buatan bisa diberi angka atau teks yang berbeda-beda.", "shape": "Stack",
         "fungsi": "Membuat lubang isian yang bisa diisi angka atau teks, agar satu blok bisa dipakai "
                   "untuk banyak nilai.",
         "contoh": "define gambar persegi\n  (sisi)\nrepeat (4)\n  move (sisi) steps\n  turn right (90) degrees\n\nPemakaian:\ngambar persegi (50)\ngambar persegi (200)",
         "catatan": "Nama input muncul sebagai blok oval kecil di dalam define — tarik dari situ untuk "
                    "memakainya di dalam perintah."},
        {"n": "Input: boolean", "mudah": "menambah kolom heksagon supaya blok buatan bisa diberi syarat benar atau salah.", "shape": "Boolean",
         "fungsi": "Membuat lubang segi enam yang menerima kondisi benar atau salah.",
         "contoh": "define bergerak (jarak)\n  jika (aman)\nif <aman> then\n  move (jarak) steps\n\nPemakaian:\nbergerak (10) jika\n  <not <touching\n   (Musuh)?>>",
        "catatan": "Lubangnya segi enam, jadi hanya menerima blok kondisi. Di dalam define, nama input itu dipakai langsung sebagai kondisi — tanpa dibandingkan dengan apa pun."},
        {"n": "Add a label text", "mudah": "menambah tulisan penjelas di dalam blok supaya lebih mudah dibaca.", "shape": "Stack",
         "fungsi": "Menambahkan teks hiasan di dalam blok — tidak bisa diisi, hanya membuat blok lebih "
                   "mudah dibaca.",
         "catatan": "Contoh: \"gambar persegi (100) berwarna (merah)\" — kata \"berwarna\" adalah label, "
                    "bukan input."},
        {"n": "Opsi: Run without screen refresh", "mudah": "membuat blok jalan sampai selesai dalam sekejap tanpa menggambar ulang layar. Cocok untuk menggambar.", "shape": "Stack",
         "fungsi": "Menjalankan seluruh isi blok dalam SATU FRAME sehingga hasilnya muncul seketika.",
         "param": ["Tidak dicentang = layar diperbarui tiap perulangan (gerakan terlihat)",
                   "Dicentang = hasil muncul seketika (cocok untuk menggambar dengan Pen)"],
         "catatan": "JANGAN dicentang bila blok memuat wait atau loop tak berujung seperti forever — "
                    "proyek akan MEMBEKU sampai setengah detik atau lebih.", "warn": True},
        {"n": "Rekursi: blok memanggil dirinya sendiri", "mudah": "blok buatan yang memanggil dirinya sendiri. Dipakai untuk pola berulang seperti spiral.", "shape": "Stack",
         "fungsi": "Blok buatan sendiri boleh memanggil dirinya sendiri untuk menyelesaikan masalah "
                   "bertingkat.",
         "contoh": "define hitung mundur (n)\nif <(n) > (0)> then\n  say (n)\n    for (0.5) seconds\n  hitung mundur\n    ((n) - (1))\n\nhitung mundur (5)\n=> 5, 4, 3, 2, 1",
         "catatan": "SYARAT MUTLAK: harus ada KONDISI BERHENTI. Tanpa itu blok memanggil dirinya tanpa "
                    "akhir dan proyek macet.", "warn": True},
        {"n": "Keterbatasan & jalan keluarnya", "mudah": "blok buatan tidak bisa mengembalikan nilai seperti reporter; siasatnya pakai variabel.", "shape": "Reporter",
         "fungsi": "Scratch belum punya custom reporter dan custom boolean block.",
         "contoh": "define hitung luas\n  (p) (l)\nset (hasil) to\n  ((p) * (l))\n\nPemakaian:\nhitung luas (5) (3)\nsay (hasil)",
         "catatan": "Blok buatan tidak bisa \"mengembalikan nilai\". Jalan keluarnya: simpan hasil ke "
                    "VARIABEL, lalu baca variabel itu setelah blok dipanggil."},
        {"n": "Blok bersifat lokal per sprite", "mudah": "blok buatan hanya ada di sprite tempat ia dibuat; sprite lain tidak melihatnya.", "shape": "Stack",
         "fungsi": "Blok buatan sendiri hanya tersedia di sprite tempat ia dibuat.",
         "catatan": "Untuk memakainya di sprite lain: duplicate sprite, atau tarik script ke kartu "
                    "sprite tujuan, atau simpan lewat Backpack."},
    ],
    "compare": [
        ["define  vs  blok pemanggil", "define adalah resep (tidak jalan sendiri); pemanggil yang menjalankan"],
        ["My Blocks  vs  broadcast", "My Blocks memanggil di sprite yang sama; broadcast lintas sprite"],
        ["Input number/text  vs  boolean", "Lubang oval untuk nilai; lubang segi enam untuk kondisi"],
        ["Label  vs  input", "Label hanya hiasan yang tidak bisa diisi"],
    ],
    "banding": [
        ("define  vs  blok pemanggil",
         [("assets/banding/my_blocks/02-define-saja.png", "tempat isi blok ditulis, sekali saja"),
          ("assets/banding/my_blocks/01-pemanggil.png", "yang dipasang di script, boleh berkali-kali")]),
        ("input angka  vs  input boolean",
         [("assets/my_blocks/03-input-angka.png", "diisi angka atau teks"),
          ("assets/my_blocks/04-input-boolean.png", "diisi blok benar/salah")]),
        ("My Blocks  vs  broadcast",
         [("assets/banding/my_blocks/01-pemanggil.png", "sprite ini saja, script menunggu"),
          ("assets/events/08-broadcast.png", "semua sprite, tidak menunggu")]),
    ],
    "patterns": [
        ("Segi banyak", "define segi banyak\n  (jumlah sisi)\n  (panjang)\nrepeat (jumlah sisi)\n  move (panjang) steps\n  turn right ((360) /\n    (jumlah sisi))\n    degrees\n\nsegi banyak (3) (100)\nsegi banyak (6) (60)"),
        ("Reset semua", "define reset semua\nshow\nclear graphic effects\nset size to (100) %\ngo to x: (0) y: (0)\npoint in direction (90)\nset (skor) to (0)\nset (nyawa) to (3)\n\nwhen green flag clicked\nreset semua"),
        ("Pohon fraktal (Pen)", "define cabang (panjang)\nif <(panjang) > (5)>\n  then\n  move (panjang) steps\n  turn right (30) degrees\n  cabang ((panjang)\n    * (0.7))\n  turn left (60) degrees\n  cabang ((panjang)\n    * (0.7))\n  turn right (30) degrees\n  move ((0) -\n    (panjang)) steps"),
    ],
    "mistakes": [
        ["Menyusun kode di area kode biasa, bukan di bawah define", "Blok buatan tidak melakukan apa-apa", "Sambungkan blok DI BAWAH define"],
        ["Mengira define berjalan sendiri", "Tidak terjadi apa-apa", "define hanya resep; panggil bloknya dari script lain"],
        ["Run without screen refresh pada blok berisi wait", "Proyek membeku", "Hilangkan centangnya"],
        ["Rekursi tanpa kondisi berhenti", "Proyek macet / hang", "Selalu beri if sebagai penghenti"],
        ["Nama blok terlalu umum (blok1)", "Proyek tidak terbaca", "Beri nama kata kerja: gambar persegi, reset semua"],
    ],
    "practice": [
        ["**", "Buat blok gambar persegi tanpa input", "Make a Block, repeat"],
        ["**", "Tambahkan input sisi agar ukurannya bisa diatur", "input number or text"],
        ["**", "Buat blok reset semua dan pakai di proyek lama", "dekomposisi"],
        ["***", "Buat blok segi banyak (n) (panjang)", "input ganda + 360/n"],
        ["***", "Buat blok hitung luas yang hasilnya ke variabel", "jalan keluar reporter"],
        ["****", "Buat pohon fraktal dengan rekursi", "rekursi + ekstensi Pen"],
    ],
    "quiz": [
        "Apa fungsi blok define? Apakah ia berjalan sendiri?",
        "Sebutkan tiga jenis input yang bisa ditambahkan ke blok buatan sendiri.",
        "Kapan opsi run without screen refresh TIDAK boleh dicentang?",
        "Scratch tidak punya custom reporter block. Bagaimana cara sebuah blok buatan mengembalikan hasil hitungan?",
        "Apa syarat mutlak agar rekursi tidak membuat proyek macet?",
    ],
    "answers": [
        "define menyimpan isi / resep blok buatan. Ia TIDAK berjalan sendiri — baru dijalankan saat blok pemanggilnya dipakai.",
        "Input number or text, input boolean, dan label text (teks hiasan, bukan input sesungguhnya).",
        "Bila di dalam blok terdapat wait atau loop tak berujung seperti forever — proyek akan membeku.",
        "Simpan hasilnya ke sebuah VARIABEL, lalu baca variabel tersebut setelah blok dipanggil.",
        "Harus ada KONDISI BERHENTI (biasanya if) yang menghentikan pemanggilan pada suatu titik.",
    ],
    "takeaways": [
        "My Blocks mengajarkan dekomposisi, abstraksi, dan DRY sekaligus.",
        "define hanya resep — yang berjalan adalah blok pemanggilnya.",
        "Belum ada custom reporter; nilai balik dititipkan lewat variabel.",
    ],
}

CATS = [M, L, S, E, C, SE, O, V, MB]


if __name__ == "__main__":
    for cat in CATS:
        path, _ = build(cat)
        print(f"OK  {path.name:32s} {len(cat['blocks']):2d} slide blok")
    idx = build_index(CATS)
    print(f"OK  {idx.name}")
