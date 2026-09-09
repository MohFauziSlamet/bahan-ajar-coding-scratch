# Aset Blok Operators (Operator) — 14 gambar

PNG latar transparan, satu berkas per blok, warna resmi Scratch 3.0 (hijau `#59C059`).
Dirender oleh **scratchblocks 3.7.1** (MIT, di-vendor di `../../vendor/scratchblocks/`) —
pustaka yang sama dengan yang dipakai Scratch Wiki dan forum Scratch — lalu
difoto Chrome headless pada 3x (360 px per inci).

Nomor berkas mengikuti urutan blok di `_generate_pptx.py` (dikelompokkan per tema),
**bukan** urutan tampilan di palet Scratch. Nomor itulah yang mencocokkan gambar ke slide.

## Subfolder `tunggal/`

Berisi 7 gambar tunggal yang **hanya dipakai oleh `tab_code_operators.md`**, karena berkas .md membahas `+`, `-`, `*`, `/`, `<`, `=`, `>` satu per satu, sedangkan slide menggabungkannya jadi 3 slide.
Subfolder ini sengaja terpisah supaya tidak ikut terjaring pencocokan
gambar-ke-slide (yang hanya mencari `NN-*.png` di folder ini, tidak rekursif).

Dibuat ulang:

```bash
python3 _gen_block_assets.py operators
```

| No | Berkas | Nama blok di Scratch | Kegunaannya (bahasa sederhana) |
|---:|---|---|---|
| 1 | `01-tambah-kurang.png` | `(() + ())   (() - ())` | Menjumlah dan mengurangi dua angka. |
| 2 | `02-kali-bagi.png` | `(() * ())   (() / ())` | Mengalikan dan membagi dua angka. |
| 3 | `03-mod.png` | `(() mod ())` | Memberi SISA pembagian. Berguna untuk mengecek angka genap atau ganjil. |
| 4 | `04-round.png` | `(round ())` | Membulatkan angka ke bilangan bulat terdekat. |
| 5 | `05-abs-of.png` | `([abs] of ())` | Kumpulan fungsi matematika: nilai mutlak, akar, pembulatan ke bawah, dan lainnya. |
| 6 | `06-pick-random.png` | `(pick random (1) to (10))` | Mengambil satu angka acak di antara dua batas itu. |
| 7 | `07-perbandingan.png` | `(() < ())   (() = ())   (() > ())` | Membandingkan dua nilai. Hasilnya benar atau salah, dipakai di dalam blok if. |
| 8 | `08-and.png` | `(<> and <>)` | Hasilnya benar HANYA kalau kedua syarat benar. |
| 9 | `09-or.png` | `(<> or <>)` | Hasilnya benar kalau SALAH SATU syarat saja sudah benar. |
| 10 | `10-not.png` | `(not <>)` | Membalik jawaban: yang benar jadi salah, yang salah jadi benar. |
| 11 | `11-join.png` | `(join [apple] [banana])` | Menyambung dua teks jadi satu, misalnya kata Skor ditambah angkanya. |
| 12 | `12-letter-of.png` | `(letter (1) of [apple])` | Mengambil satu huruf pada urutan tertentu dari sebuah teks. |
| 13 | `13-length-of.png` | `(length of [apple])` | Menghitung ada berapa huruf dalam sebuah teks. |
| 14 | `14-contains.png` | `<[apple] contains [a]?>` | Bertanya: apakah teks itu memuat huruf atau kata tertentu? |

```bash
python3 _gen_block_assets.py operators/tunggal
```
