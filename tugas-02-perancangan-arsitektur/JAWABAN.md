
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
Pelanggan merupakan pengguna yang berinteraksi langsung dengan sistem FoodGo. Pelanggan dapat melihat daftar restoran dan menu, membuat pesanan, melakukan pembayaran, serta memperoleh informasi mengenai status pesanan.

Interaksi pelanggan dengan sistem dilakukan melalui request kepada service yang sesuai. Misalnya, ketika pelanggan ingin melihat menu, request dikirimkan ke Service Katalog Resto. Ketika pelanggan ingin membuat pesanan, request dikirimkan ke Service Pesanan.

### 2. Service Katalog Resto
Service Katalog Resto bertanggung jawab untuk menyediakan informasi mengenai restoran dan menu yang tersedia. Data yang dikelola dapat mencakup nama restoran, daftar menu, harga, ketersediaan menu, dan informasi pendukung lainnya.

Service ini menerima request dari pelanggan dan memberikan response secara langsung.

Jenis komunikasi: Sinkron / Request-Response.

Contohnya, pelanggan meminta daftar menu pada suatu restoran. Service Katalog Resto mengambil data yang diperlukan kemudian mengirimkan informasi tersebut kembali kepada pelanggan.

### 3. Service Pesanan
Service Pesanan merupakan service yang menangani proses utama pemesanan makanan. Service ini menerima pesanan dari pelanggan, mencatat detail pesanan, menghitung informasi pesanan, serta mengatur proses selanjutnya setelah pesanan dibuat.

Service Pesanan berkomunikasi secara sinkron dengan Service Pembayaran ketika membutuhkan proses pembayaran. Setelah pesanan berhasil dibuat dan pembayaran berhasil diproses, Service Pesanan menghasilkan event yang dikirimkan ke Message Broker.

Jenis komunikasi:

Pelanggan → Service Pesanan: Sinkron / Request-Response.

Service Pesanan → Service Pembayaran: Sinkron / Request-Response.

Service Pesanan → Message Broker: Asinkron / Event.

Salah satu event yang dihasilkan adalah OrderCreated, yang menunjukkan bahwa pesanan telah berhasil dibuat dan dapat diproses oleh service lain yang membutuhkan informasi tersebut.

### 4. Service Pembayaran
Service Pembayaran bertanggung jawab menangani proses pembayaran dan memberikan informasi mengenai hasil pembayaran kepada Service Pesanan.

Ketika Service Pesanan mengirimkan request pembayaran, Service Pembayaran melakukan proses dan memberikan response berupa status pembayaran, misalnya berhasil atau gagal.

Jenis komunikasi: Sinkron / Request-Response.

Komunikasi ini menggunakan pola sinkron karena Service Pesanan membutuhkan hasil pembayaran untuk menentukan apakah proses pesanan dapat dilanjutkan. Jika pembayaran berhasil, pesanan dapat diteruskan ke tahap berikutnya. Jika pembayaran gagal, proses pesanan dapat dihentikan atau ditangani sesuai mekanisme yang telah ditentukan.

### 5. Service Resto
Service Resto menangani proses yang berkaitan dengan pihak restoran setelah pesanan dibuat. Service ini dapat menerima informasi mengenai pesanan yang perlu diproses oleh restoran.

Informasi pesanan diterima melalui event yang disebarkan oleh Message Broker. Dengan demikian, Service Pesanan tidak perlu melakukan pemanggilan langsung ke Service Resto.

Jenis komunikasi: Asinkron / Publish-Subscribe.

Sebagai contoh, ketika Service Pesanan menghasilkan event OrderCreated, Service Resto yang berlangganan event tersebut dapat menerima informasi pesanan dan menggunakannya untuk memulai proses pada restoran.

### 6. Service Kurir/Notifikasi
Service Kurir/Notifikasi menangani proses yang berkaitan dengan penugasan kurir dan penyampaian informasi status pesanan kepada pihak yang membutuhkan.

Service ini dapat menerima event dari Message Broker untuk mengetahui adanya pesanan yang perlu diproses. Setelah kurir berhasil ditugaskan, service menghasilkan event CourierAssigned dan mengirimkannya kembali ke Message Broker.

Jenis komunikasi: Asinkron / Publish-Subscribe.

Event CourierAssigned kemudian dapat diterima oleh service lain yang membutuhkan informasi mengenai kurir yang telah ditugaskan, misalnya service yang menangani informasi status pesanan atau notifikasi kepada pelanggan.

### 7. Message Broker
Message Broker berfungsi sebagai perantara komunikasi asinkron antara service dalam arsitektur FoodGo. Message Broker menerima event yang dipublikasikan oleh suatu service dan mendistribusikannya kepada service yang telah berlangganan event tersebut.

Pada rancangan ini, beberapa event yang digunakan antara lain:

OrderCreated, yaitu event yang menunjukkan bahwa pesanan telah berhasil dibuat.

CourierAssigned, yaitu event yang menunjukkan bahwa kurir telah berhasil ditugaskan.

Penggunaan Message Broker membuat publisher tidak perlu mengetahui secara langsung siapa saja subscriber dari suatu event. Hal ini mengurangi ketergantungan langsung antar-service dan memungkinkan service baru untuk berlangganan event tertentu tanpa harus mengubah service yang menghasilkan event.

Berikut merupakan diagram arsitektur FoodGo:

![Diagram Arsitektur FoodGo](diagram/Diagram%20Tanpa%20Judul.drawio.png)

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

### Ringkasan jenis komunikasi
| Komunikasi | Jenis |
|---|---|
| Pelanggan → Service Katalog Resto | Sinkron / Request-Response |
| Pelanggan → Service Pesanan | Sinkron / Request-Response |
| Service Pesanan → Service Pembayaran | Sinkron / Request-Response |
| Service Pembayaran → Service Pesanan | Sinkron / Response |
| Service Pesanan → Message Broker | Asinkron / Event |
| Message Broker → Service terkait | Asinkron / Publish-Subscribe |
| Service Kurir/Notifikasi → Message Broker | Asinkron / Event |
| Message Broker → Service terkait | Asinkron / Event |
## 4. Analisis

Arsitektur ini mengatasi masalah coupling pada Tugas 1 karena sistem FoodGo yang sebelumnya berbentuk monolith dipisahkan menjadi beberapa service dengan tanggung jawab yang berbeda. Dengan pemisahan tersebut, perubahan pada satu bagian tidak harus menyebabkan seluruh sistem ikut berubah atau mengalami gangguan.

Pada bagian SOA, komunikasi antara Service Pesanan dan Service Pembayaran dilakukan secara langsung menggunakan request-response. Hal ini membuat Service Pesanan dapat mengetahui hasil pembayaran sebelum melanjutkan proses berikutnya.

Sementara itu, penggunaan Publish-Subscribe membuat service tidak perlu mengetahui secara langsung seluruh service yang menerima suatu event. Service Pesanan cukup mengirim event ke Message Broker, kemudian broker mendistribusikannya kepada service yang membutuhkan.

### Trade-off SOA

Pemisahan service membuat sistem lebih terstruktur dan setiap service dapat dikembangkan secara lebih independen. Namun, komunikasi antar-service bergantung pada jaringan. Jika Service Pembayaran mengalami gangguan atau lambat memberikan respons, proses pada Service Pesanan juga dapat tertunda karena menggunakan komunikasi sinkron.

Untuk mengurangi dampak tersebut, sistem dapat menggunakan mekanisme seperti timeout dan retry pada komunikasi antar-service.

### Trade-off Publish-Subscribe

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
