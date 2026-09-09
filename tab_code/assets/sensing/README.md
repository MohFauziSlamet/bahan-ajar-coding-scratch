# Aset Blok Sensing (Sensor) — 18 gambar

PNG latar transparan, satu berkas per blok, warna resmi Scratch 3.0 (biru muda `#5CB1D6`).
Dirender oleh **scratchblocks 3.7.1** (MIT, di-vendor di `../../vendor/scratchblocks/`) —
pustaka yang sama dengan yang dipakai Scratch Wiki dan forum Scratch — lalu
difoto Chrome headless pada 3x (360 px per inci).

Nomor berkas mengikuti urutan blok di `_generate_pptx.py` (dikelompokkan per tema),
**bukan** urutan tampilan di palet Scratch. Nomor itulah yang mencocokkan gambar ke slide.

Dibuat ulang:

```bash
python3 _gen_block_assets.py sensing
```

| No | Berkas | Nama blok di Scratch | Kegunaannya (bahasa sederhana) |
|---:|---|---|---|
| 1 | `01-touching.png` | `<touching (mouse-pointer)?>` | Bertanya: apakah sprite sedang bersentuhan dengan sasaran itu? Jawabannya benar atau salah. |
| 2 | `02-touching-color.png` | `<touching color [ ]?>` | Bertanya: apakah sprite sedang menyentuh warna tertentu? |
| 3 | `03-color-is-touching.png` | `<color [ ] is touching [ ]?>` | Bertanya: apakah bagian berwarna tertentu pada sprite menyentuh warna lain? |
| 4 | `04-distance-to.png` | `(distance to (mouse-pointer))` | Memberi tahu jarak sprite ke sasaran dalam satuan titik. |
| 5 | `05-ask-and-wait.png` | `ask [Siapa namamu?] and wait` | Memunculkan kotak pertanyaan lalu menunggu pemain mengetik jawabannya. |
| 6 | `06-answer.png` | `(answer)` | Menyimpan jawaban terakhir yang diketik pemain. |
| 7 | `07-key-pressed.png` | `<key (space) pressed?>` | Bertanya: apakah tombol itu sedang ditekan sekarang? |
| 8 | `08-mouse-down.png` | `<mouse down?>` | Bertanya: apakah tombol mouse sedang ditekan? |
| 9 | `09-mouse-x.png` | `(mouse x)` | Memberi tahu posisi kiri-kanan kursor mouse. |
| 10 | `10-mouse-y.png` | `(mouse y)` | Memberi tahu posisi atas-bawah kursor mouse. |
| 11 | `11-set-drag-mode.png` | `set drag mode (draggable)` | Mengatur boleh tidaknya sprite digeser pakai mouse saat proyek berjalan. |
| 12 | `12-loudness.png` | `(loudness)` | Memberi tahu seberapa keras suara di sekitar, ditangkap lewat mikrofon. |
| 13 | `13-timer.png` | `(timer)` | Memberi tahu sudah berapa detik berjalan sejak penghitung waktu terakhir dinolkan. |
| 14 | `14-reset-timer.png` | `reset timer` | Mengembalikan penghitung waktu ke nol. |
| 15 | `15-current-year.png` | `(current (year))` | Mengambil waktu sekarang dari jam komputer: tahun, bulan, jam, dan seterusnya. |
| 16 | `16-days-since-2000.png` | `(days since 2000)` | Memberi tahu sudah berapa hari sejak 1 Januari 2000. Sering dipakai membuat angka acak. |
| 17 | `17-of-sprite.png` | `([x position] of (Sprite1))` | Mengintip nilai milik sprite lain, misalnya posisi atau ukurannya. |
| 18 | `18-username.png` | `(username)` | Memberi tahu nama akun Scratch pemain, bila proyek dibuka di situs Scratch. |
