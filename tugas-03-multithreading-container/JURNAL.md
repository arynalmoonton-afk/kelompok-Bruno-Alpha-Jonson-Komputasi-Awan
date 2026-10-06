# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock

- Jumlah pesanan yang disimulasikan: **100 pesanan** dengan **10 thread**.
- Hasil `processed_count`: **36 dari 100 pesanan**.

Race condition terjadi karena beberapa thread mengakses dan mengubah `processed_count` secara bersamaan tanpa penguncian. Beberapa thread dapat membaca nilai counter yang sama sebelum thread lain selesai memperbaruinya. Akibatnya, hasil perubahan dari satu thread dapat tertimpa oleh thread lain sehingga jumlah akhir menjadi lebih kecil dari jumlah pesanan sebenarnya.

Percobaan tanpa lock ini dilakukan untuk membuktikan bahwa penggunaan data bersama pada multithreading dapat menghasilkan nilai yang tidak sesuai apabila tidak ada mekanisme sinkronisasi.

## Percobaan dengan Lock

- Jumlah pesanan yang disimulasikan: **100 pesanan** dengan **10 thread**.
- Hasil `processed_count`: **100 dari 100 pesanan**.

Perbaikan dilakukan dengan menggunakan `threading.Lock()`. Bagian kode yang membaca dan mengubah `processed_count` dibungkus dengan `with lock:` sehingga hanya satu thread yang dapat mengakses bagian tersebut pada satu waktu.

Setelah menggunakan lock, hasil counter menjadi sesuai dengan jumlah pesanan. Hal ini menunjukkan bahwa race condition yang terjadi pada percobaan sebelumnya berhasil dicegah.

## Perbandingan

| Percobaan | Hasil | Keterangan |
|---|---:|---|
| Tanpa Lock | 36/100 | Terjadi race condition |
| Dengan Lock | 100/100 | Race condition berhasil dicegah |

## Docker

Program kemudian dijalankan menggunakan Docker dengan base image **`python:3.12-slim`**. Karena program hanya menggunakan library bawaan Python, tidak diperlukan dependency tambahan.

Image dibuat dengan perintah:

`docker build -t foodgo-order-sim .`

Setelah image berhasil dibuat, container dijalankan menggunakan:

`docker run --rm foodgo-order-sim`

Hasil pengujian di dalam container menunjukkan **100 dari 100 pesanan berhasil diproses**.

## Kendala Docker

Kendala awal terjadi karena Dockerfile masih menggunakan placeholder `python:__ISI_VERSI__-slim`, sehingga proses build gagal. Masalah tersebut diperbaiki dengan menggantinya menjadi `python:3.12-slim`.

Setelah diperbaiki, proses build dan run Docker berhasil dilakukan tanpa masalah.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 06-10-2026 | ChatGPT | Membantu memberikan gambaran struktur pengerjaan Tugas 3 tentang multithreading, race condition, penggunaan Lock, dan Docker. | AI memberikan gambaran mengenai tahapan pengerjaan, poin-poin yang perlu diperhatikan dalam percobaan, serta struktur dokumentasi yang dapat digunakan dalam jurnal. | Saran tersebut digunakan sebagai referensi awal untuk menentukan alur pengerjaan. Penjelasan, hasil percobaan, kode, dan dokumentasi kemudian disesuaikan serta dikerjakan berdasarkan proses yang dilakukan oleh kelompok. |
