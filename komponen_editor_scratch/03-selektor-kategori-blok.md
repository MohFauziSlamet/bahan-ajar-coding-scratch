# Modul ③ — Selektor Kategori Blok

**Lokasi:** kolom paling kiri di dalam tab **Code**, berupa deretan bulatan warna.
**Estimasi:** 15 menit · **Jenjang:** SD kelas 5 – SMP

```
● Motion      (biru)
● Looks       (ungu)
● Sound       (merah muda)
● Events      (kuning)
● Control     (oranye)
● Sensing     (biru muda)
● Operators   (hijau)
● Variables   (oranye tua)
● My Blocks   (merah muda tua)
─────────────
⊕  Add Extension  (tombol ungu di pojok kiri bawah)
```

---

## Tujuan Pembelajaran

1. Menyebutkan **9 kategori blok** beserta warnanya.
2. Menebak kategori yang tepat untuk sebuah kebutuhan ("aku ingin kucing bersuara → kategori apa?").
3. Menemukan dan mengaktifkan **Ekstensi**.

---

## Penjelasan

Ada ratusan blok di Scratch. Agar tidak membingungkan, blok dikelompokkan jadi **9 kategori berwarna**. Warna bukan hiasan — **warna = identitas fungsi**. Siswa yang hafal warna akan jauh lebih cepat bekerja karena bisa mengenali jenis blok dari jauh tanpa membaca tulisannya.

Klik salah satu bulatan → palet blok di sebelah kanan langsung melompat ke kategori tersebut.

---

## Rincian 9 Kategori

| ● | Kategori | Warna | Pertanyaan yang dijawab | Contoh blok |
|---|---|---|---|---|
| 🔵 | **Motion** | Biru | "Bergerak ke mana?" | `move 10 steps` |
| 🟣 | **Looks** | Ungu | "Terlihat bagaimana?" | `say [Halo!]` |
| 🩷 | **Sound** | Merah muda | "Berbunyi apa?" | `start sound (Meow)` |
| 🟡 | **Events** | Kuning | "Kapan mulai?" | `when ⚑ clicked` |
| 🟠 | **Control** | Oranye | "Berapa kali? Kalau begini bagaimana?" | `repeat 10`, `if ... then` |
| 🩵 | **Sensing** | Biru muda | "Ada apa di sekitarku?" | `touching (mouse-pointer)?` |
| 🟢 | **Operators** | Hijau | "Berapa hasil hitungnya?" | `(1) + (2)`, `pick random` |
| 🟧 | **Variables** | Oranye tua | "Simpan angka/teks di mana?" | `set (skor) to (0)` |
| 🩷 | **My Blocks** | Merah muda tua | "Bisakah aku buat perintah sendiri?" | blok buatan siswa |

> ⚠️ **Motion hanya untuk Sprite.** Bila yang dipilih adalah **Stage**, kategori Motion akan kosong karena panggung tidak bisa bergerak.

### Tombol ⊕ Add Extension

Tombol ungu di pojok kiri bawah. Membuka pustaka **ekstensi** — kategori blok tambahan yang tidak aktif secara default.

| Ekstensi populer di kelas | Isinya |
|---|---|
| **Music** | Blok not, drum, tempo — untuk membuat alat musik |
| **Pen** | Blok menggambar & `stamp` — untuk seni geometris |
| **Text to Speech** | Membuat sprite **berbicara dengan suara** (butuh internet) |
| **Translate** | Menerjemahkan teks (butuh internet) |
| **Video Sensing** | Mendeteksi gerakan lewat kamera |
| **Face Sensing** | Mendeteksi wajah lewat kamera (rilis Okt 2025) |

Ekstensi yang sudah dipilih akan **muncul sebagai kategori baru** di bawah My Blocks, dan ikut tersimpan di dalam berkas proyek.

---

## Praktik (8 menit)

**Permainan "Tebak Warna" (5 menit)**
Guru menyebut kebutuhan, siswa menyebut **warna + kategori** secepatnya:

| Guru berkata | Jawaban |
|---|---|
| "Kucing berjalan maju" | Biru — Motion |
| "Kucing bilang halo" | Ungu — Looks |
| "Mulai saat bendera diklik" | Kuning — Events |
| "Ulangi 10 kali" | Oranye — Control |
| "Apakah menyentuh tepi?" | Biru muda — Sensing |
| "Tambah 5 + 3" | Hijau — Operators |
| "Simpan skor" | Oranye tua — Variables |

**Aktivitas Ekstensi (3 menit)**
Klik ⊕ → pilih **Music** → amati kategori baru muncul → tarik blok `play drum` → klik blok tersebut → dengarkan bunyinya.

---

## Analogi untuk Siswa

> Selektor kategori itu seperti **daftar rak di perpustakaan**. Kamu tidak perlu membongkar seluruh perpustakaan untuk cari buku resep — cukup pergi ke rak "Masakan". Warna = papan nama rak.

---

## Kesalahan Umum

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Menggulir palet mencari blok satu per satu | Boros waktu | Latih klik kategori, jangan scroll |
| Mencari blok Motion saat Stage dipilih | Palet tampak kosong/aneh | Cek dulu: sprite atau Stage yang aktif? |
| Mengaktifkan banyak ekstensi sekaligus | Palet penuh & membingungkan | Aktifkan hanya yang dipakai |
| Mengira ekstensi harus dipasang tiap kali | Kebingungan | Jelaskan bahwa ekstensi ikut tersimpan di proyek |

---

## Cek Pemahaman

1. Sebutkan warna kategori **Control** dan satu blok di dalamnya.
2. Kamu ingin sprite berhenti bila menyentuh tepi. Kategori mana yang kamu buka lebih dulu?
3. Mengapa kategori Motion kosong ketika Stage dipilih?
4. Di mana letak tombol untuk menambah ekstensi Music?

<details>
<summary>Kunci jawaban</summary>

1. Oranye; contoh: `repeat`, `forever`, `if ... then`, `wait`.
2. **Sensing** (untuk mendeteksi `touching edge?`), lalu dipasang ke dalam blok **Control** `if ... then`.
3. Karena Stage tidak bisa bergerak — panggung selalu diam.
4. Tombol ⊕ **Add Extension** di pojok kiri bawah editor.
</details>
