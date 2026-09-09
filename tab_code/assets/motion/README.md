# Aset Blok Motion (Gerak) — 18 gambar

PNG latar transparan, satu berkas per blok, warna resmi Scratch 3.0 (biru `#4C97FF`).
Dirender oleh **scratchblocks 3.7.1** (MIT, di-vendor di `../../vendor/scratchblocks/`) —
pustaka yang sama dengan yang dipakai Scratch Wiki dan forum Scratch — lalu
difoto Chrome headless pada 3x (360 px per inci).

Nomor berkas mengikuti urutan blok di `_generate_pptx.py` (dikelompokkan per tema),
**bukan** urutan tampilan di palet Scratch. Nomor itulah yang mencocokkan gambar ke slide.

Dibuat ulang:

```bash
python3 _gen_block_assets.py motion
```

| No | Berkas | Nama blok di Scratch | Kegunaannya (bahasa sederhana) |
|---:|---|---|---|
| 1 | `01-move-steps.png` | `move (10) steps` | Maju ke depan sejauh 10 titik, mengikuti ke mana sprite sedang menghadap. |
| 2 | `02-turn-kanan-degrees.png` | `turn right (15) degrees` | Memutar badan sprite ke kanan sebesar 15 derajat. |
| 3 | `03-turn-kiri-degrees.png` | `turn left (15) degrees` | Memutar badan sprite ke kiri sebesar 15 derajat. |
| 4 | `04-go-to-random-position.png` | `go to (random position)` | Pindah kedip ke tempat yang dipilih — langsung sampai, tanpa terlihat berjalan. |
| 5 | `05-go-to-x-y.png` | `go to x: (0) y: (0)` | Pindah kedip ke titik koordinat tertentu di panggung. |
| 6 | `06-glide-secs-to-random-position.png` | `glide (1) secs to (random position)` | Meluncur pelan ke tempat pilihan selama 1 detik, gerakannya terlihat. |
| 7 | `07-glide-secs-to-x-y.png` | `glide (1) secs to x: (0) y: (0)` | Meluncur pelan ke titik koordinat selama 1 detik. |
| 8 | `08-point-in-direction.png` | `point in direction (90)` | Mengatur sprite mau menghadap ke mana. 90 = kanan, 0 = atas. |
| 9 | `09-point-towards.png` | `point towards (mouse-pointer)` | Memutar sprite supaya menghadap ke sasaran, misalnya kursor mouse. |
| 10 | `10-change-x-by.png` | `change x by (10)` | Menggeser sprite 10 titik ke kanan. Selalu mendatar, tak peduli arah hadapnya. |
| 11 | `11-set-x-to.png` | `set x to (0)` | Menaruh sprite di posisi kiri-kanan tertentu; ketinggiannya tidak berubah. |
| 12 | `12-change-y-by.png` | `change y by (10)` | Menggeser sprite 10 titik ke atas. Angka positif = naik, negatif = turun. |
| 13 | `13-set-y-to.png` | `set y to (0)` | Menaruh sprite di ketinggian tertentu; posisi kiri-kanannya tidak berubah. |
| 14 | `14-if-on-edge-bounce.png` | `if on edge, bounce` | Kalau sprite kena pinggir panggung, ia langsung memantul balik. |
| 15 | `15-set-rotation-style.png` | `set rotation style (left-right)` | Mengatur cara gambar sprite berubah saat ia berputar. |
| 16 | `16-x-position.png` | `(x position)` | Memberi tahu angka posisi kiri-kanan sprite saat ini. |
| 17 | `17-y-position.png` | `(y position)` | Memberi tahu angka posisi atas-bawah sprite saat ini. |
| 18 | `18-direction.png` | `(direction)` | Memberi tahu sprite sekarang menghadap ke arah berapa derajat. |
