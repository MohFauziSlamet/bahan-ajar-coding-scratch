# Aset Blok Control (Kontrol) — 11 gambar

PNG latar transparan, satu berkas per blok, warna resmi Scratch 3.0 (oranye `#FFAB19`).
Dirender oleh **scratchblocks 3.7.1** (MIT, di-vendor di `../../vendor/scratchblocks/`) —
pustaka yang sama dengan yang dipakai Scratch Wiki dan forum Scratch — lalu
difoto Chrome headless pada 3x (360 px per inci).

Nomor berkas mengikuti urutan blok di `_generate_pptx.py` (dikelompokkan per tema),
**bukan** urutan tampilan di palet Scratch. Nomor itulah yang mencocokkan gambar ke slide.

Dibuat ulang:

```bash
python3 _gen_block_assets.py control
```

| No | Berkas | Nama blok di Scratch | Kegunaannya (bahasa sederhana) |
|---:|---|---|---|
| 1 | `01-wait-seconds.png` | `wait (1) seconds` | Menjeda program selama 1 detik sebelum lanjut ke blok berikutnya. |
| 2 | `02-wait-until.png` | `wait until <>` | Menahan program sampai syarat di dalamnya benar, baru lanjut. |
| 3 | `03-repeat.png` | `repeat (10)` | Mengulang blok di dalam pelukannya tepat 10 kali, lalu berhenti. |
| 4 | `04-forever.png` | `forever` | Mengulang blok di dalamnya terus-menerus dan tidak pernah berhenti sendiri. |
| 5 | `05-repeat-until.png` | `repeat until <>` | Mengulang terus sampai syaratnya benar, baru berhenti. |
| 6 | `06-if-then.png` | `if <> then` | Menjalankan blok di dalamnya HANYA kalau syaratnya benar. |
| 7 | `07-if-then-else.png` | `if <> then ... else ...` | Kalau syaratnya benar jalankan bagian atas; kalau salah, jalankan bagian bawah. |
| 8 | `08-stop-all.png` | `stop (all)` | Menghentikan program. Bisa dipilih: semua script, script ini saja, atau script lain. |
| 9 | `09-create-clone-of.png` | `create clone of (myself)` | Membuat salinan sprite yang bisa jalan sendiri. Cocok untuk peluru atau musuh banyak. |
| 10 | `10-when-i-start-as-a-clone.png` | `when I start as a clone` | Blok di bawahnya jalan tiap kali sebuah salinan baru lahir. |
| 11 | `11-delete-this-clone.png` | `delete this clone` | Menghapus salinan ini supaya tidak menumpuk dan membuat proyek berat. |
