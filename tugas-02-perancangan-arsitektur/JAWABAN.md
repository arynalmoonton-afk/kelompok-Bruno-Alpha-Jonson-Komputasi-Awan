# Tugas 2 — Perancangan Arsitektur FoodGo

**Kelompok:** [RAHULLLLLLL, OH IYA BANG]

| Nama | NIM | Kontribusi |
|---|---|---|
| Arynal Haq Syafi'i | 103072400155 | SOA dan Service |
| Melvin Crisna Martin Adoe | 103072400146 | Diagram dan dokumentasi |
| Revaldi Ramadhan Nugraha | 103072400059 | Alur komunikasi dan trade-off |
| I Wayan Adnyana Kusuma Wijaya  | 103072400040 | Publish-Subscribe dan Message Broker |

## 1. Gaya Arsitektur yang Dipilih

Kami memilih kombinasi Service-Oriented Architecture (SOA) dan Publish-Subscribe (Pub-Sub).

SOA digunakan untuk memisahkan sistem FoodGo menjadi beberapa service berdasarkan fungsinya, yaitu Service Katalog Resto, Service Pesanan, Service Pembayaran, Service Resto, dan Service Kurir/Notifikasi. Pemisahan ini membuat setiap service memiliki tanggung jawab masing-masing sehingga tidak semua fungsi bergantung pada satu aplikasi seperti pada arsitektur monolith sebelumnya.

Komunikasi sinkron dengan pola request-response digunakan pada proses yang membutuhkan respons secara langsung, seperti ketika pelanggan meminta data katalog dan ketika Service Pesanan melakukan proses pembayaran. Hasil pembayaran perlu diketahui terlebih dahulu sebelum proses pesanan dapat dilanjutkan.

Sementara itu, Publish-Subscribe digunakan untuk komunikasi asinkron melalui Message Broker. Ketika terjadi suatu perubahan atau proses pada pesanan, service dapat mengirim event ke Message Broker dan event tersebut dapat diterima oleh service yang membutuhkan tanpa harus melakukan pemanggilan secara langsung.

Kombinasi ini dipilih karena SOA membantu memisahkan fungsi utama FoodGo, sedangkan Pub-Sub membantu mengurangi ketergantungan langsung antar-service dalam penyebaran event.

## 2. Komponen dan Interaksi

Berdasarkan rancangan arsitektur FoodGo, terdapat beberapa komponen utama:

### 1. Pelanggan

Pelanggan merupakan pengguna yang berinteraksi dengan sistem untuk melihat katalog restoran, memilih menu, membuat pesanan, dan mendapatkan informasi mengenai proses pesanannya.

### 2. Service Katalog Resto

Service ini menangani informasi mengenai restoran dan menu yang tersedia. Pelanggan dapat meminta informasi katalog melalui service ini sebelum membuat pesanan.

### 3. Service Pesanan

Service Pesanan menangani proses pembuatan dan pengelolaan pesanan. Service ini juga berinteraksi dengan Service Pembayaran dan mengirimkan event ke Message Broker setelah proses pesanan berhasil.

### 4. Service Pembayaran

Service Pembayaran bertanggung jawab untuk memproses dan memverifikasi pembayaran. Service ini memberikan hasil pembayaran kembali kepada Service Pesanan.

### 5. Service Resto

Service Resto menangani informasi dan proses yang berkaitan dengan restoran, termasuk menerima informasi pesanan yang dikirim melalui mekanisme event.

### 6. Service Kurir/Notifikasi

Service ini menangani proses yang berkaitan dengan kurir dan notifikasi. Service ini digunakan untuk proses penugasan kurir dan penyampaian informasi atau perubahan status kepada pihak yang membutuhkan.

### 7. Message Broker

Message Broker menjadi perantara komunikasi Publish-Subscribe. Service yang menghasilkan event mengirimkannya ke Message Broker, kemudian Message Broker meneruskan event tersebut kepada service yang berlangganan event tersebut.

Secara keseluruhan, interaksi pada arsitektur menggunakan dua jenis komunikasi, yaitu sinkron (request-response) untuk proses yang membutuhkan respons langsung dan asinkron (event) melalui Message Broker untuk penyebaran informasi antar-service.

## 3. Alur Skenario End-to-End

Skenario yang digunakan adalah:

Pelanggan membuat pesanan → pembayaran → restoran menerima pesanan → kurir ditugaskan.

### 3.1 Pelanggan melihat katalog

Pelanggan meminta informasi restoran dan menu kepada Service Katalog Resto.

Jenis komunikasi: Sinkron / Request-Response.

Service Katalog Resto memberikan informasi katalog sebagai response kepada pelanggan.

### 3.2 Pelanggan membuat pesanan

Setelah memilih menu, pelanggan mengirim permintaan pembuatan pesanan kepada Service Pesanan.

Jenis komunikasi: Sinkron / Request-Response.

Service Pesanan menerima request dan memproses pembuatan pesanan.

### 3.3 Service Pesanan melakukan pembayaran

Service Pesanan mengirim permintaan pembayaran kepada Service Pembayaran.

Jenis komunikasi: Sinkron / Request-Response.

Service Pembayaran memproses pembayaran dan memberikan status pembayaran kembali kepada Service Pesanan.

Komunikasi ini bersifat sinkron karena Service Pesanan membutuhkan hasil pembayaran untuk menentukan apakah proses pesanan dapat dilanjutkan.

### 3.4 Service Pesanan mengirim event

Setelah pesanan berhasil diproses, Service Pesanan mengirim event OrderCreated melalui Message Broker.

Jenis komunikasi: Asinkron / Event.

Service Pesanan tidak perlu melakukan pemanggilan langsung kepada setiap service yang membutuhkan informasi tersebut.

### 3.5 Event diterima oleh service yang berlangganan

Message Broker meneruskan event OrderCreated kepada service yang berlangganan sesuai kebutuhan pada diagram.

Jenis komunikasi: Asinkron / Publish-Subscribe.

Dengan mekanisme ini, penerima event tidak perlu dipanggil secara langsung oleh Service Pesanan.

### 3.6 Kurir ditugaskan

Setelah proses terkait pesanan dan kurir dilakukan, Service Kurir/Notifikasi menghasilkan event CourierAssigned melalui Message Broker.

Jenis komunikasi: Asinkron / Event.

Event tersebut dapat digunakan oleh service yang membutuhkan informasi bahwa kurir telah ditugaskan.

Ringkasan jenis komunikasi
Komunikasi	Jenis
Pelanggan → Service Katalog Resto	Sinkron / Request-Response
Pelanggan → Service Pesanan	Sinkron / Request-Response
Service Pesanan → Service Pembayaran	Sinkron / Request-Response
Service Pembayaran → Service Pesanan	Sinkron / Response
Service Pesanan → Message Broker	Asinkron / Event
Message Broker → Service terkait	Asinkron / Publish-Subscribe
Service Kurir/Notifikasi → Message Broker	Asinkron / Event
Message Broker → Service terkait	Asinkron / Event
## 4. Analisis

Arsitektur ini mengatasi masalah coupling pada Tugas 1 karena sistem FoodGo yang sebelumnya berbentuk monolith dipisahkan menjadi beberapa service dengan tanggung jawab yang berbeda. Dengan pemisahan tersebut, perubahan pada satu bagian tidak harus menyebabkan seluruh sistem ikut berubah atau mengalami gangguan.

Pada bagian SOA, komunikasi antara Service Pesanan dan Service Pembayaran dilakukan secara langsung menggunakan request-response. Hal ini membuat Service Pesanan dapat mengetahui hasil pembayaran sebelum melanjutkan proses berikutnya.

Sementara itu, penggunaan Publish-Subscribe membuat service tidak perlu mengetahui secara langsung seluruh service yang menerima suatu event. Service Pesanan cukup mengirim event ke Message Broker, kemudian broker mendistribusikannya kepada service yang membutuhkan.

Trade-off SOA

Pemisahan service membuat sistem lebih terstruktur dan setiap service dapat dikembangkan secara lebih independen. Namun, komunikasi antar-service bergantung pada jaringan. Jika Service Pembayaran mengalami gangguan atau lambat memberikan respons, proses pada Service Pesanan juga dapat tertunda karena menggunakan komunikasi sinkron.

Untuk mengurangi dampak tersebut, sistem dapat menggunakan mekanisme seperti timeout dan retry pada komunikasi antar-service.

Trade-off Publish-Subscribe

Publish-Subscribe mengurangi ketergantungan langsung antar-service, tetapi membuat alur sistem menjadi lebih sulit dilacak karena proses tidak berjalan dalam satu jalur yang linear.

Jika event OrderCreated atau CourierAssigned mengalami masalah, perlu dilakukan pengecekan pada beberapa bagian, seperti service yang mengirim event, Message Broker, dan service yang menerima event.

Selain itu, event dapat mengalami keterlambatan atau gagal diproses. Sistem dapat menggunakan mekanisme retry agar event yang gagal dapat diproses kembali.

Terdapat juga kemungkinan event diterima lebih dari satu kali. Karena itu, service penerima perlu memastikan bahwa event yang sama tidak menyebabkan proses ganda.

Monitoring juga menjadi lebih kompleks karena satu pesanan melewati beberapa service. Penggunaan ID pesanan atau correlation ID dapat membantu melacak proses pesanan dari satu service ke service lainnya.

Jadi, trade-off utama dari arsitektur ini adalah coupling antar-service berkurang dan sistem menjadi lebih fleksibel, tetapi kompleksitas dalam pengelolaan, monitoring, error handling, dan debugging menjadi lebih tinggi.

## Kesimpulan

FoodGo menggunakan kombinasi Service-Oriented Architecture (SOA) dan Publish-Subscribe (Pub-Sub) untuk mengatasi masalah coupling pada sistem monolith sebelumnya. SOA digunakan untuk memisahkan fungsi utama FoodGo menjadi beberapa service, sedangkan Pub-Sub digunakan untuk komunikasi berbasis event melalui Message Broker.

Komunikasi sinkron digunakan pada proses yang membutuhkan respons secara langsung, seperti pengambilan data katalog dan proses pembayaran. Sementara itu, komunikasi asinkron digunakan untuk penyebaran event seperti OrderCreated dan CourierAssigned melalui Message Broker.

Dengan rancangan ini, setiap service dapat memiliki tanggung jawab yang lebih jelas dan tidak terlalu bergantung langsung pada service lainnya. Namun, penggunaan beberapa service dan Message Broker juga menambah kompleksitas dalam monitoring, error handling, dan debugging.
