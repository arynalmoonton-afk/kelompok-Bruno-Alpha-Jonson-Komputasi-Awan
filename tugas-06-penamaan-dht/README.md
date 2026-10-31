# Tugas 6 (Pekan 6) — Penamaan & Resolusi Lokasi

**Materi terkait:** Flat Naming, Structured Naming (DNS), Distributed Hash Table (DHT)/Chord.

## Studi Kasus

Pelanggan FoodGo kesulitan menemukan alamat IP server kurir yang **dinamis** (kurir berpindah lokasi/jaringan, IP-nya sering berubah). FoodGo butuh cara memetakan **ID Kurir** (identitas tetap) ke **alamat IP terkininya** tanpa server pusat tunggal yang jadi bottleneck/single point of failure.

## Tugas Kelompok

Implementasikan **simulasi Chord DHT** sederhana (single-process, tidak perlu jaringan sungguhan — cukup simulasi struktur data & algoritma di satu program Python) yang memetakan ID Kurir ke alamat IP mereka.

Konsep yang harus terlihat jalan dalam simulasi kalian:
1. **Consistent hashing**: ID Kurir dan ID Node di-hash ke ruang angka yang sama (mis. 0–255 untuk kesederhanaan, `m=8` bit).
2. **Ring topology**: node-node diurutkan melingkar berdasarkan hasil hash-nya.
3. **Lookup**: fungsi `lookup(kurir_id)` yang menemukan node mana yang bertanggung jawab menyimpan mapping ID Kurir tersebut → alamat IP-nya (aturan Chord: node dengan ID hash **terkecil yang lebih besar atau sama dengan** hash key, disebut *successor*).
4. **Perubahan topologi**: simulasikan minimal satu node baru bergabung (`join`) atau satu node keluar (`leave`), tunjukkan bagaimana mapping berpindah tanggung jawab ke node lain.

Skeleton disediakan di `src/chord_simulation.py` dengan fungsi hashing dan struktur ring sudah ada — bagian `lookup()`, `join()`, dan `leave()` sengaja dikosongkan.

### Cara Menjalankan

```bash
python3 src/chord_simulation.py
```

## Tugas Analisis (`README.md`)

1. Jelaskan **kenapa DHT/Chord** lebih cocok untuk kasus ini dibanding **flat naming sederhana** (mis. tabel pusat ID→IP) atau **DNS konvensional** — kaitkan dengan sifat "IP kurir sering berubah" dan kebutuhan tanpa titik gagal tunggal.
2. Gambarkan (boleh pakai Mermaid, lihat Tugas 2) ring topology dari simulasi kalian, tandai node mana yang bertanggung jawab atas ID Kurir mana.
3. Jelaskan apa yang terjadi pada mapping saat sebuah node **keluar** dari ring (siapa yang mengambil alih tanggung jawabnya) — dukung dengan output program.

## Jawaban

### 1. Analisis DHT/Chord Dibandingkan Flat Naming dan DNS Konvensional (Arynal Haq Syafi'i & I Wayan Adnyana Kusuma)

FoodGo membutuhkan mekanisme pemetaan ID Kurir yang bersifat tetap ke alamat IP yang dapat berubah karena kurir dapat berpindah lokasi atau jaringan. Oleh karena itu, diperlukan sistem penamaan yang mampu menangani perubahan alamat IP tanpa bergantung pada satu server pusat.

#### Perbandingan dengan Flat Naming (I Wayan Adnyana Kusuma)

Pada pendekatan flat naming sederhana, pemetaan ID Kurir ke alamat IP dapat disimpan dalam sebuah tabel pusat. Pendekatan ini mudah diterapkan, tetapi seluruh proses pencarian dan pembaruan alamat IP bergantung pada satu komponen. Jika server pusat mengalami gangguan, proses pencarian alamat IP kurir dapat terhambat. Selain itu, meningkatnya jumlah kurir dapat menambah beban pada server tersebut sehingga berpotensi menjadi *bottleneck*.

Sebaliknya, Chord DHT menggunakan *consistent hashing* untuk memetakan ID Kurir dan ID node ke ruang identitas yang sama. Setiap mapping menjadi tanggung jawab node *successor* yang ditentukan berdasarkan aturan Chord. Dengan pembagian tanggung jawab tersebut, penyimpanan dan pencarian mapping tidak harus bergantung pada satu tabel pusat.

#### Perbandingan dengan DNS Konvensional (Arynal Haq Syafi'i)

DNS konvensional juga menggunakan sistem terdistribusi untuk menerjemahkan nama domain menjadi alamat IP. Namun, perubahan alamat IP membutuhkan pembaruan record DNS dan dapat dipengaruhi oleh mekanisme *caching* serta TTL. Akibatnya, pengguna masih mungkin memperoleh alamat IP lama selama informasi sebelumnya masih tersimpan dalam cache.

Pada simulasi FoodGo, Chord memperlihatkan secara langsung bagaimana ID Kurir yang bersifat tetap digunakan untuk menemukan node yang bertanggung jawab atas mapping alamat IP-nya. Ketika terjadi perubahan topologi, seperti node bergabung atau keluar, tanggung jawab mapping dapat berpindah ke node *successor* yang sesuai dengan aturan ring.

#### Kesimpulan

Berdasarkan perbandingan tersebut, Chord DHT merupakan pendekatan yang relevan untuk kasus FoodGo karena mampu membagi tanggung jawab penyimpanan mapping ID Kurir ke beberapa node tanpa memerlukan satu server pusat sebagai tempat seluruh mapping disimpan.

Mekanisme *successor* juga memungkinkan pencarian mapping berdasarkan ID Kurir tetap meskipun alamat IP dan susunan node mengalami perubahan.

## 2. Analisis dan Visualisasi Ring Chord DHT (Arynal Haq Syafi'i & Melvin Crisna Martin Adoe)

Bagian ini menjelaskan struktur ring Chord DHT serta pemetaan Courier ke node yang bertanggung jawab. Visualisasi dilakukan untuk melihat perubahan pemetaan ketika terjadi proses *join* dan *leave* node.

### 2.1 Kondisi Awal Ring Chord (Arynal Haq Syafi'i)

Pada kondisi awal, terdapat empat node dalam ring Chord, yaitu ID 40, 102, 136, dan 177. Setiap Courier dipetakan ke node *successor* berdasarkan Hash ID masing-masing.

**Gambar 2.1 Kondisi Awal Ring Chord**

```mermaid
graph TD
    subgraph ring[" "]
        nodeBandung1["<b>node-bandung-1</b><br/>ID: 40"]
        nodeJakarta2["<b>node-jakarta-2</b><br/>ID: 102"]
        nodeSurabaya1["<b>node-surabaya-1</b><br/>ID: 136"]
        nodeJakarta1["<b>node-jakarta-1</b><br/>ID: 177"]
    end

    subgraph couriers[" "]
        kurir002["<b>kurir-002</b><br/>Hash: 28<br/>IP: 192.168.1.11"]
        kurir001["<b>kurir-001</b><br/>Hash: 50<br/>IP: 192.168.1.10"]
        kurirUji23["<b>kurir-uji-23</b><br/>Hash: 119<br/>IP: 192.168.1.23"]
        kurir003["<b>kurir-003</b><br/>Hash: 132<br/>IP: 192.168.1.12"]
        kurirLeave14["<b>kurir-leave-14</b><br/>Hash: 151<br/>IP: 192.168.1.14"]
    end

    nodeBandung1 -->|" " | nodeJakarta2
    nodeJakarta2 -->|" " | nodeSurabaya1
    nodeSurabaya1 -->|" " | nodeJakarta1
    nodeJakarta1 -->|Wrap-around| nodeBandung1

    kurir002 -.->|" " | nodeBandung1
    kurir001 -.->|" " | nodeJakarta2
    kurirUji23 -.->|" " | nodeSurabaya1
    kurir003 -.->|" " | nodeSurabaya1
    kurirLeave14 -.->|" " | nodeJakarta1

    classDef nodeStyle fill:#242424,stroke:#FF1493,stroke-width:3px,color:#ffffff,font-family:courier
    classDef courierStyle fill:#242424,stroke:#FF69B4,stroke-width:2px,color:#ffffff,font-family:courier
    classDef ringGroup fill:none,stroke:none
    classDef courierGroup fill:none,stroke:none

    class nodeBandung1,nodeJakarta2,nodeSurabaya1,nodeJakarta1 nodeStyle
    class kurir002,kurir001,kurirUji23,kurir003,kurirLeave14 courierStyle
    class ring ringGroup
    class couriers courierGroup
```

Berdasarkan diagram, `node-surabaya-1` bertanggung jawab atas dua Courier, yaitu `kurir-uji-23` dan `kurir-003`. Sementara itu, setiap Courier lainnya dipetakan ke node *successor* masing-masing.

### 2.2 Kondisi Setelah Node Join (Melvin Crisna Martin Adoe)

Pada tahap ini, node baru yaitu `node-medan-1` dengan ID 123 bergabung ke dalam ring Chord. Bergabungnya node tersebut menyebabkan perubahan tanggung jawab pemetaan Courier, khususnya pada `kurir-uji-23` dengan Hash ID 119.

**Gambar 2.2 Kondisi Setelah Node Join**

```mermaid
flowchart TB
    subgraph Ring["CHORD DHT RING AFTER NODE JOIN"]
        direction LR
        nb["node-bandung-1<br>ID: 40"]
        nj2["node-jakarta-2<br>ID: 102"]
        nm["node-medan-1<br>ID: 123<br>🆕 NEW NODE"]
        ns["node-surabaya-1<br>ID: 136"]
        nj1["node-jakarta-1<br>ID: 177"]
    end

    subgraph Couriers["COURIER INFORMATION"]
        direction TB
        k2["kurir-002<br>Hash: 28<br>IP: 192.168.1.11"]
        k1["kurir-001<br>Hash: 50<br>IP: 192.168.1.10"]
        ku["kurir-uji-23<br>Hash: 119<br>IP: 192.168.1.23"]
        k3["kurir-003<br>Hash: 132<br>IP: 192.168.1.12"]
        kl["kurir-leave-14<br>Hash: 151<br>IP: 192.168.1.14"]
    end

    subgraph Changes["JOIN IMPACT ANALYSIS"]
        direction TB
        before["BEFORE JOIN:<br>kurir-uji-23 hash 119 → node-surabaya-1 ID 136"]
        after["AFTER JOIN:<br>kurir-uji-23 hash 119 → node-medan-1 ID 123<br><br>Node ID 123 is first node ≥ hash 119"]
    end

    nb --> nj2
    nj2 --> nm
    nm --> ns
    ns --> nj1
    nj1 -->|Wrap-around| nb

    k2 -. assigns .-> nb
    k1 -. assigns .-> nj2
    ku -. assigns .-> nm
    k3 -. assigns .-> ns
    kl -. assigns .-> nj1

    classDef node fill:#242424,stroke:#FF1493,stroke-width:3px,color:#FFFFFF
    classDef newNode fill:#242424,stroke:#FF1493,stroke-width:4px,color:#FF69B4
    classDef courier fill:#242424,stroke:#FF69B4,stroke-width:2px,color:#FFFFFF
    classDef change fill:#242424,stroke:#FF69B4,stroke-width:2px,color:#FFFFFF
    classDef changeHL fill:#242424,stroke:#FF1493,stroke-width:3px,color:#FF69B4

    class nb,nj2,ns,nj1 node
    class nm newNode
    class k2,k1,ku,k3,kl courier
    class before change
    class after changeHL

    style Ring fill:#121212,stroke:#FF1493,color:#FFFFFF
    style Couriers fill:#121212,stroke:#FF69B4,color:#FFFFFF
    style Changes fill:#121212,stroke:#FF1493,color:#FFFFFF
```

Berdasarkan diagram, `node-medan-1` (ID 123) mengambil alih tanggung jawab `kurir-uji-23` dengan Hash ID 119 yang sebelumnya berada pada `node-surabaya-1` (ID 136). Hal ini terjadi karena ID 123 merupakan node successor pertama yang lebih besar atau sama dengan Hash ID 119. Sementara itu, pemetaan Courier lainnya tetap sama.

### 2.3 Kondisi Setelah Node Leave (Melvin Crisna Martin Adoe)

Pada tahap ini, `node-jakarta-1` dengan ID 177 meninggalkan jaringan. Setelah node tersebut keluar, ring Chord memiliki empat node aktif dan terjadi perubahan tanggung jawab pemetaan Courier.

**Gambar 2.3 Kondisi Setelah Node Leave**

```mermaid
graph TD
    subgraph ring["CHORD DHT RING - AFTER NODE LEAVE"]
        N40["node-bandung-1<br/>ID: 40"]
        N102["node-jakarta-2<br/>ID: 102"]
        N123["node-medan-1<br/>ID: 123"]
        N136["node-surabaya-1<br/>ID: 136"]
    end

    subgraph couriers["COURIER MAPPING"]
        C28["kurir-002<br/>Hash ID: 28<br/>IP: 192.168.1.11"]
        C50["kurir-001<br/>Hash ID: 50<br/>IP: 192.168.1.10"]
        C119["kurir-uji-23<br/>Hash ID: 119<br/>IP: 192.168.1.23"]
        C132["kurir-003<br/>Hash ID: 132<br/>IP: 192.168.1.12"]
        C151["kurir-leave-14<br/>Hash ID: 151<br/>IP: 192.168.1.14"]
    end

    N40 -->|Ring Link| N102
    N102 -->|Ring Link| N123
    N123 -->|Ring Link| N136
    N136 -->|Ring Link| N40

    C28 -.->|Responsible| N40
    C50 -.->|Responsible| N102
    C119 -.->|Responsible| N123
    C132 -.->|Responsible| N136
    C151 -.->|Responsible| N40

    NOTE["Setelah node Jakarta-1 ID 177 meninggalkan jaringan, tanggung jawab untuk<br/>Courier dengan Hash ID 151 berpindah ke node-bandung-1 ID 40 sebagai successor<br/>berikutnya dalam ring. Node lainnya tetap mempertahankan tanggung jawab sesuai<br/>pemetaan sebelumnya."]

    classDef nodeStyle fill:#242424,stroke:#FF1493,stroke-width:2px,color:#FFFFFF
    classDef courierStyle fill:#242424,stroke:#FF69B4,stroke-width:2px,color:#FFFFFF
    classDef noteStyle fill:#1a1a1a,stroke:#FF1493,stroke-width:1px,color:#FFFFFF
    classDef ringGroup fill:none,stroke:#FF1493,stroke-width:2px
    classDef courierGroup fill:none,stroke:#FF69B4,stroke-width:2px

    class N40,N102,N123,N136 nodeStyle
    class C28,C50,C119,C132,C151 courierStyle
    class NOTE noteStyle
    class ring ringGroup
    class couriers courierGroup
```

Berdasarkan diagram, `kurir-leave-14` dengan Hash ID 151 yang sebelumnya berada pada `node-jakarta-1` (ID 177) kini berpindah ke `node-bandung-1` (ID 40) sebagai *successor* berikutnya dalam ring. Pemetaan Courier lainnya tetap sama seperti pada kondisi setelah node join.

## 3. Analisis Hasil Simulasi (I Wayan Adnyana Kusuma Wijaya & Revaldi Ramadhan Nugraha) 

### 3.1 Hasil Sebelum dan Sesudah Node Baru Bergabung (I Wayan Adnyana Kusuma Wijaya)

Sebelum proses join, node ID 123 belum tersedia di dalam ring. Hash `kurir-uji-23` adalah 119, sehingga successor yang bertanggung jawab adalah node ID 136. Setelah `node-medan-1` (ID 123) bergabung, successor pertama yang memiliki ID lebih besar atau sama dengan 119 adalah node ID 123. Dengan demikian, tanggung jawab mapping berpindah dari node ID 136 ke node ID 123.

**Output program:**

```text
--- Node baru bergabung ---
Node 'node-medan-1' (id=123) bergabung, alamat 10.0.0.5
  Mapping kurir-uji-23 (192.168.1.23) berpindah ke node 123
kurir-uji-23 -> 192.168.1.23
```

### 3.2 Hasil Sebelum dan Sesudah Node Keluar (Revaldi Ramadhan Nugraha)

Sebelum proses leave, `kurir-leave-14` memiliki hash 151 dan successor node ID 177 (`node-jakarta-1`). Setelah node ID 177 keluar dari ring, tidak ada lagi node dengan ID lebih besar atau sama dengan 151. Oleh karena itu, fungsi `find_successor()` melakukan mekanisme *wrap-around* ke node dengan ID terkecil, yaitu node ID 40 (`node-bandung-1`). Dengan demikian, tanggung jawab mapping berpindah dari node ID 177 ke node ID 40.

**Output program:**

```text
--- Sebuah node keluar ---
Node 'node-jakarta-1' (id=177) keluar dari ring
  Mapping kurir-leave-14 (192.168.1.14) berpindah ke node 40
kurir-leave-14 -> 192.168.1.14
kurir-001 -> 192.168.1.10
kurir-002 -> 192.168.1.11
```

Output tersebut membuktikan bahwa alamat IP kurir tetap dapat ditemukan setelah terjadi perubahan topologi. Hal yang berubah adalah node successor yang bertanggung jawab atas mapping.

### 3.3 Tabel Ringkasan Perubahan (Revaldi Ramadhan Nugraha)

Tabel berikut menunjukkan perubahan tanggung jawab mapping setelah proses join dan leave:

| Perubahan Topologi | Mapping | Sebelum | Sesudah |
|---|---|---|---|
| `node-medan-1` (ID 123) bergabung | `kurir-uji-23` (hash 119) | Node 136 | Node 123 |
| `node-jakarta-1` (ID 177) keluar | `kurir-leave-14` (hash 151) | Node 177 | Node 40 |

**Ringkasan Tanggung Jawab Akhir**

| Node | ID Node | Mapping Kurir yang Menjadi Tanggung Jawab |
|---|---:|---|
| `node-bandung-1` | 40 | `kurir-002` (hash 28), `kurir-leave-14` (hash 151) |
| `node-jakarta-2` | 102 | `kurir-001` (hash 50) |
| `node-medan-1` | 123 | `kurir-uji-23` (hash 119) |
| `node-surabaya-1` | 136 | `kurir-003` (hash 132) |

**Catatan Batasan Implementasi:**

Pada implementasi ini, seluruh mapping disimpan dalam satu dictionary `self.data`. Oleh karena itu, perpindahan yang ditampilkan pada output merupakan perubahan tanggung jawab logis berdasarkan successor, bukan transfer data fisik antarserver. Simulasi ini juga belum mencakup komunikasi jaringan antarnode, *finger table*, dan replikasi data.

## Struktur Submission

```
tugas-06-penamaan-dht/
├── README.md      # Analisis + diagram ring
├── JURNAL.md
├── src/
│   └── chord_simulation.py
└── bukti/          # Output program (screenshot/log) untuk skenario join & leave
```

## Rubrik Penilaian (Tugas 6)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Implementasi lookup/join/leave benar | 35% | Consistent hashing & successor lookup sesuai aturan Chord |
| Bukti perubahan topologi (join/leave) | 25% | Output menunjukkan mapping berpindah dengan benar |
| Analisis kenapa DHT vs flat naming/DNS | 25% | Argumen spesifik ke kasus IP kurir dinamis, bukan definisi umum |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistent hashing/Chord ke AI; **tidak boleh** meminta AI menuliskan isi `# TODO` di `src/chord_simulation.py` (`find_successor`, `join`, `leave`, dst). Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menelusuri manual (langkah demi langkah) bagaimana `lookup()` menemukan successor untuk salah satu ID Kurir contoh yang dipakai di `chord_simulation.py` — bukan cuma menempelkan output program.
