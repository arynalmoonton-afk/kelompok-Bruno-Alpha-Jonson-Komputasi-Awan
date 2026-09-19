# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## Sabtu, 19 September 2026
- Peserta: Reynal, Melvin, Reval
- Poin diskusi: Menentukan pitfall yang paling sesuai dengan kondisi FoodGo. Kelompok kami memilih the network is reliable, latency is zero, dan single point of failure karena satu server menangani modul pesanan, pembayaran, dan notifikasi kurir dalam satu proses monolitik.
- Perbedaan pendapat (jika ada): ...

## [Tanggal diskusi 2]
- ...

## Review Silang
- Reynal mengomentari analisis Melvin: Analisis tentang latency is zero sudah sesuai dengan skenario karena modul pesanan memang menunggu respons dari modul pembayaran tanpa batas waktu. Disarankan agar dampaknya lebih dikaitkan dengan penggunaan sumber daya server ketika banyak permintaan tertahan.
- Reynal mengomentari analisis Reval: Penjelasan tentang satu server yang menangani beberapa modul sudah sesuai dengan skenario. Disarankan untuk memperjelas bahwa ketika server mengalami kegagalan, beberapa fungsi dapat ikut terganggu karena berjalan dalam satu proses yang sama.
- Reval mengomentari analisis Melvin: Analisis sudah menjelaskan hubungan antara keterlambatan modul pembayaran dan aplikasi yang menjadi lambat. Disarankan untuk menambahkan bahwa sistem perlu memiliki batas waktu agar tidak terus menunggu layanan yang sedang bermasalah.
- Reval mengomentari analisis Reynal: Analisis tentang the network is reliable sudah sesuai dengan asumsi yang tertulis pada skenario. Disarankan agar bagian solusi juga menjelaskan bahwa percobaan ulang perlu dibatasi supaya tidak menambah beban pada layanan yang sedang bermasalah.
- Melvin mengomentari analisis Reynal: Penjelasan mengenai kegagalan komunikasi antar layanan sudah relevan dengan kondisi FoodGo. Disarankan untuk memperjelas contoh dampaknya ketika permintaan dari modul pesanan gagal diproses.
- Melvin mengomentari analisis Reval: Analisis mengenai satu server dan beberapa modul sudah sesuai dengan kondisi yang diberikan. Disarankan agar pemisahan modul dilakukan secara bertahap agar tidak membuat sistem menjadi terlalu kompleks.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
