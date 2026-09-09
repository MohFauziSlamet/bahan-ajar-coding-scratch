# Modul ⑦ — Kontrol Panggung (Bendera Hijau, Stop, Ukuran Tampilan)

**Lokasi:** baris tombol tepat di atas panggung.
**Estimasi:** 10 menit · **Jenjang:** SD kelas 5 – SMP

```
   ⚑        ⛔                              [▫] [▪] [▦]   [⛶]
bendera    stop                          tata letak &   layar
 hijau                                   ukuran panggung penuh
```

---

## Tujuan Pembelajaran

1. Menjalankan dan menghentikan proyek dengan benar.
2. Membedakan **menjalankan proyek** (bendera hijau) dan **menjalankan satu script** (klik blok).
3. Mengatur ukuran tampilan panggung sesuai kebutuhan kerja.
4. Menampilkan proyek dalam **mode layar penuh** saat presentasi.

---

## Rincian

### 1. ⚑ Bendera Hijau — *Tombol Mulai*

Menjalankan **semua script** yang diawali blok `when ⚑ clicked`, di **semua sprite**, secara bersamaan.

| Yang perlu dipahami siswa | Penjelasan |
|---|---|
| Bendera hijau **bukan tombol ajaib** | Ia hanya memicu script yang punya blok kuning `when ⚑ clicked`. Tanpa blok itu, tidak ada yang terjadi |
| Bisa memicu banyak script sekaligus | Semua sprite ikut bereaksi — inilah *paralelisme* |
| **Shift + klik** bendera hijau | Mengaktifkan **Turbo Mode** (proyek berjalan sangat cepat) |

### 2. ⛔ Stop (segi delapan merah)

Menghentikan **seluruh** script yang sedang berjalan, sama seperti blok `stop (all)`.

> Ajarkan sebagai **tombol darurat**: kalau proyek "kesurupan" (kucing berputar tak berhenti karena `forever`), tekan stop.

### 3. Tombol Tata Letak & Ukuran Panggung

Deretan tombol persegi di kanan atas untuk mengatur seberapa besar panggung ditampilkan.

| Mode | Kegunaan |
|---|---|
| **Panggung kecil** | Panggung mengecil, **area kode melebar** — dipakai saat sedang banyak menyusun blok |
| **Panggung normal/besar** | Panggung penuh 480×360 — dipakai saat menguji tampilan permainan |
| **Fokus panggung** | Menyembunyikan/mempersempit area kode agar panggung dominan |

> 📝 **Catatan untuk guru:** ikon dan jumlah tombol tata letak ini **berubah antar pembaruan Scratch**. Arahkan kursor ke tiap tombol (muncul keterangan) dan cocokkan dengan versi yang dipakai sekolah sebelum mengajar.

⚠️ Yang berubah **hanya ukuran tampilan di editor** — ukuran panggung sesungguhnya tetap 480×360 piksel, dan koordinat sprite tidak berubah sama sekali.

### 4. ⛶ Layar Penuh (*Full Screen*)

Panggung memenuhi seluruh layar; palet dan area kode disembunyikan. Tekan **Esc** atau klik ikon keluar untuk kembali.

Dipakai saat:
- Presentasi karya di depan kelas
- Menguji permainan seperti pemain sungguhan
- Pameran/gelar karya

---

## Praktik (6 menit)

1. Susun script berikut lalu klik **bendera hijau**:
   ```
   when ⚑ clicked
   forever
     move (5) steps
     if on edge, bounce
   ```
2. Tekan **⛔ Stop** untuk menghentikan. Diskusikan mengapa perlu tombol stop pada `forever`.
3. Hapus blok `when ⚑ clicked` dari script tersebut, lalu klik bendera hijau lagi → tidak terjadi apa-apa. **Diskusi:** mengapa?
4. Coba tiap tombol ukuran panggung, amati area kode melebar/menyempit.
5. Masuk **layar penuh**, jalankan, lalu tekan **Esc**.

---

## Analogi untuk Siswa

> Bendera hijau adalah **peluit wasit** — semua pemain yang sudah bersiap (punya blok `when ⚑ clicked`) langsung bergerak. Pemain yang tidak mendengar peluit (tidak punya blok itu) tetap diam saja.
>
> Tombol stop adalah **peluit panjang tanda pertandingan usai**.

---

## Kesalahan Umum

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Menekan bendera hijau padahal script tanpa hat block | "Tidak terjadi apa-apa" → siswa mengira Scratch rusak | Aturan: **tiap script diawali blok kuning** |
| Turbo Mode aktif karena Shift terpencet | Proyek berjalan super cepat | Cek menu **Edit** → matikan Turbo Mode |
| Mengira mengecilkan panggung mengecilkan sprite | Salah paham koordinat | Tegaskan: hanya tampilan yang berubah |
| Tidak tahu keluar dari layar penuh | Panik | Ajarkan tombol **Esc** |
| Lupa tombol stop saat memakai `forever` | Komputer terasa lambat | Biasakan menekan stop setelah menguji |

---

## Cek Pemahaman

1. Kamu klik bendera hijau tapi tidak terjadi apa pun. Sebutkan penyebab paling mungkin.
2. Apa yang terjadi bila kamu menekan **Shift + klik** bendera hijau?
3. Apakah mengecilkan tampilan panggung mengubah nilai koordinat sprite?
4. Bagaimana cara keluar dari mode layar penuh?

<details>
<summary>Kunci jawaban</summary>

1. Script belum diawali blok `when ⚑ clicked` (tidak ada hat block Events).
2. Turbo Mode aktif — proyek berjalan jauh lebih cepat.
3. Tidak. Panggung tetap 480×360 dan koordinat tidak berubah; hanya ukuran tampilannya di editor.
4. Tekan tombol **Esc** atau klik ikon keluar layar penuh.
</details>
