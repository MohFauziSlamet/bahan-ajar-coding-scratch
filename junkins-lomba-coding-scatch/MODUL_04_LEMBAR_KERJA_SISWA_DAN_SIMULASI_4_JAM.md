# MODUL 04: LEMBAR KERJA SISWA, SIMULASI MARATHON 4 JAM & PANDUAN PENJURIAN
**Panduan Pemrograman Visual Scratch — OISEN 2026**  
**Tema Game:** *"Satria Nusantara: Api Abadi Perjuangan"*  
**Format:** Lembar Kerja Siswa Siap Cetak (*Printable Handout*), Protokol Simulasi 240 Menit & Rubrik Juri

---

## 1. STRUKTUR LKS & JADWAL PELATIHAN EKSKUL (8 PERTEMUAN)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   ROADMAP PELATIHAN MENUJU HARI-H LOMBA                     │
├─────────────┬───────────────────────────────────────────────────────────────┤
│ Pertemuan 1 │ Pengenalan Juknis, Tema Perjuangan & Master State Engine      │
│ Pertemuan 2 │ Bedah Praktek Babak 1 (Melee Combat Bambu Runcing)            │
│ Pertemuan 3 │ Bedah Praktek Babak 2 (Surabaya 360° Mouse Aim Shooter)       │
│ Pertemuan 4 │ Bedah Praktek Babak 3 (Dogfight Dirgantara TNI AU)            │
│ Pertemuan 5 │ Bedah Praktek Babak 4 (Perang Bintang & Final Boss 20 HP)     │
│ Pertemuan 6 │ Workshop Cepat Prompting AI Aset & Background Remover         │
│ Pertemuan 7 │ SIMULASI LOMBA MARATHON 4 JAM (240 MENIT) NON-STOP            │
│ Pertemuan 8 │ Final Polish, Evaluasi Bebas Bug & Latihan Pitching Juri      │
└───────────────────────────────┴─────────────────────────────────────────────┘
```

---

## 2. LEMBAR KERJA SISWA (LKS) SIAP CETAK

```
===============================================================================
                    LEMBAR KERJA SISWA (LKS) CODING SCRATCH
                            PERSIAPAN OISEN 2026
===============================================================================
Nama Peserta : _____________________________   Sekolah : ______________________
Pembimbing   : _____________________________   Tanggal : ______________________

[ TANTANGAN UTAMA: MEMBUAT GAME 4 BABAK "SATRIA NUSANTARA" ]
-------------------------------------------------------------------------------
Petunjuk: Berikan tanda centang [V] pada setiap capaian yang berhasil kamu selesaikan!
-------------------------------------------------------------------------------

[ ] TAHAP 1: PERSIAPAN ASET VISUAL & AUDIO (Maksimal 30 Menit)
    [ ] 1. Generate 4 Karakter Pejuang (Bambu Runcing, TNI, Pilot AU, Jet Sci-Fi).
    [ ] 2. Generate 4 Musuh (Infanteri Belanda, Penjajah Surabaya, Pesawat, Boss).
    [ ] 3. Generate 4 Backdrop (Desa 1945, Surabaya, Langit Dirgantara, Antariksa).
    [ ] 4. Hapus background gambar di editor Scratch hingga rapi & bersih.

[ ] TAHAP 2: CORE ENGINE & UI/UX (Modul 01)
    [ ] 1. Stage memiliki 4 Stack (Reset Menu, Start Game, Level Clear, Game Over).
    [ ] 2. Variabel GameState, Score, Lives, dan CurrentLevel aktif For All Sprites.
    [ ] 3. Sprite UI_Button_Play muncul di menu dan berfungsi saat diklik.
    [ ] 4. Sprite Dialog_Box menampilkan prolog cerita interaktif dengan tombol Spasi.
    [ ] 5. Sprite HUD_Hearts memantau 3 nyawa dan berganti kostum hati dinamis.

[ ] TAHAP 3: PRAKTIK CODING BABAK 1 & BABAK 2 (Modul 02)
    [ ] 1. Pejuang Babak 1 bergerak halus kiri-kanan dan menusuk dengan tombol Spasi.
    [ ] 2. Kloning musuh infanteri berjalan dari kanan ke kiri dan hancur saat ditusuk (+10).
    [ ] 3. Skor 100 berhasil memicu transisi ke Cerita Babak 2.
    [ ] 4. Pejuang TNI Babak 2 membidik 360° mengikuti kursor mouse.
    [ ] 5. Klik mouse menembakkan peluru proyektil Bullet_Player.
    [ ] 6. Musuh Surabaya memiliki ketahanan 2x tembak dan hancur (+20 Skor).
    [ ] 7. Skor 250 berhasil memicu transisi ke Cerita Babak 3.

[ ] TAHAP 4: PRAKTIK CODING BABAK 3 & BABAK 4 (Modul 03)
    [ ] 1. Pesawat TNI AU Babak 3 bermanuver 8 arah di langit tanpa tembus layar.
    [ ] 2. Kloning awan Cloud_Scroller meluncur di lapisan paling belakang (Parallax).
    [ ] 3. Pesawat musuh meliuk gelombang sinus dan hancur saat kena tembak (+25 Skor).
    [ ] 4. Skor 500 berhasil memicu transisi ke Cerita Babak 4 Antariksa.
    [ ] 5. Jet Mecha Babak 4 menembakkan laser plasma ganda vertikal.
    [ ] 6. Kapal Induk Boss Antariksa berpatroli kiri-kanan dan menembakkan laser merah.
    [ ] 7. Boss menerima 20 hit tembakan sebelum meledak dahsyat (+200 Skor).
    [ ] 8. Layar Kemenangan Akhir (Victory Screen) tampil membawa pesan moral bangsa!

Catatan Guru Pembimbing:
_______________________________________________________________________________
_______________________________________________________________________________
```

---

## 3. PROTOKOL & RUNDOWN SIMULASI LOMBA 4 JAM (240 MENIT)

Simulasi lomba wajib dilakukan minimal 1 kali menjelang hari-H dengan kondisi menyerupai lomba aslinya di lab komputer:

```
                  MANAJEMEN WAKTU 240 MENIT (4 JAM LOMBA)
  ┌──────────────────┬──────────┬────────────────────────────────────────────┐
  │ Waktu Pengerjaan │ Durasi   │ Target Capaian Siswa                       │
  ├──────────────────┼──────────┼────────────────────────────────────────────┤
  │ 00:00 - 00:30    │ 30 Menit │ Pembuatan Seluruh Aset AI & Import Scratch │
  │ 00:30 - 01:00    │ 30 Menit │ Perakitan Core Engine & UI/UX (Modul 01)   │
  │ 01:00 - 01:40    │ 40 Menit │ Perakitan & Uji Coba Babak 1 (Bambu)       │
  │ 01:40 - 02:20    │ 40 Menit │ Perakitan & Uji Coba Babak 2 (Surabaya)    │
  │ 02:20 - 03:00    │ 40 Menit │ Perakitan & Uji Coba Babak 3 (Dirgantara)  │
  │ 03:00 - 03:30    │ 30 Menit │ Perakitan & Uji Coba Babak 4 (Boss Fight)  │
  │ 03:30 - 03:50    │ 20 Menit │ Polish Audio, Efek Visual & Backdrops      │
  │ 03:50 - 04:00    │ 10 Menit │ Playtest Akhir Playthrough & Clean Code    │
  └──────────────────┴──────────┴────────────────────────────────────────────┘
```

### 📋 Peraturan Ketat Saat Simulasi Berlangsung:
1. Siswa **TIDAK BOLEH** melihat file projek Scratch yang sudah jadi (harus kanvas kosong dari nol).
2. Guru pembimbing **TIDAK BOLEH** memberikan bantuan kode secara langsung (catat kesalahan di lembar evaluasi untuk dibahas setelah 4 jam selesai).
3. Gunakan stopwatch/timer layar panggung agar siswa terbiasa dengan tekanan waktu (*time pressure*).

---

## 4. LEMBAR RUBRIK PENILAIAN JURI (STANDAR OISEN 2026)

Gunakan lembar penilaian resmi ini untuk mengevaluasi karya siswa saat sesi simulasi:

```
===============================================================================
                    LEMBAR PENILAIAN DEWAN JURI (OISEN 2026)
===============================================================================
Nama Peserta : _____________________________   Asal Sekolah : _________________
Judul Game   : Satria Nusantara: Api Abadi Perjuangan

┌───┬──────────────────────────────────┬───────┬───────┬──────────────────────┐
│No │ Aspek Penilaian                  │ Bobot │ Skor  │ Catatan Evaluator    │
│   │                                  │       │(1-100)│                      │
├───┼──────────────────────────────────┼───────┼───────┼──────────────────────┤
│ 1 │ Logika & Kompleksitas Pemrograman│  25%  │ [   ] │ Algoritma, variabel, │
│   │                                  │       │       │ kloning, broadcast   │
├───┼──────────────────────────────────┼───────┼───────┼──────────────────────┤
│ 2 │ Kesesuaian Tema & Kreativitas    │  20%  │ [   ] │ Alur cerita 4 babak  │
│   │                                  │       │       │ tema Perjuangan      │
├───┼──────────────────────────────────┼───────┼───────┼──────────────────────┤
│ 3 │ Kelengkapan Babak, Skor & Nyawa  │  20%  │ [   ] │ 4 Babak tuntas, skor │
│   │                                  │       │       │ & nyawa aktif        │
├───┼──────────────────────────────────┼───────┼───────┼──────────────────────┤
│ 4 │ User Experience (UX) & Desain    │  15%  │ [   ] │ Estetika antarmuka,  │
│   │                                  │       │       │ SFX audio & navigasi │
├───┼──────────────────────────────────┼───────┼───────┼──────────────────────┤
│ 5 │ Fungsionalitas & Bebas Bug       │  10%  │ [   ] │ Kelancaran game tanpa│
│   │                                  │       │       │ error fatal          │
├───┼──────────────────────────────────┼───────┼───────┼──────────────────────┤
│ 6 │ Presentasi & Dokumentasi Kode    │  10%  │ [   ] │ Pitching 2 menit &   │
│   │                                  │       │       │ kerapian blok kode   │
└───┴──────────────────────────────────┴───────┴───────┴──────────────────────┘
                                TOTAL NILAI AKHIR : [       ] / 100
```

---

## 5. KARTU PINTAR: BANK PROMPT AI CEPAT (< 20 MENIT)

Berikan lembar ringkasan prompt ini untuk dipelajari dan dihafal siswa:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KARTU PINTAR PROMPT AI VISUAL CEPAT                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 💡 Rumus Dasar:                                                             │
│ "2D game sprite, [Subjek], [Pakaian/Senjata], [Pose], isolated on pure     │
│  white background, flat vector game art, clean outlines"                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Pejuang Bambu (Babak 1):                                                 │
│    2D game sprite, Indonesian freedom fighter hero 1945, muscular man,      │
│    shirtless, red-and-white headband, holding sharpened bamboo spear thrust │
│    pose, side view, isolated on pure white background, flat game asset      │
│                                                                             │
│ 2. Infanteri Belanda (Babak 1):                                             │
│    2D vector game sprite, colonial dutch army soldier 1945, khaki military  │
│    uniform, vintage helmet, holding rifle, marching side view pose,         │
│    isolated on pure white background, game enemy asset                      │
│                                                                             │
│ 3. TNI Surabaya (Babak 2):                                                  │
│    2D game sprite, Indonesian soldier 1945 battle of Surabaya, green army   │
│    uniform, aiming vintage rifle straight, side view, isolated on white bg  │
│                                                                             │
│ 4. Pesawat TNI AU (Babak 3):                                                │
│    2D top-down game sprite, vintage Indonesian air force fighter plane,     │
│    camo military green, red-and-white insignia on wings, isolated on white  │
│                                                                             │
│ 5. Jet Antariksa Mecha (Babak 4):                                           │
│    2D top-down sci-fi spaceship sprite, sleek cyberpunk mecha jet fighter,  │
│    glowing cyan wings and thrusters, isolated on pure white background      │
│                                                                             │
│ 6. Kapal Induk Final Boss (Babak 4):                                        │
│    2D top-down sci-fi mothership boss sprite, menacing alien dreadnought,   │
│    glowing red plasma cannons, dark metallic armor, isolated on white bg    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. PANDUAN PITCHING & TANYA JAWAB JURI (5 MENIT)

Jika siswa terpilih masuk babak final presentasi:

```
                    RUNDOWN PRESENTASI FINALIS (5 MENIT)
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ ⏱️ MENIT 00:00 - 02:00 : PRESENTASI SINGKAT PEMAIN (PITCHING)             │
  │                                                                           │
  │ 1. Pembuka (15 Detik):                                                    │
  │    "Selamat pagi/siang Dewan Juri yang terhormat. Saya [Nama] perwakilan  │
  │    dari [Sekolah]. Game yang saya rancang berjudul 'Satria Nusantara: Api │
  │    Abadi Perjuangan'."                                                    │
  │                                                                           │
  │ 2. Konsep Cerita & Pesan Moral (45 Detik):                                │
  │    "Game ini mengangkat tema kepahlawanan dalam 4 babak: dimulai dari     │
  │    perjuangan fisik bambu runcing 1945, pertempuran heroik Surabaya,     │
  │    kedaulatan dirgantara TNI AU, hingga kedaulatan sains dan teknologi  │
  │    di masa depan melalui pertempuran antariksa."                          │
  │                                                                           │
  │ 3. Fitur Logika & UX Unggulan (45 Detik):                                 │
  │    "Keunggulan game ini adalah arsitektur State Machine yang modular,     │
  │    sistem HUD 3 nyawa terpadu, kontrol kombinasi keyboard dan mouse yang  │
  │    responsif, serta sistem kloning musuh dan boss dengan multi-phase HP." │
  │                                                                           │
  │ 4. Penutup (15 Detik):                                                    │
  │    "Game ini menyampaikan pesan bahwa semangat bela negara harus terus    │
  │    hidup dari masa lalu hingga masa depan melalui penguasaan teknologi."  │
  ├───────────────────────────────────────────────────────────────────────────┤
  │ ⏱️ MENIT 02:00 - 05:00 : TANYA JAWAB TEKNIS DEWAN JURI                   │
  │                                                                           │
  │ Q1: "Bagaimana cara kerjamu mengatur pergantian babak tanpa bentrok?"     │
  │ A1: "Saya menggunakan variabel global GameState dan perintah broadcast   │
  │     and wait pada Stage, sehingga setiap sprite hanya aktif di babaknya." │
  │                                                                           │
  │ Q2: "Mengapa kamu membedakan variabel Global dan Lokal?"                  │
  │ A2: "Variabel Global seperti Skor dan Nyawa dibaca bersama oleh HUD dan  │
  │     Panggung, sedangkan variabel Lokal seperti enemy_speed dan Boss_HP   │
  │     hanya dimiliki oleh klon masing-masing agar nilainya mandiri."       │
  └───────────────────────────────────────────────────────────────────────────┘
```
