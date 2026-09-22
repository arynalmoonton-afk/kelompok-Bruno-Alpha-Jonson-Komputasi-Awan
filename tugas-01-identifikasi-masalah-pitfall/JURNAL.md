# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [Tanggal diskusi 1 Sabtu, 19 September 2026]
- Peserta: Reynal, Melvin, Reval, Wayan
- Poin diskusi: Menentukan pitfall yang paling sesuai dengan kondisi FoodGo. Kelompok kami memilih the network is reliable, latency is zero, single point of failure, dan cascading failure karena pada skenario terdapat asumsi jaringan selalu dapat diandalkan, modul pesanan menunggu respons pembayaran tanpa batas waktu, serta satu server menangani modul pesanan, pembayaran, dan notifikasi kurir dalam satu proses monolitik sehingga dapat menyebabkan kegagalan berantai ketika salah satu bagian mengalami masalah.
- Perbedaan pendapat (jika ada): ...

## [Tanggal diskusi 2 Selasa, 22 September 2026]
- Peserta: Reynal, Melvin, Reval, Wayan
- Poin diskusi: Memantapkan empat pitfall yang dipilih serta argumen dan solusi masing-masing agar sesuai dengan kondisi pada skenario FoodGo.
- Perbedaan pendapat (jika ada): Tidak ada.

## Review Silang
- Reynal mengomentari analisis Melvin: Analisis latency is zero sudah sesuai dengan skenario karena modul pesanan menunggu respons pembayaran tanpa batas waktu. Disarankan agar dampaknya terhadap aplikasi yang menjadi lambat dijelaskan lebih jelas.
- Melvin mengomentari analisis Reval: Analisis single point of failure sudah sesuai karena satu server menangani beberapa modul dalam satu proses monolitik. Disarankan agar dampak kegagalan server terhadap beberapa fungsi FoodGo dijelaskan lebih konkret.
- Reval mengomentari analisis Wayan: Analisis cascading failure sudah relevan karena masalah pada satu bagian dapat memengaruhi bagian lain. Disarankan agar hubungan antara permintaan yang tertahan dan meningkatnya beban server dijelaskan lebih jelas.
- Wayan mengomentari analisis Reynal: Analisis the network is reliable sudah sesuai dengan skenario karena terdapat asumsi jaringan selalu dapat diandalkan. Disarankan agar percobaan ulang dilakukan secara terbatas agar tidak menambah beban sistem.
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 19 September 2026 | ChatGPT | Dari skenario FoodGo ini, pitfall apa saja yang paling sesuai? Kami ingin membagi analisis untuk 4 anggota kelompok. | AI menyarankan beberapa masalah yang dapat dikaitkan dengan skenario, termasuk *the network is reliable*, *latency is zero*, *single point of failure*, dan *cascading failure*. | Kelompok mencocokkan kembali setiap masalah dengan kondisi yang benar-benar disebutkan dalam skenario dan mendiskusikannya sebelum menentukan pembagian tugas. |
| 19 September 2026 | ChatGPT | Bisa bantu jelaskan keempat pitfall tersebut sesuai dengan format tugas, terutama bagian bukti dari skenario, dampak, solusi, dan trade-off? | AI memberikan kerangka pembahasan untuk masing-masing pitfall berdasarkan bagian-bagian yang diminta dalam tugas. | Kelompok menggunakan kerangka tersebut sebagai bahan diskusi, kemudian mengembangkan analisis dan menyesuaikannya dengan pemahaman masing-masing anggota. |
| 19 September 2026 | ChatGPT | Apakah *single point of failure* dan *cascading failure* memang boleh digunakan untuk tugas ini, mengingat keduanya bukan bagian dari delapan *Fallacies*? | AI menjelaskan bahwa tugas juga memperbolehkan masalah desain sistem terdistribusi lain yang relevan, sehingga kedua masalah tersebut dapat digunakan selama dikaitkan dengan skenario. | Kelompok memeriksa kembali instruksi tugas dan menggunakan kedua masalah tersebut sebagai masalah desain tambahan, bukan sebagai bagian dari delapan *Fallacies*. |
| 22 September 2026 | ChatGPT | Bisa bantu merapikan poin diskusi dan review silang untuk empat anggota supaya sesuai dengan format JURNAL.md? | AI memberikan contoh struktur poin diskusi dan review silang. | Kelompok menyesuaikan struktur tersebut dengan kegiatan diskusi dan hasil review yang dilakukan oleh anggota kelompok. |
| 22 September 2026 | ChatGPT | Tolong bantu cek apakah kesimpulan kami sudah mencakup keempat masalah yang dianalisis dan apakah istilah teknisnya sudah konsisten. | AI membantu mengecek keterkaitan antara keempat masalah dengan kesimpulan serta menyarankan konsistensi penggunaan istilah. | Kelompok menggunakan saran tersebut untuk memperbaiki istilah dan memastikan kesimpulan tetap sesuai dengan hasil analisis kelompok. |
