# Modul ⑧ — Panel Info Sprite

**Lokasi:** kotak putih tepat di bawah panggung, berisi kolom-kolom isian.
**Estimasi:** 20 menit · **Jenjang:** SD kelas 5 – SMP

```
┌──────────────────────────────────────────────────────────────┐
│ Sprite [ Sprite1 ]   ↔ x [ 0 ]    ↕ y [ 0 ]                  │
│ Show  [👁] [👁̸]      Size [ 100 ]   Direction [ 90 ]          │
└──────────────────────────────────────────────────────────────┘
```

---

## Tujuan Pembelajaran

1. Menyebutkan arti keenam properti sprite.
2. Mengubah properti **langsung dari panel** dan mengamati akibatnya di panggung.
3. Menjelaskan hubungan antara panel ini dengan blok yang setara.
4. Memakai panel ini sebagai alat **debugging**.

---

## Penjelasan

Panel ini adalah **kartu identitas sprite yang sedang dipilih**. Semua angkanya **hidup** — berubah otomatis saat sprite bergerak, dan bisa diketik manual untuk langsung memindahkan sprite.

> **Konsep besar yang harus ditanamkan:** setiap properti di panel ini punya **blok yang setara**. Panel = mengatur dengan tangan, blok = mengatur lewat program. Inilah pintu masuk memahami bahwa program hanyalah "cara otomatis melakukan yang biasa kita lakukan manual".

---

## Rincian Keenam Properti

| Properti | Isi di gambar | Arti | Blok setara |
|---|---|---|---|
| **Sprite** (nama) | `Sprite1` | Nama sprite | — (dipakai di dropdown blok lain) |
| **↔ x** | `0` | Posisi mendatar (−240…240) | `set x to ()`, `(x position)` |
| **↕ y** | `0` | Posisi tegak (−180…180) | `set y to ()`, `(y position)` |
| **Show** 👁 / 👁̸ | tampil | Sprite terlihat atau tersembunyi | `show`, `hide` |
| **Size** | `100` | Ukuran dalam **persen** | `set size to ()%`, `(size)` |
| **Direction** | `90` | Arah hadap dalam **derajat** | `point in direction ()`, `(direction)` |

### Penjelasan per properti

#### 1. Nama Sprite
Klik dan ketik untuk mengganti. **Sangat penting** karena nama inilah yang muncul di dropdown blok lain, misalnya `touching (Bola ▾)?` atau `create clone of (Peluru ▾)`.

💡 **Aturan kelas:** ganti `Sprite1` menjadi nama bermakna — `Kucing`, `Bola`, `Musuh`, `Peluru`. Proyek dengan `Sprite1, Sprite2, Sprite3` mustahil dipahami saat sudah besar.

#### 2. x dan y
Ketik angka → sprite langsung pindah. Angkanya juga **berubah sendiri** saat sprite digerakkan program atau diseret mouse.

#### 3. Show (👁 tampil / 👁̸ sembunyi)
Sprite yang disembunyikan **tetap ada dan kodenya tetap berjalan** — hanya tidak terlihat.

⚠️ Jebakan klasik: siswa menyembunyikan sprite lewat blok `hide`, lalu di sesi berikutnya sprite "hilang". Solusinya: biasakan setiap proyek diawali script *reset*:
```
when ⚑ clicked
show
go to x: (0) y: (0)
set size to (100) %
point in direction (90)
```

#### 4. Size (ukuran, dalam persen)

| Nilai | Hasil |
|---|---|
| `100` | Ukuran asli |
| `50` | Setengah ukuran |
| `200` | Dua kali ukuran |

Batas maksimal bergantung ukuran kostum — sprite tidak bisa diperbesar melebihi ukuran panggung secara tak terbatas.

#### 5. Direction (arah hadap, dalam derajat)

| Nilai | Arah |
|---|---|
| **90** | Kanan (default) |
| **0** | Atas |
| **180** | Bawah |
| **−90** | Kiri |

Klik kolom Direction → muncul **piringan pemutar** (dial). Di bawah piringan ada 3 pilihan **gaya rotasi**:

| Gaya rotasi | Perilaku | Cocok untuk |
|---|---|---|
| **All Around** ↻ | Sprite ikut berputar penuh | Roket, jarum jam, panah |
| **Left/Right** ↔ | Hanya menghadap kiri/kanan, tidak terbalik | **Tokoh berjalan** (paling sering dipakai) |
| **Do not rotate** ● | Tampilan tidak pernah berubah | Ikon, tombol, latar bergerak |

> 💡 Ini menjawab keluhan paling sering di kelas: *"Pak, kucingnya jalan terbalik/jungkir balik!"* → ubah gaya rotasi ke **Left/Right**.

---

## Praktik (12 menit)

**Latihan 1 — Kenali panel (4 menit)**
Seret kucing di panggung dengan mouse. Minta siswa mengamati kolom **x** dan **y** berubah. Lalu sebaliknya: ketik `x = -200`, `y = 100`, amati kucing pindah.

**Latihan 2 — Ukuran (2 menit)**
Ubah **Size** menjadi `50`, lalu `200`, lalu kembali `100`.

**Latihan 3 — Arah & gaya rotasi (4 menit)**
1. Ubah **Direction** menjadi `-90`. Amati kucing terbalik (jungkir).
2. Klik Direction → pilih gaya rotasi **Left/Right** → amati kucing kini menghadap kiri dengan benar.
3. Jalankan:
   ```
   when ⚑ clicked
   set rotation style [left-right]
   forever
     move (5) steps
     if on edge, bounce
   ```

**Latihan 4 — Script reset (2 menit)**
Sembunyikan sprite lewat tombol 👁̸, lalu tampilkan lagi lewat 👁. Diskusikan pentingnya script reset di awal proyek.

---

## Analogi untuk Siswa

> Panel ini adalah **KTP sprite**: nama, alamat (x, y), tinggi badan (size), arah hadap (direction), dan status "sedang terlihat atau bersembunyi".

---

## Kesalahan Umum

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Membiarkan nama `Sprite1`, `Sprite2` | Proyek sulit dibaca | Wajib ganti nama sejak awal |
| Sprite jungkir balik saat bergerak | Tampilan aneh | Ubah gaya rotasi ke **Left/Right** |
| Sprite "hilang" karena pernah `hide` | Siswa mengira terhapus | Buat script reset di awal |
| Mengubah properti lewat panel lalu mengira itu tersimpan sebagai program | Saat dijalankan ulang posisi berbeda | Tegaskan: **panel = sementara, blok = permanen** |
| Size diketik `0` | Sprite tak terlihat | Cek nilai Size bila sprite menghilang |

---

## Cek Pemahaman

1. Nilai Direction berapa yang membuat sprite menghadap **ke atas**?
2. Sprite kamu berjalan terbalik saat ke kiri. Apa solusinya?
3. Apa beda mengetik `x = 100` di panel dengan memakai blok `set x to (100)`?
4. Sprite tidak terlihat di panggung. Sebutkan **tiga** kemungkinan penyebabnya.

<details>
<summary>Kunci jawaban</summary>

1. **0** derajat.
2. Ubah gaya rotasi (rotation style) menjadi **Left/Right**, lewat panel Direction atau blok `set rotation style [left-right]`.
3. Panel = perubahan manual sekali saja; blok = perintah tersimpan dalam program dan berulang tiap dijalankan.
4. Antara lain: (a) status Show sedang 👁̸ / pernah kena blok `hide`; (b) Size terlalu kecil (mis. 0); (c) posisi x/y di luar area pandang atau tertutup sprite lain; (d) efek Ghost 100.
</details>
