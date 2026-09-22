# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## Sabtu, 19 September 2026
- Peserta: Reynal, Melvin, Reval, Wayan
- Poin diskusi: Menentukan pitfall yang paling sesuai dengan kondisi FoodGo. Kelompok kami memilih the network is reliable, latency is zero, single point of failure, dan cascading failure karena pada skenario terdapat asumsi jaringan selalu dapat diandalkan, modul pesanan menunggu respons pembayaran tanpa batas waktu, serta satu server menangani modul pesanan, pembayaran, dan notifikasi kurir dalam satu proses monolitik sehingga dapat menyebabkan kegagalan berantai ketika salah satu bagian mengalami masalah.
- Perbedaan pendapat (jika ada): ...

## [Tanggal diskusi 2]
- ...

## Review Silang
- Reynal mengomentari analisis Melvin: Analisis latency is zero sudah sesuai dengan skenario karena modul pesanan menunggu respons pembayaran tanpa batas waktu. Disarankan agar dampaknya terhadap aplikasi yang menjadi lambat dijelaskan lebih jelas.
- Melvin mengomentari analisis Reval: Analisis single point of failure sudah sesuai karena satu server menangani beberapa modul dalam satu proses monolitik. Disarankan agar dampak kegagalan server terhadap beberapa fungsi FoodGo dijelaskan lebih konkret.
- Reval mengomentari analisis I Adnyana Kusuma Wijaya: Analisis cascading failure sudah relevan karena masalah pada satu bagian dapat memengaruhi bagian lain. Disarankan agar hubungan antara permintaan yang tertahan dan meningkatnya beban server dijelaskan lebih jelas.
- I Adnyana Kusuma Wijaya mengomentari analisis Reynal: Analisis the network is reliable sudah sesuai dengan skenario karena terdapat asumsi jaringan selalu dapat diandalkan. Disarankan agar percobaan ulang dilakukan secara terbatas agar tidak menambah beban sistem.
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
| 19 September 2026 | ChatGPT | Membantu mengidentifikasi pitfall yang sesuai dengan skenario FoodGo dan membagi topik untuk 4 anggota kelompok. | AI memberikan beberapa pilihan pitfall yang relevan, seperti *the network is reliable*, *latency is zero*, *single point of failure*, dan *cascading failure*. | Kelompok mencocokkan kembali setiap pitfall dengan kondisi yang tertulis pada skenario dan membagi topik berdasarkan hasil diskusi kelompok. |
| 19 September 2026 | ChatGPT | Membantu menyusun poin diskusi kelompok berdasarkan pitfall yang sudah dipilih. | AI memberikan contoh hubungan antara masalah jaringan, keterlambatan komunikasi, penggunaan satu server, dan kegagalan berantai. | Kelompok memilih poin yang sesuai dengan hasil pembahasan dan menyesuaikan bahasanya agar sesuai dengan proses diskusi kelompok. |
| 22 September 2026 | ChatGPT | Membantu menyusun format review silang untuk analisis masing-masing anggota. | AI memberikan contoh masukan yang dapat digunakan untuk meninjau analisis anggota lain, seperti kesesuaian dengan skenario dan kejelasan dampak. | Kelompok menyesuaikan masukan dengan isi analisis masing-masing anggota dan mencatatnya pada bagian Review Silang. |
| 22 September 2026 | ChatGPT | Membantu mengecek dan merapikan struktur JURNAL.md serta log penggunaan AI. | AI memberikan saran mengenai urutan bagian jurnal dan cara mencatat penggunaan AI sesuai format yang diberikan. | Kelompok menggunakan saran tersebut sebagai panduan format, kemudian menyesuaikan isi berdasarkan kegiatan dan hasil diskusi kelompok sendiri. |
