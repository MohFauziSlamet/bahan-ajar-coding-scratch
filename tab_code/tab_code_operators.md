# 🟢 Operators (Operator) — 18 Blok

**Warna:** Hijau · **Fungsi umum:** menghitung, membandingkan, mengolah teks, dan menyusun logika
**Berlaku untuk:** Sprite dan Stage.

> Semua blok di kategori ini berbentuk **reporter ⬭** atau **boolean ⬡** — artinya **tidak bisa berdiri sendiri**. Blok-blok ini harus dimasukkan ke dalam lubang blok lain.

---

## Ringkasan Cepat

| Kelompok | Blok | Bentuk |
|---|---|---|
| **Aritmetika** | `+`, `-`, `*`, `/`, `mod`, `round`, `[abs] of ()` | ⬭ reporter |
| **Acak** | `pick random () to ()` | ⬭ reporter |
| **Perbandingan** | `<`, `=`, `>` | ⬡ boolean |
| **Logika** | `and`, `or`, `not` | ⬡ boolean |
| **Teks** | `join`, `letter () of`, `length of`, `contains ()?` | ⬭ / ⬡ |

---

## A. Aritmetika (7 blok)

### 1. `(() + ())` — Penjumlahan

![01-tambah](assets/operators/tunggal/01-tambah.png)

**Artinya:** Menjumlah dua angka.
**Bentuk:** ⬭ reporter
**Contoh:** `set (total) to ((harga) + (pajak))`

### 2. `(() - ())` — Pengurangan

![02-kurang](assets/operators/tunggal/02-kurang.png)

**Artinya:** Mengurangi angka pertama dengan angka kedua.
**Contoh:** `set (sisa) to ((nyawa) - (1))`

### 3. `(() * ())` — Perkalian

![03-kali](assets/operators/tunggal/03-kali.png)

**Artinya:** Mengalikan dua angka.
**Contoh:** `set (luas) to ((panjang) * (lebar))`

### 4. `(() / ())` — Pembagian

![04-bagi](assets/operators/tunggal/04-bagi.png)

**Artinya:** Membagi angka pertama dengan angka kedua.
**Catatan:** Pembagian dengan 0 menghasilkan `Infinity`, bukan pesan kesalahan. Hasilnya bisa desimal panjang — bungkus dengan `round` bila perlu dirapikan.

---

### 5. `(() mod ())` — Sisa bagi

![03-mod](assets/operators/03-mod.png)

**Artinya:** Memberi SISA pembagian. Berguna untuk mengecek angka genap atau ganjil.
**Bentuk:** ⬭ reporter
**Fungsi:** Melaporkan **sisa** pembagian.
**Contoh:** `(7) mod (2)` = `1`.
**Kegunaan utama:**

| Pola | Kegunaan |
|---|---|
| `if <((angka) mod (2)) = (0)>` | Menentukan bilangan **genap/ganjil** |
| `set (x) to (((x) + (10)) mod (480))` | Membuat objek **muncul lagi dari sisi seberang** |
| `if <((detik) mod (5)) = (0)>` | Melakukan sesuatu **setiap 5 detik** |

**Catatan:** Blok yang paling sering diabaikan padahal sangat berguna. Wajib diajarkan bersama materi bilangan genap-ganjil di Matematika.

---

### 6. `(round ())` — Pembulatan

![04-round](assets/operators/04-round.png)

**Artinya:** Membulatkan angka ke bilangan bulat terdekat.
**Bentuk:** ⬭ reporter
**Fungsi:** Membulatkan ke bilangan bulat terdekat.
**Catatan:** Nilai tepat `0.5` dibulatkan **ke atas** (`round (2.5)` = `3`). Wajib dipakai saat menampilkan hasil pembagian agar tidak muncul angka seperti `3.3333333333`.

---

### 7. `([abs ▾] of ())` — Fungsi matematika

![05-abs-of](assets/operators/05-abs-of.png)

**Artinya:** Kumpulan fungsi matematika: nilai mutlak, akar, pembulatan ke bawah, dan lainnya.
**Bentuk:** ⬭ reporter
**Fungsi:** Menerapkan salah satu dari **14 fungsi matematika**.

| Pilihan | Arti | Contoh |
|---|---|---|
| `abs` | Nilai mutlak | `abs of (-5)` = 5 |
| `floor` | Pembulatan **ke bawah** | `floor of (3.9)` = 3 |
| `ceiling` | Pembulatan **ke atas** | `ceiling of (3.1)` = 4 |
| `sqrt` | Akar kuadrat | `sqrt of (16)` = 4 |
| `sin`, `cos`, `tan` | Fungsi trigonometri (satuan **derajat**) | `sin of (90)` = 1 |
| `asin`, `acos`, `atan` | Invers trigonometri | — |
| `ln`, `log` | Logaritma natural & basis 10 | `log of (100)` = 2 |
| `e ^`, `10 ^` | Perpangkatan | `10 ^ of (3)` = 1000 |

**Catatan:** Scratch memakai **derajat**, bukan radian — memudahkan siswa SMP. Untuk gerak melingkar:
```
go to x: ((100) * ([cos] of (sudut))) y: ((100) * ([sin] of (sudut)))
```
**Perhatian:** tidak ada blok pangkat umum (`x^y`). Untuk kuadrat gunakan `(x) * (x)`.

---

## B. Bilangan Acak

### 8. `(pick random (1) to (10))`

![06-pick-random](assets/operators/06-pick-random.png)

**Artinya:** Mengambil satu angka acak di antara dua batas itu.
**Bentuk:** ⬭ reporter
**Fungsi:** Menghasilkan bilangan acak antara dua nilai (termasuk kedua ujungnya).
**Contoh:**
```
go to x: (pick random (-240) to (240)) y: (pick random (-180) to (180))
```
**Catatan penting:** Bila **kedua** input bilangan bulat, hasilnya bilangan bulat. Bila salah satu ditulis desimal (mis. `1.0`), hasilnya bisa desimal. Ini kerap membingungkan siswa yang ingin angka bulat.

**Kegunaan:** posisi acak, kemunculan musuh, dadu, soal kuis acak, warna acak.

---

## C. Perbandingan (3 blok)

### 9. `(() < ())` — Kurang dari

![05-kurang-dari](assets/operators/tunggal/05-kurang-dari.png)

**Artinya:** Bertanya: apakah nilai kiri lebih kecil dari nilai kanan?
### 10. `(() = ())` — Sama dengan

![06-sama-dengan](assets/operators/tunggal/06-sama-dengan.png)

**Artinya:** Bertanya: apakah kedua nilai sama persis?
### 11. `(() > ())` — Lebih dari

![07-lebih-dari](assets/operators/tunggal/07-lebih-dari.png)

**Artinya:** Bertanya: apakah nilai kiri lebih besar dari nilai kanan?

**Bentuk:** ⬡ boolean — hanya bisa dipasang di lubang segi enam (`if`, `repeat until`, `wait until`, `and/or/not`).

**Contoh:**
```
if <(skor) > (100)> then
  say [Menang!]
```

**Catatan penting:**
- **Tidak ada blok `≥` atau `≤`.** Solusinya:

  | Yang diinginkan | Ditulis sebagai |
  |---|---|
  | `skor ≥ 10` | `<not <(skor) < (10)>>` atau `<(skor) > (9)>` (untuk bilangan bulat) |
  | `skor ≤ 10` | `<not <(skor) > (10)>>` |

- Perbandingan teks **tidak membedakan huruf besar-kecil**: `[Halo] = [halo]` bernilai **benar**. Berguna untuk kuis agar jawaban siswa tidak salah hanya karena kapitalisasi.
- `<` dan `>` pada teks membandingkan urutan abjad.

---

## D. Logika (3 blok)

### 12. `(<> and <>)` — DAN

![08-and](assets/operators/08-and.png)

**Artinya:** Hasilnya benar HANYA kalau kedua syarat benar.
**Fungsi:** Benar **hanya bila keduanya benar**.
**Contoh:**
```
if <<(skor) > (50)> and <(nyawa) > (0)>> then
  say [Lanjut ke level 2]
```

### 13. `(<> or <>)` — ATAU

![09-or](assets/operators/09-or.png)

**Artinya:** Hasilnya benar kalau SALAH SATU syarat saja sudah benar.
**Fungsi:** Benar bila **salah satu (atau keduanya)** benar.
**Contoh:**
```
if <<touching (Musuh)?> or <touching (Duri)?>> then
  change (nyawa) by (-1)
```

### 14. `(not <>)` — BUKAN

![10-not](assets/operators/10-not.png)

**Artinya:** Membalik jawaban: yang benar jadi salah, yang salah jadi benar.
**Fungsi:** Membalik nilai — benar menjadi salah, salah menjadi benar.
**Contoh:**
```
wait until <not <key (space) pressed?>>
```
→ menunggu sampai tombol spasi **dilepas**.

**Tabel kebenaran (bagus untuk ditempel di kelas):**

| A | B | A **and** B | A **or** B | **not** A |
|---|---|---|---|---|
| Benar | Benar | Benar | Benar | Salah |
| Benar | Salah | Salah | Benar | Salah |
| Salah | Benar | Salah | Benar | Benar |
| Salah | Salah | Salah | Salah | Benar |

**Catatan:** Blok logika bisa **disarangkan** untuk kondisi rumit — tetapi bila sudah lebih dari 3 tingkat, lebih baik dipecah memakai variabel agar tetap terbaca.

---

## E. Pengolahan Teks (4 blok)

### 15. `(join [apple] [banana])`

![11-join](assets/operators/11-join.png)

**Artinya:** Menyambung dua teks jadi satu, misalnya kata Skor ditambah angkanya.
**Bentuk:** ⬭ reporter
**Fungsi:** Menyambung dua teks menjadi satu.
**Contoh:**
```
say (join [Skor kamu: ] (skor))
```
**Catatan:** Hanya menerima **dua** masukan. Untuk menyambung tiga bagian, sarangkan:
```
join [Halo, ] (join (nama) [!])
```
Blok ini **wajib** untuk menampilkan kalimat yang memuat variabel — salah satu blok paling sering dipakai.

---

### 16. `(letter (1) of [apple])`

![12-letter-of](assets/operators/12-letter-of.png)

**Artinya:** Mengambil satu huruf pada urutan tertentu dari sebuah teks.
**Bentuk:** ⬭ reporter
**Fungsi:** Mengambil satu huruf pada posisi tertentu.
**Contoh:** `letter (1) of [apple]` = `a`.
**Catatan:** Penomoran dimulai dari **1**, bukan 0 (berbeda dari kebanyakan bahasa pemrograman — sebutkan ini saat siswa nanti belajar Python).
**Contoh — mengeja kata satu per satu:**
```
set (i) to (1)
repeat (length of (kata))
  say (letter (i) of (kata)) for (0.5) seconds
  change (i) by (1)
```

---

### 17. `(length of [apple])`

![13-length-of](assets/operators/13-length-of.png)

**Artinya:** Menghitung ada berapa huruf dalam sebuah teks.
**Bentuk:** ⬭ reporter
**Fungsi:** Menghitung jumlah **karakter** dalam teks (spasi ikut dihitung).
**Contoh:** `length of [apple]` = `5`.
**Catatan:** Jangan tertukar dengan `length of (list)` di kategori Variables yang menghitung **jumlah item**, bukan huruf.

---

### 18. `<[apple] contains [a]?>`

![14-contains](assets/operators/14-contains.png)

**Artinya:** Bertanya: apakah teks itu memuat huruf atau kata tertentu?
**Bentuk:** ⬡ boolean
**Fungsi:** Bernilai benar bila teks pertama memuat teks kedua.
**Contoh — kuis yang memaklumi jawaban panjang:**
```
if <(answer) contains [jakarta]?> then
  say [Benar!]
```
**Catatan:** Tidak membedakan huruf besar-kecil. Sangat berguna untuk kuis agar jawaban "Kota Jakarta" tetap dianggap benar.

---

## Konsep Kunci: Blok Bersarang (Nesting)

Kekuatan sesungguhnya kategori ini muncul saat blok **dimasukkan ke dalam blok lain**:

```
say (join [Rata-rata: ] (round (((a) + (b)) / (2))))
```

Cara membacanya dari **dalam ke luar** — ajarkan siswa membongkarnya lapis demi lapis:

| Lapis | Bagian | Hasil |
|---|---|---|
| 1 | `(a) + (b)` | jumlah dua nilai |
| 2 | `... / (2)` | rata-rata (mungkin desimal panjang) |
| 3 | `round (...)` | dibulatkan |
| 4 | `join [Rata-rata: ] (...)` | menjadi kalimat |
| 5 | `say (...)` | ditampilkan |

💡 **Cara mengajar:** minta siswa menyusun dari **dalam ke luar** — bangun `(a)+(b)` dulu di area kosong, uji dengan mengkliknya, baru bungkus lapis berikutnya.

---

## Kesalahan Umum

| Kesalahan | Gejala | Perbaikan |
|---|---|---|
| Mencari blok `≥` / `≤` | Tidak ketemu | Pakai `not` atau geser nilainya satu angka |
| Menampilkan variabel tanpa `join` | Hanya angka polos, tanpa keterangan | Bungkus dengan `join` |
| Hasil pembagian panjang sekali | `3.3333333333` | Bungkus dengan `round` |
| Mengira `letter` mulai dari 0 | Huruf meleset satu | Tegaskan penomoran mulai dari 1 |
| `pick random` menghasilkan desimal | Angka tidak bulat | Pastikan kedua input ditulis bilangan bulat |
| Tertukar `and` dan `or` | Kondisi tidak pernah/selalu terpenuhi | Gunakan tabel kebenaran |
| Blok logika bersarang terlalu dalam | Tidak terbaca dan sulit di-debug | Pecah memakai variabel bantu |
| Tertukar `length of [teks]` dengan `length of (list)` | Angka tidak sesuai harapan | Perhatikan warna blok: hijau = teks, oranye = list |

---

## Latihan Bertingkat

| Level | Tantangan | Blok kunci |
|---|---|---|
| ⭐ | Kalkulator penjumlahan 2 bilangan | `ask`, `+`, `join` |
| ⭐ | Lempar dadu | `pick random (1) to (6)` |
| ⭐⭐ | Tentukan bilangan genap atau ganjil | `mod`, `=`, `if-else` |
| ⭐⭐ | Kuis dengan skor & pesan lulus/tidak | `=`, `>`, `and` |
| ⭐⭐ | Sprite bergerak ke posisi acak | `pick random` |
| ⭐⭐⭐ | Mengeja kata satu huruf per detik | `letter () of`, `length of`, `repeat` |
| ⭐⭐⭐ | Gerak melingkar mengelilingi titik pusat | `sin`, `cos` |

---

## Cek Pemahaman

1. Blok apa yang dipakai untuk mengecek bilangan genap atau ganjil? Tuliskan kondisinya.
2. Scratch tidak punya blok `≥`. Bagaimana menuliskan "skor ≥ 10"?
3. Apa hasil `letter (3) of [Scratch]`?
4. Kamu ingin menampilkan `Skor: 25`. Blok apa yang dibutuhkan?
5. Apakah `[Jakarta] = [jakarta]` bernilai benar atau salah?

<details>
<summary>Kunci jawaban</summary>

1. `mod` — kondisinya `<((angka) mod (2)) = (0)>` untuk genap.
2. `<not <(skor) < (10)>>`, atau untuk bilangan bulat cukup `<(skor) > (9)>`.
3. Huruf `r` (penomoran mulai dari 1: S-c-r).
4. `say (join [Skor: ] (skor))`.
5. **Benar** — perbandingan teks di Scratch tidak membedakan huruf besar-kecil.
</details>
