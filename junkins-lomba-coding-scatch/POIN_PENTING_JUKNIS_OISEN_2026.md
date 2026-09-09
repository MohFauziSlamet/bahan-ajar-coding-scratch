# PANDUAN POIN PENTING & STRATEGI LOMBA CODING SCRATCH OISEN 2026
**Dokumen Rujukan:** *Juknis Coding Visual Scratch - OISEN 2026 (MGMP Informatika & KKA SMP Kab. Malang)*  
**Tema Game:** *"PERJUANGAN" – Menyongsong Hari Pahlawan (10 November)*  
**Target Pembaca:** Guru Pembimbing & Siswa Peserta Lomba

---

## 1. Identitas & Ketentuan Pokok Lomba

| Parameter | Ketentuan Juknis |
| :--- | :--- |
| **Peserta** | Murid aktif SMP/sederajat (Individu, 1 perwakilan resmi per sekolah). |
| **Waktu Pelaksanaan** | Akhir Oktober 2026 (Durasi pengerjaan: **4 jam / 240 menit**). |
| **Platform** | Scratch Versi Online (`scratch.mit.edu`) dengan internet dari panitia. |
| **Perangkat** | Wajib menggunakan komputer lab panitia. **Dilarang bawa laptop sendiri**. |
| **Aksesoris Tambahan** | **Boleh membawa Keyboard & Mouse pribadi** untuk kenyamanan. |

---

## 2. Poin Krusial untuk GURU PEMBIMBING (Strategi & Manajemen)

### A. Regulasi Logistik & Anti-Diskualifikasi
1. **Dilarang Membawa Flashdisk / Media Penyimpanan:**
   * Pastikan siswa tidak membawa flashdisk, hard disk, atau media yang berisi aset/proyek jadi. Seluruh proyek harus dibuat **murni dari nol (*from scratch*)** di lokasi lomba.
2. **Siapkan Keyboard & Mouse Favorit Siswa:**
   * Sangat disarankan membekali siswa dengan mouse dan keyboard yang biasa dipakai latihan agar kontrol mekanik (klik tembak, gerak tombol) lebih lincah dan nyaman.
3. **Kemandirian Penuh Siswa:**
   * Selama 240 menit lomba berlangsung, guru dilarang berkomunikasi atau memberi bantuan teknis kepada siswa. Siswa harus 100% mandiri.

### B. Pola Pelatihan & Strategi Bobot Nilai
* **70% Nilai Bertumpu pada Fungsionalitas:**
  * Logika & Kompleksitas: **25%**
  * Kelengkapan 4 Babak, Skor & Nyawa: **20%**
  * Kesesuaian Tema & Alur Cerita: **20%**
  * Bebas Bug & Kelancaran: **10%**
* **Fokuskan Latihan pada Kecepatan & Ketahanan (Simulasi 4 Jam):**
  * Siswa harus dibiasakan menyelesaikan 4 babak fungsional dalam waktu kurang dari 3 jam, sehingga 1 jam terakhir bisa digunakan untuk audio, efek visual, dan uji coba bebas bug.

---

## 3. Poin Krusial untuk SISWA PESERTA (Teknis & Eksekusi)

### A. Wajib Menyelesaikan Alur 4 Babak
Juknis menyarankan 4 babak berkesinambungan. Jika babak tidak lengkap, nilai kelengkapan (bobot 20%) akan dipotong proporsional oleh juri.

1. **Babak 1 (Awal Kemerdekaan):**
   * *Sprite:* Pejuang berotot tanpa baju, bersenjatakan bambu runcing.
   * *Misi:* Melawan pasukan infanteri Belanda.
   * *Latar:* Suasana perjuangan awal kemerdekaan (desa/hutan bambu).
2. **Babak 2 (Pertempuran Surabaya):**
   * *Sprite:* Pejuang berseragam TNI.
   * *Misi:* Menyelamatkan Kota Surabaya dari penjajah.
   * *Latar:* Suasana Pertempuran Surabaya (Jembatan Merah / Hotel Yamato).
3. **Babak 3 (Pertempuran Udara TNI AU):**
   * *Sprite:* Pejuang TNI Angkatan Udara (AU) / Pesawat tempur.
   * *Misi:* Pertempuran udara melawan armada pesawat Belanda.
   * *Latar:* Suasana langit pertempuran udara (*scrolling sky*).
4. **Babak 4 ("Perang Bintang" - Masa Depan):**
   * *Sprite:* Pejuang TNI AU mengendarai jet tempur luar angkasa.
   * *Misi:* Pertempuran di angkasa luar menjaga kedaulatan bangsa.
   * *Latar:* Angkasa luar berbintang (*galaxy/nebula*).

### B. Syarat Wajib di Setiap Babak
* **Sistem Skor/Poin:** Harus bertambah saat mengalahkan musuh/menyelesaikan target misi.
* **Sistem Nyawa (Lives):** Harus berkurang jika terkena musuh/tembakan, dan memicu *Game Over* jika nyawa = 0.
* **Kombinasi Kontrol:** Manfaatkan **Keyboard** (panah/WASD/spasi) dan **Mouse** (klik tembak/bidik) secara interaktif.

### C. Aturan Sumber Aset Visual (Hanya 2 Opsi)
1. **Dibuat Sendiri dengan AI Image Generator:** Menggunakan tools AI saat lomba berjalan (misal: Bing Image Creator / Canva / Leonardo / Recraft).
2. **Pustaka Bawaan Scratch Library.**
*(Dilarang mengambil gambar sembarangan dari Google Search atau menggunakan aset siap pakai dari rumah)*.

### D. Kerapian Kode Blok (*Clean Code*)
* Jangan biarkan blok kode menumpuk acak di satu area.
* Gunakan **My Blocks (Blok Kustom)** untuk memisahkan fungsi gerak (*Movement*), serangan (*Attack*), pemunculan musuh (*Spawner*), dan transisi level.
* Tambahkan komentar pada blok penting agar mudah dinilai oleh juri.

---

## 4. Matriks Pembagian Bobot Penilaian Juri (Total 100%)

```
┌───────────────────────────────────────────────────────────────┐
│ Logika & Algoritma (25%)                                      │
├───────────────────────────────────────────────────────────────┤
│ Kesesuaian Tema "Perjuangan" & Kreativitas (20%)              │
├───────────────────────────────────────────────────────────────┤
│ Kelengkapan 4 Babak, Sistem Skor & Nyawa (20%)                │
├───────────────────────────────────────────────────────────────┤
│ User Experience (UX), Desain Visual & Efek Suara (15%)        │
├───────────────────────────────────────────────────────────────┤
│ Fungsionalitas & Bebas Bug (10%)                              │
├───────────────────────────────────────────────────────────────┤
│ Presentasi & Kerapian Dokumentasi Kode (10%)                  │
└───────────────────────────────────────────────────────────────┘
```

---

## 5. Tabel "DOs & DON'Ts" (Panduan Praktis Siswa)

| ✅ WAJIB DILAKUKAN (DOs) | ❌ DILARANG KERAS (DON'Ts) |
| :--- | :--- |
| Hadir 30 menit sebelum acara dengan seragam sekolah rapi. | Membawa laptop sendiri atau flashdisk dari rumah. |
| Membawa mouse & keyboard sendiri untuk kenyamanan bermain. | Bertanya / meminta bantuan guru saat lomba berlangsung. |
| Memastikan Skor dan Nyawa berfungsi normal di 4 babak. | Menghabiskan waktu > 40 menit hanya untuk mencari gambar AI. |
| Mengatur reset variabel saat tombol bendera hijau diklik. | Menggunakan gambar mengandung unsur SARA / hak cipta terlarang. |
| Memasukkan efek suara (*Sound Effects*) & tombol navigasi. | Membiarkan blok kode berantakan tanpa pengelompokan. |
| Menjelaskan logika kode dengan percaya diri di depan juri. | Mengabaikan layar kondisi Menang (*Win*) dan Kalah (*Game Over*). |

---

## 6. Format Presentasi Finalis di Depan Juri (Total 5 Menit)

Jika siswa terpilih menjadi finalis, alokasi waktu adalah:
* **2 Menit Presentasi Singkat (Pitching):**
  1. *Perkenalan Diri & Judul Game* (15 detik).
  2. *Penjelasan Alur Cerita 4 Babak Tema Perjuangan* (45 detik).
  3. *Demonstrasi Gameplay & Fitur Logika Blok Unggulan* (45 detik).
  4. *Pesan Moral / Nilai Kepahlawanan* (15 detik).
* **3 Menit Tanya Jawab Teknis dengan Dewan Juri:**
  * Juri biasanya menanyakan: bagaimana sistem transisi babak, cara kerja kloning musuh, penanganan tabrakan (*collision detection*), dan struktur variabel game.
