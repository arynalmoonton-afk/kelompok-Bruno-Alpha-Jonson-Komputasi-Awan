# Jurnal Proses — Tugas 7

## Diskusi Pemilihan Model Konsistensi

- **Argumen yang dipertimbangkan:**
  Pada kasus FoodGo, terdapat permasalahan keterlambatan replikasi data antara Server Jakarta dan Server Bandung. Ketika pelanggan melakukan top-up melalui Server Jakarta, saldo berhasil diperbarui menjadi Rp50.000. Namun, sebelum proses replikasi selesai, pelanggan membaca saldo melalui Server Bandung dan mendapatkan saldo lama sebesar Rp0.

  Model *Eventual Consistency* memungkinkan setiap replika memiliki data yang berbeda untuk sementara waktu hingga proses sinkronisasi selesai. Model ini cukup efisien untuk sistem terdistribusi, tetapi belum cukup untuk menjamin pelanggan selalu melihat hasil transaksi terbarunya. Sementara itu, *Sequential Consistency* dapat memberikan urutan operasi yang konsisten secara global, tetapi penerapannya memiliki kebutuhan koordinasi yang lebih besar.

- **Kesimpulan akhir & alasan:**
  Model *Eventual Consistency* dipilih sebagai dasar replikasi data karena memungkinkan sistem tetap berjalan meskipun sinkronisasi antarreplika membutuhkan waktu. Namun, model tersebut perlu dilengkapi dengan mekanisme *Client-Centric Consistency*, yaitu *Read-Your-Writes*.

  Mekanisme *Read-Your-Writes* memastikan pelanggan dapat membaca hasil transaksi yang sebelumnya berhasil dilakukan. Jika versi data pada Server Bandung belum sesuai dengan versi terbaru yang dibutuhkan pelanggan, sistem akan mengarahkan permintaan pembacaan ke Server Jakarta. Dengan demikian, pelanggan tetap mendapatkan informasi saldo terbaru meskipun proses replikasi belum selesai.

## Simulasi (Jika Dikerjakan)

- **Hasil skenario naif vs Read-Your-Writes:**

  Simulasi dilakukan menggunakan Python untuk menggambarkan keterlambatan replikasi saldo antara Server Jakarta dan Server Bandung dengan waktu tunda replikasi selama 2 detik.

  1. **Skenario Naif (Tanpa Jaminan Konsistensi):**
     - Pelanggan melakukan top-up sebesar Rp50.000 melalui Server Jakarta.
     - Server Jakarta berhasil memperbarui saldo menjadi Rp50.000.
     - Sebelum replikasi selesai, pelanggan membaca saldo melalui Server Bandung.
     - Server Bandung masih menyimpan saldo lama sebesar Rp0.
     - Kondisi ini menunjukkan terjadinya *Inconsistent Read* karena pelanggan memperoleh data yang belum diperbarui.

  2. **Skenario Read-Your-Writes:**
     - Pelanggan kembali melakukan top-up sebesar Rp20.000 melalui Server Jakarta.
     - Saldo terbaru menjadi Rp70.000 dengan versi data 2.
     - Pelanggan meminta pembacaan saldo melalui Server Bandung dengan versi minimum 2.
     - Server Bandung masih memiliki data versi 1 dengan saldo Rp50.000.
     - Sistem mendeteksi bahwa versi lokal lebih lama daripada versi yang dibutuhkan pelanggan.
     - Permintaan pembacaan kemudian dialihkan ke Server Jakarta.
     - Server Jakarta mengembalikan saldo terbaru sebesar Rp70.000 dengan versi 2.
     - Pelanggan berhasil memperoleh saldo yang benar meskipun replikasi ke Server Bandung belum selesai.

  Berdasarkan hasil simulasi, mekanisme *Read-Your-Writes* berhasil mengatasi permasalahan pembacaan data lama dengan memeriksa versi data dan mengarahkan permintaan ke replika yang memiliki versi terbaru.

## Log Penggunaan AI (Level 2)

> **Catatan:** Selama pengerjaan, AI digunakan untuk membantu brainstorming, penyusunan ide, penjelasan konsep, serta pengembangan kode simulasi dan penyusunan dokumentasi. Penggunaan tersebut perlu disesuaikan dengan ketentuan Level 2 pada RUBRIK-UMUM.md. Pastikan log ini mencerminkan penggunaan AI yang sebenarnya dan tidak mengklaim bahwa AI hanya digunakan untuk brainstorming apabila penggunaannya lebih luas.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2 November 2026 | ChatGPT | Saya ingin memahami studi kasus FoodGo terkait perbedaan saldo e-wallet akibat keterlambatan replikasi data. Bantu saya mengidentifikasi model konsistensi yang paling sesuai serta menjelaskan pertimbangan pemilihannya. | Memberikan penjelasan mengenai Eventual Consistency, Sequential Consistency, dan Read-Your-Writes beserta penerapannya dalam sistem e-wallet terdistribusi. | Menggunakan penjelasan tersebut sebagai bahan pertimbangan dalam menentukan model konsistensi dan menyusun argumentasi berdasarkan permasalahan pada studi kasus FoodGo. |
| 2 November 2026 | ChatGPT | Bantu saya memahami dan melengkapi simulasi pada file replica_simulation.py, khususnya bagian replikasi data dengan keterlambatan dan penerapan mekanisme Read-Your-Writes menggunakan versi data. | Memberikan arahan implementasi simulasi replikasi tertunda, pemeriksaan versi data, serta mekanisme pengalihan permintaan ketika replika belum memiliki data terbaru. | Menerapkan kode pada VS Code, menjalankan simulasi, dan memeriksa hasil keluaran untuk memahami perbedaan antara pembacaan data secara naif dan menggunakan Read-Your-Writes. |
| 2 November 2026 | ChatGPT | Bantu saya menyusun dokumentasi analisis dan memahami alur sequence diagram untuk menggambarkan kondisi sebelum dan sesudah penerapan Read-Your-Writes pada sistem FoodGo. | Memberikan saran struktur dokumentasi dan gambaran alur komunikasi antarkomponen sistem pada kedua kondisi tersebut. | Menyesuaikan dokumentasi dan membuat sequence diagram berdasarkan alur sistem serta hasil simulasi yang telah dikerjakan. |
