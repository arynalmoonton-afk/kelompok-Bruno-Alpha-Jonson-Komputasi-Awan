# Jurnal Proses — Tugas 5

## Implementasi Bully

- **Kendala saat mengisi TODO 1–4:** Kendala yang ditemui adalah memahami alur komunikasi antarnode dan memastikan proses pemilihan leader berjalan dengan benar. Saat pengujian awal, Node 1 sempat menjadi leader karena dijalankan lebih dahulu, sedangkan node lainnya belum aktif. Setelah semua node dijalankan, proses pemilihan leader berjalan dan Node 5 terpilih sebagai leader.

### Analisis Implementasi

Bully Algorithm digunakan untuk memilih satu node sebagai leader berdasarkan ID tertinggi dari node yang masih aktif. Proses pemilihan dimulai ketika sebuah node mengirim pesan `ELECTION` kepada node dengan ID lebih tinggi. Jika node tersebut masih aktif, ia akan membalas dengan pesan `OK` dan memulai proses pemilihan sendiri. Jika tidak ada node dengan ID lebih tinggi yang merespons, node dapat menetapkan dirinya sebagai leader dan mengirim pesan `COORDINATOR` kepada node lainnya.

Pada tugas ini, terdapat lima node yang dijalankan melalui proses Python terpisah. Setiap node menggunakan port TCP yang berbeda agar dapat saling berkomunikasi melalui `localhost`. Pesan `ELECTION` digunakan untuk memulai pemilihan, `OK` sebagai respons dari node dengan ID lebih tinggi, dan `COORDINATOR` untuk memberi tahu node lain mengenai leader yang terpilih.

### Perbandingan Bully Algorithm dan Raft

Bully Algorithm memilih leader berdasarkan ID node tertinggi yang masih aktif dan dapat dijangkau. Cara kerjanya cukup sederhana sehingga cocok digunakan untuk memahami dasar pemilihan leader. Namun, ketika beberapa node memulai pemilihan secara bersamaan, jumlah pesan yang dikirim dapat meningkat dan proses pemilihan perlu dikelola dengan baik.

Raft menggunakan sistem pemungutan suara untuk memilih leader. Kandidat harus memperoleh suara mayoritas sebelum menjadi leader. Selain pemilihan leader, Raft juga mengatur replikasi log agar node dapat menyepakati perubahan data. Karena memiliki mekanisme tambahan tersebut, Raft lebih kompleks dibandingkan Bully Algorithm.

Dalam kasus FoodGo, Bully Algorithm dapat digunakan untuk menentukan node yang bertugas mengoordinasikan pemrosesan pesanan. Namun, keberadaan leader saja belum menjamin bahwa pesanan tidak diproses dua kali atau bahwa data selalu konsisten. Oleh karena itu, sistem tetap membutuhkan mekanisme tambahan untuk mengelola status pesanan dan mencegah duplikasi transaksi.

## Skenario 1: Start normal

- **Leader yang terpilih:** Node 5.
- **Log/observasi:** Setelah kelima node dijalankan, Node 5 terpilih sebagai leader karena memiliki ID tertinggi. Node 5 kemudian mengirim pesan `COORDINATOR` kepada Node 1 sampai Node 4. Berdasarkan log terminal, seluruh node menerima informasi tersebut dan mencatat Node 5 sebagai leader.

## Skenario 2: Leader dimatikan

- **Leader baru yang terpilih:** Node 4.
- **Berapa lama waktu sampai leader baru terdeteksi:** Beberapa detik setelah Node 5 dihentikan, berdasarkan pengamatan saat pengujian. Waktu pastinya tidak diukur menggunakan stopwatch.
- **Log/observasi:** Node 5 dihentikan menggunakan `Ctrl + C` untuk menyimulasikan kegagalan leader. Node yang masih aktif kemudian mendeteksi bahwa Node 5 tidak dapat dihubungi dan memulai pemilihan ulang. Node 4 terpilih sebagai leader baru karena memiliki ID tertinggi di antara node yang masih aktif. Setelah itu, Node 4 mengirim pesan `COORDINATOR` kepada node lainnya.

### Analisis Hasil Pengujian

Dari kedua skenario tersebut, proses pemilihan leader berhasil diamati pada kondisi normal maupun setelah leader dihentikan. Node 5 menjadi leader saat seluruh node aktif, sedangkan Node 4 mengambil alih setelah Node 5 tidak tersedia. Hasil ini sesuai dengan aturan dasar Bully Algorithm yang memberikan prioritas kepada node dengan ID tertinggi yang masih aktif.

Pengujian ini masih terbatas pada lima proses yang berjalan di satu komputer. Kondisi seperti gangguan jaringan, keterlambatan pesan, dan beberapa node yang memulai pemilihan secara bersamaan belum diuji secara khusus. Pengujian tambahan diperlukan untuk mengetahui apakah proses pemilihan tetap konsisten pada kondisi tersebut.

## Log Penggunaan AI (Level 2)

> Catat penggunaan AI sesuai kebijakan Level 2 pada [RUBRIK-UMUM.md](../RUBRIK-UMUM.md). Isi tabel berdasarkan bantuan yang benar-benar digunakan selama pengerjaan tugas.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 Oktober 2026 | ChatGPT | Jelaskan cara kerja Bully Algorithm dan fungsi pesan `ELECTION`, `OK`, serta `COORDINATOR` dalam simulasi lima node. | Memberikan gambaran alur pemilihan leader berdasarkan ID dan fungsi pesan yang digunakan antarnode. | Penjelasan digunakan untuk memahami alur program. Implementasi kemudian dijalankan pada lima terminal untuk melihat proses komunikasi dan menentukan leader. |
| 18 Oktober 2026 | ChatGPT | Jelaskan skenario pengujian ketika seluruh node aktif dan ketika leader dihentikan. | Memberikan gambaran pengujian normal, pemilihan ulang setelah leader gagal, dan hal-hal yang perlu diamati pada log terminal. | Pengujian dilakukan dengan menjalankan Node 1 sampai Node 5 secara terpisah. Node 5 kemudian dihentikan dan log node yang tersisa diperiksa untuk melihat apakah Node 4 menjadi leader baru. |
