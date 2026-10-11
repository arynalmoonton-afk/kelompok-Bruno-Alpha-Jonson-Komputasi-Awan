"""
Tugas 4 - Jalur B: Consumer (simulasi modul Kurir/Notifikasi)
"""

import pika
import json

QUEUE_NAME = "pembayaran_berhasil"


def callback(ch, method, properties, body):
    pesan = json.loads(body)

    print(
        f"[Kurir] Menerima notifikasi pembayaran: "
        f"user_id={pesan['user_id']}, "
        f"jumlah=Rp{pesan['jumlah']:,.0f}"
    )

    # Konfirmasi bahwa pesan berhasil diproses
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    # Hubungkan consumer ke RabbitMQ lokal
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    # Pastikan antrean sama dengan milik publisher
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Proses satu pesan pada satu waktu
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    print(
        f"Menunggu event dari antrean '{QUEUE_NAME}'... "
        "(Ctrl+C untuk berhenti)"
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nConsumer dihentikan.")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
