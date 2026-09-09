# Aset Blok Looks (Tampilan) — 21 gambar

PNG latar transparan, satu berkas per blok, warna resmi Scratch 3.0 (ungu `#9966FF`).
Dirender oleh **scratchblocks 3.7.1** (MIT, di-vendor di `../../vendor/scratchblocks/`) —
pustaka yang sama dengan yang dipakai Scratch Wiki dan forum Scratch — lalu
difoto Chrome headless pada 3x (360 px per inci).

Nomor berkas mengikuti urutan blok di `_generate_pptx.py` (dikelompokkan per tema),
**bukan** urutan tampilan di palet Scratch. Nomor itulah yang mencocokkan gambar ke slide.

Dibuat ulang:

```bash
python3 _gen_block_assets.py looks
```

| No | Berkas | Nama blok di Scratch | Kegunaannya (bahasa sederhana) |
|---:|---|---|---|
| 1 | `01-say-for-seconds.png` | `say [Hello!] for (2) seconds` | Sprite memunculkan balon bicara selama 2 detik, lalu balonnya hilang sendiri. |
| 2 | `02-say.png` | `say [Hello!]` | Sprite memunculkan balon bicara yang menempel terus sampai diganti. |
| 3 | `03-think-for-seconds.png` | `think [Hmm...] for (2) seconds` | Balon berpikir (bulat-bulat kecil) muncul selama 2 detik lalu hilang. |
| 4 | `04-think.png` | `think [Hmm...]` | Balon berpikir muncul dan menempel terus sampai diganti. |
| 5 | `05-switch-costume-to.png` | `switch costume to (costume2)` | Mengganti 'baju' atau gambar sprite ke kostum yang dipilih. |
| 6 | `06-next-costume.png` | `next costume` | Ganti ke kostum berikutnya. Kalau diulang cepat, sprite terlihat bergerak seperti animasi. |
| 7 | `07-costume-number.png` | `(costume [number])` | Memberi tahu sprite sedang memakai kostum nomor berapa (atau namanya apa). |
| 8 | `08-switch-backdrop-to.png` | `switch backdrop to (Blue Sky)` | Mengganti gambar latar panggung ke backdrop yang dipilih. |
| 9 | `09-switch-backdrop-to-and-wait.png` | `switch backdrop to (...) and wait` | Ganti latar, lalu tunggu dulu sampai semua reaksi latar itu selesai jalan. |
| 10 | `10-next-backdrop.png` | `next backdrop` | Ganti ke gambar latar berikutnya. |
| 11 | `11-backdrop-number.png` | `(backdrop [number])` | Memberi tahu panggung sedang memakai latar nomor berapa (atau namanya apa). |
| 12 | `12-change-size-by.png` | `change size by (10)` | Memperbesar sprite 10 persen dari ukuran sekarang. Angka negatif memperkecil. |
| 13 | `13-set-size-to-persen.png` | `set size to (100) %` | Menetapkan ukuran sprite. 100% = ukuran asli, 50% = separuhnya. |
| 14 | `14-size.png` | `(size)` | Memberi tahu ukuran sprite sekarang dalam persen. |
| 15 | `15-show.png` | `show` | Memunculkan sprite supaya terlihat lagi di panggung. |
| 16 | `16-hide.png` | `hide` | Menyembunyikan sprite. Sprite tetap ada dan tetap bisa jalan, hanya tak terlihat. |
| 17 | `17-go-to-front-layer.png` | `go to (front) layer` | Menaruh sprite di lapisan paling depan supaya tidak tertutup sprite lain. |
| 18 | `18-go-forward-layers.png` | `go (forward) (1) layers` | Memindahkan sprite maju 1 lapisan ke depan (atau mundur ke belakang). |
| 19 | `19-change-color-effect-by.png` | `change (color) effect by (25)` | Menambah efek warna sebanyak 25 dari nilai sekarang. |
| 20 | `20-set-color-effect-to.png` | `set (color) effect to (0)` | Menetapkan nilai efek langsung. Angka 0 berarti kembali normal. |
| 21 | `21-clear-graphic-effects.png` | `clear graphic effects` | Menghapus SEMUA efek sekaligus supaya sprite kembali normal. |
