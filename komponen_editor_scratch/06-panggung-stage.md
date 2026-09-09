# Modul ⑥ — Panggung (Stage)

**Lokasi:** kotak putih besar di kanan atas editor, tempat kucing berdiri.
**Estimasi:** 20 menit · **Jenjang:** SD kelas 5 – SMP

```
        y = +180
           ▲
           │
           │      🐱
x = −240 ──┼────────── x = +240
           │   (0,0)
           │
           ▼
        y = −180

        480 × 360 piksel
```

---

## Tujuan Pembelajaran

1. Menyebutkan ukuran panggung dan rentang koordinatnya.
2. Membaca posisi sprite dalam bentuk pasangan **(x, y)**.
3. Memindahkan sprite ke koordinat tertentu dengan blok `go to x: y:`.
4. Menjelaskan mengapa sprite tidak bisa hilang total dari panggung.

---

## Penjelasan

Panggung adalah **layar tempat proyek berjalan**. Semua yang dilihat penonton — sprite, latar, tulisan, monitor variabel — muncul di sini. Panggung tidak bisa bergerak; ia selalu berada di **lapisan paling belakang**, di belakang semua sprite.

### Ukuran & Koordinat

| Aspek | Nilai |
|---|---|
| Ukuran | **480 × 360 piksel** (rasio 4:3) |
| Titik pusat | **(0, 0)** — tepat di tengah |
| Sumbu X (mendatar) | **−240** (kiri) sampai **+240** (kanan) |
| Sumbu Y (tegak) | **−180** (bawah) sampai **+180** (atas) |

> Ini **bidang Cartesius** yang persis sama dengan pelajaran Matematika. Manfaatkan: Scratch membuat koordinat jadi terlihat dan bisa disentuh.

### Titik-titik penting untuk dihafal

| Posisi | Koordinat |
|---|---|
| Tengah | (0, 0) |
| Pojok kiri atas | (−240, 180) |
| Pojok kanan atas | (240, 180) |
| Pojok kiri bawah | (−240, −180) |
| Pojok kanan bawah | (240, −180) |

### Aturan "sprite tidak bisa kabur" (*fencing*)

Scratch selalu menjaga **minimal 15 piksel** bagian sprite tetap terlihat di panggung. Jadi walaupun diperintah `go to x: 9999`, sprite tetap menempel di tepi.

💡 Ini menjelaskan keluhan siswa *"kok kucingnya nyangkut di pinggir?"* — bukan bug, tapi memang dirancang begitu supaya sprite tidak hilang selamanya.

### Yang **tidak bisa** dilakukan Panggung

| Tidak bisa | Alasan |
|---|---|
| Bergerak / memakai blok Motion | Panggung adalah latar, bukan tokoh |
| `say` / `think` | Tidak punya balon bicara |
| Diklon | Hanya ada satu panggung |
| Diganti nama | Namanya selalu "Stage" |
| Berpindah lapisan | Selalu paling belakang |

Yang **bisa**: mengganti backdrop, memainkan suara, efek grafis, `ask ... and wait`, variabel, dan menerima broadcast.

---

## Praktik (12 menit)

**Latihan 1 — Membaca koordinat (4 menit)**
Centang ☐ `x position` dan ☐ `y position` di palet Motion. Seret kucing dengan mouse ke berbagai tempat; siswa membacakan angkanya. Guru menyebut posisi ("pojok kanan atas"), siswa menebak angkanya lebih dulu sebelum menyeret.

**Latihan 2 — Berburu harta karun (5 menit)**
Guru menyebut koordinat, siswa memindahkan kucing pakai blok:
```
go to x: (-200) y: (150)
go to x: (0)    y: (0)
go to x: (200)  y: (-150)
```

**Latihan 3 — Uji batas (3 menit)**
```
go to x: (9999) y: (9999)
```
Amati kucing berhenti di pojok, tidak hilang. Diskusikan aturan *fencing*.

---

## Analogi untuk Siswa

> Panggung adalah **panggung teater sungguhan**. Ukurannya tetap, tidak bisa dilebarkan. Aktor (sprite) boleh berlari ke mana saja, tapi tidak boleh keluar sepenuhnya dari pandangan penonton — selalu ada bagian tubuhnya yang terlihat.
>
> Koordinat adalah **alamat kursi di panggung**: angka pertama = seberapa ke kanan/kiri, angka kedua = seberapa ke atas/bawah.

---

## Hubungan Lintas Mata Pelajaran

| Mapel | Kaitan |
|---|---|
| **Matematika** | Bidang Cartesius, bilangan bulat positif–negatif, kuadran |
| **Seni Budaya** | Komposisi & tata letak visual |
| **IPA** | Simulasi gerak lurus, pantulan, gravitasi (dengan variabel kecepatan) |

---

## Kesalahan Umum

| Kesalahan | Akibat | Pencegahan |
|---|---|---|
| Mengira (0,0) di pojok kiri atas (seperti aplikasi lain) | Salah menghitung posisi | Tekankan **pusat = (0,0)** |
| Lupa Y **naik ke atas** bernilai positif | Sprite bergerak terbalik | Latih dengan menyeret sprite sambil membaca monitor |
| Menaruh sprite di luar rentang | Sprite "nyangkut" di tepi | Jelaskan *fencing* |
| Mencari blok Motion untuk Stage | Palet kosong | Ingatkan panggung tidak bisa bergerak |

---

## Cek Pemahaman

1. Berapa ukuran panggung Scratch dalam piksel?
2. Sebutkan koordinat pojok **kiri bawah** panggung.
3. Apa yang terjadi bila sprite diperintah `go to x: 500 y: 500`?
4. Sebutkan dua hal yang **tidak bisa** dilakukan Stage tetapi bisa dilakukan sprite.

<details>
<summary>Kunci jawaban</summary>

1. 480 × 360 piksel.
2. (−240, −180).
3. Sprite berhenti menempel di pojok kanan atas; Scratch menjaga minimal 15 px sprite tetap terlihat (*fencing*).
4. Antara lain: bergerak (blok Motion), berbicara (`say`/`think`), diklon, berganti lapisan, diganti nama.
</details>
