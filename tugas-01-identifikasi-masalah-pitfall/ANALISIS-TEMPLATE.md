# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [RAHULLLLLLL, OH IYA BANG]

| Nama | NIM | Kontribusi |
|---|---|---|
| Arynal Haq Syafi'i | 103072400155 | Pitfall 1 — The Network is Reliable] |
| Melvin Crisna Martin Adoe | 103072400146 | Pitfall 2 — Latency is Zero |
| Revaldi Ramadhan Nugraha | 103072400059 | Pitfall 3 — Single Point of Failure dan Masalah Skalabilitas |
| I Wayan Adnyana Kusuma Wijaya  | 103072400040 | Pitfall 4 — Cascading Failure / Kegagalan Berantai |

## Pitfall 1 — The Network is Reliable — ditulis oleh Revaldi Ramadhan Nugraha


**Bukti di skenario:** 
Pada skenario disebutkan bahwa kode FoodGo memiliki asumsi:

> `# network is always reliable, no need for retry`

Hal tersebut menunjukkan bahwa sistem menganggap komunikasi antar komponen/service akan selalu berhasil dan tidak memerlukan mekanisme penanganan kegagalan komunikasi.

**Kenapa ini keliru:** 
Dalam sistem terdistribusi, komunikasi antar service menggunakan jaringan yang dapat mengalami gangguan. Request dapat gagal, koneksi dapat terputus, atau service tujuan tidak memberikan respons. Karena itu, sistem tidak dapat menganggap setiap komunikasi pasti berhasil.

**Dampak ke FoodGo:** 
Ketika trafik meningkat pada jam makan siang atau saat promo, kemungkinan terjadinya kegagalan komunikasi juga dapat meningkat. Jika request dari modul pesanan ke service lain gagal dan tidak terdapat mekanisme retry atau penanganan error, proses pemesanan dapat gagal atau menghasilkan timeout.

Kondisi ini dapat menyebabkan pengguna mengalami kegagalan saat melakukan pemesanan, sementara sistem juga harus menangani banyak request yang masuk secara bersamaan.

**Solusi:** 
FoodGo dapat menerapkan **timeout dan retry dengan exponential backoff** pada komunikasi antar service. Selain itu, error dari service tujuan perlu ditangani sehingga kegagalan satu request tidak langsung menyebabkan seluruh proses aplikasi bermasalah.

**Trade-off:** 
Retry tidak selalu gratis. Jika service tujuan sedang mengalami overload, terlalu banyak retry justru dapat menambah jumlah request dan memperparah beban. Oleh karena itu, retry perlu dibatasi, misalnya dengan jumlah percobaan maksimum dan backoff.

---

## Pitfall 2 — Latency is Zero — ditulis oleh Arynal Haq Syafi'i

**Bukti di skenario:** 
Skenario menyebutkan bahwa:

modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu

Hal ini menunjukkan bahwa sistem tidak memperhitungkan kemungkinan adanya keterlambatan respons dari modul pembayaran.

**Kenapa ini keliru:** 
Dalam sistem yang memiliki komunikasi antar service, sebuah request tidak selalu mendapatkan respons secara langsung. Service tujuan dapat mengalami beban tinggi sehingga membutuhkan waktu lebih lama untuk memproses request.

Jika sistem menganggap komunikasi selalu cepat atau tidak memberikan batas waktu, proses yang menunggu respons dapat terus menggunakan resource.

**Dampak ke FoodGo:** 
Saat promo atau jam makan siang, service pembayaran dapat menerima banyak request sekaligus dan menjadi lambat. Modul pesanan yang menunggu respons pembayaran tanpa timeout akan memiliki banyak proses yang tertahan.

Jika jumlah request terus bertambah, resource seperti thread, connection, atau memory dapat ikut terkonsumsi. Pada akhirnya aplikasi menjadi sangat lambat dan bahkan dapat menyebabkan server crash seperti yang terjadi pada skenario.

**Solusi:** 
FoodGo dapat menerapkan timeout pada setiap komunikasi antar service. Jika diperlukan, sistem juga dapat menggunakan circuit breaker agar request ke service yang sedang bermasalah tidak terus dilakukan.

Pemisahan proses yang membutuhkan respons langsung dan proses yang dapat dilakukan secara asynchronous juga dapat dipertimbangkan.

**Trade-off:** 
Timeout dan circuit breaker dapat meningkatkan ketahanan sistem, tetapi dapat menyebabkan request dianggap gagal walaupun service sebenarnya masih sedang memprosesnya. Karena itu, sistem juga perlu mempertimbangkan mekanisme seperti idempotency agar retry atau request ulang tidak menyebabkan pembayaran atau pesanan diproses dua kali.

---

## Pitfall 3 — Single Point of Failure dan Masalah Skalabilitas — ditulis oleh Melvin Crisna Martin Adoe 

**Bukti di skenario:** 
Pada skenario disebutkan:

satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.

Selain itu, disebutkan bahwa server backend kadang crash total dan perlu di-restart manual.

**Masalah design:** 
Ketika seluruh fungsi sistem berjalan pada satu proses/server, beban dari satu bagian dapat memengaruhi bagian lainnya. Modul pembayaran yang sedang sibuk, misalnya, dapat menggunakan resource yang seharusnya juga digunakan oleh modul pesanan dan notifikasi.

Server tunggal juga menjadi single point of failure. Jika server tersebut mengalami crash, seluruh fungsi yang berada di dalamnya ikut tidak tersedia.

**Dampak ke FoodGo:** 
Ketika terjadi lonjakan pesanan, seluruh modul menerima beban secara bersamaan. Karena semuanya berada pada satu proses, peningkatan beban dapat membuat resource server habis sehingga aplikasi menjadi lambat atau crash.

Jika server crash, bukan hanya pembayaran yang terganggu, tetapi fungsi pesanan dan notifikasi kurir juga ikut terdampak. Restart manual kemudian menyebabkan downtime sampai server kembali berjalan.

**Solusi:** 
FoodGo dapat mulai memisahkan modul yang memiliki beban dan kebutuhan berbeda menjadi service yang lebih terpisah, misalnya service pesanan, pembayaran, dan notifikasi.

Untuk tahap awal, pemisahan tidak harus langsung menjadi arsitektur microservices yang kompleks. Modul yang paling kritis atau paling berat dapat dipisahkan terlebih dahulu dan kemudian dijalankan pada beberapa instance agar beban dapat didistribusikan.

**Trade-off:** 
Pemisahan service dapat meningkatkan skalabilitas dan mengurangi dampak kegagalan satu komponen, tetapi membuat sistem menjadi lebih kompleks. Tim harus menangani komunikasi antar service, monitoring, deployment, dan kemungkinan kegagalan jaringan yang sebelumnya tidak muncul pada satu proses monolitik.

---

## Pitfall 4 Cascading Failure / Kegagalan Berantai ditulis oleh I Wayan Adnyana Kusuma Wijaya 


**Bukti di skenario:** 
Skenario menyebutkan bahwa modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu. Selain itu, semua modul seperti pesanan, pembayaran, dan notifikasi kurir berjalan dalam satu proses monolitik.

**Kenapa ini keliru:** 
Ketika satu bagian sistem mengalami keterlambatan atau masalah, dampaknya dapat menyebar ke bagian lain. Modul pesanan yang terus menunggu modul pembayaran dapat membuat semakin banyak proses tertahan. Karena modul-modul tersebut juga berjalan dalam satu proses, masalah pada satu bagian dapat ikut memengaruhi bagian lainnya.

Hal ini disebut sebagai kegagalan berantai, yaitu ketika masalah pada satu bagian menyebabkan beban atau masalah baru pada bagian lain sehingga gangguan semakin meluas.

**Dampak ke FoodGo:** 
Saat jumlah pesanan meningkat, modul pembayaran yang mengalami keterlambatan dapat menyebabkan banyak permintaan dari modul pesanan ikut tertahan. Permintaan yang menumpuk menggunakan sumber daya server semakin banyak.

Jika kondisi tersebut terus berlangsung, server menjadi kewalahan. Akibatnya, aplikasi menjadi lambat, beberapa permintaan mengalami batas waktu, dan pada kondisi yang lebih parah server dapat mengalami crash seperti yang terjadi pada skenario FoodGo.

**Solusi:** 
FoodGo dapat menerapkan batas waktu komunikasi, membatasi percobaan ulang, dan menggunakan pemisahan layanan agar masalah pada satu bagian tidak langsung memengaruhi seluruh sistem. Untuk proses yang tidak harus mendapatkan respons secara langsung, FoodGo juga dapat menggunakan pemrosesan yang berjalan secara terpisah.

**Trade-off:** 
Pemisahan layanan dapat mengurangi dampak kegagalan berantai, tetapi membuat sistem lebih kompleks karena setiap layanan harus berkomunikasi melalui jaringan. Tim juga perlu melakukan pemantauan dan penanganan kegagalan pada masing-masing layanan.

---

## Kesimpulan Kelompok

Berdasarkan analisis kelompok, permasalahan FoodGo tidak hanya disebabkan oleh meningkatnya jumlah pesanan, tetapi juga oleh asumsi dan desain sistem yang kurang tepat. Asumsi bahwa jaringan selalu dapat diandalkan menyebabkan sistem tidak memiliki penanganan yang cukup ketika komunikasi mengalami kegagalan. Selain itu, tidak adanya batas waktu pada komunikasi antara modul pesanan dan pembayaran membuat proses dapat tertahan ketika modul pembayaran mengalami keterlambatan.

Penggunaan satu server dan satu proses untuk menangani modul pesanan, pembayaran, dan notifikasi kurir juga membuat sistem memiliki titik kegagalan tunggal. Ketika salah satu bagian mengalami masalah atau beban meningkat, dampaknya dapat menyebar ke bagian lain dan menyebabkan kegagalan berantai hingga server menjadi kewalahan dan mengalami crash.

Sebagai langkah awal, FoodGo dapat menerapkan batas waktu pada komunikasi, melakukan percobaan ulang secara terbatas, menggunakan mekanisme pemutus sementara komunikasi ketika suatu layanan bermasalah, serta memisahkan modul secara bertahap. Setiap solusi memiliki konsekuensi, seperti meningkatnya kerumitan sistem dan kemungkinan percobaan ulang menambah beban. Karena itu, perbaikan perlu dilakukan secara bertahap sesuai kebutuhan dan kemampuan tim.

[Ringkasan: jika FoodGo memperbaiki keempat pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
