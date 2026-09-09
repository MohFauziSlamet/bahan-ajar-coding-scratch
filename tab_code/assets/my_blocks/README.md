# Aset Blok My Blocks (Blok Buatan Sendiri) — 5 gambar

PNG latar transparan, satu berkas per blok, warna resmi Scratch 3.0 (merah muda `#FF6680`).
Dirender oleh **scratchblocks 3.7.1** (MIT, di-vendor di `../../vendor/scratchblocks/`) —
pustaka yang sama dengan yang dipakai Scratch Wiki dan forum Scratch — lalu
difoto Chrome headless pada 3x (360 px per inci).

Nomor berkas mengikuti urutan blok di `_generate_pptx.py` (dikelompokkan per tema),
**bukan** urutan tampilan di palet Scratch. Nomor itulah yang mencocokkan gambar ke slide.

Baris bertanda — adalah slide penjelasan konsep atau tombol dialog, bukan blok nyata, jadi tidak punya gambar.

Dibuat ulang:

```bash
python3 _gen_block_assets.py my_blocks
```

| No | Berkas | Nama blok di Scratch | Kegunaannya (bahasa sederhana) |
|---:|---|---|---|
| 1 | — | `Mengapa My Blocks penting?` | My Blocks membuat kita bisa memberi NAMA pada sekumpulan blok, lalu memanggilnya berkali-kali. |
| 2 | `02-define.png` | `define (nama blok)` | Kepala blok buatan sendiri. Semua blok di bawahnya jalan tiap blok itu dipanggil. |
| 3 | `03-input-angka.png` | `Input: number or text` | Menambah kolom isian supaya blok buatan bisa diberi angka atau teks yang berbeda-beda. |
| 4 | `04-input-boolean.png` | `Input: boolean` | Menambah kolom heksagon supaya blok buatan bisa diberi syarat benar atau salah. |
| 5 | `05-label-teks.png` | `Add a label text` | Menambah tulisan penjelas di dalam blok supaya lebih mudah dibaca. |
| 6 | — | `Opsi: Run without screen refresh` | Membuat blok jalan sampai selesai dalam sekejap tanpa menggambar ulang layar. Cocok untuk menggambar. |
| 7 | `07-rekursi.png` | `Rekursi: blok memanggil dirinya sendiri` | Blok buatan yang memanggil dirinya sendiri. Dipakai untuk pola berulang seperti spiral. |
| 8 | — | `Keterbatasan & jalan keluarnya` | Blok buatan tidak bisa mengembalikan nilai seperti reporter; siasatnya pakai variabel. |
| 9 | — | `Blok bersifat lokal per sprite` | Blok buatan hanya ada di sprite tempat ia dibuat; sprite lain tidak melihatnya. |
