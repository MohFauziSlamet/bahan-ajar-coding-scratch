# Aset Blok Events (Kejadian) — 9 gambar

PNG latar transparan, satu berkas per blok, warna resmi Scratch 3.0 (kuning `#FFBF00`).
Dirender oleh **scratchblocks 3.7.1** (MIT, di-vendor di `../../vendor/scratchblocks/`) —
pustaka yang sama dengan yang dipakai Scratch Wiki dan forum Scratch — lalu
difoto Chrome headless pada 3x (360 px per inci).

Nomor berkas mengikuti urutan blok di `_generate_pptx.py` (dikelompokkan per tema),
**bukan** urutan tampilan di palet Scratch. Nomor itulah yang mencocokkan gambar ke slide.

Dibuat ulang:

```bash
python3 _gen_block_assets.py events
```

| No | Berkas | Nama blok di Scratch | Kegunaannya (bahasa sederhana) |
|---:|---|---|---|
| 1 | `01-when-green-flag-clicked.png` | `when green flag clicked` | Semua blok di bawahnya jalan begitu bendera hijau ditekan. Ini pintu masuk program. |
| 2 | `02-when-key-pressed.png` | `when (space) key pressed` | Blok di bawahnya jalan tiap kali tombol yang dipilih ditekan. |
| 3 | `03-when-this-sprite-clicked.png` | `when this sprite clicked` | Blok di bawahnya jalan tiap sprite ini diklik. Cocok untuk membuat tombol. |
| 4 | `04-when-stage-clicked.png` | `when stage clicked` | Blok di bawahnya jalan tiap panggungnya yang diklik, bukan spritenya. |
| 5 | `05-when-backdrop-switches.png` | `when backdrop switches to (Level2)` | Blok di bawahnya jalan tiap latar berganti ke backdrop itu. Berguna untuk pindah level. |
| 6 | `06-when-loudness-greater.png` | `when (loudness) > (10)` | Blok di bawahnya jalan kalau suara di sekitar melebihi angka itu. Perlu mikrofon. |
| 7 | `07-when-i-receive.png` | `when I receive (mulai)` | Blok di bawahnya jalan begitu pesan itu disiarkan. Cara sprite saling memberi aba-aba. |
| 8 | `08-broadcast.png` | `broadcast (mulai)` | Menyiarkan pesan ke semua sprite lalu langsung lanjut, tanpa menunggu. |
| 9 | `09-broadcast-and-wait.png` | `broadcast (mulai) and wait` | Menyiarkan pesan lalu menunggu sampai semua penerimanya selesai bekerja. |
