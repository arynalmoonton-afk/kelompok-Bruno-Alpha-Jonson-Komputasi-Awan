"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    saldo = proxy.cek_saldo("user1")
    durasi = time.time() - start

    print(f"Saldo user1: Rp{saldo:,.0f}")
    print(f"Waktu respons: {durasi:.6f} detik")

    print("\nMemanggil proses_pembayaran('user1', 20000) ...")
    hasil = proxy.proses_pembayaran("user1", 20000)
    print(f"Hasil pembayaran: {hasil}")

    print("\nMemeriksa saldo setelah pembayaran...")
    saldo_akhir = proxy.cek_saldo("user1")
    print(f"Saldo akhir user1: Rp{saldo_akhir:,.0f}")


if __name__ == "__main__":
    main()
