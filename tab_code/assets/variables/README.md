# Aset Blok Variables (Variabel & List) — 16 gambar

PNG latar transparan, satu berkas per blok, warna resmi Scratch 3.0 (oranye `#FF8C1A`).
Dirender oleh **scratchblocks 3.7.1** (MIT, di-vendor di `../../vendor/scratchblocks/`) —
pustaka yang sama dengan yang dipakai Scratch Wiki dan forum Scratch — lalu
difoto Chrome headless pada 3x (360 px per inci).

Nomor berkas mengikuti urutan blok di `_generate_pptx.py` (dikelompokkan per tema),
**bukan** urutan tampilan di palet Scratch. Nomor itulah yang mencocokkan gambar ke slide.

Baris bertanda — adalah slide penjelasan konsep atau tombol dialog, bukan blok nyata, jadi tidak punya gambar.

## Subfolder `tunggal/`

Berisi 2 gambar tunggal yang **hanya dipakai oleh `tab_code_variables.md`**, karena berkas .md memisahkan `show list` dan `hide list`, sedangkan slide menggabungkannya jadi 1 slide.
Subfolder ini sengaja terpisah supaya tidak ikut terjaring pencocokan
gambar-ke-slide (yang hanya mencari `NN-*.png` di folder ini, tidak rekursif).

Dibuat ulang:

```bash
python3 _gen_block_assets.py variables
```

| No | Berkas | Nama blok di Scratch | Kegunaannya (bahasa sederhana) |
|---:|---|---|---|
| 1 | — | `Membuat variabel: Make a Variable` | Tombol untuk membuat kotak penyimpan angka atau teks. Belum ada variabel, belum bisa menyimpan skor. |
| 2 | `02-variabel-reporter.png` | `(nama variabel)` | Kotak penyimpan satu nilai. Isinya bisa dipakai di blok mana saja. |
| 3 | `03-set-to.png` | `set (skor) to (0)` | Mengisi variabel dengan nilai baru, menimpa isi lamanya. |
| 4 | `04-change-by.png` | `change (skor) by (1)` | Menambah isi variabel sebanyak 1 dari nilai sekarang. |
| 5 | `05-show-variable.png` | `show variable (skor)` | Menampilkan kotak nilai variabel di panggung supaya pemain bisa melihatnya. |
| 6 | `06-hide-variable.png` | `hide variable (skor)` | Menyembunyikan kotak nilai variabel dari panggung. |
| 7 | `07-list-reporter.png` | `(nama list)` | List adalah kotak penyimpan yang memuat BANYAK nilai sekaligus, bernomor urut. |
| 8 | `08-add-to.png` | `add [thing] to (daftar)` | Menambah satu isi baru di urutan paling belakang list. |
| 9 | `09-delete-of.png` | `delete (1) of (daftar)` | Menghapus isi list pada urutan tertentu. |
| 10 | `10-delete-all-of.png` | `delete all of (daftar)` | Mengosongkan seluruh isi list sekaligus. |
| 11 | `11-insert-at.png` | `insert [thing] at (1) of (daftar)` | Menyisipkan isi baru di urutan tertentu; isi lain bergeser mundur. |
| 12 | `12-replace-item.png` | `replace item (1) of (daftar) with [x]` | Mengganti isi pada urutan tertentu tanpa mengubah panjang list. |
| 13 | `13-item-of.png` | `(item (1) of (daftar))` | Mengambil isi list pada urutan tertentu. |
| 14 | `14-item-number-of.png` | `(item # of [thing] in (daftar))` | Mencari sebuah isi berada di urutan ke berapa dalam list. |
| 15 | `15-length-of-list.png` | `(length of (daftar))` | Menghitung ada berapa isi dalam list. |
| 16 | `16-list-contains.png` | `<(daftar) contains [thing]?>` | Bertanya: apakah list itu memuat isi tertentu? |
| 17 | `17-show-hide-list.png` | `show list / hide list (daftar)` | Menampilkan atau menyembunyikan kotak list di panggung. |

```bash
python3 _gen_block_assets.py variables/tunggal
```
