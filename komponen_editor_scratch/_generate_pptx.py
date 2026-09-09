#!/usr/bin/env python3
"""
Generator PPTX bahan ajar Scratch — komponen antarmuka editor.

Menghasilkan satu berkas .pptx untuk tiap berkas .md di folder ini
(nama berkas sama, hanya beda ekstensi).

Layout & tema diambil ulang dari ../tab_code/_generate_pptx.py agar
tampilannya seragam dengan dek materi blok.

Jalankan:  python3 _generate_pptx.py
Butuh   :  pip install python-pptx
"""

import importlib.util
import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from pptx.util import Inches, Pt

OUT_DIR = Path(__file__).resolve().parent
KIT_PATH = OUT_DIR.parent / "tab_code" / "_generate_pptx.py"
if not KIT_PATH.exists():
    sys.exit(f"Tidak menemukan kit layout di {KIT_PATH}")


def _load_kit():
    """Muat kit layout dari folder tab_code dengan NAMA MODUL BERBEDA.

    Kedua generator kebetulan bernama _generate_pptx.py, jadi `import
    _generate_pptx` biasa akan menunjuk berkas ini sendiri. Pemuatan eksplisit
    di bawah menghindari tabrakan nama tersebut.
    """
    spec = importlib.util.spec_from_file_location("scratch_pptx_kit", KIT_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["scratch_pptx_kit"] = mod
    spec.loader.exec_module(mod)
    return mod


kit = _load_kit()

W, H, MARGIN, BODY_W = kit.W, kit.H, kit.MARGIN, kit.BODY_W
INK, MUTED, WHITE = kit.INK, kit.MUTED, kit.WHITE
CODE_BG, NOTE_BG, WARN_BG = kit.CODE_BG, kit.NOTE_BG, kit.WARN_BG
FONT, MONO = kit.FONT, kit.MONO
rgb, tint = kit.rgb, kit.tint
_txbox, _para, _rect, _blank = kit._txbox, kit._para, kit._rect, kit._blank
_header, _footer = kit._header, kit._footer


# --------------------------------------------------------- slide baru

def slide_cover(prs, d):
    """Sampul modul: nomor, nama komponen, lokasi di layar, durasi."""
    s = _blank(prs)
    color = d["color"]

    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(4.5))
    band.fill.solid()
    band.fill.fore_color.rgb = color
    band.line.fill.background()
    band.shadow.inherit = False

    tk = _txbox(s, MARGIN, Inches(1.30), BODY_W, Inches(0.3))
    _para(tk, d["kicker"], 13, bold=True, color=tint(color, 0.78), first=True,
          space_after=0, line_spacing=1.0)

    tt = _txbox(s, MARGIN, Inches(1.85), BODY_W, Inches(1.0))
    _para(tt, d["name"], 40, bold=True, color=WHITE, first=True,
          space_after=0, line_spacing=1.0)

    ts = _txbox(s, MARGIN, Inches(3.05), BODY_W, Inches(0.5))
    _para(ts, d["lokasi"], 17, color=tint(color, 0.85), first=True,
          space_after=0, line_spacing=1.05)

    t1 = _txbox(s, MARGIN, Inches(5.05), BODY_W, Inches(0.6))
    _para(t1, d["tagline"], 17, color=INK, first=True, space_after=0, line_spacing=1.1)

    t2 = _txbox(s, MARGIN, Inches(5.95), BODY_W, Inches(0.4))
    _para(t2, d["durasi"], 13, color=MUTED, first=True, space_after=0, line_spacing=1.0)
    return s


def slide_ascii(prs, d, page, title, kicker, art, note=None):
    """Slide denah / sketsa antarmuka dalam huruf monospace, ukuran otomatis."""
    s = _blank(prs)
    _header(s, d["color"], title, kicker)

    lines = art.strip("\n").split("\n")
    ncol = max(len(x) for x in lines)
    nrow = len(lines)

    # Tinggi yang tersedia untuk TEKS saja (kotak = teks + padding 0.34in).
    # Kotak mulai di 1.5in dan harus berakhir sebelum area footer (6.75in);
    # bila ada catatan di bawahnya, sisakan ruang 0.25 + 0.8 inci.
    box_limit = 6.75 - 1.5 - (1.05 if note else 0.0)
    avail_h = box_limit - 0.34
    avail_w = (BODY_W - Inches(0.6)) / 914400
    by_h = avail_h * 72 / (nrow * 1.22)
    by_w = avail_w * 72 / (ncol * 0.605)
    size = max(6.0, min(14.0, by_h, by_w))

    # Jarak baris dikunci dalam POIN EKSAK, bukan kelipatan. Kelipatan (mis.
    # 1.22) dikalikan lagi dengan tinggi baris alami font (~1.16x untuk Courier
    # New), sehingga tinggi sebenarnya membengkak ~16% dan teks meluber.
    leading = size * 1.22
    box_h = Inches(0.34) + Emu_from_pt(leading * nrow)
    _rect(s, MARGIN, Inches(1.5), BODY_W, box_h, CODE_BG)
    tf = _txbox(s, MARGIN + Inches(0.28), Inches(1.67), BODY_W - Inches(0.56), box_h - Inches(0.34))
    for i, line in enumerate(lines):
        _para(tf, line if line.strip() else " ", size, color=INK, font=MONO,
              first=(i == 0), space_after=0, line_spacing=Pt(leading))

    if note:
        ny = Inches(1.5) + box_h + Inches(0.25)
        _rect(s, MARGIN, ny, BODY_W, Inches(0.8), NOTE_BG)
        tfn = _txbox(s, MARGIN + Inches(0.25), ny + Inches(0.15), BODY_W - Inches(0.5), Inches(0.55))
        _para(tfn, note, 13, color=INK, first=True, space_after=0)

    _footer(s, d["name"], page)
    return s


def Emu_from_pt(pt):
    return Inches(pt / 72)


def slide_detail(prs, d, item, page, idx):
    """Satu slide untuk satu bagian komponen."""
    s = _blank(prs)
    color = d["color"]
    _header(s, color, item["n"], f'{d["short"].upper()}  ·  BAGIAN {idx}')

    y = Inches(1.45)

    if item.get("chip"):
        chip = _rect(s, MARGIN, y, Inches(4.2), Inches(0.36), tint(color, 0.86))
        tfc = chip.text_frame
        tfc.word_wrap = True
        tfc.margin_left = Inches(0.14)
        tfc.margin_top = tfc.margin_bottom = 0
        tfc.vertical_anchor = MSO_ANCHOR.MIDDLE
        _para(tfc, item["chip"], 11, bold=True, color=color, first=True, space_after=0)
        y += Inches(0.55)

    has_code = bool(item.get("contoh"))
    text_w = Inches(6.4) if has_code else BODY_W

    tf = _txbox(s, MARGIN, y, text_w, Inches(3.2))
    _para(tf, "FUNGSI", 10, bold=True, color=MUTED, first=True, space_after=4)
    _para(tf, item["fungsi"], 15, color=INK, space_after=10)
    if item.get("param"):
        _para(tf, item.get("param_label", "RINCIAN"), 10, bold=True, color=MUTED, space_after=4)
        for line in item["param"]:
            _para(tf, "•  " + line, 13, color=INK, space_after=3)

    if has_code:
        cx = MARGIN + Inches(6.8)
        cw = BODY_W - Inches(6.8)
        lines = item["contoh"].strip("\n").split("\n")
        ch = Inches(0.34) + Inches(0.235) * len(lines)
        _rect(s, cx, y, cw, ch, CODE_BG)
        tfk = _txbox(s, cx + Inches(0.22), y + Inches(0.17), cw - Inches(0.44), ch - Inches(0.34))
        for i, line in enumerate(lines):
            _para(tfk, line if line else " ", 12, color=INK, font=MONO,
                  first=(i == 0), space_after=1)

    if item.get("catatan"):
        warn = item.get("warn", False)
        nh = Inches(0.95) if len(item["catatan"]) < 155 else Inches(1.25)
        ny = H - Inches(0.75) - nh
        _rect(s, MARGIN, ny, BODY_W, nh, WARN_BG if warn else NOTE_BG)
        tfn = _txbox(s, MARGIN + Inches(0.25), ny + Inches(0.15), BODY_W - Inches(0.5), nh - Inches(0.3))
        _para(tfn, "PERHATIAN" if warn else "CATATAN", 10, bold=True,
              color=rgb("B3261E") if warn else rgb("B26A00"), first=True, space_after=4)
        _para(tfn, item["catatan"], 13, color=INK, space_after=0)

    _footer(s, d["name"], page)
    return s


def slide_analogy(prs, d, page):
    """Slide analogi — satu kalimat besar, penuh warna."""
    s = _blank(prs)
    color = d["color"]
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    band.fill.solid()
    band.fill.fore_color.rgb = color
    band.line.fill.background()
    band.shadow.inherit = False

    tk = _txbox(s, MARGIN, Inches(1.55), BODY_W, Inches(0.35))
    _para(tk, "ANALOGI UNTUK SISWA", 14, bold=True, color=tint(color, 0.78),
          first=True, space_after=0, line_spacing=1.0)

    tf = _txbox(s, MARGIN, Inches(2.35), BODY_W, Inches(3.6))
    for i, line in enumerate(d["analogi"]):
        _para(tf, line, 24, color=WHITE, first=(i == 0), space_after=20, line_spacing=1.25)
    return s


# ------------------------------------------------------------ perakit

def build(d):
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H

    slide_cover(prs, d)
    page = 2

    kit.slide_bullets(prs, d, page, "Tujuan Pembelajaran", d["short"].upper(), d["tujuan"])
    page += 1

    if d.get("denah"):
        slide_ascii(prs, d, page, d.get("denah_judul", "Letak di Layar"),
                    d["short"].upper(), d["denah"], d.get("denah_note"))
        page += 1

    for i, item in enumerate(d["details"], start=1):
        slide_detail(prs, d, item, page, i)
        page += 1

    for tbl in d.get("tables", []):
        kit.slide_table(prs, d, page, tbl["judul"], d["short"].upper(),
                        tbl["headers"], tbl["rows"], widths=tbl.get("widths"),
                        font_size=tbl.get("size", 12))
        page += 1

    kit.slide_bullets(prs, d, page, "Praktik di Kelas", d["short"].upper(), d["praktik"],
                      note=d.get("praktik_note"))
    page += 1

    slide_analogy(prs, d, page)
    page += 1

    kit.slide_table(prs, d, page, "Kesalahan Umum di Kelas", d["short"].upper(),
                    ["Kesalahan", "Akibat", "Pencegahan"], d["mistakes"], widths=[34, 33, 33])
    page += 1

    kit.slide_bullets(prs, d, page, "Cek Pemahaman", d["short"].upper(), d["quiz"])
    page += 1

    kit.slide_answers(prs, d, page, d["answers"])
    page += 1

    kit.slide_closing(prs, d)

    out = OUT_DIR / f'{d["file"]}.pptx'
    prs.save(out)
    return out


def build_index(d, modules):
    prs = Presentation()
    prs.slide_width, prs.slide_height = W, H
    accent = d["color"]

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
    _para(tt, "Komponen Editor Scratch", 46, bold=True, color=WHITE, first=True,
          space_after=0, line_spacing=1.0)
    ts = _txbox(s, MARGIN, Inches(4.35), BODY_W, Inches(0.45))
    _para(ts, "11 komponen antarmuka  ·  total 165 menit", 20,
          color=tint(accent, 0.86), first=True, space_after=0, line_spacing=1.0)

    page = 2
    slide_ascii(prs, d, page, "Denah Layar Editor", "PETA", d["denah"])
    page += 1

    rows = [[m["kicker"].split("·")[0].strip(), m["name"], m["durasi"].replace("Estimasi ", "")]
            for m in modules]
    kit.slide_table(prs, d, page, "Sebelas Modul Komponen", "DAFTAR DEK",
                    ["No", "Komponen", "Waktu"], rows, widths=[12, 66, 22], font_size=12)
    page += 1

    for tbl in d["tables"]:
        kit.slide_table(prs, d, page, tbl["judul"], "PANDUAN GURU",
                        tbl["headers"], tbl["rows"], widths=tbl.get("widths"),
                        font_size=tbl.get("size", 12))
        page += 1

    kit.slide_bullets(prs, d, page, "Cara Memakai Materi Ini", "PANDUAN GURU", d["tujuan"],
                      note=d.get("catatan"))
    page += 1

    kit.slide_closing(prs, d)

    out = OUT_DIR / f'{d["file"]}.pptx'
    prs.save(out)
    return out


# =================================================================== DATA

M01 = {
    "file": "01-menu-bar", "short": "Menu Bar", "name": "Menu Bar (Baris Menu Atas)",
    "kicker": "MODUL 1  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("855CD6"),
    "lokasi": "Letak: baris ungu paling atas editor",
    "durasi": "Estimasi 20 menit  ·  Jenjang SD kelas 5 - SMP",
    "tagline": "Ruang kendali proyek: nama, penyimpanan, dan akun — bukan perintah untuk sprite.",
    "tujuan": [
        "Menyebutkan fungsi setiap menu di baris atas editor.",
        "Menyimpan dan membuka kembali proyek Scratch.",
        "Mengganti nama proyek dan menjelaskan mengapa nama proyek penting.",
        "Menggunakan Undo / Restore saat melakukan kesalahan.",
    ],
    "denah": """
[SCRATCH]  Settings v | File v | Edit v | [ Untitled-2 ] | See Project Page | Tutorials | Debug | [My Stuff] | PandaGurun v
    1          2         3        4            5                  6              7          8         9            10
""",
    "denah_note": "Siswa sering mengabaikan baris ini — akibatnya kerja satu jam hilang karena tidak pernah disimpan.",
    "details": [
        {"n": "1. Logo Scratch", "chip": "Tautan keluar editor",
         "fungsi": "Klik untuk kembali ke halaman depan scratch.mit.edu.",
         "catatan": "Peringatkan siswa: JANGAN diklik saat sedang mengerjakan proyek yang belum "
                    "disimpan, karena editor langsung ditinggalkan tanpa peringatan.", "warn": True},
        {"n": "2. Settings (Pengaturan)", "chip": "Pengaturan tampilan editor",
         "fungsi": "Mengatur tampilan editor. Umumnya berisi Bahasa dan Tema.",
         "param": ["Language / Bahasa — mengubah antarmuka DAN teks blok; tersedia Bahasa Indonesia",
                   "Theme / Tema — mis. mode kontras tinggi untuk siswa dengan hambatan penglihatan"],
         "catatan": "Menu Settings adalah pengganti ikon globe pada versi lama dan BELUM terdokumentasi "
                    "di Scratch Wiki. Buka dan cek langsung sebelum mengajar, lalu sesuaikan.", "warn": True},
        {"n": "3. Menu File", "chip": "Urusan berkas proyek",
         "fungsi": "Membuat, menyimpan, dan membuka proyek.",
         "param": ["New — proyek baru (simpan dulu yang lama!)",
                   "Save now — simpan ke akun Scratch (harus login)",
                   "Save as a copy — simpan salinan / versi percobaan",
                   "Load from your computer — buka berkas .sb3",
                   "Save to your computer — unduh berkas .sb3 (wajib bila siswa tanpa akun)"],
         "catatan": "Berkas Scratch berekstensi .sb3 — sebenarnya arsip ZIP berisi kode, gambar, "
                    "dan suara dalam satu berkas."},
        {"n": "4. Menu Edit", "chip": "Penyelamat & mode cepat",
         "fungsi": "Mengembalikan yang terhapus dan mengatur Turbo Mode.",
         "param": ["Restore (Undelete) — kembalikan sprite/kostum/suara yang TERAKHIR dihapus",
                   "Turn on Turbo Mode — jalankan proyek sangat cepat"],
         "catatan": "Pintasan Turbo Mode: Shift + klik bendera hijau. Bila proyek tiba-tiba berjalan "
                    "\"kesurupan\" cepat, periksa menu ini."},
        {"n": "5. Kolom Nama Proyek", "chip": "Identitas karya",
         "fungsi": "Klik lalu ketik untuk mengganti nama proyek.",
         "contoh": "Aturan penamaan:\n\nNama_Kelas_Judul\n\nContoh:\nRina_7A_Kucing-Menari",
         "catatan": "Nama proyek memudahkan guru menilai dan siswa mencari kembali karyanya. "
                    "Wajib diganti SEBELUM mulai koding."},
        {"n": "6. See Project Page", "chip": "Tampilan untuk orang lain",
         "fungsi": "Berpindah dari mode editor ke halaman proyek — tampilan yang dilihat orang lain.",
         "param": ["Berisi judul, instruksi, catatan & kredit",
                   "Ada tombol Love dan Favorite",
                   "Di halaman inilah terdapat tombol SHARE"],
         "catatan": "Proyek TIDAK otomatis publik. Selama tombol Share belum ditekan, proyek hanya "
                    "bisa dilihat pemiliknya. Bedakan Save dan Share.", "warn": True},
        {"n": "7. Tutorials", "chip": "Panduan interaktif bawaan",
         "fungsi": "Membuka pustaka panduan bawaan Scratch, tampil di panel samping.",
         "param": ["Contoh: Getting Started, Make it Fly, Animate a Name",
                   "Siswa bisa menonton sambil mengerjakan"],
         "catatan": "Sangat berguna untuk siswa yang sudah selesai lebih dulu — beri tugas mandiri "
                    "\"pilih satu tutorial\"."},
        {"n": "8. Debug", "chip": "Debugging Help (sejak 16 Des 2024)",
         "fungsi": "Menampilkan tips mencari kesalahan pada script.",
         "contoh": "Istilah yang diajarkan:\n\nBUG\n= kesalahan pada\n  program\n\nDEBUGGING\n= mencari dan\n  memperbaiki bug",
         "catatan": "Jadikan momen memperkenalkan istilah bug dan debugging — dua kata yang akan "
                    "dipakai siswa seumur hidup bila melanjutkan ke pemrograman."},
        {"n": "9. Ikon Folder — My Stuff", "chip": "Arsip karya",
         "fungsi": "Membuka daftar semua proyek milik kita.",
         "param": ["Proyek yang sedang dikerjakan", "Proyek yang sudah dibagikan",
                   "Proyek di keranjang sampah"]},
        {"n": "10. Menu Akun", "chip": "Identitas & keamanan",
         "fungsi": "Berisi Profile, My Stuff, Account settings, dan Sign out.",
         "catatan": "Ajarkan sejak awal: SELALU Sign out di komputer lab atau komputer bersama.",
         "warn": True},
    ],
    "praktik": [
        "Ganti nama proyek menjadi Nama_Kelas_Latihan1.",
        "Buka File > Save to your computer, simpan ke folder kelas.",
        "Hapus sprite kucing, lalu kembalikan lewat Edit > Restore.",
        "Buka Settings, ubah bahasa ke Bahasa Indonesia, amati blok berubah, lalu kembalikan.",
        "Klik See Project Page, amati tampilannya, lalu kembali ke editor.",
    ],
    "praktik_note": "Alokasi 10 menit. Tekankan kebiasaan menyimpan setiap 10 menit.",
    "analogi": [
        "Menu Bar itu seperti meja guru di depan kelas:",
        "bukan tempat kerja, tapi tempat semua urusan administrasi —",
        "nama, penyimpanan, dan siapa yang sedang bertugas.",
    ],
    "mistakes": [
        ["Tidak pernah menyimpan", "Kerja hilang saat browser tertutup", "Aturan kelas: simpan tiap 10 menit"],
        ["Klik logo Scratch di tengah pekerjaan", "Keluar editor tanpa peringatan", "Ingatkan di awal pelajaran"],
        ["Membiarkan nama Untitled-1", "Guru sulit menilai, siswa sulit mencari", "Wajib ganti nama sebelum koding"],
        ["Mengira proyek sudah dibagikan", "Tugas dianggap tidak dikumpulkan", "Bedakan Save dengan Share"],
        ["Turbo Mode aktif tanpa sadar", "Game jadi tak terkendali cepat", "Cek menu Edit bila proyek \"kesurupan\""],
    ],
    "quiz": [
        "Apa beda Save now dengan Save to your computer?",
        "Kamu tidak sengaja menghapus sprite. Menu apa yang menyelamatkanmu?",
        "Proyekmu sudah di-Save. Apakah teman sekelas otomatis bisa melihatnya? Jelaskan.",
        "Apa arti kata bug dan debugging?",
    ],
    "answers": [
        "Save now menyimpan ke akun Scratch di internet (butuh login); Save to your computer mengunduh berkas .sb3 ke komputer.",
        "Edit > Restore.",
        "Belum. Save hanya menyimpan; agar bisa dilihat orang lain harus ditekan tombol Share di halaman proyek.",
        "Bug = kesalahan pada program; debugging = proses menemukan dan memperbaikinya.",
    ],
    "takeaways": [
        "Menu Bar mengurus BERKAS dan AKUN, bukan perintah untuk sprite.",
        "Save menyimpan; Share membagikan. Dua hal yang berbeda.",
        "Edit > Restore menyelamatkan sprite yang terakhir terhapus.",
    ],
}

M02 = {
    "file": "02-tab-code-costumes-sounds", "short": "Tab", "name": "Tab Code / Costumes / Sounds",
    "kicker": "MODUL 2  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("4D97FF"),
    "lokasi": "Letak: kiri atas, tepat di bawah Menu Bar",
    "durasi": "Estimasi 10 menit  ·  Jenjang SD kelas 5 - SMP",
    "tagline": "Tiga ruang kerja yang dimiliki setiap sprite.",
    "tujuan": [
        "Menjelaskan bahwa setiap sprite punya tiga ruang kerja.",
        "Berpindah antar tab dengan tepat sesuai kebutuhan.",
        "Menyadari bahwa isi ketiga tab berubah mengikuti sprite yang sedang dipilih.",
    ],
    "denah": """
   +----------+ +------------+ +----------+
   |   Code   | |  Costumes  | |  Sounds  |
   +----------+ +------------+ +----------+
      AKTIF

   "Apa yang        "Bagaimana        "Suara apa
    DILAKUKAN        RUPA sprite       yang DIMILIKI
    sprite ini?"     ini?"             sprite ini?"
""",
    "denah_note": "Isi ketiga tab menempel pada SPRITE, bukan pada proyek. Ganti sprite, isinya ikut berganti.",
    "details": [
        {"n": "Konsep kunci yang sering terlewat", "chip": "Sumber kebingungan nomor satu",
         "fungsi": "Isi ketiga tab menempel pada SPRITE, bukan pada proyek.",
         "contoh": "Pilih Sprite2\n  -> tab Code kosong\n\nBukan berarti kode\nSprite1 terhapus!\n\nPilih Sprite1 lagi\n  -> kodenya muncul",
         "catatan": "Inilah penyebab keluhan klasik \"Pak, kode saya hilang!\" — padahal hanya salah "
                    "memilih sprite. Biasakan siswa melihat sprite mana yang bersorot ungu.", "warn": True},
        {"n": "Tab Code", "chip": "Ruang utama pemrograman",
         "fungsi": "Tempat menyusun blok menjadi script.",
         "param": ["Berisi selektor kategori blok", "Palet blok", "Area kode (kanvas)"],
         "catatan": "Dibahas rinci di modul 3, 4, dan 5."},
        {"n": "Tab Costumes", "chip": "Rupa sprite + Paint Editor",
         "fungsi": "Mengelola daftar kostum sprite dan menggambarnya.",
         "param": ["Urutan kostum menentukan hasil blok next costume",
                   "4 cara menambah: pustaka, gambar sendiri, acak, unggah",
                   "Mode Vector (tajam saat diperbesar) atau Bitmap (berbasis piksel)",
                   "Klik kanan kostum untuk menduplikasi / menghapus"],
         "catatan": "Setiap sprite WAJIB punya minimal satu kostum. Bila Stage yang dipilih, tab ini "
                    "berganti nama menjadi Backdrops."},
        {"n": "Tab Sounds", "chip": "Suara sprite + Sound Editor",
         "fungsi": "Mengelola daftar suara sprite dan mengeditnya.",
         "param": ["Sumber: pustaka Scratch, REKAM sendiri lewat mikrofon, atau unggah",
                   "Potong & salin: pilih bagian gelombang lalu Cut/Copy/Paste",
                   "9 efek: Faster, Slower, Louder, Softer, Fade In, Fade Out, Mute, Reverse, Robot"],
         "catatan": "Batasi rekaman siswa maksimal 5 detik — batas ukuran aset Scratch adalah 10 MB "
                    "dan rekaman panjang membuat proyek berat."},
    ],
    "praktik": [
        "Pilih Sprite1 > buka tab Costumes > klik costume2 > amati kucing berubah pose.",
        "Buka tab Sounds > klik tombol putar pada suara Meow.",
        "Rekam suaramu sendiri mengucapkan \"Halo!\" (Record), beri nama salam.",
        "Kembali ke tab Code. Pastikan siswa paham ketiganya milik sprite yang sama.",
    ],
    "praktik_note": "Alokasi 7 menit.",
    "analogi": [
        "Bayangkan sprite adalah seorang AKTOR:",
        "Code = naskah — apa yang harus dia lakukan",
        "Costumes = lemari kostum — pakaian yang bisa dia kenakan",
        "Sounds = pita suara — suara yang bisa dia keluarkan",
    ],
    "mistakes": [
        ["Membuat kode di sprite yang salah", "Kode \"hilang\" atau sprite tak bergerak", "Lihat sprite mana yang bersorot ungu"],
        ["Menghapus semua kostum", "Sprite tak bisa ditampilkan", "Ingatkan minimal satu kostum"],
        ["Merekam suara terlalu panjang", "Ukuran proyek membengkak", "Batasi rekaman maksimal 5 detik"],
        ["Bingung mencari Costumes saat Stage dipilih", "Tab berganti jadi Backdrops", "Jelaskan pengecualian ini sekali di awal"],
    ],
    "quiz": [
        "Kamu memilih Sprite2, lalu tab Code tampak kosong. Apakah kode Sprite1 terhapus?",
        "Di tab mana kamu merekam suaramu sendiri?",
        "Saat Stage dipilih, tab Costumes berubah menjadi apa? Mengapa?",
    ],
    "answers": [
        "Tidak. Setiap sprite punya area kode sendiri. Pilih kembali Sprite1 maka kodenya muncul lagi.",
        "Tab Sounds, dengan tombol Record.",
        "Menjadi Backdrops, karena Stage tidak memakai kostum melainkan latar belakang.",
    ],
    "takeaways": [
        "Code, Costumes, Sounds adalah tiga sisi dari SATU sprite yang sama.",
        "Isi ketiga tab menempel pada sprite — ganti sprite, isinya ikut berganti.",
        "Stage tidak punya Costumes, melainkan Backdrops.",
    ],
}

M03 = {
    "file": "03-selektor-kategori-blok", "short": "Kategori Blok", "name": "Selektor Kategori Blok",
    "kicker": "MODUL 3  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("FF8C1A"),
    "lokasi": "Letak: kolom paling kiri di dalam tab Code, berupa deretan bulatan warna",
    "durasi": "Estimasi 15 menit  ·  Jenjang SD kelas 5 - SMP",
    "tagline": "Warna bukan hiasan — warna adalah identitas fungsi blok.",
    "tujuan": [
        "Menyebutkan 9 kategori blok beserta warnanya.",
        "Menebak kategori yang tepat untuk sebuah kebutuhan.",
        "Menemukan dan mengaktifkan Ekstensi.",
    ],
    "denah": """
   O  Motion       biru
   O  Looks        ungu
   O  Sound        merah muda
   O  Events       kuning
   O  Control      oranye
   O  Sensing      biru muda
   O  Operators    hijau
   O  Variables    oranye tua
   O  My Blocks    merah muda tua
   -------------------------------
   (+) Add Extension    <-- pojok kiri bawah
""",
    "denah_note": "Klik salah satu bulatan, palet blok di sebelah kanan langsung melompat ke kategori tersebut.",
    "details": [
        {"n": "Warna = identitas fungsi", "chip": "Konsep utama modul ini",
         "fungsi": "Ratusan blok dikelompokkan jadi 9 kategori berwarna agar tidak membingungkan.",
         "contoh": "Siswa yang hafal\nwarna bekerja jauh\nlebih cepat:\n\nmengenali jenis blok\ndari JAUH tanpa\nmembaca tulisannya.",
         "catatan": "Latih pengenalan warna lewat permainan cepat, bukan hafalan daftar. "
                    "Guru menyebut kebutuhan, siswa menyebut warna."},
        {"n": "Kategori khusus: Motion", "chip": "Hanya untuk Sprite",
         "fungsi": "Kategori Motion akan KOSONG bila yang dipilih adalah Stage.",
         "catatan": "Panggung tidak bisa bergerak, jadi tidak punya blok gerak. Jelaskan sekali di "
                    "awal agar siswa tidak mengira editornya rusak."},
        {"n": "Tombol Add Extension", "chip": "Menambah kategori blok baru",
         "fungsi": "Membuka pustaka ekstensi — kategori blok tambahan yang tidak aktif secara bawaan.",
         "param": ["Music — not, drum, tempo (membuat alat musik)",
                   "Pen — menggambar dan stamp (seni geometris)",
                   "Text to Speech — sprite berbicara dengan suara (butuh internet)",
                   "Translate — menerjemahkan teks (butuh internet)",
                   "Video Sensing / Face Sensing — mendeteksi gerakan & wajah lewat kamera"],
         "catatan": "Ekstensi yang dipilih muncul sebagai kategori baru di bawah My Blocks dan IKUT "
                    "TERSIMPAN di dalam berkas proyek — tidak perlu dipasang ulang tiap kali."},
    ],
    "tables": [{
        "judul": "Sembilan Kategori Blok",
        "headers": ["Kategori", "Warna", "Pertanyaan yang dijawab", "Contoh blok"],
        "rows": [
            ["Motion", "Biru", "Bergerak ke mana?", "move (10) steps"],
            ["Looks", "Ungu", "Terlihat bagaimana?", "say [Halo!]"],
            ["Sound", "Merah muda", "Berbunyi apa?", "start sound (Meow)"],
            ["Events", "Kuning", "Kapan mulai?", "when green flag clicked"],
            ["Control", "Oranye", "Berapa kali? Kalau begini bagaimana?", "repeat (10), if ... then"],
            ["Sensing", "Biru muda", "Ada apa di sekitarku?", "touching (mouse-pointer)?"],
            ["Operators", "Hijau", "Berapa hasil hitungnya?", "(1) + (2), pick random"],
            ["Variables", "Oranye tua", "Simpan angka / teks di mana?", "set (skor) to (0)"],
            ["My Blocks", "Merah muda tua", "Bisakah aku buat perintah sendiri?", "blok buatan siswa"],
        ],
        "widths": [16, 14, 40, 30], "size": 11,
    }],
    "praktik": [
        "Permainan Tebak Warna: guru menyebut kebutuhan, siswa menyebut warna + kategori secepatnya.",
        "\"Kucing berjalan maju\" > Biru, Motion.   \"Kucing bilang halo\" > Ungu, Looks.",
        "\"Mulai saat bendera diklik\" > Kuning, Events.   \"Ulangi 10 kali\" > Oranye, Control.",
        "\"Apakah menyentuh tepi?\" > Biru muda, Sensing.   \"Simpan skor\" > Oranye tua, Variables.",
        "Aktivitas ekstensi: klik Add Extension > pilih Music > tarik blok play drum > klik bloknya.",
    ],
    "praktik_note": "Alokasi 8 menit: 5 menit permainan warna, 3 menit ekstensi.",
    "analogi": [
        "Selektor kategori itu seperti daftar rak di perpustakaan.",
        "Kamu tidak perlu membongkar seluruh perpustakaan untuk mencari buku resep —",
        "cukup pergi ke rak \"Masakan\".",
        "Warna adalah papan nama raknya.",
    ],
    "mistakes": [
        ["Menggulir palet mencari blok satu per satu", "Boros waktu", "Latih klik kategori, jangan menggulir"],
        ["Mencari blok Motion saat Stage dipilih", "Palet tampak kosong / aneh", "Cek dulu: sprite atau Stage yang aktif?"],
        ["Mengaktifkan banyak ekstensi sekaligus", "Palet penuh & membingungkan", "Aktifkan hanya yang dipakai"],
        ["Mengira ekstensi harus dipasang tiap kali", "Kebingungan", "Ekstensi ikut tersimpan di proyek"],
    ],
    "quiz": [
        "Sebutkan warna kategori Control dan satu blok di dalamnya.",
        "Kamu ingin sprite berhenti bila menyentuh tepi. Kategori mana yang dibuka lebih dulu?",
        "Mengapa kategori Motion kosong ketika Stage dipilih?",
        "Di mana letak tombol untuk menambah ekstensi Music?",
    ],
    "answers": [
        "Oranye; contoh: repeat, forever, if ... then, wait.",
        "Sensing (untuk touching edge?), lalu dipasang ke dalam blok Control if ... then.",
        "Karena Stage tidak bisa bergerak — panggung selalu diam.",
        "Tombol Add Extension di pojok kiri bawah editor.",
    ],
    "takeaways": [
        "Warna blok adalah identitas fungsi — hafal warna, kerja jadi cepat.",
        "Motion kosong di Stage karena panggung tidak bisa bergerak.",
        "Ekstensi menambah kategori baru dan ikut tersimpan dalam proyek.",
    ],
}

M04 = {
    "file": "04-palet-blok", "short": "Palet Blok", "name": "Palet Blok (Block Palette)",
    "kicker": "MODUL 4  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("59C059"),
    "lokasi": "Letak: kolom di sebelah kanan selektor kategori",
    "durasi": "Estimasi 15 menit  ·  Jenjang SD kelas 5 - SMP",
    "tagline": "Rak berisi semua blok — blok di sini belum berfungsi sebelum ditarik ke area kode.",
    "tujuan": [
        "Menarik (drag) blok dari palet ke area kode.",
        "Membedakan bentuk blok dan tahu di mana masing-masing boleh dipasang.",
        "Mengisi kolom isian dan memilih dropdown pada blok.",
        "Menggunakan kotak centang untuk menampilkan monitor nilai di panggung.",
    ],
    "denah": """
   Motion
   +----------------------------+
   | move (10) steps            |  <- blok stack
   | turn right (15) degrees    |
   | go to (random position v)  |  <- ada dropdown
   | go to x:(0) y:(0)          |  <- ada kolom isian
   | glide (1) secs to ...      |
   | ...                        |
   | [ ] (x position)           |  <- reporter + kotak centang
   | [ ] (y position)           |
   +----------------------------+
""",
    "denah_note": "Blok di palet TIDAK AKAN HABIS — menarik satu blok berarti membuat salinannya.",
    "details": [
        {"n": "Cara mengambil blok", "chip": "Dua cara, dua tujuan berbeda",
         "fungsi": "Blok bisa ditarik untuk diprogram, atau diklik untuk diuji coba.",
         "param": ["TARIK ke area kode — blok tersalin, menjadi bagian program",
                   "KLIK di palet (tanpa menarik) — blok langsung dijalankan SEKALI",
                   "Menggulir palet — berpindah kategori secara halus"],
         "catatan": "Trik mengajar: minta siswa MENGKLIK move (10) steps berkali-kali dan mengamati "
                    "kucing bergeser. Ini menanamkan hubungan sebab-akibat sebelum menyusun script."},
        {"n": "Bentuk blok = aturan pemasangan", "chip": "Scratch mencegah kesalahan secara fisik",
         "fungsi": "Bentuk lubang harus cocok dengan bentuk blok. Kalau tidak bisa masuk, berarti "
                   "memang tidak boleh.",
         "contoh": "Hat    -> paling atas\nStack  -> ditumpuk\nC      -> membungkus\nReporter -> lubang oval\nBoolean  -> lubang\n            segi enam\nCap    -> paling bawah",
         "catatan": "Inilah kelebihan bahasa visual: siswa tidak mungkin membuat kesalahan sintaks "
                    "seperti lupa titik koma di bahasa teks."},
        {"n": "Bagian yang bisa diubah di dalam blok", "chip": "Isian, dropdown, dan lubang",
         "fungsi": "Blok bukan benda mati — isinya bisa diganti agar perilakunya berubah.",
         "param": ["Kolom isian putih — klik lalu ketik angka/teks baru",
                   "Dropdown — klik untuk memilih pilihan lain",
                   "Kotak warna — klik untuk memilih warna (ada alat pipet)",
                   "Lubang oval — bisa diisi blok reporter",
                   "Lubang segi enam — hanya menerima blok boolean"],
         "catatan": "Penting: kolom isian BISA DIGANTI DENGAN BLOK LAIN. "
                    "move (pick random 1 to 10) steps adalah gerbang menuju program yang dinamis."},
        {"n": "Kotak centang di sebelah blok reporter", "chip": "Alat debugging terbaik untuk pemula",
         "fungsi": "Mencentangnya memunculkan MONITOR nilai di pojok kiri atas panggung.",
         "contoh": "[x] (x position)\n[x] (y position)\n\n-> muncul kotak\n   kecil berisi angka\n   di panggung\n\n-> seret sprite,\n   angkanya berubah",
         "catatan": "Cara termudah memperkenalkan koordinat: centang x position, lalu minta siswa "
                    "menyeret sprite dan membacakan angkanya bersama-sama."},
    ],
    "praktik": [
        "KLIK blok move (10) steps di palet 5 kali. Amati kucing.",
        "Ubah angkanya menjadi 100, klik lagi. Bandingkan hasilnya.",
        "Tarik turn right (15) degrees ke area kode, ubah jadi 90, klik. Amati arah kucing.",
        "Centang x position dan y position. Seret kucing dan bacakan angkanya bersama.",
        "Buka dropdown go to (random position) > pilih mouse-pointer > klik blok > gerakkan mouse.",
    ],
    "praktik_note": "Alokasi 8 menit.",
    "analogi": [
        "Palet blok itu rak bumbu di dapur.",
        "Bumbunya tidak pernah habis — kamu mengambil \"sesendok\"",
        "untuk dimasukkan ke panci (area kode).",
        "Selama masih di rak, bumbu itu belum jadi masakan.",
    ],
    "mistakes": [
        ["Menyusun blok DI DALAM palet", "Blok hilang saat ganti kategori", "Merangkai HANYA di area kode"],
        ["Memaksa blok masuk ke lubang salah bentuk", "Siswa frustrasi", "Ajarkan aturan bentuk sejak awal"],
        ["Mengetik di kolom isian tapi lupa klik di luar", "Nilai belum tersimpan", "Biasakan klik area kosong setelah mengetik"],
        ["Semua kotak centang dicentang", "Panggung penuh monitor", "Centang seperlunya saja"],
        ["Mengira klik blok di palet = memprogram", "Kode tidak tersimpan", "Bedakan \"mencoba\" dan \"menyusun\""],
    ],
    "quiz": [
        "Apa yang terjadi bila kamu MENGKLIK (bukan menarik) blok di palet?",
        "Blok berbentuk segi enam hanya bisa dipasang di lubang berbentuk apa?",
        "Apa fungsi kotak centang di sebelah blok x position?",
        "Bisakah lubang angka pada move ( ) steps diisi blok lain? Beri contoh.",
    ],
    "answers": [
        "Blok langsung dijalankan satu kali, tanpa menambah kode ke proyek.",
        "Lubang segi enam (slot kondisi), misalnya pada if < > then atau repeat until < >.",
        "Menampilkan atau menyembunyikan monitor nilai x di panggung.",
        "Bisa. Contoh: move (pick random (1) to (10)) steps atau move (x position) steps.",
    ],
    "takeaways": [
        "Blok di palet tidak pernah habis — yang ditarik adalah salinannya.",
        "Bentuk blok adalah tata bahasa: bentuk lubang harus cocok dengan bentuk blok.",
        "Kotak centang reporter = alat debugging paling mudah untuk pemula.",
    ],
}

M05 = {
    "file": "05-area-kode", "short": "Area Kode", "name": "Area Kode (Scripts Area)",
    "kicker": "MODUL 5  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("5CB1D6"),
    "lokasi": "Letak: kanvas abu-abu bertitik besar di tengah editor",
    "durasi": "Estimasi 20 menit  ·  Jenjang SD kelas 5 - SMP",
    "tagline": "Meja kerja tempat blok dirangkai menjadi script.",
    "tujuan": [
        "Merangkai blok menjadi script yang berjalan.",
        "Memakai klik kanan untuk Duplicate, Add Comment, Delete, dan Clean up blocks.",
        "Mengatur zoom agar kode nyaman dibaca.",
        "Menjalankan script dengan mengklik langsung tumpukan blok.",
    ],
    "denah": """
   +-------------------------------------------+
   |  . . . . . . . . . . . . . . . . . . . .  |
   |  . +----------------+ . . . . . . . . . .  |
   |  . | when green     | . . . . . . . . . .  |
   |  . |   flag clicked | . . . . . . . . . .  |
   |  . +----------------+ . . . . . . . . . .  |
   |  . | move (10) steps| . . . . . . . . . .  |
   |  . +----------------+ . . . . . . . . . .  |
   |  . . . . . . . . . . . . . . . (+)(-)(=)  |  <- tombol zoom
   +-------------------------------------------+
""",
    "denah_note": "Area kode SANGAT LUAS dan bisa digulir ke segala arah — terasa penuh bukan masalah.",
    "details": [
        {"n": "Menyambung dan melepas blok", "chip": "Keterampilan motorik dasar",
         "fungsi": "Blok menempel bila ditarik cukup dekat sampai muncul bayangan putih.",
         "param": ["Menyambung — tarik mendekat sampai muncul BAYANGAN PUTIH, lalu lepas",
                   "Melepas tumpukan — tarik blok, SEMUA blok di bawahnya ikut terbawa",
                   "Mengambil satu blok saja — lepas dulu blok di bawahnya",
                   "Menghapus — tarik kembali ke palet, atau klik kanan > Delete Block"],
         "catatan": "Cara menguji blok benar-benar menempel: tarik blok teratas. Bila blok di bawahnya "
                    "tidak ikut, berarti belum menempel."},
        {"n": "Menjalankan script", "chip": "Dua cara menjalankan",
         "fungsi": "Script bisa dijalankan langsung dengan mengkliknya, atau lewat bendera hijau.",
         "contoh": "KLIK tumpukan blok\n-> berjalan seketika\n-> ada garis KUNING\n   menyala saat aktif\n\nKlik bendera hijau\n-> semua script\n   ber-hat block\n   Events berjalan",
         "catatan": "Script berkilau kuning saat berjalan — manfaatkan ini agar siswa bisa \"melihat\" "
                    "programnya bekerja, bukan sekadar menebak."},
        {"n": "Klik kanan pada area kosong", "chip": "Menu penyelamat & perapi",
         "fungsi": "Membuka menu untuk membatalkan, merapikan, dan memberi catatan.",
         "param": ["Undo — batalkan tindakan terakhir",
                   "Redo — ulangi tindakan yang dibatalkan",
                   "Clean up blocks — MERAPIKAN semua script jadi tersusun rapi",
                   "Add Comment — menambah catatan kuning",
                   "Delete (N) Blocks — menghapus SELURUH blok di area kode"],
         "catatan": "Delete (N) Blocks bisa menghapus semua kerja siswa. Ajarkan Ctrl+Z / Undo segera "
                    "setelah memperkenalkan menu ini.", "warn": True},
        {"n": "Klik kanan pada sebuah blok", "chip": "Menu per-blok",
         "fungsi": "Menyalin, memberi catatan, atau menghapus satu blok.",
         "param": ["Duplicate — menyalin blok BESERTA blok di bawahnya",
                   "Add Comment — menempelkan catatan pada blok itu",
                   "Delete Block — menghapus blok tersebut saja"]},
        {"n": "Komentar (Comment)", "chip": "Catatan untuk manusia",
         "fungsi": "Kotak kuning berisi penjelasan; TIDAK memengaruhi jalannya program.",
         "contoh": "when green flag clicked\n  <- \"Awal permainan\"\nset (skor) to (0)\n  <- \"Skor mulai\n      dari nol\"",
         "catatan": "Ini versi Scratch dari // di JavaScript atau # di Python — kebiasaan baik yang "
                    "akan sangat berguna saat siswa pindah ke bahasa teks."},
        {"n": "Tombol Zoom", "chip": "Pojok kanan bawah area kode",
         "fungsi": "Memperbesar / memperkecil tampilan blok. Tidak mengubah program.",
         "param": ["(+) perbesar — dipakai saat memproyeksikan ke layar kelas",
                   "(-) perkecil — untuk melihat script panjang secara utuh",
                   "(=) kembalikan ke ukuran normal"],
         "catatan": "Tegaskan: zoom hanya mengubah TAMPILAN KODE, tidak mengubah ukuran sprite "
                    "maupun jalannya program."},
    ],
    "praktik": [
        "Susun: when green flag clicked > move (100) steps > say [Halo!] for (2) seconds. Jalankan.",
        "Klik kanan pada move (100) steps > Duplicate > pasang di bawahnya. Jalankan, bandingkan.",
        "Klik kanan area kosong > Add Comment > tulis \"Ini program pertamaku\". Lalu Clean up blocks.",
        "Buat script KEDUA yang terpisah: when green flag clicked > turn right (15) degrees.",
        "Diskusi: apakah dua script bisa berjalan bersamaan? (Jawab: bisa — inilah paralelisme.)",
    ],
    "praktik_note": "Alokasi 12 menit untuk empat latihan.",
    "analogi": [
        "Area kode adalah meja tempat menyusun puzzle.",
        "Palet adalah kotak kepingannya.",
        "Puzzle hanya bisa disusun di meja,",
        "dan kepingan hanya menempel kalau bentuknya cocok.",
    ],
    "mistakes": [
        ["Blok menumpuk tapi tidak menempel", "Hanya blok teratas yang jalan", "Cari bayangan putih; uji dengan menarik blok teratas"],
        ["Menekan Delete (N) Blocks tanpa sengaja", "Seluruh kode hilang", "Ajarkan Ctrl+Z / Undo segera"],
        ["Membuat script tanpa hat block", "Script tidak jalan saat bendera diklik", "Setiap script diawali blok kuning"],
        ["Script menumpuk berantakan", "Sulit dibaca & dinilai", "Biasakan Clean up blocks sebelum mengumpulkan"],
        ["Mengira zoom mengubah ukuran sprite", "Salah paham", "Zoom hanya tampilan kode"],
    ],
    "quiz": [
        "Bagaimana cara tahu dua blok benar-benar sudah menempel?",
        "Apa fungsi Clean up blocks?",
        "Apakah komentar kuning memengaruhi jalannya program?",
        "Kamu punya 3 script terpisah yang semuanya diawali when green flag clicked. Berapa yang berjalan?",
    ],
    "answers": [
        "Saat menarik blok teratas, blok di bawahnya ikut terbawa. Saat menyambung juga muncul bayangan putih.",
        "Merapikan seluruh script agar tersusun rapi dari atas ke bawah.",
        "Tidak. Komentar hanya catatan untuk manusia.",
        "Ketiganya berjalan bersamaan (paralel).",
    ],
    "takeaways": [
        "Blok hanya menempel bila muncul bayangan putih — uji dengan menarik blok teratas.",
        "Clean up blocks sebelum mengumpulkan tugas; komentar untuk menjelaskan maksud.",
        "Banyak script bisa berjalan bersamaan — inilah paralelisme.",
    ],
}

M06 = {
    "file": "06-panggung-stage", "short": "Panggung", "name": "Panggung (Stage)",
    "kicker": "MODUL 6  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("9966FF"),
    "lokasi": "Letak: kotak putih besar di kanan atas editor",
    "durasi": "Estimasi 20 menit  ·  Jenjang SD kelas 5 - SMP",
    "tagline": "Layar tempat proyek berjalan — 480 x 360 piksel, dengan bidang Cartesius sungguhan.",
    "tujuan": [
        "Menyebutkan ukuran panggung dan rentang koordinatnya.",
        "Membaca posisi sprite dalam bentuk pasangan (x, y).",
        "Memindahkan sprite ke koordinat tertentu dengan blok go to x: y:.",
        "Menjelaskan mengapa sprite tidak bisa hilang total dari panggung.",
    ],
    "denah": """
                     y = +180
                        ^
                        |
                        |         [kucing]
        x = -240 -------+---------------- x = +240
                        |   (0,0)
                        |
                        v
                     y = -180

                  480 x 360 piksel
""",
    "denah_note": "Ini bidang Cartesius yang PERSIS SAMA dengan pelajaran Matematika — manfaatkan kaitannya.",
    "details": [
        {"n": "Ukuran dan koordinat", "chip": "Angka yang wajib dihafal",
         "fungsi": "Panggung berukuran tetap dan memakai koordinat Cartesius dengan pusat di tengah.",
         "param": ["Ukuran 480 x 360 piksel (rasio 4:3)",
                   "Titik pusat (0, 0) tepat di tengah",
                   "Sumbu X mendatar: -240 (kiri) sampai +240 (kanan)",
                   "Sumbu Y tegak: -180 (bawah) sampai +180 (atas)"],
         "catatan": "Berbeda dari aplikasi lain yang menaruh (0,0) di pojok kiri atas. Tekankan: "
                    "di Scratch pusatnya di TENGAH, dan Y positif berarti NAIK."},
        {"n": "Titik penting untuk dihafal", "chip": "Lima koordinat kunci",
         "fungsi": "Menghafal lima titik ini membuat siswa cepat menempatkan sprite.",
         "contoh": "Tengah\n  (0, 0)\n\nKiri atas\n  (-240, 180)\nKanan atas\n  (240, 180)\nKiri bawah\n  (-240, -180)\nKanan bawah\n  (240, -180)"},
        {"n": "Aturan sprite tidak bisa kabur (fencing)", "chip": "Bukan bug, memang dirancang",
         "fungsi": "Scratch selalu menjaga minimal 15 piksel bagian sprite tetap terlihat di panggung.",
         "contoh": "go to x: (9999)\n  y: (9999)\n\n-> sprite BERHENTI\n   menempel di pojok\n\n-> tidak hilang\n   selamanya",
         "catatan": "Ini menjelaskan keluhan siswa \"kok kucingnya nyangkut di pinggir?\" — memang "
                    "dirancang begitu supaya sprite tidak bisa hilang."},
        {"n": "Yang TIDAK bisa dilakukan Panggung", "chip": "Beda mendasar dari sprite",
         "fungsi": "Panggung adalah latar, bukan tokoh — jadi banyak blok tidak berlaku untuknya.",
         "param": ["Tidak bisa bergerak / memakai blok Motion",
                   "Tidak bisa say atau think (tidak punya balon bicara)",
                   "Tidak bisa diklon (hanya ada satu panggung)",
                   "Tidak bisa diganti nama (selalu \"Stage\")",
                   "Tidak bisa berpindah lapisan (selalu paling belakang)"],
         "catatan": "Yang BISA: mengganti backdrop, memainkan suara, efek grafis, ask ... and wait, "
                    "variabel, dan menerima broadcast."},
    ],
    "tables": [{
        "judul": "Hubungan Lintas Mata Pelajaran",
        "headers": ["Mata pelajaran", "Kaitan dengan panggung Scratch"],
        "rows": [
            ["Matematika", "Bidang Cartesius, bilangan bulat positif-negatif, kuadran"],
            ["Seni Budaya", "Komposisi dan tata letak visual"],
            ["IPA", "Simulasi gerak lurus, pantulan, dan gravitasi (dengan variabel kecepatan)"],
        ],
        "widths": [25, 75], "size": 13,
    }],
    "praktik": [
        "Centang x position dan y position. Seret kucing; siswa membacakan angkanya.",
        "Guru menyebut posisi (\"pojok kanan atas\"), siswa menebak angkanya sebelum menyeret.",
        "Berburu harta karun: go to x: (-200) y: (150), lalu (0,0), lalu (200,-150).",
        "Uji batas: go to x: (9999) y: (9999). Amati kucing berhenti di pojok, tidak hilang.",
        "Diskusikan aturan fencing: mengapa Scratch tidak membiarkan sprite hilang?",
    ],
    "praktik_note": "Alokasi 12 menit. Latihan 1 dan 2 adalah inti pemahaman koordinat.",
    "analogi": [
        "Panggung adalah panggung teater sungguhan.",
        "Ukurannya tetap dan tidak bisa dilebarkan.",
        "Aktor boleh berlari ke mana saja, tapi selalu ada bagian tubuhnya yang terlihat penonton.",
        "Koordinat adalah alamat kursi di panggung itu.",
    ],
    "mistakes": [
        ["Mengira (0,0) di pojok kiri atas", "Salah menghitung posisi", "Tekankan pusat = (0,0)"],
        ["Lupa Y naik ke atas bernilai positif", "Sprite bergerak terbalik", "Latih menyeret sprite sambil membaca monitor"],
        ["Menaruh sprite di luar rentang", "Sprite \"nyangkut\" di tepi", "Jelaskan aturan fencing"],
        ["Mencari blok Motion untuk Stage", "Palet kosong", "Panggung tidak bisa bergerak"],
    ],
    "quiz": [
        "Berapa ukuran panggung Scratch dalam piksel?",
        "Sebutkan koordinat pojok kiri bawah panggung.",
        "Apa yang terjadi bila sprite diperintah go to x: 500 y: 500?",
        "Sebutkan dua hal yang tidak bisa dilakukan Stage tetapi bisa dilakukan sprite.",
    ],
    "answers": [
        "480 x 360 piksel.",
        "(-240, -180).",
        "Sprite berhenti menempel di pojok kanan atas; Scratch menjaga minimal 15 px tetap terlihat (fencing).",
        "Antara lain: bergerak (blok Motion), berbicara (say/think), diklon, berganti lapisan, diganti nama.",
    ],
    "takeaways": [
        "Panggung 480 x 360, pusat (0,0), Y positif berarti NAIK.",
        "Sprite tidak bisa hilang total — minimal 15 piksel selalu terlihat.",
        "Stage adalah latar, bukan tokoh: tidak bergerak, tidak bicara, tidak bisa diklon.",
    ],
}

M07 = {
    "file": "07-kontrol-panggung", "short": "Kontrol Panggung", "name": "Kontrol Panggung",
    "kicker": "MODUL 7  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("4CBF56"),
    "lokasi": "Letak: baris tombol tepat di atas panggung",
    "durasi": "Estimasi 10 menit  ·  Jenjang SD kelas 5 - SMP",
    "tagline": "Bendera hijau, Stop, ukuran tampilan, dan layar penuh.",
    "tujuan": [
        "Menjalankan dan menghentikan proyek dengan benar.",
        "Membedakan menjalankan proyek (bendera hijau) dan menjalankan satu script (klik blok).",
        "Mengatur ukuran tampilan panggung sesuai kebutuhan kerja.",
        "Menampilkan proyek dalam mode layar penuh saat presentasi.",
    ],
    "denah": """
    [ bendera ]   [ stop ]                    [ ][ ][ ]   [ layar
      hijau                                  tata letak &   penuh ]
                                            ukuran panggung
""",
    "denah_note": "Ikon tombol tata letak berubah antar pembaruan Scratch — arahkan kursor untuk melihat keterangannya.",
    "details": [
        {"n": "Bendera Hijau", "chip": "Tombol MULAI",
         "fungsi": "Menjalankan SEMUA script yang diawali blok when green flag clicked, di semua sprite.",
         "param": ["Bukan tombol ajaib — hanya memicu script yang punya blok kuning itu",
                   "Bisa memicu banyak script sekaligus (paralelisme)",
                   "Shift + klik = mengaktifkan Turbo Mode"],
         "catatan": "Bila siswa berkata \"tidak terjadi apa-apa\", periksa dulu: apakah scriptnya "
                    "sudah diawali blok when green flag clicked?"},
        {"n": "Tombol Stop", "chip": "Segi delapan merah",
         "fungsi": "Menghentikan seluruh script yang sedang berjalan, sama seperti blok stop (all).",
         "contoh": "Kapan dipakai:\n\nproyek \"kesurupan\"\nkarena forever\n\nkucing berputar\ntanpa henti\n\n-> tekan STOP",
         "catatan": "Ajarkan sebagai TOMBOL DARURAT. Biasakan menekannya setelah menguji proyek "
                    "yang memakai forever."},
        {"n": "Tombol tata letak & ukuran panggung", "chip": "Hanya mengubah TAMPILAN",
         "fungsi": "Mengatur seberapa besar panggung ditampilkan di editor.",
         "param": ["Panggung kecil — area kode melebar, dipakai saat banyak menyusun blok",
                   "Panggung normal / besar — dipakai saat menguji tampilan permainan",
                   "Fokus panggung — panggung dominan, area kode dipersempit"],
         "catatan": "Yang berubah HANYA ukuran tampilan di editor. Ukuran panggung sesungguhnya tetap "
                    "480x360 piksel dan koordinat sprite tidak berubah sama sekali.", "warn": True},
        {"n": "Layar Penuh (Full Screen)", "chip": "Mode presentasi",
         "fungsi": "Panggung memenuhi seluruh layar; palet dan area kode disembunyikan.",
         "param": ["Presentasi karya di depan kelas",
                   "Menguji permainan seperti pemain sungguhan",
                   "Pameran / gelar karya"],
         "catatan": "Keluar dari mode ini dengan menekan tombol Esc atau mengklik ikon keluar. "
                    "Ajarkan ini agar siswa tidak panik."},
    ],
    "praktik": [
        "Susun: when green flag clicked > forever > move (5) steps + if on edge, bounce. Jalankan.",
        "Tekan Stop untuk menghentikan. Diskusikan mengapa forever perlu tombol stop.",
        "Hapus blok when green flag clicked, lalu klik bendera hijau lagi. Diskusi: mengapa diam?",
        "Coba tiap tombol ukuran panggung, amati area kode melebar / menyempit.",
        "Masuk layar penuh, jalankan, lalu tekan Esc.",
    ],
    "praktik_note": "Alokasi 6 menit.",
    "analogi": [
        "Bendera hijau adalah peluit wasit.",
        "Semua pemain yang sudah bersiap langsung bergerak;",
        "pemain yang tidak mendengar peluit tetap diam saja.",
        "Tombol stop adalah peluit panjang tanda pertandingan usai.",
    ],
    "mistakes": [
        ["Bendera hijau ditekan, script tanpa hat block", "\"Tidak terjadi apa-apa\"", "Setiap script diawali blok kuning"],
        ["Turbo Mode aktif karena Shift terpencet", "Proyek berjalan super cepat", "Cek menu Edit, matikan Turbo Mode"],
        ["Mengira mengecilkan panggung mengecilkan sprite", "Salah paham koordinat", "Hanya tampilan yang berubah"],
        ["Tidak tahu cara keluar layar penuh", "Siswa panik", "Ajarkan tombol Esc"],
        ["Lupa tombol stop saat memakai forever", "Komputer terasa lambat", "Biasakan menekan stop setelah menguji"],
    ],
    "quiz": [
        "Kamu klik bendera hijau tapi tidak terjadi apa pun. Sebutkan penyebab paling mungkin.",
        "Apa yang terjadi bila kamu menekan Shift + klik bendera hijau?",
        "Apakah mengecilkan tampilan panggung mengubah nilai koordinat sprite?",
        "Bagaimana cara keluar dari mode layar penuh?",
    ],
    "answers": [
        "Script belum diawali blok when green flag clicked (tidak ada hat block Events).",
        "Turbo Mode aktif — proyek berjalan jauh lebih cepat.",
        "Tidak. Panggung tetap 480x360 dan koordinat tidak berubah; hanya ukuran tampilannya di editor.",
        "Tekan tombol Esc atau klik ikon keluar layar penuh.",
    ],
    "takeaways": [
        "Bendera hijau hanya memicu script yang punya blok when green flag clicked.",
        "Tombol Stop adalah tombol darurat — wajib dipakai saat menguji forever.",
        "Mengubah ukuran tampilan panggung TIDAK mengubah koordinat sprite.",
    ],
}

M08 = {
    "file": "08-panel-info-sprite", "short": "Info Sprite", "name": "Panel Info Sprite",
    "kicker": "MODUL 8  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("CF63CF"),
    "lokasi": "Letak: kotak putih tepat di bawah panggung",
    "durasi": "Estimasi 20 menit  ·  Jenjang SD kelas 5 - SMP",
    "tagline": "Kartu identitas sprite — semua angkanya hidup dan bisa diubah langsung.",
    "tujuan": [
        "Menyebutkan arti keenam properti sprite.",
        "Mengubah properti langsung dari panel dan mengamati akibatnya di panggung.",
        "Menjelaskan hubungan antara panel ini dengan blok yang setara.",
        "Memakai panel ini sebagai alat debugging.",
    ],
    "denah": """
   +--------------------------------------------------------------+
   |  Sprite [ Sprite1 ]      x [ 0 ]        y [ 0 ]               |
   |  Show   [eye] [eye/]     Size [ 100 ]   Direction [ 90 ]      |
   +--------------------------------------------------------------+
""",
    "denah_note": "Setiap properti di panel ini punya BLOK yang setara. Panel = atur dengan tangan, blok = atur lewat program.",
    "details": [
        {"n": "Nama Sprite", "chip": "Properti 1 dari 6",
         "fungsi": "Klik dan ketik untuk mengganti nama sprite.",
         "contoh": "Ganti:\n  Sprite1 -> Kucing\n  Sprite2 -> Bola\n  Sprite3 -> Musuh\n\nNama ini muncul di\ndropdown blok lain:\n  touching (Bola)?\n  create clone of\n    (Peluru)",
         "catatan": "Proyek dengan nama Sprite1, Sprite2, Sprite3 mustahil dipahami saat sudah besar. "
                    "Jadikan mengganti nama sebagai aturan kelas."},
        {"n": "Koordinat x dan y", "chip": "Properti 2 & 3",
         "fungsi": "Menunjukkan sekaligus mengatur posisi sprite. Ketik angka, sprite langsung pindah.",
         "param": ["x: -240 sampai 240 (mendatar)", "y: -180 sampai 180 (tegak)",
                   "Blok setara: set x to (), set y to (), (x position), (y position)"],
         "catatan": "Angkanya BERUBAH SENDIRI saat sprite digerakkan program atau diseret mouse — "
                    "inilah cara termudah mengajarkan koordinat."},
        {"n": "Show (tampil / sembunyi)", "chip": "Properti 4",
         "fungsi": "Menentukan sprite terlihat atau tersembunyi. Blok setara: show dan hide.",
         "contoh": "Script reset wajib:\n\nwhen green flag\n  clicked\nshow\ngo to x:(0) y:(0)\nset size to (100)%\npoint in direction\n  (90)",
         "catatan": "Sprite yang disembunyikan TETAP ADA dan kodenya tetap berjalan — hanya tidak "
                    "terlihat. Jebakan klasik: siswa memakai hide lalu sprite \"hilang\" di sesi berikutnya."},
        {"n": "Size (ukuran)", "chip": "Properti 5 — dalam persen",
         "fungsi": "Mengatur ukuran sprite dalam persen dari ukuran kostum aslinya.",
         "param": ["100 = ukuran asli", "50 = setengah ukuran", "200 = dua kali ukuran",
                   "Blok setara: set size to ()%, change size by (), (size)"],
         "catatan": "Batas maksimal bergantung ukuran kostum. Bila sprite tiba-tiba tak terlihat, "
                    "periksa apakah nilai Size-nya 0."},
        {"n": "Direction (arah hadap)", "chip": "Properti 6 — dalam derajat",
         "fungsi": "Mengatur arah hadap sprite. Klik kolomnya untuk memunculkan piringan pemutar.",
         "param": ["90 = kanan (bawaan)", "0 = atas", "180 = bawah", "-90 = kiri"],
         "catatan": "Di bawah piringan pemutar ada 3 pilihan GAYA ROTASI — inilah kunci menjawab "
                    "keluhan \"kucingnya jalan terbalik!\""},
    ],
    "tables": [{
        "judul": "Tiga Gaya Rotasi (Rotation Style)",
        "headers": ["Gaya rotasi", "Perilaku", "Cocok untuk"],
        "rows": [
            ["All Around", "Sprite ikut berputar penuh mengikuti arah", "Roket, jarum jam, panah"],
            ["Left / Right", "Hanya menghadap kiri atau kanan, tidak pernah terbalik", "TOKOH BERJALAN (paling sering dipakai)"],
            ["Do not rotate", "Tampilan tidak pernah berubah walau arah berubah", "Ikon, tombol, latar bergerak"],
        ],
        "widths": [20, 45, 35], "size": 13,
    }],
    "praktik": [
        "Seret kucing di panggung. Amati kolom x dan y berubah. Lalu ketik x = -200, y = 100.",
        "Ubah Size menjadi 50, lalu 200, lalu kembali 100.",
        "Ubah Direction menjadi -90. Amati kucing terbalik (jungkir).",
        "Klik Direction > pilih gaya rotasi Left/Right > amati kucing menghadap kiri dengan benar.",
        "Sembunyikan sprite lewat tombol mata, lalu tampilkan lagi. Diskusikan pentingnya script reset.",
    ],
    "praktik_note": "Alokasi 12 menit. Latihan 3-4 adalah inti materi gaya rotasi.",
    "analogi": [
        "Panel ini adalah KTP sprite:",
        "nama, alamat (x, y), tinggi badan (size), arah hadap (direction),",
        "dan status \"sedang terlihat atau bersembunyi\".",
    ],
    "mistakes": [
        ["Membiarkan nama Sprite1, Sprite2", "Proyek sulit dibaca", "Wajib ganti nama sejak awal"],
        ["Sprite jungkir balik saat bergerak", "Tampilan aneh", "Ubah gaya rotasi ke Left/Right"],
        ["Sprite \"hilang\" karena pernah hide", "Siswa mengira terhapus", "Buat script reset di awal"],
        ["Mengira ubahan di panel tersimpan sebagai program", "Posisi berbeda saat dijalankan ulang", "Panel = sementara, blok = permanen"],
        ["Size diketik 0", "Sprite tak terlihat", "Cek nilai Size bila sprite menghilang"],
    ],
    "quiz": [
        "Nilai Direction berapa yang membuat sprite menghadap ke atas?",
        "Sprite kamu berjalan terbalik saat ke kiri. Apa solusinya?",
        "Apa beda mengetik x = 100 di panel dengan memakai blok set x to (100)?",
        "Sprite tidak terlihat di panggung. Sebutkan tiga kemungkinan penyebabnya.",
    ],
    "answers": [
        "0 derajat.",
        "Ubah gaya rotasi menjadi Left/Right, lewat panel Direction atau blok set rotation style.",
        "Panel = perubahan manual sekali saja; blok = perintah tersimpan dalam program dan berulang tiap dijalankan.",
        "Status Show sedang sembunyi / pernah kena hide; Size terlalu kecil (mis. 0); posisi di luar pandang atau tertutup sprite lain; efek Ghost 100.",
    ],
    "takeaways": [
        "Setiap properti di panel punya blok yang setara — panel manual, blok otomatis.",
        "Gaya rotasi Left/Right menjawab keluhan \"kucingnya jalan terbalik\".",
        "Sprite yang di-hide tetap menjalankan kodenya, hanya tidak terlihat.",
    ],
}

M09 = {
    "file": "09-daftar-sprite", "short": "Daftar Sprite", "name": "Daftar Sprite & Tombol Tambah",
    "kicker": "MODUL 9  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("FF6680"),
    "lokasi": "Letak: area di bawah Panel Info Sprite, berisi kartu bergambar",
    "durasi": "Estimasi 15 menit  ·  Jenjang SD kelas 5 - SMP",
    "tagline": "Daftar pemain dalam proyek — hanya satu yang bisa diarahkan pada satu waktu.",
    "tujuan": [
        "Berpindah antar sprite dan memahami akibatnya pada area kode.",
        "Menambah sprite dengan empat cara yang tersedia.",
        "Menduplikasi, mengekspor, dan menghapus sprite.",
    ],
    "denah": """
   +---------------------------------+
   |   +----------+                  |
   |   | [kucing] |  <- ikon hapus   |
   |   |  Sprite1 |  <- kartu ini    |
   |   +----------+     BERSOROT     |
   |                    = aktif      |
   |                                 |
   |                    ( tambah + ) |
   +---------------------------------+
""",
    "denah_note": "Aturan wajib sebelum menyusun blok: \"Lihat dulu — sprite mana yang bersorot ungu?\"",
    "details": [
        {"n": "Kartu Sprite", "chip": "Satu kartu = satu pemain",
         "fungsi": "Mewakili satu sprite; kartu yang bersorot ungu adalah sprite yang sedang aktif.",
         "param": ["Gambar kostum — pratinjau tampilan sprite",
                   "Nama di bawah gambar",
                   "Sorotan ungu — menandai sprite aktif",
                   "Ikon tempat sampah — muncul saat kartu aktif, untuk menghapus"],
         "catatan": "Melewatkan pengecekan sorotan ungu adalah PENYEBAB NOMOR SATU kebingungan siswa "
                    "di kelas Scratch. Jadikan kebiasaan refleks.", "warn": True},
        {"n": "Klik kanan pada kartu sprite", "chip": "Menu penghemat waktu",
         "fungsi": "Menyalin, mengekspor, atau menghapus sprite.",
         "param": ["duplicate — menyalin sprite BESERTA seluruh kode, kostum, dan suaranya",
                   "export — menyimpan sebagai berkas .sprite3 untuk proyek lain",
                   "delete — menghapus sprite"],
         "catatan": "duplicate adalah penghemat waktu terbesar di kelas: buat satu musuh lengkap "
                    "dengan kodenya, duplikat 4 kali, jadilah 5 musuh dalam 10 detik."},
        {"n": "Tombol Tambah Sprite", "chip": "Arahkan kursor, muncul 4 pilihan",
         "fungsi": "Menambahkan sprite baru ke proyek dengan empat cara berbeda.",
         "contoh": "Choose a Sprite\n  -> pustaka Scratch\n     (cara utama)\n\nPaint\n  -> gambar sendiri\n\nSurprise\n  -> acak\n\nUpload Sprite\n  -> dari komputer",
         "catatan": "Pustaka sprite bisa disaring per kategori (Animals, People, Fantasy, Sports, "
                    "Food) dan dicari lewat kolom pencarian."},
        {"n": "Menghapus & menyusun urutan", "chip": "Perapian daftar",
         "fungsi": "Menghapus sprite lewat ikon tempat sampah, dan menyeret kartu untuk mengurutkan.",
         "param": ["Salah hapus? Edit > Restore (hanya yang TERAKHIR dihapus)",
                   "Menyeret kartu hanya mengatur urutan di DAFTAR",
                   "Untuk mengatur siapa di depan/belakang DI PANGGUNG, pakai blok go to [front] layer"],
         "catatan": "Bedakan dua hal ini dengan jelas: urutan di daftar sprite tidak sama dengan "
                    "urutan lapisan di panggung."},
    ],
    "praktik": [
        "Tambah sprite kedua lewat Choose a Sprite (mis. Bear).",
        "Ganti nama: Sprite1 > Kucing, sprite baru > Beruang.",
        "Di Kucing susun: when green flag clicked > say [Halo Beruang!] for (2) seconds.",
        "Di Beruang susun: when green flag clicked > wait (2) seconds > say [Halo Kucing!] for (2) seconds.",
        "Jalankan. Diskusi: mengapa Beruang perlu blok wait? Lalu coba duplicate dan Surprise.",
    ],
    "praktik_note": "Alokasi 10 menit. Latihan ini sekaligus memperkenalkan konsep sinkronisasi.",
    "analogi": [
        "Daftar Sprite adalah daftar pemain dalam sebuah drama.",
        "Sutradara (kamu) hanya bisa memberi arahan pada satu pemain dalam satu waktu —",
        "yaitu pemain yang sedang kamu tunjuk (bersorot ungu).",
        "Kalau salah menunjuk, arahanmu masuk ke pemain yang keliru.",
    ],
    "mistakes": [
        ["Menyusun kode di sprite yang salah", "Sprite target tidak bereaksi", "Cek sorotan ungu — jadikan kebiasaan refleks"],
        ["Menyalin blok satu-satu ke sprite lain", "Boros waktu", "Ajarkan duplicate dan Backpack"],
        ["Menghapus sprite tanpa sengaja", "Kerja hilang", "Ajarkan Edit > Restore"],
        ["Membiarkan nama Sprite1 / Sprite2", "Dropdown blok membingungkan", "Wajib ganti nama"],
        ["Menambah puluhan sprite lewat Surprise", "Proyek berat & berantakan", "Batasi 3-4 sprite di awal"],
    ],
    "quiz": [
        "Bagaimana cara mengetahui sprite mana yang sedang aktif?",
        "Sebutkan empat cara menambah sprite.",
        "Apa yang ikut tersalin saat kamu memakai duplicate pada sebuah sprite?",
        "Kamu ingin memakai sprite buatanmu di proyek lain, tanpa internet. Fitur apa yang dipakai?",
    ],
    "answers": [
        "Kartunya bersorot / berlatar ungu di daftar sprite.",
        "Choose a Sprite (pustaka), Paint (gambar sendiri), Surprise (acak), Upload Sprite (dari komputer).",
        "Seluruh kode/script, semua kostum, dan semua suaranya.",
        "Klik kanan sprite > export menjadi berkas .sprite3, lalu di proyek lain gunakan Upload Sprite.",
    ],
    "takeaways": [
        "Selalu cek sprite mana yang bersorot ungu SEBELUM menyusun blok.",
        "duplicate menyalin sprite beserta seluruh kode, kostum, dan suaranya.",
        "Urutan kartu di daftar berbeda dari urutan lapisan di panggung.",
    ],
}

M10 = {
    "file": "10-panel-stage-backdrop", "short": "Panel Stage", "name": "Panel Stage & Backdrop",
    "kicker": "MODUL 10  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("FFAB19"),
    "lokasi": "Letak: kolom sempit di kanan Daftar Sprite",
    "durasi": "Estimasi 10 menit  ·  Jenjang SD kelas 5 - SMP",
    "tagline": "Panggung sebagai objek yang bisa dipilih dan diberi kode.",
    "tujuan": [
        "Membedakan Stage dari sprite.",
        "Menambah dan mengganti backdrop.",
        "Menjelaskan beda backdrop dan costume.",
        "Memberi kode pada Stage dan tahu batasannya.",
    ],
    "denah": """
   +----------------+
   |     Stage      |
   |  +----------+  |
   |  |  (putih) |  |  <- pratinjau backdrop
   |  +----------+  |
   |   Backdrops    |
   |       1        |  <- jumlah backdrop
   |                |
   |   ( tambah + ) |  <- tombol tambah backdrop
   +----------------+
""",
    "denah_note": "Klik panel ini, maka tab Code, Backdrops, dan Sounds menampilkan milik STAGE, bukan sprite.",
    "details": [
        {"n": "Backdrop vs Costume", "chip": "Beda yang sering tertukar",
         "fungsi": "Backdrop adalah latar milik Stage; costume adalah tampilan milik sprite.",
         "contoh": "BACKDROP\n  milik Stage\n  ukuran ideal\n  480 x 360 px\n  switch backdrop to\n\nCOSTUME\n  milik Sprite\n  ukuran bebas\n  switch costume to",
         "catatan": "Keduanya sama-sama wajib minimal satu. Proyek baru selalu punya 1 backdrop "
                    "putih polos, terlihat dari angka \"Backdrops: 1\"."},
        {"n": "Tombol Tambah Backdrop", "chip": "Empat pilihan, sama seperti sprite",
         "fungsi": "Menambahkan latar baru ke panggung.",
         "param": ["Choose a Backdrop — pustaka (Outdoors, Indoors, Space, Sports, Underwater, Music)",
                   "Paint — gambar latar sendiri",
                   "Surprise — latar acak",
                   "Upload Backdrop — unggah gambar dari komputer"],
         "catatan": "Perhatikan: tombol tambah SPRITE dan tombol tambah BACKDROP letaknya berdekatan "
                    "tetapi berbeda. Salah tombol membuat latar menjadi sprite yang bisa bergerak.", "warn": True},
        {"n": "Kode pada Stage", "chip": "Boleh, tetapi terbatas",
         "fungsi": "Stage boleh punya script, dengan sejumlah batasan.",
         "param": ["BISA: ganti backdrop, mainkan suara & musik latar, efek grafis",
                   "BISA: ask ... and wait, variabel, broadcast",
                   "TIDAK BISA: blok Motion, say / think, diklon, ganti lapisan, ganti nama"],
         "catatan": "Praktik terbaik: taruh script \"pengatur permainan\" di Stage — musik latar, "
                    "pergantian level, reset skor. Stage mengurus dunia, sprite mengurus dirinya sendiri."},
        {"n": "Backdrop sebagai penanda level", "chip": "Teknik membuat permainan berlevel",
         "fungsi": "Blok when backdrop switches to () membuat sprite bereaksi otomatis saat latar berganti.",
         "contoh": "[di Stage]\nwhen green flag\n  clicked\nswitch backdrop to\n  (Level1)\n\n[di Sprite Musuh]\nwhen backdrop\n  switches to (Level2)\ngo to x:(200) y:(0)\nshow",
         "catatan": "Cara termudah membuat permainan berlevel atau cerita berbabak tanpa perlu "
                    "mengatur banyak broadcast."},
    ],
    "praktik": [
        "Klik panel Stage > amati tab berubah menjadi Backdrops.",
        "Klik Choose a Backdrop > pilih Blue Sky. Amati angka Backdrops menjadi 2.",
        "Tambahkan satu backdrop lagi, mis. Underwater.",
        "Pilih Stage, susun: when green flag clicked > forever > next backdrop + wait (1) seconds.",
        "Diskusi: buka tab Code saat Stage dipilih, klik kategori Motion. Mengapa kosong?",
    ],
    "praktik_note": "Alokasi 7 menit.",
    "analogi": [
        "Kalau sprite adalah aktor,",
        "maka Stage adalah panggung dan layar latarnya.",
        "Layar latar bisa diganti (hutan, laut, luar angkasa),",
        "tapi panggungnya sendiri tidak pernah ikut berjalan ke mana-mana.",
    ],
    "mistakes": [
        ["Menambah backdrop lewat tombol SPRITE", "Latar jadi sprite yang bisa bergerak", "Tunjukkan dua tombol berbeda"],
        ["Mencari blok Motion di Stage", "Palet kosong, siswa bingung", "Stage tidak bisa bergerak"],
        ["Backdrop tidak berukuran 480x360", "Gambar terpotong atau ada bagian kosong", "Pakai pustaka, atau sesuaikan di Paint Editor"],
        ["Menyusun kode di Stage padahal untuk sprite", "Kode tidak berjalan sesuai harapan", "Cek panel mana yang bersorot"],
        ["Mengunggah foto besar sebagai backdrop", "Proyek berat (batas 10 MB per aset)", "Kecilkan gambar sebelum diunggah"],
    ],
    "quiz": [
        "Apa beda backdrop dan costume?",
        "Berapa ukuran ideal gambar backdrop?",
        "Sebutkan dua hal yang bisa dilakukan Stage dan dua hal yang tidak bisa.",
        "Blok apa yang membuat sprite bereaksi otomatis saat latar berganti?",
    ],
    "answers": [
        "Backdrop = latar belakang milik Stage; costume = tampilan milik sprite.",
        "480 x 360 piksel.",
        "Bisa: ganti backdrop, mainkan suara, efek grafis, ask and wait, variabel, broadcast. Tidak bisa: bergerak, say/think, diklon, ganti lapisan, ganti nama.",
        "when backdrop switches to () di kategori Events.",
    ],
    "takeaways": [
        "Backdrop milik Stage; costume milik Sprite. Ukuran ideal backdrop 480 x 360.",
        "Stage boleh punya kode, tapi tidak bisa bergerak dan tidak bisa bicara.",
        "when backdrop switches to () adalah cara termudah membuat permainan berlevel.",
    ],
}

M11 = {
    "file": "11-backpack", "short": "Backpack", "name": "Backpack (Tas Ransel)",
    "kicker": "MODUL 11  ·  KOMPONEN EDITOR SCRATCH", "color": rgb("575E75"),
    "lokasi": "Letak: bilah abu-abu paling bawah editor",
    "durasi": "Estimasi 10 menit  ·  Jenjang SD kelas 6 - SMP (lanjutan)",
    "tagline": "Tas penyimpanan pribadi yang bisa dibawa antar proyek.",
    "tujuan": [
        "Menjelaskan fungsi Backpack sebagai tempat penyimpanan lintas proyek.",
        "Memasukkan script/sprite/kostum/suara ke Backpack dan memakainya di proyek lain.",
        "Menyebutkan syarat pemakaian Backpack.",
    ],
    "denah": """
   +=======================================================+
   |                     Backpack   ^                      |   <- klik untuk membuka
   +=======================================================+
""",
    "denah_note": "Isi Backpack tetap ada meski proyek ditutup, proyek lain dibuka, bahkan berganti komputer.",
    "details": [
        {"n": "Apa yang bisa disimpan", "chip": "Empat jenis benda",
         "fungsi": "Menyimpan bagian proyek yang berguna agar bisa dipakai ulang.",
         "param": ["Script — mis. mesin lompat (platformer engine), kode kontrol panah",
                   "Sprite — tokoh buatan sendiri lengkap dengan kode & kostumnya",
                   "Costume — gambar hasil karya sendiri",
                   "Sound — rekaman suara sendiri"],
         "catatan": "Mengambil item dari Backpack berarti MENYALINNYA — item tetap tersimpan dan "
                    "bisa dipakai berkali-kali di banyak proyek."},
        {"n": "Cara pakai", "chip": "Tarik masuk, tarik keluar",
         "fungsi": "Menyimpan dan mengambil kembali isi Backpack dengan cara menyeret.",
         "contoh": "MENYIMPAN\n  tarik script/sprite\n  KE DALAM bilah\n  Backpack\n\nMENGAMBIL\n  tarik item KELUAR\n  ke area kode atau\n  daftar sprite\n\nMENGHAPUS\n  klik kanan item\n  > delete",
         "catatan": "Perlihatkan langsung di depan kelas — konsepnya jauh lebih mudah dipahami "
                    "lewat demonstrasi daripada penjelasan lisan."},
        {"n": "Syarat & batasan", "chip": "Penting untuk sekolah",
         "fungsi": "Backpack tidak selalu tersedia — cek dulu kondisi lab sekolah.",
         "param": ["HARUS LOGIN — Backpack terikat pada akun Scratch",
                   "HANYA di editor online — tidak tersedia di Scratch Desktop (offline)",
                   "Privat — Backpack orang lain tidak bisa diakses",
                   "Kapasitas tidak dibatasi resmi, tetapi bila terlalu penuh muncul \"Error loading backpack\""],
         "catatan": "Bila lab memakai Scratch offline atau siswa tidak punya akun, Backpack TIDAK "
                    "BISA DIPAKAI. Siapkan alternatifnya sebelum mengajar.", "warn": True},
        {"n": "Alternatif tanpa Backpack", "chip": "Untuk lab offline / tanpa akun",
         "fungsi": "Tiga cara memindahkan kode dan aset tanpa Backpack.",
         "param": ["Sprite antar proyek — klik kanan sprite > export (.sprite3), lalu Upload Sprite",
                   "Kode antar sprite dalam satu proyek — TARIK TUMPUKAN BLOK ke kartu sprite tujuan",
                   "Kode antar proyek — buka dua proyek di dua tab, atau simpan sprite .sprite3"],
         "catatan": "Trik \"tarik blok ke kartu sprite lain\" sangat berguna dan sering tidak "
                    "diketahui: blok tersalin ke sprite tujuan, blok asli tetap di tempatnya."},
    ],
    "tables": [{
        "judul": "Nilai Pendidikan: Backpack Mengajarkan Code Reuse",
        "headers": ["Konsep di Scratch", "Padanan di dunia profesional"],
        "rows": [
            ["Menyimpan script ke Backpack", "Membuat library / module"],
            ["Mengambil dari Backpack", "Import library"],
            ["Export sprite .sprite3", "Membagikan package"],
        ],
        "widths": [45, 55], "size": 14,
    }],
    "praktik": [
        "Susun script kontrol panah: forever + if <key (right arrow) pressed?> then change x by (10).",
        "Buka bilah Backpack, tarik seluruh script ke dalamnya.",
        "Buat proyek baru (File > New).",
        "Buka Backpack, tarik script tadi keluar ke area kode. Jalankan — langsung bekerja.",
        "Diskusi: berapa waktu yang dihemat kalau kode ini dipakai di 5 proyek berbeda?",
    ],
    "praktik_note": "Alokasi 7 menit. Bila lab offline, ganti dengan latihan export .sprite3.",
    "analogi": [
        "Backpack adalah tas ransel yang selalu kamu bawa.",
        "Kalau kamu membuat alat yang berguna di satu proyek, masukkan ke tas —",
        "di proyek berikutnya tinggal keluarkan, tak perlu membuat ulang dari nol.",
        "Isi tas tidak berkurang saat dipakai; kamu selalu mengambil salinannya.",
    ],
    "mistakes": [
        ["Mencari Backpack di Scratch offline", "Bingung karena tidak ada", "Jelaskan syarat online + login"],
        ["Mengira item hilang setelah ditarik keluar", "Ragu memakai", "Yang keluar adalah SALINAN"],
        ["Menyimpan puluhan item sembarangan", "Error loading backpack", "Bersihkan berkala"],
        ["Memakai Backpack untuk mengumpulkan tugas", "Guru tidak bisa melihat", "Pengumpulan lewat Share / studio kelas / berkas .sb3"],
    ],
    "quiz": [
        "Sebutkan empat jenis benda yang bisa disimpan di Backpack.",
        "Apakah Backpack tersedia di Scratch Desktop (offline)? Jelaskan.",
        "Kamu menarik satu script keluar dari Backpack. Apakah script itu hilang dari Backpack?",
        "Tanpa Backpack, bagaimana cara memindahkan sprite lengkap ke proyek lain?",
    ],
    "answers": [
        "Script, sprite, costume (kostum), dan sound (suara).",
        "Tidak. Backpack hanya tersedia di editor online dan mengharuskan pengguna login, karena isinya tersimpan di akun Scratch.",
        "Tidak hilang — yang keluar adalah salinannya, item aslinya tetap tersimpan.",
        "Klik kanan sprite > export menjadi berkas .sprite3, lalu di proyek tujuan gunakan Upload Sprite.",
    ],
    "takeaways": [
        "Backpack = penggunaan ulang kode, cikal bakal konsep library dan import.",
        "Hanya tersedia online dan harus login — siapkan alternatif untuk lab offline.",
        "Yang ditarik keluar adalah salinan; isi Backpack tidak berkurang.",
    ],
}

MODULES = [M01, M02, M03, M04, M05, M06, M07, M08, M09, M10, M11]

IDX = {
    "file": "00-index-peta-editor", "short": "Index", "name": "Index Komponen Editor",
    "color": rgb("855CD6"),
    "denah": """
  +===================================================================================+
  | (1) MENU BAR                                                                      |
  | [Logo] Settings | File | Edit | [Untitled-2] | See Project Page | Tutorials | ...  |
  +===================================================================================+
  | (2) TAB          |                          | (7) KONTROL PANGGUNG                |
  | [Code][Costumes] |                          |  bendera hijau  stop   [ukuran]     |
  | [Sounds]         |                          +-------------------------------------+
  +--------+---------+                          |                                     |
  | (3)    | (4)     |   (5) AREA KODE          |   (6) PANGGUNG (STAGE)              |
  | KATEGO-| PALET   |       (Scripts Area)     |       480 x 360 piksel              |
  | RI BLOK| BLOK    |                          |                                     |
  | Motion | move 10 |   <- tempat merangkai    |          [ kucing ]                 |
  | Looks  | turn 15 |      blok                |                                     |
  | Sound  | go to   |                          +------------------+------------------+
  | Events | ...     |                          | (8) INFO SPRITE  | (10) PANEL STAGE |
  | Control|         |                          | Sprite  x  y     |    Backdrops     |
  | Sensing|         |                          | Show Size Direct.|        1         |
  | Operat.|         |                    (+)(-)+------------------+                  |
  | Variab.|         |               (zoom kode)| (9) DAFTAR SPRITE|   [tambah +]     |
  | MyBlock|         |                          |   [ Sprite1 ]    |                  |
  | (+)Ekst|         |                          |      [tambah +]  |                  |
  +========+=========+==========================+==================+==================+
  | (11) BACKPACK                                                                     |
  +===================================================================================+
""",
    "tujuan": [
        "Jangan diajarkan berurutan nomor 1-11 sekaligus — nomor itu urutan TATA LETAK LAYAR, bukan urutan mengajar.",
        "Pertemuan 1: Panggung > Daftar Sprite > Kategori > Palet > Area Kode > Bendera Hijau.",
        "Pertemuan 2: Info Sprite > Tab Costumes/Sounds > Backdrop.",
        "Pertemuan 3: Menu Bar > Backpack.",
        "Setiap modul berstruktur sama: Tujuan > Penjelasan > Rincian > Praktik > Analogi > Kesalahan Umum > Cek Pemahaman.",
    ],
    "catatan": "Alasan urutan ini: siswa sudah bisa membuat kucing bergerak di menit ke-15 pertemuan pertama.",
    "tables": [
        {"judul": "Urutan Mengajar yang Disarankan",
         "headers": ["Pertemuan", "Modul", "Alasan"],
         "rows": [
             ["1", "(6) Panggung > (9) Daftar Sprite > (3) Kategori > (4) Palet > (5) Area Kode > (7) Bendera Hijau",
              "Siswa langsung melihat hasil"],
             ["2", "(8) Info Sprite > (2) Tab Costumes/Sounds > (10) Backdrop", "Mempercantik & menganimasikan"],
             ["3", "(1) Menu Bar > (11) Backpack", "Menyimpan, berbagi, mengelola"],
         ],
         "widths": [12, 58, 30], "size": 11},
        {"judul": "Kosakata Inti untuk Ditempel di Dinding Kelas",
         "headers": ["Istilah", "Arti sederhana"],
         "rows": [
             ["Sprite", "Tokoh / objek yang bisa diperintah"],
             ["Stage / Panggung", "Layar tempat sprite tampil"],
             ["Backdrop", "Latar belakang panggung"],
             ["Costume / Kostum", "Tampilan alternatif sprite"],
             ["Blok", "Satu potong perintah"],
             ["Script", "Rangkaian blok yang tersambung"],
             ["Palet", "Rak tempat semua blok tersedia"],
             ["Area Kode", "Meja kerja tempat blok dirangkai"],
             ["Bendera Hijau", "Tombol mulai"],
         ],
         "widths": [30, 70], "size": 13},
        {"judul": "Catatan Versi Editor",
         "headers": ["Elemen", "Keterangan", "Status"],
         "rows": [
             ["Menu Settings", "Menggantikan ikon globe bahasa pada versi lama", "Belum ada di Scratch Wiki — cek langsung"],
             ["Tombol Debug", "Debugging Help — menampilkan tips mencari kesalahan", "Ditambahkan 16 Desember 2024"],
             ["Scratch Desktop", "Versi offline: tanpa Backpack dan tanpa cloud variable", "Dua elemen di atas bisa berbeda"],
         ],
         "widths": [20, 45, 35], "size": 11},
    ],
    "takeaways": [
        "Ajarkan dari yang paling terlihat hasilnya oleh siswa, bukan dari kiri ke kanan layar.",
        "Tiga pertemuan cukup untuk seluruh 11 komponen antarmuka.",
        "Tempelkan kosakata inti di dinding kelas sejak pertemuan pertama.",
    ],
}


if __name__ == "__main__":
    for d in MODULES:
        p = build(d)
        print(f"OK  {p.name:34s} {len(d['details']):2d} slide bagian")
    p = build_index(IDX, MODULES)
    print(f"OK  {p.name}")
