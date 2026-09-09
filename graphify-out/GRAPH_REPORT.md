# Graph Report - .  (2026-08-04)

## Corpus Check
- 27 files · ~168,068 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 281 nodes · 653 edges · 14 communities
- Extraction: 63% EXTRACTED · 37% INFERRED · 0% AMBIGUOUS · INFERRED: 240 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Gerak, Tampilan & Properti Sprite|Gerak, Tampilan & Properti Sprite]]
- [[_COMMUNITY_Operator, Sensor & Blok Bersarang|Operator, Sensor & Blok Bersarang]]
- [[_COMMUNITY_Generator Slide PPTX|Generator Slide PPTX]]
- [[_COMMUNITY_Kontrol Alur & Klon|Kontrol Alur & Klon]]
- [[_COMMUNITY_Variabel & List|Variabel & List]]
- [[_COMMUNITY_Generator Aset Blok SVG|Generator Aset Blok SVG]]
- [[_COMMUNITY_My Blocks & Abstraksi|My Blocks & Abstraksi]]
- [[_COMMUNITY_Events & Broadcast|Events & Broadcast]]
- [[_COMMUNITY_Identitas, Platform & Komunitas|Identitas, Platform & Komunitas]]
- [[_COMMUNITY_Manajemen Sprite, Berbagi & Batas|Manajemen Sprite, Berbagi & Batas]]
- [[_COMMUNITY_Ekstensi Scratch|Ekstensi Scratch]]
- [[_COMMUNITY_Dokumen Index & Urutan Pengajaran|Dokumen Index & Urutan Pengajaran]]
- [[_COMMUNITY_Panggung, Koordinat & Fencing|Panggung, Koordinat & Fencing]]
- [[_COMMUNITY_Area Kode & Paralelisme|Area Kode & Paralelisme]]

## God Nodes (most connected - your core abstractions)
1. `Stack Block (▭)` - 66 edges
2. `Scratch 3.0` - 42 edges
3. `Reporter Block (⬭)` - 34 edges
4. `Looks (Tampilan) — Ungu` - 25 edges
5. `Motion (Gerak) — Biru` - 23 edges
6. `Sensing (Sensor) — Biru muda` - 22 edges
7. `Operators (Operator) — Hijau` - 22 edges
8. `Variables (Variabel & List) — Oranye tua` - 20 edges
9. `_txbox()` - 16 edges
10. `_para()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `input boolean` --implements--> `Stack Block (▭)`  [INFERRED]
  tab_code/tab_code_my_blocks.md → peta-fitur-scratch.md
- `input number/text` --implements--> `Stack Block (▭)`  [INFERRED]
  tab_code/tab_code_my_blocks.md → peta-fitur-scratch.md
- `label text (hiasan)` --implements--> `Stack Block (▭)`  [INFERRED]
  tab_code/tab_code_my_blocks.md → peta-fitur-scratch.md
- `run without screen refresh` --implements--> `Stack Block (▭)`  [INFERRED]
  tab_code/tab_code_my_blocks.md → peta-fitur-scratch.md
- `ask [] and wait` --implements--> `Stack Block (▭)`  [INFERRED]
  tab_code/tab_code_sensing.md → peta-fitur-scratch.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Script reset lengkap (Motion + Looks + Variables + Sound)** — tab_code_tab_code_looks_script_reset, tab_code_tab_code_looks_blok_show, tab_code_tab_code_looks_blok_clear_graphic_effects, tab_code_tab_code_looks_blok_set_size, tab_code_tab_code_motion_blok_go_to_xy, tab_code_tab_code_motion_blok_point_in_direction, tab_code_tab_code_variables_blok_set_var [EXTRACTED 1.00]
- **Trio blok klon** — tab_code_tab_code_control_blok_create_clone, tab_code_tab_code_control_blok_when_i_start_as_clone, tab_code_tab_code_control_blok_delete_this_clone, peta_fitur_scratch_clone [EXTRACTED 1.00]
- **Enam bentuk blok = tata bahasa visual** — peta_fitur_scratch_hat_block, peta_fitur_scratch_stack_block, peta_fitur_scratch_boolean_block, peta_fitur_scratch_reporter_block, peta_fitur_scratch_c_block, peta_fitur_scratch_cap_block, peta_fitur_scratch_sistem_bentuk_blok [EXTRACTED 1.00]

## Communities (14 total, 0 thin omitted)

### Community 0 - "Gerak, Tampilan & Properti Sprite"
Cohesion: 0.07
Nodes (65): Kotak centang ☐ reporter → monitor di panggung, ④ Palet Blok, 6 properti sprite: nama, x, y, Show, Size, Direction, ⑧ Panel Info Sprite, 3 gaya rotasi: All Around / Left-Right / Do not rotate, Blocking vs non-blocking, Debugging, Koordinat kartesius (+57 more)

### Community 1 - "Operator, Sensor & Blok Bersarang"
Cohesion: 0.08
Nodes (44): Boolean Block (⬡), Deteksi tabrakan, Reporter Block (⬭), Sistem Bentuk Blok (tata bahasa visual), (backdrop [number/name]), (costume [number/name]), (() + ()), (<> and <>) (+36 more)

### Community 2 - "Generator Slide PPTX"
Cohesion: 0.17
Nodes (38): build(), build_index(), Emu_from_pt(), _load_kit(), Satu slide untuk satu bagian komponen., Slide analogi — satu kalimat besar, penuh warna., Muat kit layout dari folder tab_code dengan NAMA MODUL BERBEDA.      Kedua gener, Sampul modul: nomor, nama komponen, lokasi di layar, durasi. (+30 more)

### Community 3 - "Kontrol Alur & Klon"
Cohesion: 0.17
Nodes (20): ⑦ Kontrol Panggung (⚑ / ⛔ / layar penuh), C-Block (⊂), Cap Block (▬), Iteration (perulangan), Selection (percabangan), create clone of (), delete this clone, forever (+12 more)

### Community 4 - "Variabel & List"
Cohesion: 0.15
Nodes (17): Struktur data (array/list), Variabel, change () by (), hide variable (), add [] to (), delete () of (), hide list (), insert [] at () of () (+9 more)

### Community 5 - "Generator Aset Blok SVG"
Cohesion: 0.23
Nodes (15): block_svg(), el_icon(), el_input(), el_label(), esc(), item_w(), measure(), metrics() (+7 more)

### Community 6 - "My Blocks & Abstraksi"
Cohesion: 0.15
Nodes (15): ③ Selektor Kategori Blok, Batasan Scratch untuk guru, Abstraksi, Dekomposisi, Prosedur / fungsi, Rekursi, define …, input boolean (+7 more)

### Community 7 - "Events & Broadcast"
Cohesion: 0.30
Nodes (14): Hat Block (⌒), Event-driven, Message passing, broadcast (), broadcast () and wait, when backdrop switches to (), when ⚑ clicked, when (loudness/timer) > () (+6 more)

### Community 8 - "Identitas, Platform & Komunitas"
Cohesion: 0.17
Nodes (13): ② Tab Code / Costumes / Sounds, Kostum, Share / Remix / Studio / See Inside, MIT Media Lab — Lifelong Kindergarten, Scratch Online Editor, Paint Editor (Vector & Bitmap), Scratch 3.0, Scratch Foundation (+5 more)

### Community 9 - "Manajemen Sprite, Berbagi & Batas"
Cohesion: 0.22
Nodes (11): ⑨ Daftar Sprite, Duplicate sprite (bawa kode, kostum, suara), 4 cara menambah sprite: Choose / Paint / Surprise / Upload, Export sprite → .sprite3, ⑪ Backpack, Batas teknis Scratch, Klon — batas 300 aktif, Cloud variable (10, angka saja, online) (+3 more)

### Community 10 - "Ekstensi Scratch"
Cohesion: 0.20
Nodes (10): Ekstensi (Add Extension), Ekstensi Face Sensing (Okt 2025, BlazeFace lokal), Ekstensi LEGO (EV3/BOOST/WeDo 2.0), Ekstensi Makey Makey, Ekstensi micro:bit, Ekstensi Music, Ekstensi Pen, Ekstensi Text to Speech (+2 more)

### Community 11 - "Dokumen Index & Urutan Pengajaran"
Cohesion: 0.47
Nodes (6): Index Peta Komponen Editor, ① Menu Bar, Peta Fitur Scratch — riset menyeluruh, Format .sb3 (ZIP + project.json), Usulan urutan pengajaran 15 tahap, Index Tab Code — penjelasan blok per kategori

### Community 12 - "Panggung, Koordinat & Fencing"
Cohesion: 0.47
Nodes (6): ⑥ Panggung (Stage), ⑩ Panel Stage / Backdrop, Backdrop (latar Stage), Fencing — minimal 15 px sprite tetap terlihat, Sistem koordinat (0,0) di tengah; x −240…240, y −180…180, Stage / Panggung 480×360

### Community 13 - "Area Kode & Paralelisme"
Cohesion: 0.50
Nodes (4): ⑤ Area Kode (Scripts Area), Clean up blocks, Komentar (kotak kuning), Paralelisme (concurrency)

## Knowledge Gaps
- **20 isolated node(s):** `MIT Media Lab — Lifelong Kindergarten`, `Scratch Foundation`, `Scratch Online Editor`, `ScratchJr (usia 5–7)`, `Scratch di Raspberry Pi` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Scratch 3.0` connect `Identitas, Platform & Komunitas` to `Gerak, Tampilan & Properti Sprite`, `Operator, Sensor & Blok Bersarang`, `Kontrol Alur & Klon`, `Variabel & List`, `My Blocks & Abstraksi`, `Events & Broadcast`, `Manajemen Sprite, Berbagi & Batas`, `Ekstensi Scratch`, `Dokumen Index & Urutan Pengajaran`, `Area Kode & Paralelisme`?**
  _High betweenness centrality (0.225) - this node is a cross-community bridge._
- **Why does `Stack Block (▭)` connect `Gerak, Tampilan & Properti Sprite` to `Operator, Sensor & Blok Bersarang`, `Kontrol Alur & Klon`, `Variabel & List`, `My Blocks & Abstraksi`, `Events & Broadcast`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Why does `Index Peta Komponen Editor` connect `Dokumen Index & Urutan Pengajaran` to `Gerak, Tampilan & Properti Sprite`, `Kontrol Alur & Klon`, `My Blocks & Abstraksi`, `Identitas, Platform & Komunitas`, `Manajemen Sprite, Berbagi & Batas`, `Panggung, Koordinat & Fencing`, `Area Kode & Paralelisme`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 65 inferred relationships involving `Stack Block (▭)` (e.g. with `create clone of ()` and `wait () seconds`) actually correct?**
  _`Stack Block (▭)` has 65 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Scratch 3.0` (e.g. with `Abstraksi` and `Struktur data (array/list)`) actually correct?**
  _`Scratch 3.0` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `Reporter Block (⬭)` (e.g. with `(backdrop [number/name])` and `(costume [number/name])`) actually correct?**
  _`Reporter Block (⬭)` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Muat kit layout dari folder tab_code dengan NAMA MODUL BERBEDA.      Kedua gener`, `Sampul modul: nomor, nama komponen, lokasi di layar, durasi.`, `Slide denah / sketsa antarmuka dalam huruf monospace, ukuran otomatis.` to the rest of the system?**
  _35 weakly-connected nodes found - possible documentation gaps or missing edges._