import threading
import random
import time

NUM_ORDERS = 100
NUM_WORKERS = 10

processed_count = 0


def process_order(order_id: int) -> None:
    global processed_count

    time.sleep(random.uniform(0.001, 0.01))

    current_count = processed_count
    time.sleep(0.001)
    processed_count = current_count + 1


def worker(order_ids: list) -> None:
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    global processed_count

    order_ids = list(range(1, NUM_ORDERS + 1))
    threads = []

    chunk_size = len(order_ids) // NUM_WORKERS

    for i in range(NUM_WORKERS):
        start = i * chunk_size

        if i == NUM_WORKERS - 1:
            end = len(order_ids)
        else:
            end = (i + 1) * chunk_size

        thread = threading.Thread(
            target=worker,
            args=(order_ids[start:end],)
        )

        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    print(f"Total pesanan diproses: {processed_count}")
    print(f"Seharusnya: {NUM_ORDERS}")


if __name__ == "__main__":
    main()