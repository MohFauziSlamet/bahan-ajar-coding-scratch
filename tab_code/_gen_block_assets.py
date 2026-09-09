#!/usr/bin/env python3
"""Render tiap blok Scratch 3.0 jadi PNG transparan, satu berkas per blok.

Mesin render: scratchblocks 3.7.1 (MIT) — pustaka resmi yang dipakai Scratch
Wiki & forum Scratch, di-vendor di ./vendor/scratchblocks/. Sintaksnya sama
dengan yang dipakai di Scratch Wiki, mis. "move (10) steps".

Nomor berkas WAJIB sama dengan urutan blok pada daftar "blocks" kategori
terkait di _generate_pptx.py — nomor itulah yang dipakai untuk mencocokkan
gambar ke slide. Nomor boleh bolong bila sebuah slide tidak punya blok nyata
(mis. "Make a Variable" yang berupa tombol, bukan blok).

    python3 _gen_block_assets.py motion      # satu kategori
    python3 _gen_block_assets.py all         # semua
"""
import json
import re
import subprocess
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TMP = ROOT / ".build_assets"
SB = ROOT / "vendor" / "scratchblocks" / "build" / "scratchblocks.min.js"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SCALE = 1          # skala scratchblocks
DSF = 3            # device scale factor Chrome -> PNG 3x
GAP = 10           # jarak antar blok bila satu gambar berisi >1 blok


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def page(entries):
    """entries: [(id, [snippet, ...]), ...] -> HTML lengkap."""
    body = []
    for eid, snips in entries:
        pres = "".join(
            f'<pre class="b" style="margin:0 0 {GAP if i < len(snips)-1 else 0}px">'
            f"{esc(s)}</pre>"
            for i, s in enumerate(snips))
        body.append(f'<div class="wrap" id="{eid}" '
                    f'style="display:inline-block">{pres}</div>')
    return f"""<meta charset="utf-8">
<style>html,body{{margin:0;padding:0;background:none}}
.wrap{{display:block}}</style>
<div id="root">{"".join(body)}</div><pre id="o"></pre>
<script src="file://{SB}"></script>
<script>
scratchblocks.renderMatching("pre.b", {{style:"scratch3", scale:{SCALE}}});
const r={{}};
for (const w of document.querySelectorAll(".wrap")) {{
  const b=w.getBoundingClientRect();
  r[w.id]=[Math.ceil(b.width), Math.ceil(b.height)];
}}
document.getElementById("o").textContent=JSON.stringify(r);
</script>"""


def chrome(args, timeout=120):
    return subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                           "--hide-scrollbars", "--allow-file-access-from-files",
                           "--virtual-time-budget=5000"] + args,
                          capture_output=True, text=True, timeout=timeout)


def sizes(entries):
    """Ukur lebar/tinggi tiap blok dalam satu kali jalan Chrome."""
    TMP.mkdir(exist_ok=True)
    p = TMP / "measure.html"
    p.write_text(page(entries), encoding="utf-8")
    dom = chrome(["--dump-dom", f"file://{p}"]).stdout
    m = re.search(r'<pre id="o">(.*?)</pre>', dom, re.S)
    if not m:
        raise RuntimeError("gagal mengukur lewat Chrome:\n" + dom[-800:])
    return json.loads(unescape(m.group(1)))


def render(cat, spec, outdir):
    entries = [(f"b{i}", s if isinstance(s, list) else [s])
               for i, (_, s) in enumerate(spec)]
    dim = sizes(entries)
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("*.png"):
        old.unlink()

    made = []
    for i, ((name, snips), (eid, snip_list)) in enumerate(zip(spec, entries)):
        w, h = dim[eid]
        p = TMP / f"{name}.html"
        p.write_text(page([(eid, snip_list)]), encoding="utf-8")
        png = outdir / f"{name}.png"
        chrome(["--default-background-color=00000000",
                f"--force-device-scale-factor={DSF}",
                f"--window-size={w},{h}",
                f"--screenshot={png}", f"file://{p}"])
        if not png.exists():
            raise RuntimeError(f"gagal render {name}")
        made.append((name, png))
    return made


# =================================================================== DATA
# Sintaks scratchblocks. Kunci angka = urutan blok di _generate_pptx.py.

MOTION = [
    ("01-move-steps",                    "move (10) steps"),
    ("02-turn-kanan-degrees",            "turn cw (15) degrees"),
    ("03-turn-kiri-degrees",             "turn ccw (15) degrees"),
    ("04-go-to-random-position",         "go to (random position v)"),
    ("05-go-to-x-y",                     "go to x: (0) y: (0)"),
    ("06-glide-secs-to-random-position", "glide (1) secs to (random position v)"),
    ("07-glide-secs-to-x-y",             "glide (1) secs to x: (0) y: (0)"),
    ("08-point-in-direction",            "point in direction (90 v)"),
    ("09-point-towards",                 "point towards (mouse-pointer v)"),
    ("10-change-x-by",                   "change x by (10)"),
    ("11-set-x-to",                      "set x to (0)"),
    ("12-change-y-by",                   "change y by (10)"),
    ("13-set-y-to",                      "set y to (0)"),
    ("14-if-on-edge-bounce",             "if on edge, bounce"),
    ("15-set-rotation-style",            "set rotation style [left-right v]"),
    ("16-x-position",                    "(x position)"),
    ("17-y-position",                    "(y position)"),
    ("18-direction",                     "(direction)"),
]

LOOKS = [
    ("01-say-for-seconds",            "say [Hello!] for (2) seconds"),
    ("02-say",                        "say [Hello!]"),
    ("03-think-for-seconds",          "think [Hmm...] for (2) seconds"),
    ("04-think",                      "think [Hmm...]"),
    ("05-switch-costume-to",          "switch costume to (costume2 v)"),
    ("06-next-costume",               "next costume"),
    ("07-costume-number",             "(costume [number v])"),
    ("08-switch-backdrop-to",         "switch backdrop to (Blue Sky v)"),
    ("09-switch-backdrop-to-and-wait", "switch backdrop to (Blue Sky v) and wait"),
    ("10-next-backdrop",              "next backdrop"),
    ("11-backdrop-number",            "(backdrop [number v])"),
    ("12-change-size-by",             "change size by (10)"),
    ("13-set-size-to-persen",         "set size to (100) %"),
    ("14-size",                       "(size)"),
    ("15-show",                       "show"),
    ("16-hide",                       "hide"),
    ("17-go-to-front-layer",          "go to [front v] layer"),
    ("18-go-forward-layers",          "go [forward v] (1) layers"),
    ("19-change-color-effect-by",     "change [color v] effect by (25)"),
    ("20-set-color-effect-to",        "set [color v] effect to (0)"),
    ("21-clear-graphic-effects",      "clear graphic effects"),
]

SOUND = [
    ("01-play-sound-until-done", "play sound (Meow v) until done"),
    ("02-start-sound",           "start sound (Meow v)"),
    ("03-stop-all-sounds",       "stop all sounds"),
    ("04-change-pitch-effect",   "change [pitch v] effect by (10)"),
    ("05-set-pitch-effect",      "set [pitch v] effect to (100)"),
    ("06-clear-sound-effects",   "clear sound effects"),
    ("07-change-volume-by",      "change volume by (-10)"),
    ("08-set-volume-to",         "set volume to (100) %"),
    ("09-volume",                "(volume)"),
]

EVENTS = [
    ("01-when-green-flag-clicked",  "when green flag clicked"),
    ("02-when-key-pressed",         "when [space v] key pressed"),
    ("03-when-this-sprite-clicked", "when this sprite clicked"),
    ("04-when-stage-clicked",       "when stage clicked"),
    ("05-when-backdrop-switches",   "when backdrop switches to [Level2 v]"),
    ("06-when-loudness-greater",    "when [loudness v] > (10)"),
    ("07-when-i-receive",           "when I receive [mulai v]"),
    ("08-broadcast",                "broadcast [mulai v]"),
    ("09-broadcast-and-wait",       "broadcast [mulai v] and wait"),
]

CONTROL = [
    ("01-wait-seconds",        "wait (1) seconds"),
    ("02-wait-until",          "wait until <>"),
    ("03-repeat",              "repeat (10)\nend"),
    ("04-forever",             "forever\nend"),
    ("05-repeat-until",        "repeat until <>\nend"),
    ("06-if-then",             "if <> then\nend"),
    ("07-if-then-else",        "if <> then\nelse\nend"),
    ("08-stop-all",            "stop [all v]"),
    ("09-create-clone-of",     "create clone of (myself v)"),
    ("10-when-i-start-as-a-clone", "when I start as a clone"),
    ("11-delete-this-clone",   "delete this clone"),
]

SENSING = [
    ("01-touching",            "<touching (mouse-pointer v)?>"),
    ("02-touching-color",      "<touching color [#ff4d4d]?>"),
    ("03-color-is-touching",   "<color [#ff4d4d] is touching [#4d79ff]?>"),
    ("04-distance-to",         "(distance to (mouse-pointer v))"),
    ("05-ask-and-wait",        "ask [Siapa namamu?] and wait"),
    ("06-answer",              "(answer)"),
    ("07-key-pressed",         "<key (space v) pressed?>"),
    ("08-mouse-down",          "<mouse down?>"),
    ("09-mouse-x",             "(mouse x)"),
    ("10-mouse-y",             "(mouse y)"),
    ("11-set-drag-mode",       "set drag mode [draggable v]"),
    ("12-loudness",            "(loudness)"),
    ("13-timer",               "(timer)"),
    ("14-reset-timer",         "reset timer"),
    ("15-current-year",        "(current [year v])"),
    ("16-days-since-2000",     "(days since 2000)"),
    ("17-of-sprite",           "([x position v] of (Sprite1 v))"),
    ("18-username",            "(username)"),
]

OPERATORS = [
    ("01-tambah-kurang",   ["(() + ())", "(() - ())"]),
    ("02-kali-bagi",       ["(() * ())", "(() / ())"]),
    ("03-mod",             "(() mod ())"),
    ("04-round",           "(round ())"),
    ("05-abs-of",          "([abs v] of ())"),
    ("06-pick-random",     "(pick random (1) to (10))"),
    ("07-perbandingan",    ["<() < (50)>", "<() = (50)>", "<() > (50)>"]),
    ("08-and",             "<<> and <>>"),
    ("09-or",              "<<> or <>>"),
    ("10-not",             "<not <>>"),
    ("11-join",            "(join [apple ] [banana])"),
    ("12-letter-of",       "(letter (1) of [apple])"),
    ("13-length-of",       "(length of [apple])"),
    ("14-contains",        "<[apple] contains [a]?>"),
]

VARIABLES = [
    # 01 "Make a Variable" = tombol di palet, bukan blok -> tanpa gambar
    ("02-variabel-reporter",   "(skor)"),
    ("03-set-to",              "set [skor v] to (0)"),
    ("04-change-by",           "change [skor v] by (1)"),
    ("05-show-variable",       "show variable [skor v]"),
    ("06-hide-variable",       "hide variable [skor v]"),
    ("07-list-reporter",       "(daftar :: list)"),
    ("08-add-to",              "add [thing] to [daftar v]"),
    ("09-delete-of",           "delete (1) of [daftar v]"),
    ("10-delete-all-of",       "delete all of [daftar v]"),
    ("11-insert-at",           "insert [thing] at (1) of [daftar v]"),
    ("12-replace-item",        "replace item (1) of [daftar v] with [x]"),
    ("13-item-of",             "(item (1) of [daftar v])"),
    ("14-item-number-of",      "(item # of [thing] in [daftar v])"),
    ("15-length-of-list",      "(length of [daftar v])"),
    ("16-list-contains",       "<[daftar v] contains [thing]?>"),
    ("17-show-hide-list",      ["show list [daftar v]", "hide list [daftar v]"]),
]

MY_BLOCKS = [
    # 01, 06, 08, 09 = penjelasan konsep / opsi dialog -> tanpa gambar
    ("02-define",          ["define (lompat)", "lompat"]),
    ("03-input-angka",     ["define (lompat (tinggi))", "lompat (50)"]),
    ("04-input-boolean",   ["define (cek <kena?>)", "cek <touching (edge v)?>"]),
    ("05-label-teks",      ["define (lompat (tinggi) kali (jumlah))",
                            "lompat (50) kali (3)"]),
    ("07-rekursi",         "define (spiral (sisi))\nif <(sisi) > (5)> then\n"
                           "move (sisi) steps\nturn cw (30) degrees\n"
                           "spiral ((sisi) - (2))\nend"),
]

# Beberapa slide memuat 2-3 blok sekaligus, sedangkan berkas .md membahasnya
# satu per satu. Versi tunggal ini hanya dipakai oleh .md — ditaruh di subfolder
# supaya tidak ikut terjaring pencocokan gambar-ke-slide (yang mencari "NN-*.png").
OPERATORS_TUNGGAL = [
    ("01-tambah",      "(() + ())"),
    ("02-kurang",      "(() - ())"),
    ("03-kali",        "(() * ())"),
    ("04-bagi",        "(() / ())"),
    ("05-kurang-dari", "<() < (50)>"),
    ("06-sama-dengan", "<() = (50)>"),
    ("07-lebih-dari",  "<() > (50)>"),
]

VARIABLES_TUNGGAL = [
    ("01-show-list", "show list [daftar v]"),
    ("02-hide-list", "hide list [daftar v]"),
]

# --------------------------------------------------------------- CONTOH
# Potongan script contoh, dirender sebagai blok puzzle (bukan teks monospace).
# Kunci = nomor blok pada daftar "blocks" kategori terkait di _generate_pptx.py.
# Tiap blok diberi BEBERAPA contoh supaya siswa melihat lebih dari satu pemakaian.
CONTOH = {
 "control": {
  1: [("Kedip berulang",
       "forever\nhide\nwait (0.5) seconds\nshow\nwait (0.5) seconds\nend"),
      ("Dialog bergantian",
       "say [Halo!]\nwait (1) seconds\nsay [Apa kabar?]\nwait (1) seconds"),
      ("Jeda kecil mengatur kecepatan",
       "forever\nchange x by (5)\nwait (0.05) seconds\nend")],
  2: [("Tunggu pemain menekan spasi",
       "say [Tekan spasi untuk mulai]\nwait until <key (space v) pressed?>\n"
       "say [Mulai!] for (1) seconds"),
      ("Tunggu skor cukup",
       "wait until <(skor) > (9)>\nswitch backdrop to (Menang v)"),
      ("Sprite muncul saat permainan mulai",
       "hide\nwait until <(mulai) = (1)>\nshow")],
  3: [("Menggambar persegi",
       "repeat (4)\nmove (100) steps\nturn cw (90) degrees\nend"),
      ("Melompat tiga kali",
       "repeat (3)\nchange y by (50)\nwait (0.2) seconds\n"
       "change y by (-50)\nwait (0.2) seconds\nend"),
      ("Segitiga: 360 dibagi 3",
       "repeat (3)\nmove (100) steps\nturn cw (120) degrees\nend")],
  4: [("Bola memantul tanpa henti",
       "when green flag clicked\nforever\nmove (5) steps\nif on edge, bounce\nend"),
      ("Selalu mengejar mouse",
       "forever\npoint towards (mouse-pointer v)\nmove (3) steps\nend"),
      ("Animasi berjalan",
       "forever\nnext costume\nwait (0.1) seconds\nend")],
  5: [("Jalan sampai kena tepi",
       "repeat until <touching (edge v)?>\nmove (10) steps\nend\nsay [Sampai!]"),
      ("Turun sampai dasar panggung",
       "repeat until <(y position) < (-150)>\nchange y by (-5)\nend"),
      ("Mengejar sampai tertangkap",
       "repeat until <touching (Pemain v)?>\npoint towards (Pemain v)\nmove (3) steps\nend")],
  6: [("Nyawa berkurang saat kena musuh",
       "forever\nif <touching (Musuh v)?> then\nchange [nyawa v] by (-1)\nend\nend"),
      ("Bergerak saat tombol ditekan",
       "forever\nif <key (right arrow v) pressed?> then\nchange x by (10)\nend\nend"),
      ("Dua syarat sekaligus",
       "if <<(skor) > (9)> and <(nyawa) > (0)>> then\nswitch backdrop to (Menang v)\nend")],
  7: [("Kuis benar atau salah",
       "ask [Berapa 5 + 3?] and wait\nif <(answer) = (8)> then\nsay [Benar!]\n"
       "else\nsay [Salah]\nend"),
      ("Lanjut atau berhenti",
       "if <(nyawa) > (0)> then\nsay [Lanjut]\nelse\nstop [all v]\nend"),
      ("Menghadap kiri atau kanan",
       "if <(direction) > (0)> then\nswitch costume to (kanan v)\nelse\nswitch costume to (kiri v)\nend")],
  8: [("Game over saat nyawa habis",
       "if <(nyawa) = (0)> then\nsay [Game Over] for (2) seconds\nstop [all v]\nend"),
      ("Hentikan script lain saja",
       "when I receive [selesai v]\nstop [other scripts in sprite v]"),
      ("Menghentikan script ini saja",
       "repeat until <(waktu) = (0)>\nchange [waktu v] by (-1)\nwait (1) seconds\nend\nstop [this script v]")],
  9: [("Menghujani klon tiap setengah detik",
       "when green flag clicked\nhide\nforever\ncreate clone of (myself v)\n"
       "wait (0.5) seconds\nend"),
      ("Menembakkan sprite lain",
       "when [space v] key pressed\ncreate clone of (Peluru v)"),
      ("Membatasi jumlah klon",
       "if <(jumlah klon) < (20)> then\ncreate clone of (myself v)\nchange [jumlah klon v] by (1)\nend")],
  10: [("Tetesan hujan jatuh",
        "when I start as a clone\ngo to x: (pick random (-240) to (240)) y: (180)\n"
        "show\nrepeat until <(y position) < (-170)>\nchange y by (-5)\nend\n"
        "delete this clone"),
       ("Peluru terbang lalu lenyap",
        "when I start as a clone\nshow\nrepeat (30)\nchange y by (10)\nend\n"
        "delete this clone"),
       ("Tiap klon punya kecepatan sendiri",
       "when I start as a clone\nset [laju v] to (pick random (2) to (6))\nrepeat until <touching (edge v)?>\nchange x by (laju)\nend")],
  11: [("Lenyap setelah mengenai musuh",
        "when I start as a clone\nwait until <touching (Musuh v)?>\ndelete this clone"),
       ("Lenyap setelah dua detik",
        "when I start as a clone\nshow\nwait (2) seconds\ndelete this clone"),
       ("Lenyap setelah keluar panggung",
       "when I start as a clone\nrepeat until <(y position) > (170)>\nchange y by (10)\nend\ndelete this clone")],
 },
 "motion": {
  1: [("Jalan saat panah kanan ditekan",
       "when green flag clicked\nforever\nif <key (right arrow v) pressed?> then\n"
       "move (10) steps\nend\nend"),
      ("Mundur pakai angka negatif", "move (-10) steps"),
      ("Menggambar persegi",
       "repeat (4)\nmove (100) steps\nturn cw (90) degrees\nend")],
  2: [("Berputar satu lingkaran penuh", "repeat (36)\nturn cw (10) degrees\nend"),
      ("Jarum jam berdetak",
       "forever\nturn cw (6) degrees\nwait (1) seconds\nend"),
      ("Belok acak saat kena tepi",
       "if <touching (edge v)?> then\nturn cw (pick random (90) to (270)) degrees\nend")],
  3: [("Segitiga ke arah kiri",
       "repeat (3)\nmove (100) steps\nturn ccw (120) degrees\nend"),
      ("Menengok lalu kembali",
       "turn ccw (90) degrees\nwait (1) seconds\nturn cw (90) degrees"),
      ("Setir ke kiri", "when [left arrow v] key pressed\nturn ccw (15) degrees")],
  4: [("Muncul di tempat acak terus-menerus",
       "forever\ngo to (random position v)\nwait (1) seconds\nend"),
      ("Pindah ke sprite lain", "go to (Pemain v)"),
      ("Menempel pada mouse", "forever\ngo to (mouse-pointer v)\nend")],
  5: [("Kembali ke tengah saat mulai",
       "when green flag clicked\ngo to x: (0) y: (0)"),
      ("Teleport ke titik acak",
       "when [space v] key pressed\ngo to x: (pick random (-200) to (200)) "
       "y: (pick random (-150) to (150))"),
      ("Garis start di kiri panggung", "go to x: (-200) y: (-100)\nshow")],
  6: [("Melayang halus ke tempat acak",
       "forever\nglide (2) secs to (random position v)\nend"),
      ("Mengejar pemain dengan halus",
       "repeat (10)\nglide (1) secs to (Pemain v)\nend"),
      ("Melayang ke mouse", "glide (0.5) secs to (mouse-pointer v)")],
  7: [("Menyeberang panggung",
       "go to x: (-200) y: (0)\nglide (3) secs to x: (200) y: (0)"),
      ("Bolak-balik tanpa henti",
       "forever\nglide (2) secs to x: (150) y: (0)\n"
       "glide (2) secs to x: (-150) y: (0)\nend"),
      ("Makin cepat tiap putaran",
       "set [laju v] to (3)\nrepeat (3)\nglide (laju) secs to x: (200) y: (0)\n"
       "change [laju v] by (-1)\nglide (laju) secs to x: (-200) y: (0)\nend")],
  8: [("Menghadap kanan sebelum mulai",
       "when green flag clicked\npoint in direction (90)\ngo to x: (0) y: (0)"),
      ("Menghadap ke atas lalu naik", "point in direction (0)\nmove (100) steps"),
      ("Arah acak",
       "point in direction (pick random (-179) to (180))\nmove (50) steps")],
  9: [("Musuh selalu mengejar pemain",
       "forever\npoint towards (Pemain v)\nmove (2) steps\nend"),
      ("Meriam mengikuti mouse", "forever\npoint towards (mouse-pointer v)\nend"),
      ("Menembak ke arah mouse",
       "point towards (mouse-pointer v)\nrepeat (20)\nmove (10) steps\nend")],
  10: [("Kontrol kiri-kanan",
        "forever\nif <key (right arrow v) pressed?> then\nchange x by (10)\nend\n"
        "if <key (left arrow v) pressed?> then\nchange x by (-10)\nend\nend"),
       ("Bergeser terus ke kanan", "forever\nchange x by (3)\nend"),
       ("Kecepatan disimpan di variabel",
        "forever\nchange x by (laju)\nif <touching (edge v)?> then\n"
        "set [laju v] to ((laju) * (-1))\nend\nend")],
  11: [("Lewat kanan, muncul lagi dari kiri",
        "forever\nchange x by (5)\nif <(x position) > (230)> then\n"
        "set x to (-230)\nend\nend"),
       ("Kembali ke garis start",
        "when green flag clicked\nset x to (-200)"),
       ("Menyusun sprite pada satu titik", "set x to (0)\nset y to (100)")],
  12: [("Melompat lalu jatuh",
        "repeat (10)\nchange y by (10)\nend\nrepeat (10)\nchange y by (-10)\nend"),
       ("Gravitasi sederhana",
        "forever\nchange y by (kecepatan)\nchange [kecepatan v] by (-1)\nend"),
       ("Naik saat panah atas",
        "when [up arrow v] key pressed\nchange y by (50)")],
  13: [("Berdiri di lantai", "set y to (-120)"),
       ("Hujan: kembali ke atas",
        "forever\nchange y by (-5)\nif <(y position) < (-170)> then\n"
        "set y to (180)\nend\nend"),
       ("Reset posisi tiap mulai",
        "when green flag clicked\nset x to (0)\nset y to (0)")],
  14: [("Bola memantul tanpa henti",
        "when green flag clicked\nforever\nmove (5) steps\nif on edge, bounce\nend"),
       ("Supaya tidak jungkir balik",
        "set rotation style [left-right v]\nforever\nmove (10) steps\n"
        "if on edge, bounce\nend"),
       ("Ikan berenang acak",
        "forever\nmove (3) steps\nif on edge, bounce\n"
        "turn cw (pick random (-5) to (5)) degrees\nend")],
  15: [("Kiri-kanan: paling sering dipakai",
        "set rotation style [left-right v]\nforever\nmove (10) steps\n"
        "if on edge, bounce\nend"),
       ("Jangan berputar sama sekali",
        "set rotation style [don't rotate v]\npoint towards (mouse-pointer v)\n"
        "move (5) steps"),
       ("Berputar bebas untuk jarum",
        "set rotation style [all around v]\nforever\nturn cw (5) degrees\nend")],
  16: [("Cek sudah sampai tepi kanan",
        "if <(x position) > (200)> then\nsay [Aku di tepi kanan!]\nend"),
       ("Menampilkan posisi mendatar", "forever\nsay (x position)\nend"),
       ("Menyalin posisi ke variabel", "set [posisi v] to (x position)")],
  17: [("Game over kalau jatuh",
        "forever\nif <(y position) < (-170)> then\nsay [Game Over] for (2) seconds\n"
        "stop [all v]\nend\nend"),
       ("Skor mengikuti ketinggian", "set [skor v] to (y position)"),
       ("Turun sampai menyentuh lantai",
        "repeat until <(y position) < (-120)>\nchange y by (-5)\nend")],
  18: [("Menghadap kanan atau kiri",
        "if <(direction) > (0)> then\nswitch costume to (kanan v)\nelse\n"
        "switch costume to (kiri v)\nend"),
       ("Menampilkan arah", "say (join [Arah: ] (direction))"),
       ("Mengingat arah lalu kembali",
        "set [arah awal v] to (direction)\nturn cw (90) degrees\n"
        "wait (1) seconds\npoint in direction (arah awal)")],
 },
 "looks": {
  1: [("Perkenalan berurutan",
       "when green flag clicked\nsay [Halo!] for (2) seconds\n"
       "say [Namaku Kucing] for (2) seconds"),
      ("Menanggapi jawaban kuis",
       "if <(answer) = [8]> then\nsay [Benar!] for (1) seconds\nend"),
      ("Menggabungkan teks dengan angka",
       "say (join [Skormu ] (skor)) for (2) seconds")],
  2: [("Papan skor yang selalu tampak",
       "forever\nsay (join [Skor: ] (skor))\nend"),
      ("Menghapus balon kata", "say [Hai]\nwait (2) seconds\nsay []"),
      ("Balon tetap sambil sprite bergerak",
       "say [Aku jalan...]\nrepeat (20)\nmove (10) steps\nend")],
  3: [("Berpikir sebelum menjawab",
       "think [Hmm...] for (2) seconds\nsay [Aku tahu!] for (2) seconds"),
      ("Ragu saat jawabannya salah",
       "if <not <(answer) = [8]>> then\nthink [Kok beda ya?] for (2) seconds\nend"),
      ("Bergantian berpikir dan bicara",
       "repeat (3)\nthink [...] for (1) seconds\nsay [Ya!] for (1) seconds\nend")],
  4: [("Berpikir tanpa batas waktu",
       "think [Sedang menghitung...]\nwait (3) seconds\nthink []"),
      ("Menampilkan isi variabel", "forever\nthink (nyawa)\nend"),
      ("Berpikir sambil menunggu tombol",
       "think [Menunggu spasi]\nwait until <key (space v) pressed?>\nsay [Mulai!]")],
  5: [("Animasi dua kostum",
       "forever\nswitch costume to (costume1 v)\nwait (0.2) seconds\n"
       "switch costume to (costume2 v)\nwait (0.2) seconds\nend"),
      ("Kostum terluka lalu pulih",
       "if <touching (Musuh v)?> then\nswitch costume to (terluka v)\n"
       "wait (0.5) seconds\nswitch costume to (normal v)\nend"),
      ("Menghadap sesuai tombol",
       "when [right arrow v] key pressed\nswitch costume to (kanan v)\n"
       "change x by (10)")],
  6: [("Berjalan sambil bergerak",
       "forever\nnext costume\nmove (10) steps\nwait (0.1) seconds\nend"),
      ("Ganti kostum saat diklik", "when this sprite clicked\nnext costume"),
      ("Animasi cepat sebentar",
       "repeat (10)\nnext costume\nwait (0.05) seconds\nend")],
  7: [("Bereaksi pada kostum tertentu",
       "if <(costume [name v]) = [terluka]> then\nchange [nyawa v] by (-1)\nend"),
      ("Menampilkan nomor kostum", "say (costume [number v])"),
      ("Berhenti di kostum ketiga",
       "repeat until <(costume [number v]) = (3)>\nnext costume\n"
       "wait (0.1) seconds\nend")],
  8: [("Pindah level saat skor cukup",
       "if <(skor) > (9)> then\nswitch backdrop to (Level2 v)\nend"),
      ("Layar menang", "when I receive [menang v]\nswitch backdrop to (Menang v)"),
      ("Latar awal saat mulai",
       "when green flag clicked\nswitch backdrop to (Mulai v)\ngo to x: (0) y: (0)")],
  9: [("Menunggu skrip latar selesai",
       "switch backdrop to (Level2 v) and wait\nsay [Level 2 siap!]"),
      ("Cerita berurutan rapi",
       "switch backdrop to (Adegan1 v) and wait\n"
       "switch backdrop to (Adegan2 v) and wait"),
      ("Bandingkan: tanpa dan dengan and wait",
       ["switch backdrop to (Level2 v)\nsay [Langsung lanjut]",
        "switch backdrop to (Level2 v) and wait\nsay [Menunggu dulu]"])],
  10: [("Slideshow otomatis",
        "when green flag clicked\nforever\nnext backdrop\nwait (3) seconds\nend"),
       ("Ganti latar saat spasi", "when [space v] key pressed\nnext backdrop"),
       ("Naik level tiap 10 poin",
        "if <(skor) > (9)> then\nnext backdrop\nset [skor v] to (0)\nend")],
  11: [("Kesulitan mengikuti latar",
        "if <(backdrop [name v]) = [Level3]> then\nset [kesulitan v] to (3)\nend"),
       ("Menampilkan nomor latar", "say (backdrop [number v])"),
       ("Berhenti di latar terakhir",
        "repeat until <(backdrop [name v]) = [Tamat]>\nnext backdrop\n"
        "wait (2) seconds\nend")],
  12: [("Membesar lalu mengecil",
        "repeat (10)\nchange size by (5)\nend\nrepeat (10)\nchange size by (-5)\nend"),
       ("Efek denyut tanpa henti",
        "forever\nrepeat (5)\nchange size by (2)\nend\n"
        "repeat (5)\nchange size by (-2)\nend\nend"),
       ("Mengecil saat menjauh",
        "forever\nif <(y position) > (100)> then\nchange size by (-1)\nend\nend")],
  13: [("Ukuran normal saat mulai",
        "when green flag clicked\nset size to (100) %\nshow"),
       ("Sprite kecil untuk peluru",
        "set size to (30) %\ncreate clone of (myself v)"),
       ("Ukuran acak tiap klon",
        "when I start as a clone\nset size to (pick random (50) to (150)) %\nshow")],
  14: [("Batas maksimal membesar",
        "if <(size) < (200)> then\nchange size by (10)\nend"),
       ("Menampilkan ukuran", "say (join [Ukuran: ] (size))"),
       ("Mengecil sampai hilang",
        "repeat until <(size) < (10)>\nchange size by (-5)\nend\nhide")],
  15: [("Muncul saat permainan mulai",
        "when green flag clicked\nshow\ngo to x: (0) y: (0)"),
       ("Sembunyi dulu, muncul saat dipanggil",
        ["when green flag clicked\nhide",
         "when I receive [munculkan v]\nshow"]),
       ("Klon wajib di-show",
        "when I start as a clone\nshow\nglide (1) secs to (random position v)")],
  16: [("Sembunyi saat kena musuh",
        "if <touching (Musuh v)?> then\nhide\nstop [this script v]\nend"),
       ("Sembunyi di awal, muncul kemudian",
        "when green flag clicked\nhide\nwait (3) seconds\nshow"),
       ("Efek kedip",
        "forever\nhide\nwait (0.3) seconds\nshow\nwait (0.3) seconds\nend")],
  17: [("Pemain selalu di depan",
        "when green flag clicked\ngo to [front v] layer"),
       ("Dekorasi di paling belakang", "go to [back v] layer"),
       ("Maju ke depan saat diklik",
        "when this sprite clicked\ngo to [front v] layer\nsay [Aku di depan!]")],
  18: [("Naik satu lapis", "go [forward v] (1) layers"),
       ("Turun tiga lapis", "go [backward v] (3) layers"),
       ("Naik lapis saat bersentuhan",
        "forever\nif <touching (Pemain v)?> then\ngo [forward v] (1) layers\nend\nend")],
  19: [("Warna berubah terus",
        "forever\nchange [color v] effect by (25)\nend"),
       ("Berkedip saat terluka",
        "repeat (5)\nchange [ghost v] effect by (50)\nwait (0.1) seconds\n"
        "change [ghost v] effect by (-50)\nwait (0.1) seconds\nend"),
       ("Muncul perlahan",
        "set [ghost v] effect to (100)\nshow\nrepeat (20)\n"
        "change [ghost v] effect by (-5)\nend")],
  20: [("Warna tetap tiap pemain",
        "when green flag clicked\nset [color v] effect to (75)"),
       ("Transparan setengah", "set [ghost v] effect to (50)"),
       ("Kembali normal",
        "set [color v] effect to (0)\nset [ghost v] effect to (0)")],
  21: [("Bersihkan semua efek saat mulai",
        "when green flag clicked\nclear graphic effects\nshow\nset size to (100) %"),
       ("Setelah animasi menghilang",
        "repeat (20)\nchange [ghost v] effect by (5)\nend\nhide\n"
        "clear graphic effects"),
       ("Satu blok mengganti banyak set",
        ["set [color v] effect to (0)\nset [ghost v] effect to (0)\n"
         "set [brightness v] effect to (0)",
         "clear graphic effects"])],
 },
 "sound": {
  1: [("Dialog berurutan",
       "when green flag clicked\nplay sound [Halo v] until done\n"
       "play sound [ApaKabar v] until done"),
      ("Musik latar berulang",
       "forever\nplay sound [Musik v] until done\nend"),
      ("Suara selesai dulu baru pindah layar",
       "play sound [Tamat v] until done\nswitch backdrop to (Menang v)")],
  2: [("Suara lompat tanpa menunda gerakan",
       "when [space v] key pressed\nstart sound [Pop v]\nchange y by (50)"),
      ("Suara koin saat bersentuhan",
       "if <touching (Koin v)?> then\nstart sound [Koin v]\n"
       "change [skor v] by (1)\nend"),
      ("Beberapa suara bertumpuk",
       "repeat (3)\nstart sound [Tik v]\nwait (0.2) seconds\nend")],
  3: [("Diam saat kalah",
       "when I receive [game over v]\nstop all sounds\n"
       "play sound [Kalah v] until done"),
      ("Tombol senyap", "when [m v] key pressed\nstop all sounds"),
      ("Bersihkan suara lama saat mulai",
       "when green flag clicked\nstop all sounds\n"
       "play sound [Musik v] until done")],
  4: [("Nada makin tinggi tiap koin",
       "repeat (10)\nchange [pitch v] effect by (20)\nstart sound [Koin v]\n"
       "wait (0.2) seconds\nend"),
      ("Suara berat saat terluka",
       "change [pitch v] effect by (-50)\nstart sound [Aduh v]"),
      ("Nada acak",
       "change [pitch v] effect by (pick random (-100) to (100))\n"
       "start sound [Pop v]")],
  5: [("Nada tetap untuk sprite ini",
       "set [pitch v] effect to (200)\nplay sound [Meow v] until done"),
      ("Suara raksasa",
       "set [pitch v] effect to (-300)\nplay sound [Halo v] until done"),
      ("Kembali ke nada asli",
       "set [pitch v] effect to (0)\nplay sound [Meow v] until done")],
  6: [("Bersihkan sebelum suara penting",
       "clear sound effects\nplay sound [Pengumuman v] until done"),
      ("Reset di awal permainan",
       "when green flag clicked\nclear sound effects\nset volume to (100) %"),
      ("Satu blok mengganti dua set",
       ["set [pitch v] effect to (0)\nset [pan left/right v] effect to (0)",
        "clear sound effects"])],
  7: [("Musik memudar lalu berhenti",
       "repeat (10)\nchange volume by (-10)\nwait (0.1) seconds\nend\n"
       "stop all sounds"),
      ("Tombol pengeras suara",
       "when [up arrow v] key pressed\nchange volume by (10)"),
      ("Turun sampai benar-benar diam",
       "repeat until <(volume) = (0)>\nchange volume by (-5)\nend")],
  8: [("Volume standar saat mulai",
       "when green flag clicked\nset volume to (100) %"),
      ("Musik latar lebih pelan dari efek",
       "set volume to (40) %\nforever\nplay sound [Musik v] until done\nend"),
      ("Makin dekat makin keras",
       "forever\nset volume to ((100) - (distance to (Pemain v))) %\nend")],
  9: [("Pelankan selama masih bersuara",
       "if <(volume) > (0)> then\nchange volume by (-10)\nend"),
      ("Menampilkan volume", "say (join [Volume: ] (volume))"),
      ("Tombol senyap-nyala",
       "if <(volume) = (0)> then\nset volume to (100) %\nelse\n"
       "set volume to (0) %\nend")],
 },
 "events": {
  1: [("Script reset wajib",
       "when green flag clicked\ngo to x: (0) y: (0)\npoint in direction (90)\n"
       "show\nset size to (100) %"),
      ("Beberapa script jalan bersamaan",
       ["when green flag clicked\nforever\nmove (5) steps\nif on edge, bounce\nend",
        "when green flag clicked\nforever\nnext costume\nwait (0.2) seconds\nend"]),
      ("Menyiapkan skor dan nyawa",
       "when green flag clicked\nset [skor v] to (0)\nset [nyawa v] to (3)")],
  2: [("Lompat dengan spasi",
       "when [space v] key pressed\nchange y by (50)\nwait (0.3) seconds\n"
       "change y by (-50)"),
      ("Satu script tiap tombol arah",
       ["when [right arrow v] key pressed\nchange x by (10)",
        "when [left arrow v] key pressed\nchange x by (-10)"]),
      ("Tombol huruf untuk senyap",
       "when [m v] key pressed\nstop all sounds")],
  3: [("Tombol mulai",
       "when this sprite clicked\nbroadcast [mulai v]\nhide"),
      ("Menambah skor saat diklik",
       "when this sprite clicked\nstart sound [Pop v]\nchange [skor v] by (1)\n"
       "go to (random position v)"),
      ("Sprite menjelaskan dirinya",
       "when this sprite clicked\nsay [Aku kucing!] for (2) seconds")],
  4: [("Klik di mana saja untuk mulai",
       "when stage clicked\nbroadcast [mulai v]"),
      ("Klik latar untuk menembak",
       "when stage clicked\ncreate clone of (Peluru v)"),
      ("Bandingkan: sprite vs latar yang diklik",
       ["when this sprite clicked\nsay [Sprite yang kena]",
        "when stage clicked\nsay [Latar yang kena]"])],
  5: [("Musuh muncul di level 2",
       "when backdrop switches to [Level2 v]\nshow\ngo to x: (200) y: (0)"),
      ("Musik ganti tiap adegan",
       "when backdrop switches to [Malam v]\nplay sound [Sunyi v] until done"),
      ("Menyiapkan tingkat kesulitan",
       "when backdrop switches to [Level3 v]\nset [kesulitan v] to (3)\n"
       "set [nyawa v] to (5)")],
  6: [("Bertepuk untuk melompat",
       "when [loudness v] > (30)\nchange y by (60)\nwait (0.3) seconds\n"
       "change y by (-60)"),
      ("Suara keras memicu pesan",
       "when [loudness v] > (50)\nbroadcast [teriak v]"),
      ("Timer sebagai pemicu",
       "when [timer v] > (10)\nsay [Waktu habis!] for (2) seconds\nstop [all v]")],
  7: [("Semua sprite bereaksi bersamaan",
       "when I receive [mulai v]\nshow\ngo to x: (0) y: (0)"),
      ("Mengakhiri permainan",
       "when I receive [game over v]\nstop all sounds\nsay [Kalah] for (2) seconds\n"
       "stop [all v]"),
      ("Satu pesan, banyak reaksi",
       ["when I receive [tembak v]\ncreate clone of (myself v)",
        "when I receive [tembak v]\nstart sound [Tembak v]"])],
  8: [("Tombol mengirim pesan",
       "when this sprite clicked\nbroadcast [mulai v]\nhide"),
      ("Kirim saat syarat tercapai",
       "if <(skor) > (9)> then\nbroadcast [menang v]\nend"),
      ("Pengirim langsung lanjut",
       "broadcast [mulai v]\nsay [Aku tidak menunggu] for (2) seconds")],
  9: [("Menunggu semua penerima selesai",
       "broadcast [adegan1 v] and wait\nbroadcast [adegan2 v] and wait\n"
       "say [Tamat] for (2) seconds"),
      ("Cerita berurutan rapi",
       "when green flag clicked\nbroadcast [perkenalan v] and wait\n"
       "broadcast [konflik v] and wait\nbroadcast [selesai v] and wait"),
      ("Bandingkan dengan broadcast biasa",
       ["broadcast [cek v]\nsay [Langsung lanjut]",
        "broadcast [cek v] and wait\nsay [Menunggu dulu]"])],
 },
 "sensing": {
  1: [("Nyawa berkurang saat kena musuh",
       "forever\nif <touching (Musuh v)?> then\nchange [nyawa v] by (-1)\n"
       "wait (1) seconds\nend\nend"),
      ("Berhenti di dinding",
       "repeat until <touching (Dinding v)?>\nmove (5) steps\nend"),
      ("Berbalik saat kena tepi panggung",
       "if <touching (edge v)?> then\nturn cw (180) degrees\nend")],
  2: [("Jatuh sampai menyentuh tanah",
       "repeat until <touching color [#00cc44]?>\nchange y by (-5)\nend"),
      ("Kena lava, permainan berakhir",
       "if <touching color [#ff0000]?> then\nbroadcast [game over v]\nend"),
      ("Robot mengikuti garis hitam",
       "forever\nif <touching color [#000000]?> then\nmove (3) steps\nelse\n"
       "turn cw (15) degrees\nend\nend")],
  3: [("Hanya bagian tertentu sprite yang dicek",
       "if <color [#ff0000] is touching [#0000ff]?> then\nsay [Kena!]\nend"),
      ("Sensor kiri robot",
       "forever\nif <color [#000000] is touching [#ffffff]?> then\n"
       "turn cw (5) degrees\nend\nend"),
      ("Roda menyentuh jalan",
       "wait until <color [#333333] is touching [#999999]?>\n"
       "start sound [Rem v]")],
  4: [("Musuh mengejar bila sudah dekat",
       "forever\nif <(distance to (Pemain v)) < (100)> then\n"
       "point towards (Pemain v)\nmove (3) steps\nend\nend"),
      ("Menampilkan jarak ke mouse",
       "forever\nsay (join [Jarak: ] (distance to (mouse-pointer v)))\nend"),
      ("Suara makin keras bila makin dekat",
       "forever\nset volume to ((100) - (distance to (Pemain v))) %\nend")],
  5: [("Menanyakan nama",
       "ask [Siapa namamu?] and wait\nsay (join [Halo, ] (answer)) for (2) seconds"),
      ("Kuis benar-salah",
       "ask [Berapa 5 + 3?] and wait\nif <(answer) = [8]> then\nsay [Benar!]\n"
       "else\nsay [Salah]\nend"),
      ("Dua pertanyaan, simpan dulu jawabannya",
       "ask [Namamu?] and wait\nset [nama v] to (answer)\n"
       "ask [Umurmu?] and wait\nset [umur v] to (answer)")],
  6: [("Memakai jawaban langsung",
       "ask [Berapa umurmu?] and wait\nsay (join [Umurmu ] (answer)) for (2) seconds"),
      ("Jawaban lama tertimpa — simpan dulu",
       ["ask [A?] and wait\nask [B?] and wait\nsay (answer)",
        "ask [A?] and wait\nset [jawab A v] to (answer)\nask [B?] and wait"]),
      ("Membandingkan jawaban",
       "if <(answer) = [merah]> then\nswitch backdrop to (Merah v)\nend")],
  7: [("Kontrol halus di dalam forever",
       "forever\nif <key (right arrow v) pressed?> then\nchange x by (10)\nend\nend"),
      ("Dua tombol sekaligus",
       "if <<key (up arrow v) pressed?> and <key (right arrow v) pressed?>> then\n"
       "point in direction (45)\nmove (10) steps\nend"),
      ("Menunggu tombol ditekan",
       "say [Tekan spasi]\nwait until <key (space v) pressed?>\n"
       "broadcast [mulai v]")],
  8: [("Menembak selama tombol ditahan",
       "forever\nif <mouse down?> then\ncreate clone of (Peluru v)\n"
       "wait (0.2) seconds\nend\nend"),
      ("Menggambar saat diklik",
       "forever\nif <mouse down?> then\ngo to (mouse-pointer v)\nend\nend"),
      ("Menunggu klik",
       "wait until <mouse down?>\nsay [Kamu klik!] for (1) seconds")],
  9: [("Papan pingpong mengikuti mouse",
       "forever\nset x to (mouse x)\nend"),
      ("Menampilkan koordinat mouse",
       "forever\nsay (join (mouse x) (join [ , ] (mouse y)))\nend"),
      ("Bergerak hanya bila mouse di kanan",
       "if <(mouse x) > (0)> then\nchange x by (5)\nend")],
  10: [("Naik-turun mengikuti mouse",
        "forever\nset y to (mouse y)\nend"),
       ("Peringatan bila mouse terlalu tinggi",
        "if <(mouse y) > (150)> then\nsay [Terlalu tinggi]\nend"),
       ("Mengikuti mouse dengan halus",
        "forever\nchange y by (((mouse y) - (y position)) / (10))\nend")],
  11: [("Boleh digeser pemain",
        "when green flag clicked\nset drag mode [draggable v]"),
       ("Dikunci supaya tidak digeser",
        "set drag mode [not draggable v]"),
       ("Puzzle: geser lalu terkunci",
        "set drag mode [draggable v]\nwait until <touching (Tempat v)?>\n"
        "set drag mode [not draggable v]")],
  12: [("Sprite membesar saat berisik",
        "forever\nset size to ((50) + (loudness)) %\nend"),
       ("Melompat saat bertepuk",
        "forever\nif <(loudness) > (30)> then\nchange y by (50)\nend\nend"),
       ("Menampilkan tingkat suara", "forever\nsay (loudness)\nend")],
  13: [("Batas waktu permainan",
        "wait until <(timer) > (30)>\nsay [Waktu habis!] for (2) seconds\n"
        "stop [all v]"),
       ("Menampilkan waktu berjalan",
        "forever\nsay (join [Waktu: ] (round (timer)))\nend"),
       ("Mencatat lama pemain menyelesaikan",
        "reset timer\nwait until <touching (Finish v)?>\n"
        "say (join [Waktumu ] (timer)) for (3) seconds")],
  14: [("Mulai hitungan dari nol",
        "when green flag clicked\nreset timer\nforever\nsay (round (timer))\nend"),
       ("Ulang hitungan tiap level",
        "when I receive [level baru v]\nreset timer"),
       ("Jeda aman antar tabrakan",
        "if <<touching (Musuh v)?> and <(timer) > (1)>> then\n"
        "change [nyawa v] by (-1)\nreset timer\nend")],
  15: [("Menyapa sesuai jam",
        "if <(current [hour v]) < (12)> then\nsay [Selamat pagi!]\nelse\n"
        "say [Selamat siang!]\nend"),
       ("Menampilkan tanggal",
        "say (join (current [date v]) (join [/] (current [month v])))"),
       ("Jam digital",
        "forever\nsay (join (current [hour v]) (join [:] (current [minute v])))\nend")],
  16: [("Menghitung selisih hari",
        "set [mulai v] to (days since 2000)\nwait until <touching (Finish v)?>\n"
        "say ((days since 2000) - (mulai))"),
       ("Angka berbeda tiap hari",
        "set [kode v] to ((days since 2000) mod (7))"),
       ("Menampilkan angkanya", "say (days since 2000)")],
  17: [("Mengikuti posisi sprite lain",
        "forever\nset x to ([x position v] of (Pemain v))\nend"),
       ("Membaca ukuran sprite lain",
        "if <([size v] of (Musuh v)) > (100)> then\nsay [Musuhnya besar!]\nend"),
       ("Membaca variabel milik panggung",
        "say ([skor v] of (Stage v))")],
  18: [("Menyapa pemain dengan namanya",
        "say (join [Halo, ] (username)) for (2) seconds"),
       ("Papan skor pribadi",
        "add (join (username) (join [ : ] (skor))) to [papan skor v]"),
       ("Kosong bila belum masuk akun",
        "if <(username) = []> then\nsay [Kamu belum login]\nend")],
 },
 "operators": {
  1: [("Menambah skor", "set [skor v] to ((skor) + (10))"),
      ("Mengurangi nyawa", "set [nyawa v] to ((nyawa) - (1))"),
      ("Menghitung sisa waktu", "say (join [Sisa: ] ((60) - (timer)))")],
  2: [("Skor berlipat dua", "set [skor v] to ((skor) * (2))"),
      ("Nilai rata-rata",
       "say ((((nilai1) + (nilai2)) + (nilai3)) / (3))"),
      ("Mendekat setengah jarak tiap langkah",
       "forever\nchange x by (((mouse x) - (x position)) / (2))\nend")],
  3: [("Genap atau ganjil",
       "if <((angka) mod (2)) = (0)> then\nsay [Genap]\nelse\nsay [Ganjil]\nend"),
      ("Bonus tiap kelipatan lima",
       "if <((skor) mod (5)) = (0)> then\nplay sound [Bonus v] until done\nend"),
      ("Sudut tidak pernah lewat 360",
       "set [arah v] to (((arah) + (10)) mod (360))")],
  4: [("Membulatkan timer", "say (round (timer))"),
      ("Membulatkan hasil bagi", "say (round ((skor) / (3)))"),
      ("Membulatkan posisi mouse", "set x to (round (mouse x))")],
  5: [("Jarak selalu positif",
       "say ([abs v] of ((x position) - ([x position v] of (Musuh v))))"),
      ("Akar kuadrat", "say ([sqrt v] of (81))"),
      ("Membulatkan ke bawah", "say ([floor v] of ((skor) / (10)))")],
  6: [("Muncul di tempat acak",
       "go to x: (pick random (-200) to (200)) y: (pick random (-150) to (150))"),
      ("Soal penjumlahan acak",
       "set [a v] to (pick random (1) to (10))\n"
       "set [b v] to (pick random (1) to (10))\n"
       "ask (join (a) (join [ + ] (b))) and wait"),
      ("Peluang 1 dari 5",
       "if <(pick random (1) to (5)) = (1)> then\ncreate clone of (myself v)\nend")],
  7: [("Menang bila skor cukup",
       "if <(skor) > (99)> then\nswitch backdrop to (Menang v)\nend"),
      ("Kalah bila nyawa habis",
       "if <(nyawa) < (1)> then\nstop [all v]\nend"),
      ("Tidak ada tanda lebih-dari-sama-dengan",
       ["if <(skor) > (9)> then\nsay [Skor 10 ke atas]\nend",
        "if <not <(skor) < (10)>> then\nsay [Cara lain, sama hasilnya]\nend"])],
  8: [("Dua syarat harus benar dua-duanya",
       "if <<(skor) > (9)> and <(nyawa) > (0)>> then\n"
       "switch backdrop to (Menang v)\nend"),
      ("Dua tombol ditekan bersamaan",
       "if <<key (up arrow v) pressed?> and <key (right arrow v) pressed?>> then\n"
       "point in direction (45)\nend"),
      ("Rentang angka",
       "if <<(nilai) > (69)> and <(nilai) < (86)>> then\nsay [Nilai B]\nend")],
  9: [("Salah satu tombol boleh",
       "if <<key (space v) pressed?> or <mouse down?>> then\n"
       "create clone of (Peluru v)\nend"),
      ("Kena musuh mana pun",
       "if <<touching (Musuh1 v)?> or <touching (Musuh2 v)?>> then\n"
       "change [nyawa v] by (-1)\nend"),
      ("Selesai kalau menang ATAU kalah",
       "wait until <<(skor) > (99)> or <(nyawa) = (0)>>\nstop [all v]")],
  10: [("Jalan selama tidak kena dinding",
        "forever\nif <not <touching (Dinding v)?>> then\nmove (5) steps\nend\nend"),
       ("Bukan jawaban yang benar",
        "if <not <(answer) = [8]>> then\nsay [Salah]\nend"),
       ("Membuat 'minimal 10'",
        "if <not <(skor) < (10)>> then\nsay [Skor minimal 10]\nend")],
  11: [("Menyapa dengan nama",
        "say (join [Halo, ] (answer)) for (2) seconds"),
       ("Papan skor", "forever\nsay (join [Skor: ] (skor))\nend"),
       ("Menggabung tiga bagian",
        "say (join (nama) (join [ punya ] (skor)))")],
  12: [("Huruf pertama jawaban", "say (letter (1) of (answer))"),
       ("Mengeja satu per satu",
        "set [i v] to (1)\nrepeat (length of (kata))\n"
        "say (letter (i) of (kata)) for (0.3) seconds\nchange [i v] by (1)\nend"),
       ("Cek huruf awal",
        "if <(letter (1) of (answer)) = [a]> then\nsay [Mulai huruf A]\nend")],
  13: [("Panjang jawaban", "say (length of (answer))"),
       ("Menolak nama terlalu pendek",
        "if <(length of (answer)) < (3)> then\nsay [Namanya terlalu pendek]\nend"),
       ("Mengulang sebanyak jumlah huruf",
        "repeat (length of (kata))\nnext costume\nwait (0.2) seconds\nend")],
  14: [("Cek kata kunci di jawaban",
        "if <(answer) contains [merah]?> then\nsay [Betul, ada merah!]\nend"),
       ("Menyaring kata terlarang",
        "if <(answer) contains [x]?> then\nsay [Tidak boleh]\nend"),
       ("Beda dengan sama dengan",
        ["if <(answer) = [merah]> then\nsay [Harus persis]\nend",
         "if <(answer) contains [merah]?> then\nsay [Cukup mengandung]\nend"])],
 },
 "variables": {
  1: [("Setelah dibuat, langsung disiapkan nilainya",
       "when green flag clicked\nset [skor v] to (0)\nset [nyawa v] to (3)"),
      ("Beri nama yang jelas",
       ["set [s v] to (0)", "set [skor pemain v] to (0)"]),
      ("Satu variabel dipakai di banyak tempat",
       "change [skor v] by (1)\nsay (join [Skor: ] (skor))")],
  2: [("Menampilkan isinya",
       "say (join [Skor: ] (skor)) for (2) seconds"),
      ("Dipakai sebagai angka", "move (kecepatan) steps"),
      ("Dibandingkan dengan angka lain",
       "if <(nyawa) < (1)> then\nstop [all v]\nend")],
  3: [("Reset di awal permainan",
       "when green flag clicked\nset [skor v] to (0)"),
      ("Menyimpan jawaban pemain",
       "ask [Namamu?] and wait\nset [nama v] to (answer)"),
      ("Menyimpan hasil hitungan",
       "set [sisa v] to ((60) - (timer))")],
  4: [("Skor bertambah saat kena koin",
       "if <touching (Koin v)?> then\nchange [skor v] by (1)\nend"),
      ("Nyawa berkurang", "change [nyawa v] by (-1)"),
      ("Gravitasi",
       "forever\nchange y by (kecepatan)\nchange [kecepatan v] by (-1)\nend")],
  5: [("Menampilkan skor di panggung",
       "when green flag clicked\nset [skor v] to (0)\nshow variable [skor v]"),
      ("Tampil hanya selama bermain",
       ["when I receive [mulai v]\nshow variable [waktu v]",
        "when I receive [selesai v]\nhide variable [waktu v]"]),
      ("Variabel bantu sebaiknya disembunyikan",
       "show variable [skor v]\nhide variable [i v]")],
  6: [("Rapikan layar saat permainan selesai",
       "when I receive [game over v]\nhide variable [skor v]"),
      ("Sembunyi sejak awal",
       "when green flag clicked\nhide variable [kecepatan v]"),
      ("Sembunyikan yang bukan untuk pemain",
       "show variable [skor v]\nhide variable [i v]")],
  7: [("Menampilkan seluruh isi daftar", "say (daftar)"),
      ("Dipakai untuk menghitung isinya", "say (length of [daftar v])"),
      ("Mengisi daftar dari nol",
       "delete all of [daftar v]\nadd [merah] to [daftar v]\n"
       "add [biru] to [daftar v]")],
  8: [("Menyimpan banyak nama",
       "ask [Namamu?] and wait\nadd (answer) to [pemain v]"),
      ("Bank soal",
       "add [Ibu kota Indonesia?] to [soal v]\nadd [Warna langit?] to [soal v]"),
      ("Mencatat skor tiap ronde", "add (skor) to [riwayat v]")],
  9: [("Menghapus soal yang sudah dipakai",
       "set [n v] to (pick random (1) to (length of [soal v]))\n"
       "say (item (n) of [soal v])\ndelete (n) of [soal v]"),
      ("Menghapus yang paling depan", "delete (1) of [antrean v]"),
      ("Menghapus yang paling belakang",
       "delete (length of [daftar v]) of [daftar v]")],
  10: [("Kosongkan dulu sebelum diisi ulang",
        "when green flag clicked\ndelete all of [soal v]\n"
        "add [Soal 1] to [soal v]"),
       ("Reset papan skor",
        "when I receive [main lagi v]\ndelete all of [riwayat v]"),
       ("Beda dengan menghapus satu",
        ["delete (1) of [daftar v]", "delete all of [daftar v]"])],
  11: [("Menyisipkan di urutan paling depan",
        "insert [penting] at (1) of [antrean v]"),
       ("Menyisipkan di tengah", "insert [baru] at (3) of [daftar v]"),
       ("Beda dengan add",
        ["add [x] to [daftar v]", "insert [x] at (1) of [daftar v]"])],
  12: [("Memperbarui skor tertinggi",
        "replace item (1) of [rekor v] with (skor)"),
       ("Mengganti isi yang salah",
        "replace item (2) of [daftar v] with [benar]"),
       ("Menaikkan nilai yang sudah ada",
        "replace item (i) of [nilai v] with ((item (i) of [nilai v]) + (10))")],
  13: [("Mengambil soal acak",
        "say (item (pick random (1) to (length of [soal v])) of [soal v])"),
       ("Membaca isi satu per satu",
        "set [i v] to (1)\nrepeat (length of [daftar v])\n"
        "say (item (i) of [daftar v]) for (1) seconds\nchange [i v] by (1)\nend"),
       ("Mengambil yang paling akhir",
        "say (item (length of [daftar v]) of [daftar v])")],
  14: [("Mencari letak sebuah isi",
        "say (item # of [merah] in [warna v])"),
       ("Cek ada atau tidak",
        "if <(item # of (answer) in [jawaban v]) > (0)> then\n"
        "say [Ada di daftar]\nend"),
       ("Menghapus berdasarkan isinya",
        "delete (item # of [merah] in [warna v]) of [warna v]")],
  15: [("Menghitung jumlah isi",
        "say (join [Ada ] (length of [daftar v]))"),
       ("Mengulang sebanyak isinya",
        "repeat (length of [daftar v])\nnext costume\nend"),
       ("Cek daftar sudah kosong",
        "if <(length of [soal v]) = (0)> then\nsay [Soal habis]\nend")],
  16: [("Cek jawaban ada di daftar",
        "if <[jawaban v] contains (answer)?> then\nsay [Benar!]\nend"),
       ("Mencegah nama ganda",
        "if <not <[pemain v] contains (answer)?>> then\n"
        "add (answer) to [pemain v]\nend"),
       ("Cek barang sudah terkumpul",
        "if <[barang v] contains [kunci]?> then\nbroadcast [buka pintu v]\nend")],
  17: [("Menampilkan daftar di panggung",
        "show list [papan skor v]"),
       ("Sembunyikan selama bermain",
        "when I receive [mulai v]\nhide list [papan skor v]"),
       ("Tampil di akhir permainan",
        "when I receive [selesai v]\nadd (skor) to [papan skor v]\n"
        "show list [papan skor v]")],
 },
 "my_blocks": {
  1: [("Tanpa My Blocks: berulang-ulang",
       "move (100) steps\nturn cw (90) degrees\nmove (100) steps\n"
       "turn cw (90) degrees\nmove (100) steps\nturn cw (90) degrees\n"
       "move (100) steps\nturn cw (90) degrees"),
      ("Dengan My Blocks: rapi",
       ["define persegi\nrepeat (4)\nmove (100) steps\nturn cw (90) degrees\nend",
        "persegi"]),
      ("Sekali diperbaiki, semua pemakaian ikut berubah",
       ["define reset\ngo to x: (0) y: (0)\npoint in direction (90)\nshow",
        "when green flag clicked\nreset"])],
  2: [("Membuat blok baru",
       ["define sapa\nsay [Halo!] for (2) seconds",
        "when green flag clicked\nsapa"]),
      ("Blok tanpa input",
       "define reset\nset [skor v] to (0)\nset [nyawa v] to (3)\n"
       "go to x: (0) y: (0)"),
      ("Dipanggil berkali-kali",
       ["define lompat\nrepeat (10)\nchange y by (10)\nend\n"
        "repeat (10)\nchange y by (-10)\nend",
        "repeat (3)\nlompat\nend"])],
  3: [("Satu input angka",
       ["define lompat (tinggi)\nrepeat (10)\nchange y by (tinggi)\nend",
        "lompat (5)"]),
      ("Dua input sekaligus",
       ["define segi (sisi) (panjang)\nrepeat (sisi)\nmove (panjang) steps\n"
        "turn cw ((360) / (sisi)) degrees\nend",
        "segi (5) (80)"]),
      ("Input berupa teks",
       ["define sapa (nama)\nsay (join [Halo, ] (nama)) for (2) seconds",
        "sapa [Budi]"])],
  4: [("Menyalakan atau mematikan suara",
       ["define gerak (langkah) <pakai suara>\nif <pakai suara> then\n"
        "start sound [Pop v]\nend\nmove (langkah) steps",
        "gerak (10) <>"]),
      ("Pilihan di dalam blok",
       "define gambar <isi>\nif <isi> then\nsay [Diisi warna]\nelse\n"
       "say [Hanya garis]\nend"),
      ("Memanggil dengan syarat langsung",
       "gerak (10) <key (space v) pressed?>")],
  5: [("Label membuat blok terbaca seperti kalimat",
       "define lompat (tinggi) kali (jumlah)\nrepeat (jumlah)\n"
       "change y by (tinggi)\nend"),
      ("Tanpa label vs dengan label",
       ["define lompat (tinggi) (jumlah)",
        "define lompat (tinggi) kali (jumlah)"]),
      ("Label boleh di depan input",
       "define gambar persegi sisi (panjang)\nrepeat (4)\n"
       "move (panjang) steps\nturn cw (90) degrees\nend")],
  6: [("Gambar langsung jadi, tidak terlihat digambar",
       "define gambar cepat\nrepeat (360)\nmove (1) steps\n"
       "turn cw (1) degrees\nend"),
      ("Perhitungan berat jadi seketika",
       "define hitung\nset [i v] to (1)\nrepeat (1000)\nchange [i v] by (1)\nend"),
      ("JANGAN dipakai untuk animasi — gerakannya hilang",
       "define animasi\nrepeat (10)\nnext costume\nwait (0.1) seconds\nend")],
  7: [("Spiral memanggil dirinya sendiri",
       "define spiral (sisi)\nif <(sisi) > (5)> then\nmove (sisi) steps\n"
       "turn cw (30) degrees\nspiral ((sisi) - (2))\nend"),
      ("Hitung mundur",
       "define mundur (n)\nif <(n) > (0)> then\nsay (n) for (0.5) seconds\n"
       "mundur ((n) - (1))\nend"),
      ("Wajib ada penghenti — kiri macet, kanan aman",
       ["define ulang (n)\nsay (n)\nulang ((n) - (1))",
        "define ulang (n)\nif <(n) > (0)> then\nsay (n)\n"
        "ulang ((n) - (1))\nend"])],
  8: [("Tidak bisa mengembalikan nilai — titip di variabel",
       ["define hitung luas (p) (l)\nset [luas v] to ((p) * (l))",
        "hitung luas (5) (3)\nsay (luas)"]),
      ("Hasilnya dibaca setelah blok selesai",
       "hitung luas (4) (6)\nsay (join [Luasnya ] (luas))"),
      ("Tanpa refresh, wait di dalamnya tidak terasa",
       "define kedip\nrepeat (5)\nhide\nwait (0.2) seconds\nshow\n"
       "wait (0.2) seconds\nend")],
  9: [("Blok hanya ada di sprite tempat ia dibuat",
       "define reset\ngo to x: (0) y: (0)\npoint in direction (90)"),
      ("Pakai broadcast untuk menyuruh sprite lain",
       ["broadcast [reset semua v]",
        "when I receive [reset semua v]\nreset"]),
      ("Menyalin sprite ikut membawa My Blocks-nya",
       ["define reset\nshow\nset size to (100) %",
        "when green flag clicked\nreset"])],
 },
}


def render_contoh(cat):
    """Render potongan contoh + tulis index.json berisi judul tiap potongan."""
    spec = CONTOH[cat]
    flat, judul = [], {}
    for idx, items in sorted(spec.items()):
        for j, (cap, src) in enumerate(items):
            name = f"{idx:02d}-{chr(97+j)}"
            flat.append((name, src))
            judul[name + ".png"] = cap
    out = ROOT / "assets" / "contoh" / cat
    made = render(cat, flat, out)
    (out / "index.json").write_text(json.dumps(judul, ensure_ascii=False, indent=1),
                                    encoding="utf-8")
    return made


POLA = {
 "control": [
  ("01-mesin-permainan",
   "when green flag clicked\nforever\n"
   "if <key (right arrow v) pressed?> then\nchange x by (10)\nend\n"
   "if <touching (Musuh v)?> then\nbroadcast [game over v]\nend\nend"),
  ("02-peluru-dengan-klon",
   ["when I receive [tembak v]\ncreate clone of (myself v)",
    "when I start as a clone\ngo to (Pemain v)\nshow\n"
    "repeat until <touching (edge v)?>\nchange y by (10)\nend\ndelete this clone"]),
  ("03-percabangan-bertingkat",
   "if <(nilai) > (85)> then\nsay [A]\nelse\n"
   "if <(nilai) > (70)> then\nsay [B]\nelse\nsay [C]\nend\nend"),
 ],
 "motion": [
  ("01-script-reset",
   "when green flag clicked\ngo to x: (0) y: (0)\npoint in direction (90)\n"
   "set rotation style [left-right v]\nshow\nset size to (100) %"),
  ("02-kontrol-tombol-panah",
   "when green flag clicked\nforever\n"
   "if <key (right arrow v) pressed?> then\nchange x by (10)\nend\n"
   "if <key (left arrow v) pressed?> then\nchange x by (-10)\nend\nend"),
  ("03-bola-memantul",
   "when green flag clicked\nset rotation style [left-right v]\nforever\n"
   "move (10) steps\nif on edge, bounce\nend"),
 ],
 "looks": [
  ("01-script-reset-lengkap",
   "when green flag clicked\nshow\nset size to (100) %\nclear graphic effects\n"
   "switch costume to (costume1 v)\ngo to [front v] layer"),
  ("02-animasi-berjalan",
   "when green flag clicked\nforever\nnext costume\nmove (10) steps\n"
   "wait (0.1) seconds\nend"),
  ("03-muncul-perlahan",
   "set [ghost v] effect to (100)\nshow\nrepeat (20)\n"
   "change [ghost v] effect by (-5)\nend"),
 ],
 "sound": [
  ("01-musik-latar",
   "when green flag clicked\nset volume to (40) %\nforever\n"
   "play sound [Musik v] until done\nend"),
  ("02-efek-suara-permainan",
   "forever\nif <touching (Koin v)?> then\nstart sound [Koin v]\n"
   "change [skor v] by (1)\nwait (0.5) seconds\nend\nend"),
  ("03-reset-suara",
   "when green flag clicked\nstop all sounds\nclear sound effects\n"
   "set volume to (100) %"),
 ],
 "events": [
  ("01-dialog-dua-sprite",
   ["when green flag clicked\nsay [Halo!] for (2) seconds\n"
    "broadcast [giliranmu v]",
    "when I receive [giliranmu v]\nsay [Hai juga!] for (2) seconds"]),
  ("02-cerita-berurutan",
   "when green flag clicked\nbroadcast [adegan1 v] and wait\n"
   "broadcast [adegan2 v] and wait\nbroadcast [selesai v] and wait"),
  ("03-kontrol-game-yang-benar",
   "when green flag clicked\nforever\n"
   "if <key (right arrow v) pressed?> then\nchange x by (10)\nend\n"
   "if <key (left arrow v) pressed?> then\nchange x by (-10)\nend\nend"),
 ],
 "sensing": [
  ("01-kontrol-pemain",
   "when green flag clicked\nforever\n"
   "if <key (right arrow v) pressed?> then\nchange x by (10)\nend\n"
   "if <key (left arrow v) pressed?> then\nchange x by (-10)\nend\nend"),
  ("02-tabrakan-dengan-jeda-aman",
   "forever\nif <<touching (Musuh v)?> and <(timer) > (1)>> then\n"
   "change [nyawa v] by (-1)\nreset timer\nend\nend"),
  ("03-kuis-dengan-jawaban",
   "ask [Berapa 5 + 3?] and wait\nif <(answer) = [8]> then\n"
   "say [Benar!] for (2) seconds\nelse\nsay [Belum tepat] for (2) seconds\nend"),
 ],
 "operators": [
  ("01-tabel-kebenaran",
   ["if <<(a) > (0)> and <(b) > (0)>> then\nsay [dua-duanya benar]\nend",
    "if <<(a) > (0)> or <(b) > (0)>> then\nsay [salah satu saja cukup]\nend",
    "if <not <(a) > (0)>> then\nsay [kebalikannya]\nend"]),
  ("02-genap-atau-ganjil",
   "ask [Masukkan angka] and wait\nif <((answer) mod (2)) = (0)> then\n"
   "say [Genap]\nelse\nsay [Ganjil]\nend"),
  ("03-blok-bersarang",
   "say (join [Rata-rata: ] (round ((((n1) + (n2)) + (n3)) / (3))))"),
 ],
 "variables": [
  ("01-skor-dan-nyawa",
   "when green flag clicked\nset [skor v] to (0)\nset [nyawa v] to (3)\nforever\n"
   "if <touching (Koin v)?> then\nchange [skor v] by (1)\nend\n"
   "if <touching (Musuh v)?> then\nchange [nyawa v] by (-1)\nend\nend"),
  ("02-gravitasi",
   "when green flag clicked\nset [kecepatan v] to (0)\nforever\n"
   "change y by (kecepatan)\nchange [kecepatan v] by (-1)\n"
   "if <(y position) < (-120)> then\nset y to (-120)\n"
   "set [kecepatan v] to (0)\nend\nend"),
  ("03-kuis-dari-bank-soal",
   "set [n v] to (pick random (1) to (length of [soal v]))\n"
   "ask (item (n) of [soal v]) and wait\n"
   "if <(answer) = (item (n) of [jawaban v])> then\nchange [skor v] by (1)\nend"),
 ],
 "my_blocks": [
  ("01-segi-banyak",
   ["define segi (sisi) (panjang)\nrepeat (sisi)\nmove (panjang) steps\n"
    "turn cw ((360) / (sisi)) degrees\nend",
    "segi (5) (80)\nsegi (6) (60)"]),
  ("02-reset-semua",
   ["define reset\ngo to x: (0) y: (0)\npoint in direction (90)\nshow\n"
    "set size to (100) %\nclear graphic effects",
    "when green flag clicked\nreset"]),
  ("03-pohon-fraktal",
   "define cabang (panjang)\nif <(panjang) > (10)> then\nmove (panjang) steps\n"
   "turn cw (30) degrees\ncabang ((panjang) * (0.7))\n"
   "turn ccw (60) degrees\ncabang ((panjang) * (0.7))\n"
   "turn cw (30) degrees\nmove ((0) - (panjang)) steps\nend"),
 ],
}


def render_pola(cat):
    return render(cat, POLA[cat], ROOT / "assets" / "pola" / cat)


# Blok yang HANYA dipakai strip "LIHAT BEDANYA" — varian yang tidak ada di
# daftar blok utama kategorinya, jadi tidak bisa diambil dari assets/<kat>/.
BANDING_CONTROL = [
    ("01-stop-this-script", "stop [this script v]"),
]

BANDING_MY_BLOCKS = [
    ("01-pemanggil", "lompat (5)"),
    # "02-define" di daftar utama sudah memuat blok pemanggilnya sekalian, jadi
    # tidak bisa dipakai untuk menyandingkan define LAWAN pemanggil.
    ("02-define-saja", "define (lompat)"),
]

BANDING_LOOKS = [
    ("01-set-ghost-100", "set [ghost v] effect to (100)"),
]

CATALOG = {
    "motion": MOTION, "looks": LOOKS, "sound": SOUND, "events": EVENTS,
    "control": CONTROL, "sensing": SENSING, "operators": OPERATORS,
    "variables": VARIABLES, "my_blocks": MY_BLOCKS,
    "banding/control": BANDING_CONTROL,
    "banding/my_blocks": BANDING_MY_BLOCKS,
    "banding/looks": BANDING_LOOKS,
    "operators/tunggal": OPERATORS_TUNGGAL,
    "variables/tunggal": VARIABLES_TUNGGAL,
}

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg.startswith("pola"):                      # pola  /  pola:control
        for c in (list(POLA) if arg == "pola" else [arg.split(":", 1)[1]]):
            print(f"pola {c:10s} {len(render_pola(c)):2d} script -> assets/pola/{c}/")
        sys.exit()
    if arg.startswith("contoh"):                    # contoh  /  contoh:control
        for c in (list(CONTOH) if arg == "contoh" else [arg.split(":", 1)[1]]):
            print(f"contoh {c:8s} {len(render_contoh(c)):2d} potongan "
                  f"-> assets/contoh/{c}/")
        sys.exit()
    cats = list(CATALOG) if arg == "all" else [arg]
    for cat in cats:
        out = ROOT / "assets" / cat
        made = render(cat, CATALOG[cat], out)
        print(f"{cat:11s} {len(made):2d} blok -> assets/{cat}/")
