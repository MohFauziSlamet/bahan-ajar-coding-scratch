# Modul ⑤ — Area Kode (Scripts Area)

**Lokasi:** kanvas abu-abu bertitik besar di tengah editor.
**Estimasi:** 20 menit · **Jenjang:** SD kelas 5 – SMP

```
┌───────────────────────────────────────────┐
│  · · · · · · · · · · · · · · · · · · · ·  │
│  · ┌────────────────┐ · · · · · · · · ·   │
│  · │ when ⚑ clicked │ · · · · · · · · ·   │
│  · ├────────────────┤ · · · · · · · · ·   │
│  · │ move (10) steps│ · · · · · · · · ·   │
│  · └────────────────┘ · · · · · · · · ·   │
│  · · · · · · · · · · · · · · · · · ⊕ ⊖ =  │  ← tombol zoom
└───────────────────────────────────────────┘
```

---

## Tujuan Pembelajaran

1. Merangkai blok menjadi **script** yang berjalan.
2. Memakai **klik kanan** untuk Duplicate, Add Comment, Delete, dan Clean up blocks.
3. Mengatur **zoom** agar kode nyaman dibaca.
4. Menjalankan script dengan mengklik langsung tumpukan blok.

---

## Penjelasan

Area kode adalah **meja kerja**. Di sinilah blok dari palet dirangkai menjadi **script** — tumpukan blok yang saling menempel dan dijalankan berurutan dari atas ke bawah.

Ciri khas area kode:
- **Sangat luas** — bisa digulir ke segala arah, jadi bukan masalah kalau terasa "penuh".
- **Milik sprite yang sedang dipilih** — ganti sprite, isi area kode ikut berganti.
- **Boleh menampung banyak script terpisah**, dan semuanya bisa berjalan bersamaan.

---

## Rincian

### 1. Menyambung dan melepas blok

| Aksi | Cara |
|---|---|
| Menyambung | Tarik blok mendekat sampai muncul **bayangan putih**, lalu lepas |
| Melepas satu tumpukan | Tarik blok — **semua blok di bawahnya ikut terbawa** |
| Mengambil satu blok saja | Lepas dulu blok di bawahnya, ambil yang diinginkan, pasang kembali |
| Menghapus blok | Tarik kembali ke **palet** (kiri), atau klik kanan → Delete Block |

### 2. Menjalankan script

| Cara | Hasil |
|---|---|
| **Klik tumpukan blok** | Script langsung berjalan; ada garis kuning menyala saat aktif |
| Klik **bendera hijau ⚑** | Semua script berawalan `when ⚑ clicked` berjalan |

> Script berkilau kuning saat berjalan — pakai ini untuk mengajarkan siswa "melihat" program bekerja.

### 3. Menu klik kanan pada **area kosong**

| Pilihan | Fungsi |
|---|---|
| **Undo** | Batalkan tindakan terakhir |
| **Redo** | Ulangi tindakan yang dibatalkan |
| **Clean up blocks** | **Merapikan** semua script jadi tersusun rapi ke bawah |
| **Add Comment** | Menambah catatan kuning di kanvas |
| **Delete (N) Blocks** | Menghapus seluruh blok di area kode ⚠️ |

### 4. Menu klik kanan pada **sebuah blok**

| Pilihan | Fungsi |
|---|---|
| **Duplicate** | Menyalin blok tersebut **beserta blok di bawahnya** |
| **Add Comment** | Menempelkan catatan pada blok itu |
| **Delete Block** | Menghapus blok tersebut saja |

### 5. Komentar (Comment)

Kotak kuning berisi catatan. **Tidak memengaruhi jalannya program** — murni penjelasan untuk manusia.

Ajarkan sebagai kebiasaan baik:
```
when ⚑ clicked          ← 💬 "Ini bagian awal permainan"
set (skor) to (0)       ← 💬 "Skor selalu mulai dari nol"
```

> Ini adalah versi Scratch dari `//` di JavaScript atau `#` di Python — bekal penting untuk bahasa berikutnya.

### 6. Tombol Zoom (pojok kanan bawah area kode)

| Tombol | Fungsi |
|---|---|
| **⊕** | Perbesar tampilan blok |
| **⊖** | Perkecil tampilan blok |
| **=** | Kembalikan ke ukuran normal |

💡 Zoom **hanya mengubah tampilan**, tidak mengubah program. Perbesar saat memproyeksikan ke layar kelas; perkecil untuk melihat script panjang secara utuh.

---

## Praktik (12 menit)

**Latihan 1 — Script pertama (4 menit)**
```
when ⚑ clicked
move (100) steps
say [Halo!] for (2) seconds
```
Klik bendera hijau. Amati.

**Latihan 2 — Duplicate (3 menit)**
Klik kanan pada `move (100) steps` → **Duplicate** → pasang di bawahnya. Jalankan lagi, bandingkan hasilnya.

**Latihan 3 — Komentar & rapikan (3 menit)**
Klik kanan area kosong → **Add Comment** → tulis "Ini program pertamaku". Lalu klik kanan → **Clean up blocks**.

**Latihan 4 — Paralel (2 menit)**
Buat script **kedua yang terpisah**:
```
when ⚑ clicked
turn ↻ (15) degrees
```
Jalankan. Diskusikan: apakah dua script bisa berjalan bersamaan? (Jawab: **bisa** — inilah *paralelisme*.)

---

## Analogi untuk Siswa

> Area kode adalah **meja tempat menyusun puzzle**. Palet = kotak kepingannya. Puzzle hanya bisa disusun di meja, dan kepingan hanya menempel kalau bentuknya cocok.

---

## Kesalahan Umum

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Blok terlihat menumpuk tapi **tidak menempel** | Hanya blok teratas yang jalan | Ajarkan mencari **bayangan putih** sebelum melepas; uji dengan menarik blok teratas — bila yang lain tidak ikut, berarti belum menempel |
| Menekan **Delete (N) Blocks** tanpa sengaja | Seluruh kode hilang | Ajarkan **Ctrl+Z / Undo** segera |
| Membuat script tanpa **hat block** | Script tidak jalan saat bendera hijau diklik | Aturan: setiap script diawali blok kuning |
| Script menumpuk berantakan | Sulit dibaca & dinilai | Biasakan **Clean up blocks** sebelum mengumpulkan tugas |
| Mengira zoom mengubah ukuran sprite | Salah paham | Tegaskan zoom hanya tampilan kode |

---

## Cek Pemahaman

1. Bagaimana cara tahu dua blok benar-benar sudah menempel?
2. Apa fungsi **Clean up blocks**?
3. Apakah komentar kuning memengaruhi jalannya program?
4. Kamu punya 3 script terpisah yang semuanya diawali `when ⚑ clicked`. Berapa yang berjalan saat bendera diklik?

<details>
<summary>Kunci jawaban</summary>

1. Saat menarik blok teratas, blok di bawahnya ikut terbawa. Saat menyambung juga muncul bayangan putih.
2. Merapikan seluruh script agar tersusun rapi dari atas ke bawah.
3. Tidak. Komentar hanya catatan untuk manusia.
4. **Ketiganya** berjalan bersamaan (paralel).
</details>
