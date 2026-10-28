# Jurnal Proses — Tugas 6

## Implementasi find_successor

- **Kesalahan pertama yang ditemui:** Pada proses pengujian awal, lookup lokasi entitas menghasilkan `None`. Hal ini menunjukkan bahwa proses pencarian successor belum menghasilkan node tujuan sebagaimana yang diharapkan.
- **Cara memperbaikinya:** Pemeriksaan difokuskan pada logika pencarian successor, terutama pemilihan node dengan ID yang lebih besar atau sama dengan ID target serta penanganan *wrap-around* ketika ID target melewati ID node terbesar dalam ring. Dengan mekanisme ini, pencarian dapat kembali ke node dengan ID terkecil jika tidak ditemukan node yang memenuhi kondisi tersebut.

## Skenario join/leave

- **Hasil sebelum & sesudah node baru bergabung:** Ketika node Medan dengan ID 123 bergabung ke ring Chord, pemetaan entitas `kurir-uji-23` berubah dari node 136 menjadi node 123. Perubahan ini menunjukkan bahwa penambahan node dapat memengaruhi pembagian tanggung jawab terhadap ID entitas di dalam ring.

- **Hasil sebelum & sesudah node keluar:** Ketika node Jakarta-1 dengan ID 177 keluar dari ring, pemetaan entitas `kurir-leave-14` berubah dari node 177 menjadi node 40. Hal ini menunjukkan bahwa entitas yang sebelumnya ditangani oleh node yang keluar perlu dipetakan kembali ke node yang masih tersedia.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 29-10-2026 | ChatGPT | Meminta penjelasan konsep penamaan dan resolusi lokasi pada Chord Distributed Hash Table (DHT). | AI menjelaskan hubungan antara ID node, ID entitas, dan mekanisme pencarian lokasi dalam ring Chord. | Penjelasan digunakan sebagai referensi untuk memahami konsep dasar, kemudian dicocokkan dengan implementasi simulasi. |
| 29-10-2026 | ChatGPT | Meminta penjelasan fungsi `find_successor` dan cara menentukan node yang bertanggung jawab atas suatu ID. | AI menjelaskan pencarian successor berdasarkan urutan ID node dan penanganan *wrap-around*. | Konsep digunakan untuk membantu memahami alur pencarian dan memeriksa hasil pengujian program. |
| 29-10-2026 | ChatGPT | Meminta penjelasan perubahan pemetaan entitas ketika node baru bergabung ke ring Chord. | AI menjelaskan bahwa penambahan node dapat mengubah node yang bertanggung jawab atas sebagian ID entitas. | Penjelasan dibandingkan dengan hasil simulasi join untuk memahami perubahan pemetaan entitas. |
| 29-10-2026 | ChatGPT | Meminta penjelasan perubahan pemetaan entitas ketika sebuah node keluar dari ring Chord. | AI menjelaskan bahwa keluarnya node dapat menyebabkan entitas dipetakan ulang ke node lain yang masih tersedia. | Penjelasan digunakan untuk membantu memahami hasil simulasi leave dan menyusun uraian berdasarkan hasil yang tercatat. |
| 29-10-2026 | ChatGPT | Meminta bantuan menyusun kerangka jurnal proses yang mencakup implementasi `find_successor` serta skenario join dan leave. | AI menyarankan struktur dokumentasi yang memisahkan implementasi, hasil pengujian, dan analisis perubahan pemetaan. | Kerangka digunakan sebagai acuan penyusunan jurnal dan disesuaikan dengan instruksi tugas serta hasil pengerjaan. |
