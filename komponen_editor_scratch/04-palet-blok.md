# Modul ④ — Palet Blok (Block Palette)

**Lokasi:** kolom di sebelah kanan selektor kategori, berisi daftar blok yang bisa ditarik.
**Estimasi:** 15 menit · **Jenjang:** SD kelas 5 – SMP

```
Motion
┌──────────────────────────┐
│ move (10) steps          │  ← blok stack
│ turn ↻ (15) degrees      │
│ turn ↺ (15) degrees      │
│ go to (random position▾) │  ← ada dropdown
│ go to x:(0) y:(0)        │  ← ada kolom isian
│ glide (1) secs to ...    │
│ ...                      │
│ ☐ (x position)           │  ← reporter + kotak centang
│ ☐ (y position)           │
└──────────────────────────┘
```

---

## Tujuan Pembelajaran

1. Menarik (*drag*) blok dari palet ke area kode.
2. Membedakan **bentuk** blok dan tahu di mana masing-masing boleh dipasang.
3. Mengisi **kolom isian** dan memilih **dropdown** pada blok.
4. Menggunakan **kotak centang** untuk menampilkan monitor nilai di panggung.

---

## Penjelasan

Palet adalah **rak berisi semua blok yang tersedia**. Blok di palet tidak ikut dijalankan — ia baru berfungsi setelah **ditarik ke area kode**. Blok di palet **tidak akan habis**: menarik satu blok berarti membuat salinannya.

---

## Rincian

### 1. Cara mengambil blok

| Aksi | Hasil |
|---|---|
| **Tarik** blok ke area kode | Blok tersalin ke area kode |
| **Klik** blok di palet (tanpa menarik) | Blok **langsung dijalankan sekali** — cara cepat menguji efek sebuah blok |
| Menggulir palet | Berpindah kategori secara halus (kategori berikutnya menyambung) |

💡 **Trik mengajar:** minta siswa **mengklik** `move 10 steps` di palet berkali-kali dan mengamati kucing bergeser. Ini menanamkan hubungan sebab-akibat sebelum mereka menyusun script.

### 2. Bentuk blok dan artinya

| Bentuk | Nama | Boleh dipasang di mana |
|---|---|---|
| Atas melengkung ⌒ | **Hat** | Hanya di **paling atas** script |
| Persegi bertakik ▭ | **Stack** | Ditumpuk atas-bawah |
| Huruf C ⊂ | **C-block** | Membungkus blok lain di dalamnya |
| Oval ⬭ | **Reporter** | Dimasukkan ke **lubang oval** di blok lain |
| Segi enam ⬡ | **Boolean** | Dimasukkan ke **lubang segi enam** |
| Bawah rata ▬ | **Cap** | Di **paling bawah**, tidak bisa disambung lagi |

> Aturan emas: **bentuk lubang harus cocok dengan bentuk blok.** Kalau tidak bisa masuk, berarti memang tidak boleh — Scratch mencegah kesalahan sintaks secara fisik.

### 3. Bagian yang bisa diubah di dalam blok

| Bagian | Contoh | Cara pakai |
|---|---|---|
| **Kolom isian putih** | `move (10) steps` | Klik lalu ketik angka/teks baru |
| **Dropdown ▾** | `go to (random position ▾)` | Klik untuk memilih pilihan lain |
| **Kotak warna** | `set pen color to [■]` | Klik untuk memilih warna |
| **Lubang oval** | `move ( ) steps` | Bisa diisi blok reporter, mis. `(x position)` |
| **Lubang segi enam** | `if < > then` | Hanya menerima blok boolean |

> Penting: kolom isian **bisa diganti dengan blok lain**. `move (pick random 1 to 10) steps` adalah gerbang menuju pemrograman yang benar-benar dinamis.

### 4. Kotak centang ☐ di sebelah blok reporter

Terlihat di bawah palet Motion pada `x position` dan `y position`.

- Dicentang → muncul **monitor** (kotak kecil bertuliskan nilai) di pojok kiri atas panggung.
- Tidak dicentang → monitor disembunyikan.

💡 **Sangat berguna untuk debugging.** Centang `x position`, lalu gerakkan sprite dan minta siswa membaca angkanya berubah. Ini cara termudah memperkenalkan koordinat.

---

## Praktik (8 menit)

1. **Klik** blok `move 10 steps` di palet 5 kali. Amati kucing.
2. Ubah angkanya menjadi `100`, klik lagi. Bandingkan.
3. Tarik `turn ↻ 15 degrees` ke area kode, ubah jadi `90`, klik. Amati arah kucing.
4. Centang ☐ `x position` dan ☐ `y position`. Tarik kucing di panggung dengan mouse dan bacakan angkanya bersama-sama.
5. Buka dropdown `go to (random position ▾)` → pilih `mouse-pointer` → klik blok → gerakkan mouse.

---

## Analogi untuk Siswa

> Palet blok itu **rak bumbu di dapur**. Bumbunya tidak pernah habis — kamu mengambil "sesendok" untuk dimasukkan ke panci (area kode). Selama masih di rak, bumbu itu belum jadi masakan.

---

## Kesalahan Umum

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Menyusun blok **di dalam palet** | Blok tidak tersimpan / hilang saat ganti kategori | Tegaskan: merangkai **hanya** di area kode |
| Memaksa blok masuk ke lubang yang salah bentuk | Frustrasi | Ajarkan aturan bentuk sejak awal |
| Mengetik di kolom isian tapi lupa klik di luar | Nilai belum tersimpan | Biasakan klik area kosong setelah mengetik |
| Semua kotak centang dicentang | Panggung penuh monitor | Centang seperlunya saja |
| Mengira klik blok di palet = memprogram | Kode tidak tersimpan | Jelaskan beda "mencoba" dan "menyusun" |

---

## Cek Pemahaman

1. Apa yang terjadi bila kamu **mengklik** (bukan menarik) blok di palet?
2. Blok berbentuk **segi enam** hanya bisa dipasang di lubang berbentuk apa?
3. Apa fungsi kotak centang di sebelah blok `x position`?
4. Bisakah lubang angka pada `move ( ) steps` diisi blok lain? Beri contoh.

<details>
<summary>Kunci jawaban</summary>

1. Blok langsung dijalankan satu kali, tanpa menambah kode ke proyek.
2. Lubang **segi enam** (slot kondisi), misalnya pada `if < > then` atau `repeat until < >`.
3. Menampilkan/menyembunyikan **monitor** nilai x di panggung.
4. Bisa. Contoh: `move (pick random (1) to (10)) steps` atau `move (x position) steps`.
</details>
