# Peta Komponen Editor Scratch — Index Materi

> Kumpulan materi ajar **per komponen** antarmuka editor Scratch 3.0, disusun dari tangkapan layar editor resmi ([scratch.mit.edu](https://scratch.mit.edu)).
> Pendamping: [peta-fitur-scratch.md](../peta-fitur-scratch.md) (peta fitur menyeluruh) dan [pengenalan-coding-dasar-scratch-part-1.md](../pengenalan_coding_scratch/pengenalan-coding-dasar-scratch-part-1.md).

---

## Denah Layar Editor

```
╔═══════════════════════════════════════════════════════════════════════════════════╗
║ ①  MENU BAR                                                                       ║
║ [Logo] Settings ▾  File ▾  Edit ▾  [Untitled-2]  See Project Page  Tutorials  Debug   📁  👤 ║
╠═══════════════════════════════════════════════════════════════════════════════════╣
║ ② TAB              │                              │  ⑦ KONTROL PANGGUNG          ║
║ [Code][Costumes]   │                              │  ⚑  ⛔        [▫][▪][⛶]      ║
║ [Sounds]           │                              ├──────────────────────────────╢
╟────────┬───────────┤                              │                              ║
║ ③      │ ④         │   ⑤  AREA KODE               │   ⑥  PANGGUNG (STAGE)        ║
║ KATEGORI│ PALET     │      (Scripts Area)          │      480 × 360 px            ║
║ BLOK   │ BLOK      │                              │                              ║
║ ●Motion│ move 10   │   ← tempat merangkai blok    │        🐱 Sprite1            ║
║ ●Looks │ turn 15   │                              │                              ║
║ ●Sound │ go to x y │                              ├──────────────────┬───────────╢
║ ●Events│ ...       │                              │ ⑧ INFO SPRITE    │ ⑩ PANEL   ║
║ ●Control│          │                              │ Sprite  x  y     │   STAGE   ║
║ ●Sensing│          │                              │ Show  Size  Dir  │  Backdrops║
║ ●Operators│        │                        ⊕ ⊖ = ├──────────────────┤     1     ║
║ ●Variables│        │                   (zoom kode)│ ⑨ DAFTAR SPRITE  │           ║
║ ●My Blocks│        │                              │   [🐱 Sprite1]   │  [🖼️ +]   ║
║ ⊕ Ekstensi│        │                              │            [🐱 +]│           ║
╠════════╧═══════════╧══════════════════════════════╧══════════════════╧═══════════╣
║ ⑪  BACKPACK                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
```

---

## Daftar Modul

| No | Komponen | Berkas | Estimasi waktu ajar |
|---|---|---|---|
| ① | **Menu Bar** — Logo, Settings, File, Edit, Nama Proyek, See Project Page, Tutorials, Debug, My Stuff, Akun | [01-menu-bar.md](01-menu-bar.md) | 20 menit |
| ② | **Tab Code / Costumes / Sounds** | [02-tab-code-costumes-sounds.md](02-tab-code-costumes-sounds.md) | 10 menit |
| ③ | **Selektor Kategori Blok** + tombol Ekstensi | [03-selektor-kategori-blok.md](03-selektor-kategori-blok.md) | 15 menit |
| ④ | **Palet Blok** | [04-palet-blok.md](04-palet-blok.md) | 15 menit |
| ⑤ | **Area Kode (Scripts Area)** | [05-area-kode.md](05-area-kode.md) | 20 menit |
| ⑥ | **Panggung (Stage)** | [06-panggung-stage.md](06-panggung-stage.md) | 20 menit |
| ⑦ | **Kontrol Panggung** — Bendera hijau, Stop, ukuran tampilan, layar penuh | [07-kontrol-panggung.md](07-kontrol-panggung.md) | 10 menit |
| ⑧ | **Panel Info Sprite** — nama, x, y, Show, Size, Direction | [08-panel-info-sprite.md](08-panel-info-sprite.md) | 20 menit |
| ⑨ | **Daftar Sprite** + tombol tambah sprite | [09-daftar-sprite.md](09-daftar-sprite.md) | 15 menit |
| ⑩ | **Panel Stage / Backdrop** | [10-panel-stage-backdrop.md](10-panel-stage-backdrop.md) | 10 menit |
| ⑪ | **Backpack** | [11-backpack.md](11-backpack.md) | 10 menit |

**Total ±165 menit** (≈4 jam pelajaran). Bisa dipadatkan jadi 2 pertemuan: modul ①–⑤ (editor & kode) lalu ⑥–⑪ (panggung & objek).

---

## Cara Memakai Materi Ini

1. **Jangan diajarkan berurutan nomor 1–11 sekaligus.** Nomor di sini adalah urutan *tata letak layar*, bukan urutan mengajar.
2. **Urutan mengajar yang disarankan** (dari yang paling terlihat hasilnya oleh siswa):

   | Pertemuan | Modul | Alasan |
   |---|---|---|
   | 1 | ⑥ Panggung → ⑨ Daftar Sprite → ③ Kategori → ④ Palet → ⑤ Area Kode → ⑦ Bendera Hijau | Siswa langsung bisa membuat kucing bergerak di menit ke-15 |
   | 2 | ⑧ Info Sprite → ② Tab Costumes/Sounds → ⑩ Backdrop | Mempercantik & menganimasikan |
   | 3 | ① Menu Bar → ⑪ Backpack | Menyimpan, berbagi, dan mengelola proyek |

3. Setiap modul punya struktur sama: **Tujuan → Penjelasan → Rincian → Praktik → Analogi → Kesalahan Umum → Cek Pemahaman**.

---

## Kosakata Inti (untuk ditempel di dinding kelas)

| Istilah | Arti sederhana |
|---|---|
| **Sprite** | Tokoh/objek yang bisa diperintah |
| **Stage / Panggung** | Layar tempat sprite tampil |
| **Backdrop** | Latar belakang panggung |
| **Costume / Kostum** | Tampilan alternatif sprite |
| **Blok** | Satu potong perintah |
| **Script** | Rangkaian blok yang tersambung |
| **Palet** | Rak tempat semua blok tersedia |
| **Area Kode** | Meja kerja tempat blok dirangkai |
| **Bendera Hijau** | Tombol "mulai" |

---

## Catatan Versi

Materi ini disusun dari editor Scratch versi **2026** yang sudah memuat:
- Menu **Settings** (menggantikan ikon globe bahasa)
- Tombol **Debug** / *Debugging Help* — ditambahkan **16 Desember 2024**

Jika sekolah memakai **Scratch Desktop (offline)** atau versi lama, dua elemen di atas bisa berbeda atau tidak ada. Lihat catatan di [01-menu-bar.md](01-menu-bar.md).
