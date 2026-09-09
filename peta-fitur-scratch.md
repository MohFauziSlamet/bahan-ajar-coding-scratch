# Peta Fitur Scratch — Riset Mendalam untuk Bahan Ajar

> Dokumen riset & pemetaan fitur Scratch (versi 3.0) sebagai basis penyusunan materi ajar SD–SMP.
> Sumber utama: [Scratch Wiki (en.scratch-wiki.info)](https://en.scratch-wiki.info) dan [scratch.mit.edu](https://scratch.mit.edu).
> Disusun: 29 Juli 2026. Status data: Scratch 3.0 (rilis 2 Januari 2019) + ekstensi terbaru *Face Sensing* (7 Oktober 2025).

---

## Daftar Isi

1. [Ringkasan Eksekutif](#1-ringkasan-eksekutif)
2. [Identitas & Sejarah](#2-identitas--sejarah)
3. [Varian & Platform](#3-varian--platform)
4. [Anatomi Editor (Antarmuka)](#4-anatomi-editor-antarmuka)
5. [Sistem Blok: Bentuk & Tata Bahasa Visual](#5-sistem-blok-bentuk--tata-bahasa-visual)
6. [Peta Lengkap 9 Kategori Blok Inti](#6-peta-lengkap-9-kategori-blok-inti)
7. [Ekstensi (Extensions)](#7-ekstensi-extensions)
8. [Fitur Data: Variabel, List, Cloud Variable](#8-fitur-data-variabel-list-cloud-variable)
9. [Fitur Objek: Sprite, Kostum, Backdrop, Klon, Layer](#9-fitur-objek-sprite-kostum-backdrop-klon-layer)
10. [Studio Media: Paint Editor & Sound Editor](#10-studio-media-paint-editor--sound-editor)
11. [Fitur Proyek & Berkas](#11-fitur-proyek--berkas)
12. [Fitur Komunitas & Sosial](#12-fitur-komunitas--sosial)
13. [Fitur Edukasi (Guru & Kelas)](#13-fitur-edukasi-guru--kelas)
14. [Batas Teknis (Limits)](#14-batas-teknis-limits)
15. [Pemetaan Fitur → Konsep Informatika](#15-pemetaan-fitur--konsep-informatika)
16. [Usulan Urutan Pengajaran](#16-usulan-urutan-pengajaran)
17. [Batasan Scratch (yang perlu diketahui guru)](#17-batasan-scratch-yang-perlu-diketahui-guru)
18. [Sumber](#18-sumber)

---

## 1. Ringkasan Eksekutif

Scratch adalah **bahasa pemrograman visual berbasis blok** sekaligus **platform komunitas daring**. Dua sisi ini penting dibedakan saat mengajar:

| Sisi | Isinya | Relevansi ajar |
|---|---|---|
| **Bahasa & Editor** | ±125 blok inti dalam 9 kategori, 11+ ekstensi, paint editor, sound editor | Inti materi pemrograman |
| **Platform Komunitas** | Share, remix, studio, komentar, forum, profil | Materi literasi digital & etika daring |
| **Ekosistem Edukasi** | Akun guru, kelas, tutorial, kurikulum Creative Computing, CS First | Perangkat pendukung guru |

Poin kunci teknis: Scratch **Turing-complete**, **event-driven**, mendukung **variabel, list, prosedur (custom block), dan rekursi** — jadi bukan sekadar "mainan", tapi bahasa pemrograman sungguhan dengan sintaks visual.

---

## 2. Identitas & Sejarah

| Aspek | Keterangan |
|---|---|
| Pengembang | **MIT Media Lab — Lifelong Kindergarten Group**; sejak Maret 2019 dinaungi **Scratch Foundation** |
| Mulai dikembangkan | 2003 |
| Rilis publik | 2007 |
| Target usia | 8–16 tahun (dipakai luas di luar rentang itu) |
| Motto | *Imagine, Program, Share* |
| Biaya | Gratis, tanpa iklan |
| Skala (Des 2024) | 135+ juta pengguna terdaftar, 164 juta proyek dibagikan |

### Garis waktu versi

| Versi | Waktu | Perubahan besar |
|---|---|---|
| **Scratch 1.0 – 1.4** | 2007–2009 | Editor **offline** saja (dibangun dengan Squeak/Smalltalk) |
| **Scratch 2.0** | 9 Mei 2013 | Editor **online berbasis Flash**, redesain situs, muncul custom block & clone |
| **Scratch 3.0** | 2 Januari 2019 | Ditulis ulang total dengan **HTML5 + JavaScript** (lepas dari Flash), sistem **ekstensi**, jalan di **tablet & HP** |
| Pembaruan 3.0 | 2019 → sekarang | Penambahan ekstensi bertahap; terbaru **Face Sensing** (7 Okt 2025) |

**Untuk diajarkan:** poin "Scratch 3.0 tidak lagi butuh Flash sehingga bisa dibuka di HP/tablet" penting karena banyak siswa hanya punya HP.

---

## 3. Varian & Platform

| Varian | Platform | Catatan penting |
|---|---|---|
| **Scratch Online Editor** | Browser modern (Chrome, Firefox, Safari, Edge). **Tidak** mendukung Internet Explorer, Opera, Silk | Fitur paling lengkap: cloud variable, backpack, share |
| **Scratch Desktop / Offline Editor** | Windows 10 (14316+), macOS 10.13+, Android 6.0+/ChromeOS | **Tanpa** cloud variable & backpack; tidak bisa upload langsung ke situs. Instalasi ±400 MB (Win), ±230 MB (macOS), ±75 MB (Android/ChromeOS) |
| **Aplikasi tablet/HP** | Microsoft Store, Mac App Store, Google Play | Cocok untuk sekolah tanpa lab komputer |
| **ScratchJr** | iPad, iPhone, Android, ChromeOS, Windows, macOS | Usia **5–7 tahun**. Blok disusun **kiri→kanan**, panggung pakai grid **20×15** (bukan piksel), blok pakai **simbol** bukan teks |
| **Scratch di Raspberry Pi** | Raspberry Pi OS | Punya ekstensi eksklusif: GPIO, Sense HAT, Simple Electronics |

> **Rekomendasi kelas:** gunakan **Online Editor** bila internet stabil (agar bisa share & simpan otomatis); siapkan **Offline Editor** sebagai cadangan saat internet mati.

---

## 4. Anatomi Editor (Antarmuka)

Layout Scratch 3.0 terbagi 3 panel:

```
┌───────────── Menu Bar (Bahasa, File, Edit, Tutorials, Nama Proyek, Share, See Project Page) ─────────────┐
│                          │                                        │                                     │
│  [Tab: Code|Costumes|    │      AREA SCRIPT / KODE                │        STAGE (Panggung)            │
│        Sounds]           │      (kanvas tempat menyusun blok)      │        480 × 360 piksel            │
│                          │                                        │  ┌──────────────────────────────┐  │
│  PALET BLOK              │   - drag & drop blok                   │  │  ▶ bendera hijau  ⛔ stop     │  │
│  ● Motion   ● Looks      │   - klik-kanan: Duplicate / Add        │  │  ⛶ mode layar penuh          │  │
│  ● Sound    ● Events     │     Comment / Delete                   │  └──────────────────────────────┘  │
│  ● Control  ● Sensing    │   - zoom in/out/reset                  │                                     │
│  ● Operators ● Variables │   - "Clean up blocks" (rapikan)        │   SPRITE PANE                       │
│  ● My Blocks             │                                        │   (daftar sprite + properti)        │
│  ⊕ Add Extension         │                                        │   STAGE PANE (daftar backdrop)      │
├──────────────────────────┴────────────────────────────────────────┴─────────────────────────────────────┤
│  BACKPACK (tas ransel) — simpan script/sprite/kostum/suara lintas proyek                                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Komponen yang wajib dikenalkan ke siswa

| Komponen | Fungsi |
|---|---|
| **Stage (Panggung)** | Tempat proyek berjalan. 480×360 px. Ada 3 ukuran tampilan: normal, *small stage* (240×180), *full screen* |
| **Sprite** | Objek/karakter yang bisa diberi perintah. Punya script, kostum, dan suara sendiri |
| **Sprite Pane** | Daftar sprite + properti: nama, posisi x/y, tampil/sembunyi, ukuran, arah |
| **Block Palette** | Daftar blok, dikelompokkan per kategori berwarna |
| **Area Script** | Kanvas tempat blok dirangkai |
| **Tab Code / Costumes / Sounds** | Tiga "ruang kerja" tiap sprite |
| **Bendera hijau ▶ & Stop ⛔** | Tombol jalankan / hentikan proyek |
| **Backpack** | Menyalin aset & script antar proyek (**online saja**, harus login) |
| **Tutorials** | Panduan interaktif bawaan di dalam editor |

---

## 5. Sistem Blok: Bentuk & Tata Bahasa Visual

Bentuk blok = **tata bahasa** Scratch. Bentuk menentukan di mana blok boleh dipasang — ini konsep yang sering dilewat guru padahal sangat membantu siswa.

| Bentuk | Nama | Ciri fisik | Fungsi | Jumlah (inti) |
|---|---|---|---|---|
| ⌒▔ | **Hat Block** | Atas melengkung, bawah bertakik | **Memulai** script (pemicu/event) | 8 |
| ▭ | **Stack Block** | Takik atas & tonjolan bawah | Perintah biasa, bisa ditumpuk | 62 |
| ⬡ | **Boolean Block** | Segi enam | Menghasilkan **benar/salah** — hanya masuk ke slot segi enam | 14 |
| ⬭ | **Reporter Block** | Oval/bulat | Menghasilkan **nilai** (angka/teks) — masuk ke slot oval | 34 |
| ⊂ | **C-Block** | Berbentuk huruf C | **Membungkus** blok lain (loop & percabangan) | 5 |
| ▬ | **Cap Block** | Bawah rata (tanpa tonjolan) | **Mengakhiri** script, tidak bisa disambung lagi | 2 |

> **Total blok inti ±125** (belum termasuk ekstensi & blok list).

**Analogi mengajar:** Hat = "aba-aba mulai", Stack = "kalimat perintah", C = "kurung/pengulangan", Boolean = "pertanyaan ya/tidak", Reporter = "nilai/jawaban", Cap = "titik akhir".

---

## 6. Peta Lengkap 9 Kategori Blok Inti

| # | Kategori | Warna | Jumlah blok | Ringkas isi |
|---|---|---|---|---|
| 1 | **Motion** | Biru | 18 (15 stack, 3 reporter) | Gerak & posisi (sprite saja) |
| 2 | **Looks** | Ungu | 21 (18 stack, 3 reporter) | Tampilan, kostum, backdrop, efek |
| 3 | **Sound** | Merah muda | 9 (8 stack, 1 reporter) | Suara & volume |
| 4 | **Events** | Kuning | 8–9 (hat + broadcast) | Pemicu & pesan siaran |
| 5 | **Control** | Oranye | 11 (1 hat, 3 stack, 5 C, 2 cap) | Loop, percabangan, klon |
| 6 | **Sensing** | Biru muda | 18 (3 stack, 5–6 boolean, 10 reporter) | Deteksi & input |
| 7 | **Operators** | Hijau | 18 (7 boolean, 11 reporter) | Matematika, teks, logika |
| 8 | **Variables** | Oranye tua (+ merah tua utk List) | 5 (variabel) + 12 (list) | Penyimpanan data |
| 9 | **My Blocks** | Merah muda tua | Dibuat sendiri | Prosedur/fungsi buatan pengguna |

---

### 6.1 Motion (Gerak) — 18 blok · **hanya untuk Sprite, Stage tidak bisa**

| Blok | Bentuk | Fungsi |
|---|---|---|
| `move () steps` | stack | Maju sejauh N langkah sesuai arah hadap |
| `turn ↻ () degrees` | stack | Putar searah jarum jam |
| `turn ↺ () degrees` | stack | Putar berlawanan jarum jam |
| `go to (random position / mouse-pointer / sprite)` | stack | Pindah seketika ke lokasi preset |
| `go to x:() y:()` | stack | Pindah seketika ke koordinat tertentu |
| `glide () secs to (target)` | stack | Meluncur halus ke lokasi preset selama N detik |
| `glide () secs to x:() y:()` | stack | Meluncur halus ke koordinat |
| `point in direction ()` | stack | Set arah hadap (derajat) |
| `point towards (target)` | stack | Hadap ke sprite / mouse-pointer |
| `change x by ()` | stack | Geser horizontal |
| `set x to ()` | stack | Set koordinat X |
| `change y by ()` | stack | Geser vertikal |
| `set y to ()` | stack | Set koordinat Y |
| `if on edge, bounce` | stack | Memantul saat kena tepi panggung |
| `set rotation style (all around / left-right / do not rotate)` | stack | Gaya rotasi sprite |
| `(x position)` | reporter | Melaporkan X saat ini |
| `(y position)` | reporter | Melaporkan Y saat ini |
| `(direction)` | reporter | Melaporkan arah hadap |

**Sistem koordinat:** titik pusat panggung = **(0, 0)**; X dari **−240 s.d. 240**; Y dari **−180 s.d. 180**. Sprite tidak bisa hilang total dari panggung — Scratch menjaga **minimal 15 piksel** sprite tetap terlihat (*fencing*).

---

### 6.2 Looks (Tampilan) — 21 blok

**Khusus Sprite (14):**

| Blok | Fungsi |
|---|---|
| `say [] for () seconds` / `say []` | Balon bicara (berdurasi / permanen) |
| `think [] for () seconds` / `think []` | Balon pikiran |
| `switch costume to (…)` | Ganti kostum |
| `next costume` | Kostum berikutnya (dasar animasi) |
| `change size by ()` / `set size to ()%` | Ubah / set ukuran |
| `show` / `hide` | Tampilkan / sembunyikan |
| `go to (front/back) layer` | Ke lapisan paling depan/belakang |
| `go (forward/backward) () layers` | Geser N lapisan |
| `(costume [number/name])` | Laporkan nomor/nama kostum |
| `(size)` | Laporkan ukuran (%) |

**Khusus Stage (4):** `switch backdrop to () and wait`, `switch backdrop to ()`, `next backdrop`, `(backdrop [number/name])`

**Bisa keduanya (3):** `change () effect by ()`, `set () effect to ()`, `clear graphic effects`

**7 Efek Grafis:**

| Efek | Rentang | Hasil |
|---|---|---|
| **Color** | 0–200 (berulang) | Ubah warna/hue |
| **Fisheye** | −100 ke atas | Efek lensa cembung |
| **Whirl** | bebas | Puntiran memutar dari titik pusat |
| **Pixelate** | 0 ke atas (praktis ≤5105) | Kotak-kotak/pixelated |
| **Brightness** | −100 s.d. 100 | −100 = hitam, 100 = putih |
| **Ghost** | 0–100 | 100 = transparan penuh (tetap terdeteksi sensor) |
| **Mosaic** | 0–5105 | Banyak salinan kecil sprite |

---

### 6.3 Sound (Suara) — 9 blok

| Blok | Fungsi |
|---|---|
| `play sound () until done` | Putar suara **sampai selesai** baru lanjut |
| `start sound ()` | Putar suara **tanpa menunggu** |
| `stop all sounds` | Hentikan semua suara |
| `change (pitch/pan) effect by ()` | Ubah efek nada / kiri-kanan |
| `set (pitch/pan) effect to ()` | Set efek suara |
| `clear sound effects` | Hapus semua efek suara |
| `change volume by ()` | Ubah volume |
| `set volume to ()%` | Set volume |
| `(volume)` | Laporkan volume (reporter) |

> Perbedaan `play sound until done` vs `start sound` adalah contoh konkret **blocking vs non-blocking** — bagus untuk mengajarkan urutan eksekusi.

---

### 6.4 Events (Kejadian) — 8–9 blok

| Blok | Bentuk | Fungsi |
|---|---|---|
| `when ⚑ clicked` | hat | Mulai saat bendera hijau diklik |
| `when () key pressed` | hat | Mulai saat tombol keyboard ditekan |
| `when this sprite clicked` | hat | Mulai saat sprite diklik *(versi Stage: `when stage clicked`)* |
| `when backdrop switches to ()` | hat | Mulai saat backdrop berganti |
| `when (loudness/timer) > ()` | hat | Mulai saat sensor melewati ambang |
| `when I receive ()` | hat | Mulai saat menerima pesan siaran |
| `broadcast ()` | stack | Kirim pesan siaran |
| `broadcast () and wait` | stack | Kirim pesan lalu **tunggu** semua penerima selesai |

> **Broadcast** = mekanisme komunikasi antar-sprite. Ini konsep *message passing* — bekal awal memahami event/API di bahasa lain.

---

### 6.5 Control (Kontrol) — 11 blok

| Blok | Bentuk | Fungsi |
|---|---|---|
| `wait () seconds` | stack | Jeda N detik |
| `wait until <>` | stack | Jeda sampai kondisi benar |
| `repeat ()` | C | Ulang N kali (*counted loop*) |
| `forever` | C | Ulang selamanya (*infinite loop*) |
| `repeat until <>` | C | Ulang sampai kondisi benar |
| `if <> then` | C | Percabangan satu jalur |
| `if <> then … else` | C | Percabangan dua jalur |
| `stop (all / this script / other scripts in sprite)` | cap* | Hentikan eksekusi (*jadi stack block bila opsi "other scripts"*) |
| `when I start as a clone` | hat | Dijalankan tiap klon baru lahir |
| `create clone of ()` | stack | Buat klon |
| `delete this clone` | cap | Hapus klon ini |

---

### 6.6 Sensing (Sensor) — 18 blok

| Blok | Bentuk | Fungsi |
|---|---|---|
| `<touching (sprite/mouse/edge)?>` | boolean | Deteksi sentuhan objek |
| `<touching color []?>` | boolean | Deteksi menyentuh warna |
| `<color [] is touching []?>` | boolean | Warna tertentu di sprite menyentuh warna lain |
| `<key () pressed?>` | boolean | Tombol sedang ditekan? |
| `<mouse down?>` | boolean | Tombol mouse sedang ditekan? |
| `(distance to (sprite/mouse-pointer))` | reporter | Jarak ke objek |
| `ask [] and wait` | stack | Tampilkan kotak input & tunggu jawaban |
| `(answer)` | reporter | Jawaban terakhir dari `ask` |
| `(mouse x)` / `(mouse y)` | reporter | Koordinat kursor |
| `set drag mode (draggable/not draggable)` | stack | Boleh/tidaknya sprite diseret pemain |
| `(loudness)` | reporter | Tingkat suara dari mikrofon |
| `(timer)` | reporter | Waktu berjalan (detik) |
| `reset timer` | stack | Reset timer ke 0 |
| `([property] of (sprite/stage))` | reporter | Ambil properti objek lain (x, y, arah, kostum, variabel…) |
| `(current (year/month/date/day of week/hour/minute/second))` | reporter | Data waktu nyata |
| `(days since 2000)` | reporter | Hari sejak 2000 (untuk hitung selisih waktu) |
| `(username)` | reporter | Username Scratch pemain |
| `<online?>` | boolean | *Blok tersembunyi, tidak tampil di palet standar* |

> `ask and wait` + `answer` = pintu masuk mengajarkan **input pengguna**, dan `([property] of ())` adalah cara membaca data sprite lain (konsep akses antar-objek).

---

### 6.7 Operators (Operator) — 18 blok

**Matematika (7):**
`(() + ())` · `(() - ())` · `(() * ())` · `(() / ())` · `(() mod ())` · `(round ())` · `([abs/floor/ceiling/sqrt/sin/cos/tan/asin/acos/atan/ln/log/e^/10^] of ())`

**Acak (1):** `(pick random () to ())`

**Perbandingan (3):** `([] < [])` · `([] = [])` · `([] > [])`

**Logika (3):** `(<> and <>)` · `(<> or <>)` · `(not <>)`

**Teks/String (4):** `(join [] [])` · `(letter () of [])` · `(length of [])` · `<[] contains []?>`

> Dropdown `([…] of ())` memuat 14 fungsi matematika — cukup untuk materi trigonometri & logaritma di jenjang SMP/SMA.

---

### 6.8 Variables & Lists

**Blok Variabel (5):**

| Blok | Fungsi |
|---|---|
| `(nama variabel)` | reporter — baca nilai |
| `set () to ()` | Isi nilai |
| `change () by ()` | Tambah/kurangi nilai |
| `show variable ()` | Tampilkan monitor di panggung |
| `hide variable ()` | Sembunyikan monitor |

**Blok List (12):**

| Blok | Bentuk | Fungsi |
|---|---|---|
| `(nama list)` | reporter | Isi seluruh list |
| `add [] to ()` | stack | Tambah item di akhir |
| `delete () of ()` | stack | Hapus item ke-N |
| `delete all of ()` | stack | Kosongkan list |
| `insert [] at () of ()` | stack | Sisip item di posisi N |
| `replace item () of () with []` | stack | Ganti item ke-N |
| `(item () of ())` | reporter | Baca item ke-N |
| `(item # of [] in ())` | reporter | Cari posisi item |
| `(length of ())` | reporter | Jumlah item |
| `<() contains []?>` | boolean | Apakah list memuat item tsb |
| `show list ()` / `hide list ()` | stack | Tampil/sembunyikan monitor list |

---

### 6.9 My Blocks (Blok Buatan Sendiri)

Fitur **prosedur/fungsi** di Scratch. Dibuat lewat tombol **"Make a Block"**.

| Aspek | Keterangan |
|---|---|
| Jenis input | **number/text**, **boolean**, dan **label** (teks hiasan, bukan input) |
| Opsi `run without screen refresh` | Jalankan seluruh isi blok **dalam satu frame** (cepat, cocok untuk menggambar/perhitungan berat). **Jangan** dipakai bila di dalamnya ada `wait` atau loop tak terbatas — proyek bisa membeku |
| **Rekursi** | Didukung — blok bisa memanggil dirinya sendiri |
| **Keterbatasan** | Belum ada custom **reporter** & **boolean** block. Nilai balik harus dititipkan lewat variabel |

> My Blocks = jalan masuk mengajarkan **dekomposisi**, **abstraksi**, dan **DRY (jangan menyalin kode berulang)**.

---

## 7. Ekstensi (Extensions)

Diaktifkan lewat tombol **⊕ Add Extension** di kiri bawah editor. Ekstensi menambah kategori blok baru.

### 7.1 Ekstensi Perangkat Lunak

| Ekstensi | Blok | Isi & catatan |
|---|---|---|
| **Music** | 7 | `play drum () for () beats`, `rest for () beats`, `play note () for () beats`, `set instrument to ()`, `set tempo to ()`, `change tempo by ()`, `(tempo)`. Ada 21 instrumen & 18 drum di dropdown |
| **Pen** | 9 | `erase all`, `stamp`, `pen down`, `pen up`, `set pen color to ()`, `change pen () by ()`, `set pen () to ()`, `change pen size by ()`, `set pen size to ()`. Dasar *turtle graphics* & seni generatif |
| **Video Sensing** | 4 | `when video motion > ()`, `(video () on ())`, `turn video ()`, `set video transparency to ()`. Butuh kamera |
| **Face Sensing** | 9 | Rilis **7 Okt 2025**. Deteksi wajah via model **BlazeFace** yang berjalan **lokal di perangkat** (tidak mengirim wajah ke server). Blok: `when face tilts`, `when this sprite touches (fitur wajah)`, `when a face is detected`, `(face tilt)`, `(face size)`, `<a face is detected?>`, `go to (fitur wajah)`, `point in direction of face tilt`, `set size to face size` |
| **Text to Speech** | 3 | `speak []`, `set voice to ()`, `set language to ()`. 5 suara (alto, tenor, squeak, giant, kitten), **23 bahasa**. Ditenagai AWS, butuh internet |
| **Translate** | 2 | `(translate [] to ())`, `(language)`. **66 bahasa** (48 di dropdown + 18 tersembunyi). Ditenagai Google Translate, butuh internet |

### 7.2 Ekstensi Perangkat Keras

| Ekstensi | Perangkat | Kemampuan |
|---|---|---|
| **Makey Makey** | Papan Makey Makey | 2 hat block: `when () key pressed`, `when () pressed in order`. Mengubah benda konduktif (pisang, air, aluminium foil) jadi tombol |
| **micro:bit** | BBC micro:bit | 10 blok: tombol A/B, LED matrix (`display ()`, `display text []`, `clear display`), gerak/goyang, kemiringan (`tilt angle ()`), pin |
| **LEGO MINDSTORMS EV3** | LEGO EV3 | Kontrol motor & sensor robot |
| **LEGO BOOST** | LEGO BOOST | Kontrol motor, warna, jarak |
| **LEGO Education WeDo 2.0** | LEGO WeDo 2.0 | Motor & sensor tilt/distance |
| **Go Direct Force & Acceleration** | Sensor Vernier | Gaya & percepatan — untuk eksperimen fisika |

### 7.3 Eksklusif Raspberry Pi

**Raspberry Pi GPIO**, **Sense HAT**, **Simple Electronics** — hanya tersedia di Scratch versi Raspberry Pi.

> ⚠️ **Dihentikan di Scratch 3.0:** dukungan **PicoBoard** dan **LEGO WeDo 1.0**.

---

## 8. Fitur Data: Variabel, List, Cloud Variable

### 8.1 Cakupan (Scope) Variabel

| Jenis | Pilihan saat membuat | Perilaku |
|---|---|---|
| **Global** | "For all sprites" | Dibaca & ditulis semua sprite dan Stage |
| **Lokal** | "For this sprite only" | Milik satu sprite; **klon mewarisi salinannya sendiri** |
| **Cloud ☁** | "Cloud variable (stored on server)" | Disimpan di server Scratch, dibagi ke semua pemain |

> Variabel lokal pada klon adalah cara alami mengajarkan konsep *instance variable* — misal tiap peluru punya `kecepatan` sendiri.

### 8.2 Cloud Variable — batasan penting

| Batas | Nilai |
|---|---|
| Jumlah per proyek | **maksimal 10** |
| Tipe data | **hanya angka** (tidak boleh huruf/simbol, tidak boleh heksadesimal) |
| Panjang | maksimal **256 digit** |
| Kecepatan update | maksimal **10 update/detik** |
| Siapa yang boleh | **bukan** *New Scratcher* (harus akun yang sudah naik status) |
| Lokasi | **online saja** — tidak jalan di offline editor |
| Terlarang | proyek chat dengan penyaringan kata (alasan moderasi) |

**Pemakaian umum:** papan skor tertinggi, penghitung menang/kalah, jajak pendapat, dasar multiplayer sederhana.

---

## 9. Fitur Objek: Sprite, Kostum, Backdrop, Klon, Layer

### 9.1 Sprite

**4 cara menambah sprite:** (1) pilih dari **Library**, (2) **Paint** — gambar sendiri, (3) **Surprise** — acak, (4) **Upload** — dari berkas komputer.

Setiap sprite punya: **script sendiri**, **daftar kostum**, **daftar suara**, dan properti (nama, x, y, tampil/sembunyi, ukuran, arah).

Manajemen: **duplicate**, **delete** (hanya sprite terakhir yang bisa di-*undo* dari menu Edit), **export ke berkas `.sprite3`**, atau taruh di **Backpack**.

### 9.2 Kostum & Backdrop

- **Kostum** = tampilan alternatif sprite. Animasi dibuat dengan mengganti kostum berurutan (`next costume` di dalam loop).
- **Backdrop** = latar panggung. Stage punya backdrop, **bukan** kostum.
- Sumber sama seperti sprite: library / gambar sendiri / acak / unggah.

### 9.3 Klon (Clone)

| Aspek | Keterangan |
|---|---|
| Definisi | Salinan sprite yang dibuat **saat proyek berjalan**, punya script & variabel sendiri |
| Membuat | `create clone of (myself / sprite lain)` |
| Pemicu | `when I start as a clone` |
| Menghapus | `delete this clone` (tidak berpengaruh pada sprite asli) |
| Warisan | Kostum, suara, script, nilai variabel lokal, posisi, arah, kostum aktif |
| **Batas** | **300 klon** aktif bersamaan |
| Pemakaian | Peluru, koin, musuh, partikel (salju/kembang api), elemen UI |

### 9.4 Layer (Lapisan)

Sprite tersusun berlapis. Diatur dengan `go to (front/back) layer` dan `go (forward/backward) () layers`. **Stage selalu berada di lapisan paling belakang.**

---

## 10. Studio Media: Paint Editor & Sound Editor

### 10.1 Paint Editor

Dua mode grafis:

| Mode | Sifat | Cocok untuk |
|---|---|---|
| **Vector** (default) | Objek matematis, **tetap tajam saat diperbesar** | Karakter, ikon, bentuk geometris |
| **Bitmap** | Kisi piksel, **pecah saat diperbesar** | Gaya pixel-art, mengedit foto/gambar unggahan |

| Kelompok | Isi |
|---|---|
| Warna | 3 slider: **Color (hue)**, **Saturation**, **Brightness**; gradien; *color picker* dengan kaca pembesar |
| Alat vektor | **Reshape** (geser titik kurva), paint bucket, group/ungroup, flip horizontal/vertical, layering (Forward/Backward/Front/Back) |
| Alat bitmap | Kuas, garis, penghapus (membuat area jadi transparan) |
| Umum di kedua mode | Teks, pindah objek presisi pakai tombol panah, Undo/Redo, ganti nama kostum, select, duplicate |

### 10.2 Sound Editor

| Kelompok | Isi |
|---|---|
| Sumber suara | Library Scratch, **rekam sendiri via mikrofon**, unggah berkas |
| Edit dasar | Ganti nama, Undo/Redo, Copy, Paste, **Copy to New**, Delete |
| Seleksi | Sejak **Agustus 2019** bisa **memilih sebagian gelombang** lalu memberi efek hanya pada bagian itu |
| **9 efek** | Faster, Slower (nada), Louder, Softer (volume), Fade In, Fade Out, Mute, Reverse, **Robot** |

> Efek **Echo dihapus** pada Agustus 2019 untuk menyederhanakan antarmuka.

---

## 11. Fitur Proyek & Berkas

| Fitur | Keterangan |
|---|---|
| **Format berkas** | **`.sb3`** — sebenarnya arsip **ZIP** berisi `project.json` + aset (gambar/suara) yang dinamai dengan **checksum MD5** |
| Isi `project.json` | *Targets* (Stage + sprite), *blocks* (opcode, input, field), *assets*, *monitors* (tampilan variabel/list di panggung), *extensions*, *metadata* |
| Format sprite | **`.sprite3`** (struktur sama, JSON-nya bernama `sprite.json`) |
| Format lama | `.sb` (Scratch 1.x), `.sb2` (Scratch 2.0) — bisa dibuka Scratch 3.0 |
| Simpan | Auto-save di online editor; `File > Save to your computer` untuk unduh `.sb3` |
| Buka | `File > Load from your computer` |
| **Backpack** | Simpan script/sprite/kostum/suara lintas proyek. **Online saja + harus login.** Item yang ditarik keluar **disalin**, bukan dipindah |
| Kolaborasi | Tidak ada editing *real-time* bersama — kolaborasi lewat **remix** & **backpack** |

---

## 12. Fitur Komunitas & Sosial

| Fitur | Keterangan | Nilai ajar |
|---|---|---|
| **Share** | Publikasikan proyek ke komunitas | Kebanggaan berkarya |
| **Remix** | Menyalin & memodifikasi proyek orang lain — **atribusi otomatis** ke pembuat asli | Etika hak cipta & atribusi |
| **See Inside** | Siapa pun bisa melihat kode proyek yang dibagikan | Belajar dari kode orang lain |
| **Studio** | Kumpulan proyek bertema; bisa punya kurator | Wadah portofolio kelas |
| **Komentar** | Di proyek, profil, dan studio | Etika berkomentar |
| **Loves & Favorites** | Apresiasi proyek | Umpan balik positif |
| **Follow** | Ikuti pembuat lain; muncul di beranda | Jejaring belajar |
| **Profil** | Halaman "About me", "What I'm working on", proyek & studio | Identitas digital |
| **Discussion Forums** | Forum diskusi & bantuan | Tanya-jawab komunitas |
| **Explore / Featured** | Penjelajahan proyek & studio pilihan | Sumber inspirasi |
| **Moderasi** | Community Guidelines + tim moderator + pelaporan | Keamanan anak |

> **Catatan keamanan untuk sekolah:** proyek **tidak otomatis publik** — harus ditekan tombol *Share*. Guru bisa mengarahkan siswa untuk tidak membagikan data pribadi.

---

## 13. Fitur Edukasi (Guru & Kelas)

### 13.1 Teacher Account

Beta Januari 2016, resmi **Agustus 2016**. Diajukan lewat halaman **For Educators**, diverifikasi tim Scratch (umumnya ±1 hari).

| Kemampuan | Detail |
|---|---|
| **Buat kelas** | Undang siswa lewat tautan; kelas bisa ditutup/dibuka kapan saja |
| **Akun siswa** | Dibuat guru; tidak butuh email pribadi siswa |
| **Kelola siswa** | Edit "About me" & foto profil, reset/ganti password (2 cara: paksa ganti saat login, atau atur manual) |
| **Class Studio** | Studio khusus kelas untuk mengumpulkan tugas |
| **Pemantauan** | Melihat aktivitas siswa: proyek yang dibuat, di-*love*, perubahan profil, notifikasi |
| **Moderasi** | Hapus komentar siswa di profil & studio |

### 13.2 Sumber Belajar Resmi

| Sumber | Isi |
|---|---|
| **Tutorials** (di dalam editor) | Panduan interaktif langkah demi langkah |
| **Scratch Ideas Page** | Kartu ide proyek + panduan cetak |
| **Educator Guides** | Panduan mengajar per topik |
| **Creative Computing Curriculum** (Harvard) | Kurikulum lengkap berbasis Scratch |
| **CS First** (Google) | Program & modul CS berbasis Scratch |
| **Scratch Wiki** | Dokumentasi komunitas paling lengkap |

---

## 14. Batas Teknis (Limits)

| Aspek | Batas |
|---|---|
| Ukuran panggung | **480 × 360 piksel** (rasio 4:3) |
| Small stage layout | 240 × 180 piksel |
| Rentang koordinat | X: **−240 … 240**, Y: **−180 … 180**, pusat (0,0) |
| *Fencing* sprite | Minimal **15 px** sprite selalu terlihat di panggung |
| **Klon aktif** | **300** bersamaan |
| **Item list** | Tidak bisa `add`/`insert` bila list sudah ≥ **200.000** item (impor list tidak dibatasi) |
| **Ukuran aset** | Maksimal **10 MB per aset** |
| **project.json** | Maksimal **5 MB** |
| Total proyek | Tidak ada batas eksplisit (teoretis ±70.847 aset) |
| **Cloud variable** | 10 per proyek · angka saja · ≤256 digit · ≤10 update/detik |
| Efek Ghost | 0–100 |
| Efek Color | 0–200 (berulang) |
| Backpack | Tanpa batas jelas, tetapi terlalu banyak data → error "Error loading backpack" |
| Sprite di Stage | Stage tidak bisa bergerak, tidak bisa `say`/`think`, tidak bisa diklon, tidak bisa diganti nama; selalu di lapisan belakang |

---

## 15. Pemetaan Fitur → Konsep Informatika

Tabel ini menghubungkan fitur Scratch dengan Capaian Pembelajaran Informatika (elemen **Algoritma & Pemrograman** dan **Berpikir Komputasional**).

| Konsep CS | Fitur Scratch | Blok kunci |
|---|---|---|
| **Sequence (urutan)** | Blok ditumpuk atas→bawah | `move`, `say`, `wait` |
| **Event-driven** | Hat block & broadcast | `when ⚑ clicked`, `when I receive` |
| **Iteration (perulangan)** | C-block loop | `repeat`, `forever`, `repeat until` |
| **Selection (percabangan)** | C-block kondisi | `if…then`, `if…then…else` |
| **Boolean & logika** | Operator logika | `and`, `or`, `not`, `<`, `=`, `>` |
| **Variabel** | Kategori Variables | `set`, `change`, reporter variabel |
| **Struktur data (array)** | List | `add`, `item () of`, `length of` |
| **Prosedur / fungsi** | My Blocks | "Make a Block" + parameter |
| **Parameter & argumen** | Input pada custom block | number/text & boolean input |
| **Rekursi** | Custom block memanggil dirinya | My Blocks |
| **Abstraksi** | My Blocks + backpack | — |
| **Dekomposisi** | Pembagian tugas antar sprite/script | broadcast |
| **Paralelisme (concurrency)** | Banyak script berjalan bersamaan | beberapa `when ⚑ clicked` |
| **Objek & instance** | Sprite & klon (variabel lokal per klon) | `create clone of`, `when I start as a clone` |
| **Input/Output** | ask/answer, keyboard, mouse, mikrofon, kamera | `ask and wait`, `key pressed?`, `loudness` |
| **Koordinat kartesius** | Sistem koordinat panggung | `go to x: y:`, `x position` |
| **Sudut & rotasi** | Arah hadap sprite | `point in direction`, `turn` |
| **Random & probabilitas** | Operator acak | `pick random () to ()` |
| **String processing** | Operator teks | `join`, `letter () of`, `length of` |
| **Deteksi tabrakan (collision)** | Sensing | `touching ()?`, `touching color ()?` |
| **Debugging** | Klik script untuk uji, monitor variabel, komentar | show variable, klik-kanan Add Comment |
| **Jaringan/klien-server** | Cloud variable | ☁ variabel |
| **Fisika komputasi** | Variabel kecepatan + gravitasi | `change y by`, variabel `vy` |
| **Robotika & IoT** | Ekstensi micro:bit, LEGO, Makey Makey | ekstensi hardware |
| **AI dasar / computer vision** | Face Sensing, Video Sensing | ekstensi |
| **Etika digital & lisensi** | Remix + atribusi otomatis, Community Guidelines | fitur komunitas |

---

## 16. Usulan Urutan Pengajaran

Urutan bertingkat berdasarkan beban kognitif, bukan urutan kategori palet.

| Tahap | Fokus | Fitur yang dipakai | Proyek contoh |
|---|---|---|---|
| **1. Orientasi** | Kenal antarmuka | Stage, sprite, palet, bendera hijau | Kucing bicara & bergerak |
| **2. Sequence** | Urutan perintah | Motion + Looks + Sound dasar | Animasi perkenalan diri |
| **3. Event** | Pemicu | `when ⚑`, `when key pressed`, `when sprite clicked` | Piano/drum interaktif |
| **4. Loop** | Perulangan | `repeat`, `forever`, `next costume` | Animasi berjalan & tarian |
| **5. Kondisi** | Percabangan | `if`, `if-else`, Sensing dasar | Game hindari rintangan |
| **6. Koordinat** | Kartesius & sudut | `go to x y`, `point in direction` | Menggambar bentuk (+ ekstensi Pen) |
| **7. Variabel** | Menyimpan data | set/change, monitor skor | Game skor & nyawa |
| **8. Operator** | Matematika & logika | operator aritmetika, `pick random`, `and/or/not` | Kuis matematika |
| **9. Broadcast** | Komunikasi antar-objek | `broadcast`, `when I receive` | Cerita berbabak / ganti level |
| **10. Klon** | Objek dinamis | `create clone of`, `when I start as a clone` | Shooter / hujan koin |
| **11. List** | Struktur data | blok List | Kuis dari bank soal, papan skor lokal |
| **12. My Blocks** | Prosedur & abstraksi | Make a Block + parameter | Refactor game jadi rapi |
| **13. Ekstensi** | Perluasan | Music, Pen, TTS, Translate, Face Sensing | Alat musik, seni generatif, chatbot |
| **14. Hardware** | Fisik-digital | micro:bit / Makey Makey / LEGO | Piano pisang, robot sederhana |
| **15. Komunitas** | Publikasi & etika | Share, Remix, Studio kelas | Pameran karya kelas |

---

## 17. Batasan Scratch (yang perlu diketahui guru)

Agar ekspektasi realistis dan siswa disiapkan untuk transisi ke bahasa teks:

| Batasan | Dampak |
|---|---|
| Belum ada **custom reporter/boolean block** | Nilai balik fungsi harus lewat variabel — kurang rapi dibanding `return` |
| Tidak ada **struktur data bersarang** | List tidak bisa berisi list; tidak ada dictionary/objek |
| **Cloud variable hanya angka & maks 10** | Multiplayer & chat sangat terbatas |
| Tidak ada **akses file/jaringan bebas** | Disengaja demi keamanan anak — tidak bisa panggil API sembarangan |
| **Tidak ada editing kolaboratif real-time** | Kerja kelompok harus lewat remix/backpack |
| Performa terbatas | Proyek berat (banyak klon/pen) bisa lag; `run without screen refresh` jadi trik wajib |
| Tidak ada **type system** & error message | Bug logika sulit dilacak; debugging harus diajarkan eksplisit |
| **Fitur online tidak jalan offline** | Cloud variable & backpack hilang di Scratch Desktop; TTS & Translate butuh internet |

**Jalur lanjutan setelah Scratch:** ScratchJr (lebih muda) → Scratch → mBlock/micro:bit MakeCode → **Python** (transisi paling umum) atau JavaScript.

---

## 18. Sumber

**Utama — Scratch Wiki:**
- [Scratch](https://en.scratch-wiki.info/wiki/Scratch) · [Scratch 3.0](https://en.scratch-wiki.info/wiki/Scratch_3.0) · [Blocks](https://en.scratch-wiki.info/wiki/Blocks)
- [Motion Blocks](https://en.scratch-wiki.info/wiki/Motion_Blocks) · [Looks Blocks](https://en.scratch-wiki.info/wiki/Looks_Blocks) · [Sound Blocks](https://en.scratch-wiki.info/wiki/Sound_Blocks) · [Events Blocks](https://en.scratch-wiki.info/wiki/Events_Blocks) · [Control Blocks](https://en.scratch-wiki.info/wiki/Control_Blocks) · [Sensing Blocks](https://en.scratch-wiki.info/wiki/Sensing_Blocks) · [Operators Blocks](https://en.scratch-wiki.info/wiki/Operators_Blocks) · [Variables Blocks](https://en.scratch-wiki.info/wiki/Variables_Blocks) · [My Blocks](https://en.scratch-wiki.info/wiki/My_Blocks)
- [Extension](https://en.scratch-wiki.info/wiki/Extension) · [Music Blocks](https://en.scratch-wiki.info/wiki/Music_Blocks) · [Pen Blocks](https://en.scratch-wiki.info/wiki/Pen_Blocks) · [Video Sensing Extension](https://en.scratch-wiki.info/wiki/Video_Sensing_Extension) · [Face Sensing Extension](https://en.scratch-wiki.info/wiki/Face_Sensing_Extension) · [Text to Speech Extension](https://en.scratch-wiki.info/wiki/Text_to_Speech_Extension) · [Translate Extension](https://en.scratch-wiki.info/wiki/Translate_Extension) · [micro:bit Extension](https://en.scratch-wiki.info/wiki/micro:bit_Extension) · [Makey Makey Extension](https://en.scratch-wiki.info/wiki/Makey_Makey_Extension)
- [Stage](https://en.scratch-wiki.info/wiki/Stage) · [Sprite](https://en.scratch-wiki.info/wiki/Sprite) · [Clone](https://en.scratch-wiki.info/wiki/Clone) · [Coordinate System](https://en.scratch-wiki.info/wiki/Coordinate_System) · [Graphic Effects](https://en.scratch-wiki.info/wiki/Graphic_Effects)
- [Paint Editor](https://en.scratch-wiki.info/wiki/Paint_Editor) · [Sound Editor](https://en.scratch-wiki.info/wiki/Sound_Editor) · [Backpack](https://en.scratch-wiki.info/wiki/Backpack)
- [Cloud Variable](https://en.scratch-wiki.info/wiki/Cloud_Variable) · [Project File Size](https://en.scratch-wiki.info/wiki/Project_File_Size) · [Scratch File Format](https://en.scratch-wiki.info/wiki/Scratch_File_Format)
- [Scratch Desktop](https://en.scratch-wiki.info/wiki/Scratch_Desktop) · [ScratchJr](https://en.scratch-wiki.info/wiki/ScratchJr) · [Scratch Website](https://en.scratch-wiki.info/wiki/Scratch_Website) · [Teacher Account](https://en.scratch-wiki.info/wiki/Teacher_Account)

**Resmi:**
- [scratch.mit.edu](https://scratch.mit.edu) · [Scratch for Educators](https://scratch.mit.edu/educators) · [Scratch Ideas](https://scratch.mit.edu/ideas)

---

*Dokumen ini adalah peta fitur hasil riset, bukan modul ajar final. Langkah berikutnya: turunkan menjadi RPP/modul per pertemuan mengikuti [usulan urutan pengajaran](#16-usulan-urutan-pengajaran).*
