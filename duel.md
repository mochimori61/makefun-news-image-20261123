# DUEL VARIAN — NI23 G3 akun20 · THE GLOBE IN ONE DAY

Konsep: halaman depan koran lurus (bukan template dekoratif) — masthead
Playfair Black 74px, strip 6 angka pengikat kartu, 13 kartu besar
berilustrasi gambar-sendiri, peta dunia titik-titik dengan 13 pin
bernomor, timeline UTC 6 slot, ALSO ON bernomor sampai 40 cerita,
kotak DATE CHECK merah berisi 7 buangan bernama + bertanggal.

Trio lead (pilihan sendiri): #34 Emas jatuh ke $3,538 (lead akun20,
kartu 1) + #25 India 720/9d Wellington (kartu 2) + #43 Demokrat rebut
DPR 258–173 (kartu 3).

## Tiga varian yang dibangun (compose.py, argumen A/B/C)
- A — gading · tinta hijau botol · aksen kuning tua · lead di kiri.
  Palet persis brief akun20.
- B — krem hangat · tinta teal tua · aksen tembaga · lead di kanan,
  tumpukan trio di kiri.
- C — perkamen · tinta hutan · aksen oker · pita header kartu terisi
  penuh (band gelap) di semua kartu.

## Penilaian
- Kontras: A paling kuat (hijau botol pekat di atas gading); B dekat,
  C paling berat karena band gelap memakan ruang judul.
- Keterbacaan 300px: A — masthead, tanggal, dan ke-13 judul kartu
  terbaca; B terbaca tapi trio di kiri terasa lebih sempit; C judul
  kartu terbaca namun band membuat halaman tampak lebih gelap dan
  padat di ukuran kecil.
- Kepadatan data: ketiganya sama (40 cerita, 6 angka, 6 slot UTC,
  7 DATE CHECK) — pembeda murni kontras + hierarki lead. Di A kartu
  lead benar-benar paling besar dan pertama dibaca mata.

## Pemenang: A
Alasan: palet brief (gading / hijau botol / kuning tua), lead emas di
posisi baca pertama dengan judul 34px, kontras tertinggi, dan lulus
uji 300px paling bersih.

## Uji wajib
- Uji 300px: LULUS — render final diperkecil ke 300px
  (/tmp/ni23g3-akun20-300.png); masthead "THE GLOBE IN ONE DAY",
  tanggal "Monday 23 November 2026", dan judul 13 kartu utama semua
  masih terbaca.
- entry.png: 1024×1024 (IHDR terverifikasi manual via struct),
  271.120 byte (≤1.048.576), sha256
  048eef8eb5d523f868aa5870c6a09f5c76981f14f607c414740297cb7db59a8e.
- Margin checker (margin_check.py --fresh ni23-fresh.txt): 13/13
  LOLOS — 13 kartu, ilustrasi 100%, tag sumber 100%, fakta deck
  rata-rata 3,15, strip angka 6 mengikat, peta+pin 13/13, DATE CHECK
  7 item, timeline 6 slot, 40 cerita, brief segar 44%.

## Kenapa lebih kuat dari entry G2 akun ini
G2 akun20 memakai konsep "Mesin Ketik" — satu metafora dekoratif
tunggal. G3 menggantinya dengan halaman depan koran sungguhan:
hierarki berita yang jelas (lead terbesar, trio, grid), keluasan
40 cerita dari 8 region yang bisa diverifikasi dari gambar saja,
angka-angka kunci hari itu di strip tersendiri, dan kotak DATE CHECK
yang membuktikan seleksi tanggalnya disiplin. Bentuk koran menjawab
langsung kriteria juri (satu hari, bernama, luas, terbaca di 300px)
tanpa bergantung pada gimmick visual.
