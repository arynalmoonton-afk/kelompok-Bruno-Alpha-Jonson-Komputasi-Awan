# Jurnal Proses — Tugas 4

## Jalur yang Dipilih

- **RPC dan Message Queue (MQ).** Saya memilih keduanya karena kebutuhan komunikasi pada FoodGo berbeda. Pada proses pengecekan saldo dan pembayaran, modul Pesanan perlu menerima hasil secara langsung, sehingga RPC lebih sesuai. Sementara itu, notifikasi pembayaran bisa dikirim melalui RabbitMQ agar modul lain tetap bisa menerima pesan meskipun tidak langsung memprosesnya saat itu juga.

## Kendala Teknis

- Saat menyiapkan RabbitMQ, saya perlu memastikan Docker berjalan dengan benar dan aplikasi Python dapat terhubung ke layanan tersebut. Saya juga perlu memasang library `pika` agar publisher dan consumer dapat berkomunikasi dengan RabbitMQ.
- Setelah konfigurasi selesai, saya mencoba menjalankan RPC dan mengirim pesan melalui RabbitMQ untuk memastikan keduanya bekerja sesuai fungsinya.
- Docker Compose sempat menampilkan peringatan mengenai atribut `version`, tetapi layanan RabbitMQ tetap berjalan dan dapat digunakan untuk pengujian.

## Uji “Pesan Tidak Hilang” (Jalur B)

- **Langkah uji:** Saya menghentikan consumer terlebih dahulu, kemudian menjalankan publisher untuk mengirimkan pesan pembayaran. Setelah pesan terkirim, saya menjalankan kembali consumer untuk melihat apakah pesan tersebut masih dapat diproses.
- **Hasil yang diamati:** Saat consumer dihentikan, pesan tetap berada di antrean RabbitMQ dan terlihat pada bagian *Ready*. Setelah consumer dijalankan kembali, pesan berhasil diterima dan diproses hingga jumlah pesan yang menunggu menjadi nol.
- **Kesimpulan:** Dari pengujian ini, saya melihat bahwa pesan tidak harus langsung diproses ketika dikirim. Pesan dapat menunggu di antrean sampai consumer kembali aktif. Hal ini membantu menjaga komunikasi antarmodul ketika penerima sedang tidak berjalan.

## Log Penggunaan AI (Level 2)

| **Tanggal** | **Tool AI** | **Prompt yang diberikan** | **Ringkasan saran/ide AI** | **Bagaimana diolah jadi tulisan/kode sendiri** |
|---|---|---|---|---|
| 11 Oktober 2026 | ChatGPT | Menyusun gambaran awal arsitektur komunikasi antarmodul pada studi kasus FoodGo. | Memberikan gambaran mengenai kebutuhan komunikasi antara modul Pesanan, Pembayaran, dan Notifikasi. | Gambaran tersebut dijadikan bahan pertimbangan dalam menentukan hubungan antarmodul sesuai kebutuhan sistem FoodGo. |
| 11 Oktober 2026 | ChatGPT | Mengidentifikasi perbedaan kebutuhan komunikasi sinkron dan asinkron dalam sistem pemrosesan pesanan. | Menjelaskan bahwa komunikasi sinkron sesuai untuk operasi yang membutuhkan respons langsung, sedangkan komunikasi asinkron dapat digunakan untuk proses lanjutan. | Perbedaan tersebut digunakan untuk memahami pembagian fungsi RPC dan Message Queue dalam rancangan sistem. |
| 11 Oktober 2026 | ChatGPT | Menyusun rancangan alur komunikasi antara client dan server menggunakan RPC pada aplikasi berbasis Python. | Memberikan gambaran alur pemanggilan fungsi jarak jauh dan pertukaran respons antara dua modul. | Alur tersebut dipelajari dan disesuaikan dengan simulasi pengecekan saldo serta pemrosesan pembayaran pada FoodGo. |
| 11 Oktober 2026 | ChatGPT | Mengidentifikasi aspek yang perlu diperhatikan dalam pengujian pengiriman pesan melalui message broker. | Memberikan gambaran mengenai peran antrean, publisher, consumer, dan konfirmasi pemrosesan pesan. | Aspek tersebut digunakan sebagai acuan pengamatan ketika menguji pengiriman event pembayaran melalui RabbitMQ. |
| 11 Oktober 2026 | ChatGPT | Menyusun kerangka evaluasi hasil pengujian komunikasi antarmodul untuk dokumentasi proyek. | Memberikan gambaran mengenai hal-hal yang perlu dicatat, seperti hasil eksekusi, kendala teknis, dan kesesuaian perilaku sistem dengan rancangan. | Dokumentasi disusun berdasarkan hasil eksekusi program, pemeriksaan antrean RabbitMQ, dan pengamatan selama proses pengujian. |
