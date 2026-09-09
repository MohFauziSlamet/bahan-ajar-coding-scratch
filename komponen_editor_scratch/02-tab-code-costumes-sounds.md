# Modul ② — Tab Code / Costumes / Sounds

**Lokasi:** kiri atas, tepat di bawah Menu Bar.
**Estimasi:** 10 menit · **Jenjang:** SD kelas 5 – SMP

```
[ 🧩 Code ] [ 🖌 Costumes ] [ 🔊 Sounds ]
   aktif
```

---

## Tujuan Pembelajaran

1. Menjelaskan bahwa setiap sprite punya **tiga ruang kerja**.
2. Berpindah antar tab dengan tepat sesuai kebutuhan.
3. Menyadari bahwa isi ketiga tab **berubah mengikuti sprite yang sedang dipilih**.

---

## Penjelasan

Tiga tab ini adalah **tiga sisi dari satu sprite yang sama**:

| Tab | Isi | Pertanyaan pemandu |
|---|---|---|
| 🧩 **Code** | Blok & script | "Apa yang **dilakukan** sprite ini?" |
| 🖌 **Costumes** | Daftar kostum + Paint Editor | "Bagaimana **rupa** sprite ini?" |
| 🔊 **Sounds** | Daftar suara + Sound Editor | "Suara apa yang **dimiliki** sprite ini?" |

### Konsep kunci yang sering terlewat

> **Isi ketiga tab menempel pada sprite, bukan pada proyek.**

Kalau siswa memilih Sprite2 lalu membuka tab Code, yang muncul adalah script **Sprite2** — bukan script Sprite1. Ini penyebab keluhan klasik: *"Pak, kode saya hilang!"* Padahal hanya salah pilih sprite.

Pengecualian: bila yang dipilih adalah **Stage**, tab **Costumes** berganti nama menjadi **Backdrops**.

---

## Rincian Tiap Tab

### 🧩 Tab Code
Ruang utama pemrograman. Berisi selektor kategori, palet blok, dan area kode
→ dibahas terpisah di [03](03-selektor-kategori-blok.md), [04](04-palet-blok.md), [05](05-area-kode.md).

### 🖌 Tab Costumes
Daftar kostum sprite di kiri + **Paint Editor** di kanan.

| Yang bisa dilakukan | Keterangan |
|---|---|
| Melihat & mengurutkan kostum | Urutan menentukan hasil blok `next costume` |
| Menambah kostum | 4 cara: pilih dari pustaka, gambar sendiri, acak (*Surprise*), unggah |
| Menggambar & mengedit | Mode **Vector** (tajam saat diperbesar) atau **Bitmap** (berbasis piksel) |
| Menduplikasi & menghapus kostum | Klik kanan pada kostum |
| Mengubah nama kostum | Kolom nama di atas kanvas |

> Setiap sprite **wajib punya minimal satu kostum**.

### 🔊 Tab Sounds
Daftar suara sprite + **Sound Editor**.

| Yang bisa dilakukan | Keterangan |
|---|---|
| Menambah suara | Pustaka Scratch, **rekam sendiri lewat mikrofon**, atau unggah berkas |
| Memotong & menyalin | Pilih bagian gelombang lalu Cut/Copy/Paste/Delete |
| Memberi efek | 9 efek: Faster, Slower, Louder, Softer, Fade In, Fade Out, Mute, Reverse, Robot |

---

## Praktik (7 menit)

1. Pilih Sprite1 → buka tab **Costumes** → klik kostum kedua (`costume2`) → amati kucing di panggung berubah pose.
2. Buka tab **Sounds** → klik ▶ pada suara `Meow`.
3. Rekam suaramu sendiri mengucapkan "Halo!" (**Record**), beri nama `salam`.
4. Kembali ke tab **Code**. Pastikan siswa paham ketiganya milik sprite yang sama.

---

## Analogi untuk Siswa

> Bayangkan sprite adalah **seorang aktor**:
> - **Code** = naskah — apa yang harus dia lakukan
> - **Costumes** = lemari kostum — pakaian yang bisa dia kenakan
> - **Sounds** = pita suara — suara yang bisa dia keluarkan

---

## Kesalahan Umum

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Membuat kode di sprite yang salah | Kode "hilang" atau sprite tak bergerak | Biasakan **lihat sprite mana yang bersorot ungu** sebelum menyusun blok |
| Menghapus semua kostum | Sprite tak bisa ditampilkan | Ingatkan minimal 1 kostum |
| Merekam suara terlalu panjang | Ukuran proyek membengkak (batas 10 MB per aset) | Batasi rekaman ≤5 detik |
| Bingung mencari "Costumes" saat Stage dipilih | Tab berganti jadi "Backdrops" | Jelaskan pengecualian ini sekali di awal |

---

## Cek Pemahaman

1. Kamu memilih Sprite2, lalu tab Code tampak kosong. Apakah kode Sprite1 terhapus?
2. Di tab mana kamu merekam suaramu sendiri?
3. Saat Stage dipilih, tab "Costumes" berubah menjadi apa? Mengapa?

<details>
<summary>Kunci jawaban</summary>

1. Tidak. Setiap sprite punya area kode sendiri. Pilih kembali Sprite1 maka kodenya muncul lagi.
2. Tab **Sounds**, dengan tombol **Record**.
3. Menjadi **Backdrops**, karena Stage tidak memakai kostum melainkan latar belakang (backdrop).
</details>
