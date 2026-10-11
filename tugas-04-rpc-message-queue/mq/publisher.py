"""
Tugas 4 - Jalur B: Publisher (simulasi modul Pembayaran)
Mengirim event pembayaran berhasil ke RabbitMQ tanpa
menunggu modul Kurir memprosesnya.
"""

import pika
import json

QUEUE_NAME = "pembayaran_berhasil"


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

   
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    pesan = {
        "event": "pembayaran_berhasil",
        "user_id": "user1",
        "jumlah": 20000
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(pesan),
        properties=pika.BasicProperties(
            delivery_mode=2,
            content_type="application/json"
        )
    )

    print(f"[Pembayaran] Event berhasil dikirim: {pesan}")

    connection.close()


if __name__ == "__main__":
    main()
