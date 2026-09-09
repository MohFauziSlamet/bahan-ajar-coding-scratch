# Modul ⑪ — Backpack (Tas Ransel)

**Lokasi:** bilah abu-abu paling bawah editor, bertuliskan **Backpack**.
**Estimasi:** 10 menit · **Jenjang:** SD kelas 6 – SMP (materi lanjutan)

```
╔═══════════════════════════════════════════════════════╗
║                      Backpack   ▲                     ║  ← klik untuk membuka
╚═══════════════════════════════════════════════════════╝
```

---

## Tujuan Pembelajaran

1. Menjelaskan fungsi Backpack sebagai tempat penyimpanan lintas proyek.
2. Memasukkan script/sprite/kostum/suara ke Backpack dan memakainya di proyek lain.
3. Menyebutkan syarat pemakaian Backpack.

---

## Penjelasan

Backpack adalah **tas penyimpanan pribadi yang bisa dibawa antar proyek**. Isi yang dimasukkan ke sini tetap ada meskipun kamu menutup proyek, membuka proyek lain, bahkan berganti komputer — karena tersimpan di akun Scratch.

Klik bilah **Backpack** untuk membuka/menutup panelnya.

### Yang bisa disimpan

| Jenis | Contoh |
|---|---|
| **Script** | Mesin lompat (*platformer engine*), kode kontrol panah |
| **Sprite** | Tokoh buatan sendiri lengkap dengan kode & kostumnya |
| **Costume** | Gambar hasil karya sendiri |
| **Sound** | Rekaman suara sendiri |

### Cara pakai

| Aksi | Cara |
|---|---|
| **Menyimpan** | Tarik script/sprite/kostum/suara **ke dalam** bilah Backpack |
| **Mengambil** | Tarik item **keluar** dari Backpack ke area kode atau daftar sprite |
| **Menghapus** | Klik kanan item di Backpack → *delete* |

> Penting: mengambil item dari Backpack berarti **menyalinnya** — item tetap tersimpan di Backpack dan bisa dipakai berkali-kali di banyak proyek.

---

## Syarat & Batasan

| Syarat/Batas | Keterangan |
|---|---|
| **Harus login** | Backpack terikat pada akun Scratch |
| **Hanya di editor online** | **Tidak tersedia** di Scratch Desktop (offline) |
| Privat | Backpack orang lain tidak bisa diakses |
| Kapasitas | Tidak ada batas resmi, tetapi bila terlalu penuh muncul pesan *"Error loading backpack"* |

⚠️ **Implikasi untuk sekolah:** bila lab memakai Scratch offline atau siswa tidak punya akun, Backpack **tidak bisa dipakai**. Gunakan alternatif ini:

| Kebutuhan | Alternatif tanpa Backpack |
|---|---|
| Memindahkan sprite antar proyek | Klik kanan sprite → **export** (`.sprite3`) → di proyek lain **Upload Sprite** |
| Menyalin kode antar sprite dalam satu proyek | **Tarik tumpukan blok ke kartu sprite tujuan** di daftar sprite |
| Menyalin kode antar proyek | Buka dua proyek di dua tab, atau simpan sprite `.sprite3` |

> 💡 Trik "tarik blok ke kartu sprite lain" sangat berguna dan sering tidak diketahui — blok akan tersalin ke sprite tujuan (blok asli tetap di tempatnya).

---

## Praktik (7 menit)

1. Susun script berikut di area kode:
   ```
   when ⚑ clicked
   forever
     if <key (right arrow) pressed?> then
       change x by (10)
     if <key (left arrow) pressed?> then
       change x by (-10)
   ```
2. Buka bilah **Backpack**, **tarik seluruh script** ke dalamnya.
3. Buat proyek baru (**File > New**).
4. Buka Backpack, **tarik script tadi keluar** ke area kode.
5. Jalankan — kontrol panah langsung bekerja tanpa menyusun ulang.
6. **Diskusi:** berapa waktu yang dihemat kalau kode ini dipakai di 5 proyek berbeda?

---

## Analogi untuk Siswa

> Backpack adalah **tas ransel yang selalu kamu bawa**. Kalau kamu membuat alat yang berguna di satu proyek, masukkan ke tas — di proyek berikutnya tinggal keluarkan, tak perlu membuat ulang dari nol. Isi tas tidak berkurang saat dipakai; kamu selalu mengambil salinannya.

---

## Nilai Pendidikan

Backpack adalah cara paling nyata memperkenalkan konsep **penggunaan ulang kode** (*code reuse*) — prinsip yang di dunia kerja muncul sebagai *library*, *module*, dan *package*.

| Konsep Scratch | Padanan di dunia profesional |
|---|---|
| Menyimpan script ke Backpack | Membuat *library* / *module* |
| Mengambil dari Backpack | *Import* library |
| Export sprite `.sprite3` | Membagikan *package* |

---

## Kesalahan Umum

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Mencari Backpack di Scratch offline | Bingung karena tidak ada | Jelaskan syarat online + login |
| Mengira item hilang setelah ditarik keluar | Ragu memakai | Tegaskan: yang keluar adalah **salinan** |
| Menyimpan puluhan item sembarangan | Error loading backpack | Bersihkan berkala, simpan yang benar-benar berguna |
| Memakai Backpack untuk mengumpulkan tugas | Guru tidak bisa melihat | Pengumpulan tetap lewat **Share / studio kelas / berkas `.sb3`** |

---

## Cek Pemahaman

1. Sebutkan 4 jenis benda yang bisa disimpan di Backpack.
2. Apakah Backpack tersedia di Scratch Desktop (offline)? Jelaskan.
3. Kamu menarik satu script keluar dari Backpack. Apakah script itu hilang dari Backpack?
4. Tanpa Backpack, bagaimana cara memindahkan sprite lengkap ke proyek lain?

<details>
<summary>Kunci jawaban</summary>

1. Script, sprite, costume (kostum), dan sound (suara).
2. Tidak. Backpack hanya tersedia di editor online dan mengharuskan pengguna login, karena isinya tersimpan di akun Scratch.
3. Tidak hilang — yang keluar adalah salinannya, item aslinya tetap tersimpan.
4. Klik kanan sprite → **export** menjadi berkas `.sprite3`, lalu di proyek tujuan gunakan **Upload Sprite**.
</details>
