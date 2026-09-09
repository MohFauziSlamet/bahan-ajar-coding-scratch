# Tab Code — Index Penjelasan Blok per Kategori

> Penjelasan **detail setiap blok** di dalam tab **Code** editor Scratch 3.0.
> Satu berkas = satu kategori. Pendamping: [komponen_editor_scratch/](../komponen_editor_scratch/00-index-peta-editor.md) (komponen antarmuka) dan [peta-fitur-scratch.md](../peta-fitur-scratch.md) (peta fitur menyeluruh).

---

## Daftar Berkas

| ● | Kategori | Jumlah blok | Berkas | Tingkat |
|---|---|---|---|---|
| 🔵 | **Motion** (Gerak) | 18 | [tab_code_motion.md](tab_code_motion.md) | Dasar |
| 🟣 | **Looks** (Tampilan) | 21 | [tab_code_looks.md](tab_code_looks.md) | Dasar |
| 🩷 | **Sound** (Suara) | 9 | [tab_code_sound.md](tab_code_sound.md) | Dasar |
| 🟡 | **Events** (Kejadian) | 9 | [tab_code_events.md](tab_code_events.md) | Dasar |
| 🟠 | **Control** (Kontrol) | 11 | [tab_code_control.md](tab_code_control.md) | Menengah |
| 🩵 | **Sensing** (Sensor) | 18 | [tab_code_sensing.md](tab_code_sensing.md) | Menengah |
| 🟢 | **Operators** (Operator) | 18 | [tab_code_operators.md](tab_code_operators.md) | Menengah |
| 🟧 | **Variables** (Variabel & List) | 5 + 12 | [tab_code_variables.md](tab_code_variables.md) | Menengah–Lanjut |
| 🩷 | **My Blocks** (Blok Sendiri) | dibuat sendiri | [tab_code_my_blocks.md](tab_code_my_blocks.md) | Lanjut |

**Total ±125 blok inti.** Blok **ekstensi** (Music, Pen, Text to Speech, dll.) dibahas di [peta-fitur-scratch.md §7](../peta-fitur-scratch.md#7-ekstensi-extensions).

---

## Cara Membaca Berkas Ini

Setiap blok dijelaskan dengan format tetap:

```
### N. `nama blok`
**Bentuk:** stack / reporter / boolean / C-block / hat / cap
**Fungsi:** apa yang dilakukan blok ini
**Parameter:** arti tiap kolom isian & dropdown
**Contoh:** potongan script siap coba
**Catatan:** jebakan, tips, atau perilaku tak terduga
```

### Lambang bentuk blok

| Lambang | Bentuk | Aturan pemasangan |
|---|---|---|
| ⌒ | **Hat** | Hanya di paling atas script |
| ▭ | **Stack** | Ditumpuk atas–bawah |
| ⊂ | **C-block** | Membungkus blok lain |
| ⬭ | **Reporter** | Masuk ke lubang **oval** |
| ⬡ | **Boolean** | Masuk ke lubang **segi enam** |
| ▬ | **Cap** | Paling bawah, tak bisa disambung |

---

## Urutan Mengajar yang Disarankan

Jangan urut abjad kategori. Urutan berikut menaikkan kesulitan secara bertahap:

| Tahap | Kategori | Fokus konsep |
|---|---|---|
| 1 | **Events** (blok `when ⚑ clicked` saja) | Pemicu |
| 2 | **Motion** | Urutan (*sequence*), koordinat |
| 3 | **Looks** | Animasi, kostum |
| 4 | **Sound** | Media & sinkronisasi |
| 5 | **Control** (`repeat`, `forever`, `wait`) | Perulangan |
| 6 | **Sensing** | Input & deteksi |
| 7 | **Control** (`if`, `if-else`) + **Operators** (perbandingan) | Percabangan & logika |
| 8 | **Variables** | Penyimpanan data, skor |
| 9 | **Events** (`broadcast`) | Komunikasi antar objek |
| 10 | **Control** (klon) | Objek dinamis |
| 11 | **Variables** (List) | Struktur data |
| 12 | **My Blocks** | Prosedur & abstraksi |

---

## Catatan Umum yang Berlaku di Semua Kategori

1. **Klik blok di palet = uji coba sekali jalan.** Tidak menambah kode ke proyek.
2. **Blok menempel pada sprite yang sedang dipilih.** Ganti sprite → area kode ikut berganti.
3. **Blok kategori Motion tidak tersedia untuk Stage** karena panggung tidak bisa bergerak.
4. **Lubang angka bisa diisi blok reporter.** `move (pick random 1 to 10) steps` sah dan sangat berguna.
5. **Perbandingan teks tidak membedakan huruf besar-kecil.** `[Halo] = [halo]` bernilai **benar**.
6. Semua nomor urut di Scratch (**item list, huruf pada kata, kostum**) dimulai dari **1**, bukan 0.
