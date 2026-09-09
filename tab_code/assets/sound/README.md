# Aset Blok Sound (Suara) — 9 gambar

PNG latar transparan, satu berkas per blok, warna resmi Scratch 3.0 (magenta `#CF63CF`).
Dirender oleh **scratchblocks 3.7.1** (MIT, di-vendor di `../../vendor/scratchblocks/`) —
pustaka yang sama dengan yang dipakai Scratch Wiki dan forum Scratch — lalu
difoto Chrome headless pada 3x (360 px per inci).

Nomor berkas mengikuti urutan blok di `_generate_pptx.py` (dikelompokkan per tema),
**bukan** urutan tampilan di palet Scratch. Nomor itulah yang mencocokkan gambar ke slide.

Dibuat ulang:

```bash
python3 _gen_block_assets.py sound
```

| No | Berkas | Nama blok di Scratch | Kegunaannya (bahasa sederhana) |
|---:|---|---|---|
| 1 | `01-play-sound-until-done.png` | `play sound (Meow) until done` | Memainkan suara sampai habis dulu, baru blok berikutnya jalan. |
| 2 | `02-start-sound.png` | `start sound (Meow)` | Menyalakan suara lalu langsung lanjut ke blok berikutnya, tanpa menunggu. |
| 3 | `03-stop-all-sounds.png` | `stop all sounds` | Menghentikan seketika semua suara yang sedang berbunyi. |
| 4 | `04-change-pitch-effect.png` | `change (pitch) effect by (10)` | Menambah efek suara, misalnya nada makin tinggi seperti suara tupai. |
| 5 | `05-set-pitch-effect.png` | `set (pitch) effect to (100)` | Menetapkan langsung nilai efek suara. Nilai 0 berarti suara normal. |
| 6 | `06-clear-sound-effects.png` | `clear sound effects` | Menghapus semua efek suara supaya kembali normal. |
| 7 | `07-change-volume-by.png` | `change volume by (-10)` | Mengurangi keras suara 10 persen dari yang sekarang. |
| 8 | `08-set-volume-to.png` | `set volume to (100) %` | Menetapkan keras suara. 100% = paling keras, 0% = diam. |
| 9 | `09-volume.png` | `(volume)` | Memberi tahu keras suara sprite ini sekarang berapa persen. |
