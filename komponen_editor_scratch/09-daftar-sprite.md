# Modul ⑨ — Daftar Sprite & Tombol Tambah Sprite

**Lokasi:** area di bawah Panel Info Sprite, berisi kartu bergambar tiap sprite.
**Estimasi:** 15 menit · **Jenjang:** SD kelas 5 – SMP

```
┌─────────────────────────────────┐
│  ┌────────┐                     │
│  │  🐱 ⊗  │  ← ikon ⊗ = hapus   │
│  │Sprite1 │  ← kartu bersorot   │
│  └────────┘     ungu = aktif    │
│                                 │
│                          ( 🐱+ )│ ← tombol tambah sprite
└─────────────────────────────────┘
```

---

## Tujuan Pembelajaran

1. Berpindah antar sprite dan memahami akibatnya pada area kode.
2. Menambah sprite dengan **4 cara** yang tersedia.
3. Menduplikasi, mengekspor, dan menghapus sprite.

---

## Penjelasan

Daftar Sprite adalah **daftar pemain** dalam proyek. Setiap kartu mewakili satu sprite. Kartu yang sedang **bersorot ungu** adalah sprite aktif — dan **semua yang kamu lakukan di tab Code, Costumes, dan Sounds berlaku untuk sprite itu saja**.

> ⚠️ **Aturan wajib sebelum menyusun blok:** *"Lihat dulu — sprite mana yang bersorot?"*
> Melewatkan langkah ini adalah penyebab nomor satu kebingungan siswa di kelas Scratch.

---

## Rincian

### 1. Kartu Sprite

| Bagian | Fungsi |
|---|---|
| Gambar kostum | Pratinjau tampilan sprite |
| Nama di bawah gambar | Nama sprite |
| Sorotan ungu | Menandai sprite yang sedang aktif |
| **Ikon ⊗ / tempat sampah** (muncul saat kartu aktif) | Menghapus sprite |

### 2. Klik kanan pada kartu sprite

| Pilihan | Fungsi |
|---|---|
| **duplicate** | Menyalin sprite **beserta seluruh kode, kostum, dan suaranya** |
| **export** | Menyimpan sprite sebagai berkas **`.sprite3`** untuk dipakai di proyek lain |
| **delete** | Menghapus sprite |

💡 **duplicate** adalah penghemat waktu terbesar di kelas. Contoh: buat satu musuh lengkap dengan kodenya, lalu duplikat 4 kali — jadilah 5 musuh dalam 10 detik.

### 3. Tombol Tambah Sprite (ikon kucing 🐱+ di pojok kanan bawah)

**Arahkan kursor** ke tombol ini → muncul 4 pilihan:

| Ikon | Pilihan | Fungsi | Kapan dipakai |
|---|---|---|---|
| 🔍 | **Choose a Sprite** | Pilih dari **pustaka Scratch** (ratusan karakter siap pakai) | Cara utama & tercepat |
| 🖌 | **Paint** | Membuat sprite kosong lalu **menggambar sendiri** | Melatih kreativitas |
| ⚡ | **Surprise** | Mengambil sprite **acak** dari pustaka | Pemantik ide / permainan |
| ⬆ | **Upload Sprite** | Mengunggah gambar dari komputer | Foto siswa, logo sekolah |

> Pustaka sprite bisa disaring per kategori (Animals, People, Fantasy, Sports, Food, dll.) dan bisa dicari lewat kolom pencarian.

### 4. Menghapus sprite

Klik ikon ⊗ pada kartu, atau klik kanan → **delete**.
Salah hapus? → **Edit > Restore** (hanya untuk yang **terakhir** dihapus).

### 5. Menyusun urutan

Kartu sprite bisa **diseret** untuk diurutkan. Ini hanya mengatur urutan tampilan di daftar — untuk mengatur siapa di depan/belakang **di panggung**, gunakan blok Looks `go to [front] layer`.

---

## Praktik (10 menit)

**Latihan 1 — Dua sprite berbicara (6 menit)**
1. Tambah sprite kedua lewat **Choose a Sprite** (mis. `Bear`).
2. Ganti nama: `Sprite1` → `Kucing`, sprite baru → `Beruang`.
3. Pilih **Kucing**, susun:
   ```
   when ⚑ clicked
   say [Halo Beruang!] for (2) seconds
   ```
4. Pilih **Beruang**, susun:
   ```
   when ⚑ clicked
   wait (2) seconds
   say [Halo Kucing!] for (2) seconds
   ```
5. Jalankan. **Diskusi:** mengapa Beruang perlu blok `wait`?

**Latihan 2 — Duplicate (2 menit)**
Klik kanan Beruang → **duplicate**. Amati bahwa `Beruang2` sudah membawa kode yang sama tanpa perlu disusun ulang.

**Latihan 3 — Surprise (2 menit)**
Klik tombol **Surprise** tiga kali, lalu hapus lagi sprite yang tidak diinginkan.

---

## Analogi untuk Siswa

> Daftar Sprite adalah **daftar pemain dalam sebuah drama**. Sutradara (kamu) hanya bisa memberi arahan pada **satu pemain dalam satu waktu** — yaitu pemain yang sedang kamu tunjuk (bersorot ungu). Kalau salah menunjuk, arahanmu masuk ke pemain yang keliru.

---

## Kesalahan Umum

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Menyusun kode di sprite yang salah | Sprite target tidak bereaksi | Biasakan cek sorotan ungu — jadikan kebiasaan refleks |
| Menyalin blok satu-satu ke sprite lain | Boros waktu | Ajarkan **duplicate** dan **backpack** |
| Menghapus sprite tanpa sengaja | Kerja hilang | Ajarkan **Edit > Restore** |
| Membiarkan nama Sprite1/Sprite2 | Dropdown blok membingungkan | Wajib ganti nama |
| Menambah puluhan sprite lewat Surprise | Proyek berat & berantakan | Batasi jumlah sprite di awal (maks 3–4) |

---

## Cek Pemahaman

1. Bagaimana cara mengetahui sprite mana yang sedang aktif?
2. Sebutkan 4 cara menambah sprite.
3. Apa yang ikut tersalin saat kamu memakai **duplicate** pada sebuah sprite?
4. Kamu ingin memakai sprite buatanmu di proyek lain, tanpa internet. Fitur apa yang dipakai?

<details>
<summary>Kunci jawaban</summary>

1. Kartunya bersorot/berlatar ungu di daftar sprite.
2. Choose a Sprite (pustaka), Paint (gambar sendiri), Surprise (acak), Upload Sprite (dari komputer).
3. Seluruh kode/script, semua kostum, dan semua suaranya.
4. Klik kanan sprite → **export** menjadi berkas `.sprite3`, lalu di proyek lain gunakan **Upload Sprite**. (Alternatif bila online & login: Backpack.)
</details>
