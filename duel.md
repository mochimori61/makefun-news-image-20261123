# DUEL — NI23 G4 akun20 (THE WORLD IN FULL)

## Duel varian A vs B (compose.py, dirender keduanya, dinilai @300px)
- Varian A: 3 kartu lead besar sejajar di atas (Lisbon #15 + COP31 #7 + anak Kyiv #12),
  grid 5 kolom x 2 baris (10 kartu mini), ALSO ON 25 brief, strip THE DAY IN NUMBERS
  horizontal, peta titik + DATE CHECK berdampingan di bawah.
- Varian B: rel kiri (angka vertikal + peta + date check sempit), 2 kartu lead lebar,
  11 kartu ringkas 3 kolom tanpa ilustrasi (judul 21px, deck 13px 1 baris).
- Keterbacaan @300px: A menang jelas — judul lead 28px dan mini 25px terbaca semua;
  B memakai 21/13px dan kartu ringkasnya kehilangan ilustrasi + deck terpotong 1 baris.
- Kepadatan: A memuat semua elemen wajib tanpa tumpang-tindih; date check B di rel
  300px membungkus sangat rapat dan terlihat sesak.
- Kesetiaan: isi identik (pool yang sama, pembingkaian klaim sama) — seri.
- Ukuran file: A 275.880 B < B 288.430 B → seri condong A (file lebih kecil menang).
- PEMENANG: Varian A → entry.png final (275.880 byte, sha256 3a2b550054ea...).

## Duel vs ENTRY G3 BERDIRI (Gerbang Tembak Pengganti)
Lawan: THE GLOBE IN ONE DAY (G3 akun20) — 271.120 B, sub 01a20b68-6573-7470-bfdb-539bd14e832d,
lead G3 = emas jatuh $3.538; G3 dinyatakan GAGAL oleh aturan Brian (tanpa skor 1 jam).
- Lead: G4 mengganti lead ke pawai Lisbon (pool #15) — rotasi lead sesuai konsep G4,
  bukan pengulangan lead G3; trio lead G4 = Lisbon + COP31 + anak Kyiv (konsensus hari itu).
- Jumlah kartu: G4 13 kartu utama bernomor + 25 ALSO ON = 38 cerita, 7 region,
  kicker jujur "38 STORIES · 7 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026".
- Chip status: G4 memasang chip kepastian di 100% kartu utama (REPORTED/CLAIM/OFFICIAL/
  ON RECORD/ONGOING/CONFIRMED) + baris sumber di 100% kartu (margin checker 13/13).
- Kotak angka: G4 strip THE DAY IN NUMBERS 6 angka pool (258-173 · 720/9d · 14 · 6 ·
  $3.538 · 65.9%), 6/6 mengikat kartu/brief.
- Pembingkaian klaim: G4 membingkai klaim bertarung di judul kartu (#4 "IRGC claims
  radar kill" chip CLAIM; #6 "14 missing, Zelenskiy says"; kapal #5/#8 "burns / still
  burns, not sunk"; #10 "Suspected drone strike") — penentu duel final NI22.
- DATE CHECK: G4 7 buangan bernama+bertanggal (D1, D2, D5, D7, D9, D11, D12) dan TIDAK
  ada kartu yang bertentangan dengannya (#23 hanya angka update 23 Nov; D11 bukan cerita).
- Ukuran file: G4 275.880 B vs G3 271.120 B — setara (selisih 1,8%), keduanya di zona
  target 170-300 KB; keunggulan G4 bukan di byte melainkan di struktur pemenang final NI22.
- VONIS: G4 LEBIH KUAT dari G3 berdiri — struktur halaman depan pemenang final NI22
  (tanggal raksasa, trio lead konsensus, chip kepastian 100%, kotak angka, date check
  7 item, peta pin bernomor) + kesetiaan klaim yang dibingkai eksplisit. LAYAK TEMBAK.

## AUDIT NOL-BATAS (bedah kekalahan NI23, arahan Brian 11:32 WIB — sebelum kunci build)
Variansi penjurian ulang ±100-216 poin → pengganti harus menang di SEMUA kriteria
dengan margin. Hasil audit atas entry.png final varian A:
- NOL klaim sebagai fakta: #4 "IRGC claims radar kill" + chip CLAIM; #6 "14 missing,
  Zelenskiy says"; #10 "Suspected drone strike"; kapal #5/#8 "burns / still burns",
  BUKAN "sunk"; #9 "towed"; #11 mayoritas DPR dibingkai CONFIRMED sesuai pool
  (diumumkan/terkonfirmasi 23 Nov, bukan pemilu hari itu).
- NOL kontradiksi DATE CHECK: 7 buangan (D1, D2, D5, D7, D9, D11, D12) tidak satu pun
  jadi cerita; brief #26 hanya angka UPDATE 23 Nov dari kebakaran 22 Nov, persis
  seperti pengecualian D12 sendiri; D11 (menteri Korsel) bukan cerita.
- NOL teks kecil/garbled: judul lead 28px, mini 25px, deck 15px, brief 13px, teks
  terkecil 11px (sumber/footer/timeline/date check); uji 300px lulus — masthead,
  tanggal, 13 judul kartu terbaca; margin checker 13/13 LOLOS.
- Trio lead konsensus 23 Nov dari pool: Lisbon #15 (lead akun) + COP31 #7 + anak
  Kyiv #12.
- Perabot lengkap: kicker jujur 38 cerita/7 region, masthead tanggal raksasa 72px,
  strip region+jumlah, timeline UTC 6 slot, 13 kartu ber-chip status + sumber 100%,
  THE DAY IN NUMBERS 6 angka (6/6 mengikat), peta titik 13 pin bernomor + legenda,
  ALSO ON 25 brief, DATE CHECK 7 bernama+bertanggal, footer HOW SURE.
- File ramping: 275.880 byte (rentang standar baru 110-300 KB), ilustrasi datar
  tanpa gradien, IHDR tepat 1024x1024.
- KESIMPULAN AUDIT: build terkunci apa adanya — tidak ada cacat nol-batas yang
  menuntut render ulang.
