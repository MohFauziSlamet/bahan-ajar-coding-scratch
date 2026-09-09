# Modul ⑩ — Panel Stage & Backdrop

**Lokasi:** kolom sempit di kanan Daftar Sprite, bertuliskan **Stage** dan **Backdrops 1**.
**Estimasi:** 10 menit · **Jenjang:** SD kelas 5 – SMP

```
┌──────────────┐
│    Stage     │
│  ┌────────┐  │
│  │ (putih)│  │ ← pratinjau backdrop
│  └────────┘  │
│  Backdrops   │
│      1       │ ← jumlah backdrop
│              │
│       (🖼️+)  │ ← tombol tambah backdrop
└──────────────┘
```

---

## Tujuan Pembelajaran

1. Membedakan **Stage** dari sprite.
2. Menambah dan mengganti **backdrop**.
3. Menjelaskan beda **backdrop** dan **costume**.
4. Memberi kode pada Stage dan tahu batasannya.

---

## Penjelasan

Panel ini mewakili **panggung itu sendiri sebagai objek yang bisa dipilih**. Klik panel ini → panel jadi bersorot → sekarang tab Code, **Backdrops**, dan Sounds menampilkan milik Stage, bukan milik sprite.

Angka **Backdrops: 1** menunjukkan jumlah latar yang dimiliki proyek. Proyek baru selalu punya 1 backdrop putih polos.

### Backdrop vs Costume

| | **Backdrop** | **Costume** |
|---|---|---|
| Milik siapa | Stage | Sprite |
| Fungsi | Latar belakang | Tampilan tokoh |
| Ukuran ideal | 480 × 360 px (penuh panggung) | Bebas |
| Blok pengganti | `switch backdrop to ()`, `next backdrop` | `switch costume to ()`, `next costume` |
| Jumlah minimal | 1 | 1 |

---

## Rincian

### 1. Tombol Tambah Backdrop (ikon 🖼️+)

Arahkan kursor → muncul 4 pilihan, sama polanya dengan tombol tambah sprite:

| Pilihan | Fungsi |
|---|---|
| **Choose a Backdrop** | Pilih dari pustaka (Outdoors, Indoors, Space, Sports, Underwater, Music, dll.) |
| **Paint** | Gambar latar sendiri |
| **Surprise** | Latar acak |
| **Upload Backdrop** | Unggah gambar dari komputer |

### 2. Kode pada Stage

Stage **boleh punya script**, tetapi dengan batasan:

| ✅ Bisa | ❌ Tidak bisa |
|---|---|
| Mengganti backdrop | Blok Motion (bergerak) |
| Memainkan suara & musik latar | `say` / `think` |
| Efek grafis (`change color effect`) | Diklon |
| `ask ... and wait` | Berpindah lapisan (selalu paling belakang) |
| Variabel & broadcast | Diganti nama |

💡 **Praktik terbaik:** taruh script "pengatur permainan" di Stage — musik latar, pergantian level, reset skor. Ini mengajarkan **pemisahan tanggung jawab**: Stage mengurus dunia, sprite mengurus dirinya sendiri.

### 3. Backdrop sebagai penanda level

Blok `when backdrop switches to ()` di kategori Events memungkinkan sprite bereaksi otomatis saat latar berganti — cara termudah membuat permainan berlevel atau cerita berbabak.

```
[di Stage]                    [di Sprite Musuh]
when ⚑ clicked                when backdrop switches to (Level2)
switch backdrop to (Level1)   go to x: (200) y: (0)
                              show
```

---

## Praktik (7 menit)

1. Klik panel **Stage** → amati tab berubah menjadi **Backdrops**.
2. Klik tombol **Choose a Backdrop** → pilih `Blue Sky`. Amati angka Backdrops menjadi **2**.
3. Tambahkan satu backdrop lagi, mis. `Underwater`.
4. Pilih Stage, susun:
   ```
   when ⚑ clicked
   forever
     next backdrop
     wait (1) seconds
   ```
   Jalankan, amati latar bergantian. Tekan **stop**.
5. **Diskusi:** buka tab Code saat Stage dipilih, lalu klik kategori **Motion**. Mengapa kosong?

---

## Analogi untuk Siswa

> Kalau sprite adalah **aktor**, maka Stage adalah **panggung dan layar latarnya**. Layar latar bisa diganti (hutan → laut → luar angkasa), tapi panggungnya sendiri tidak pernah ikut berjalan ke mana-mana.

---

## Kesalahan Umum

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Menambahkan backdrop lewat tombol **sprite** | Latar jadi sprite yang bisa bergerak & menutupi | Tunjukkan dua tombol berbeda: 🐱+ vs 🖼️+ |
| Mencari blok Motion di Stage | Palet kosong, siswa bingung | Jelaskan Stage tidak bisa bergerak |
| Backdrop tidak berukuran 480×360 | Gambar terpotong atau ada bagian kosong | Sarankan pakai pustaka, atau sesuaikan di Paint Editor |
| Menyusun kode di Stage padahal maksudnya untuk sprite | Kode tidak berjalan sesuai harapan | Cek panel mana yang bersorot |
| Mengunggah foto besar sebagai backdrop | Proyek berat (batas 10 MB per aset) | Kecilkan gambar sebelum diunggah |

---

## Cek Pemahaman

1. Apa beda backdrop dan costume?
2. Berapa ukuran ideal gambar backdrop?
3. Sebutkan dua hal yang bisa dilakukan Stage dan dua hal yang tidak bisa.
4. Blok apa yang membuat sprite bereaksi otomatis saat latar berganti?

<details>
<summary>Kunci jawaban</summary>

1. Backdrop = latar belakang milik Stage; costume = tampilan milik sprite.
2. 480 × 360 piksel.
3. Bisa: ganti backdrop, mainkan suara, efek grafis, `ask and wait`, variabel, broadcast. Tidak bisa: bergerak (Motion), `say`/`think`, diklon, ganti lapisan, ganti nama.
4. `when backdrop switches to ()` di kategori **Events**.
</details>
