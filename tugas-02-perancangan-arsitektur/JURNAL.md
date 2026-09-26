# Jurnal Proses — Tugas 2

## [26 September 2026]
- Opsi arsitektur yang dipertimbangkan: Service-Oriented Architecture (SOA) dan Publish-Subscribe (Pub-Sub). Kedua opsi ini dipertimbangkan karena pada Tugas 1 sistem FoodGo masih memiliki masalah ketergantungan antar modul dan proses deployment yang dapat memengaruhi keseluruhan sistem.
- Kenapa akhirnya pilih [SOA/Pub-Sub]: Setelah melihat masalah pada Tugas 1, kami memilih menggunakan kombinasi SOA dan Pub-Sub. SOA digunakan untuk memisahkan fungsi utama FoodGo menjadi beberapa service, seperti Pesanan, Pembayaran, Katalog Resto, dan Kurir/Notifikasi. Pub-Sub digunakan untuk komunikasi berbasis event sehingga antar-service tidak harus saling terhubung secara langsung.
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): Pada versi awal, rancangan masih berfokus pada pemisahan service. Setelah dianalisis kembali, kami menambahkan Message Broker dan komunikasi berbasis event untuk mengurangi ketergantungan langsung antar-service. Jenis komunikasi sinkron dan asinkron juga diperjelas agar alur dari pelanggan membuat pesanan sampai kurir mendapatkan tugas lebih mudah dipahami.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
