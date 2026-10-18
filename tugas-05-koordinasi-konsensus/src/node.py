
"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Simulasi lima node menggunakan TCP socket pada localhost.
Node dengan ID tertinggi yang masih hidup akan menjadi leader.
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0
MONITOR_INTERVAL = 3.0


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        self.peers = peers
        self.leader_id = None

        self.lock = threading.Lock()
        self.election_lock = threading.Lock()
        self.ok_received = threading.Event()

    # ---------- Infrastruktur jaringan ----------

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", self.port))
        server.listen()

        print(f"[Node {self.node_id}] Listening di port {self.port}")

        while True:
            conn, _ = server.accept()
            threading.Thread(
                target=self.handle_connection,
                args=(conn,),
                daemon=True,
            ).start()

    def handle_connection(self, conn: socket.socket):
        with conn:
            try:
                data = conn.recv(1024).decode().strip()

                if not data:
                    return

                sender_id, msg_type = data.split(":", 1)
                self.on_message(int(sender_id), msg_type)

            except (ValueError, OSError) as error:
                print(
                    f"[Node {self.node_id}] "
                    f"Gagal memproses pesan: {error}"
                )

    def send_message(self, target_port: int, msg_type: str) -> bool:
        """Mengirim pesan ke node lain dan memeriksa koneksi TCP."""
        try:
            with socket.create_connection(
                ("localhost", target_port),
                timeout=1.0,
            ) as conn:
                conn.sendall(
                    f"{self.node_id}:{msg_type}".encode()
                )
            return True

        except (ConnectionRefusedError, socket.timeout, OSError):
            return False

    # ---------- Logika Bully Algorithm ----------

    def on_message(self, sender_id: int, msg_type: str):
        """Memproses pesan dari node lain."""

        if msg_type == "ELECTION":
            print(
                f"[Node {self.node_id}] Menerima ELECTION "
                f"dari node {sender_id}"
            )

            if self.node_id > sender_id:
                sender_port = self.peers.get(sender_id)

                if sender_port is not None:
                    if self.send_message(sender_port, "OK"):
                        print(
                            f"[Node {self.node_id}] Mengirim OK "
                            f"ke node {sender_id}"
                        )

                threading.Thread(
                    target=self.start_election,
                    daemon=True,
                ).start()

        elif msg_type == "OK":
            print(
                f"[Node {self.node_id}] Menerima OK "
                f"dari node {sender_id}"
            )
            self.ok_received.set()

        elif msg_type == "COORDINATOR":
            with self.lock:
                self.leader_id = sender_id

            print(
                f"[Node {self.node_id}] Leader saat ini: "
                f"node {sender_id}"
            )

    def start_election(self):
        """Memulai pemilihan leader menggunakan Bully Algorithm."""

        # Hindari beberapa election berjalan bersamaan pada node yang sama.
        if not self.election_lock.acquire(blocking=False):
            return

        try:
            self.ok_received.clear()

            with self.lock:
                previous_leader = self.leader_id

            higher_peers = {
                peer_id: peer_port
                for peer_id, peer_port in self.peers.items()
                if peer_id > self.node_id
            }

            print(f"[Node {self.node_id}] Memulai election")

            for peer_id, peer_port in higher_peers.items():
                berhasil = self.send_message(
                    peer_port,
                    "ELECTION",
                )

                if berhasil:
                    print(
                        f"[Node {self.node_id}] Mengirim ELECTION "
                        f"ke node {peer_id}"
                    )
                else:
                    print(
                        f"[Node {self.node_id}] Node {peer_id} "
                        f"tidak merespons"
                    )

            # Tunggu balasan OK dari node yang lebih tinggi.
            menerima_ok = self.ok_received.wait(
                timeout=ELECTION_TIMEOUT
            )

            if menerima_ok:
                print(
                    f"[Node {self.node_id}] Ada node lebih tinggi "
                    "yang aktif; menunggu COORDINATOR"
                )

                # Jika COORDINATOR tidak diterima, coba election lagi.
                time.sleep(ELECTION_TIMEOUT)

                with self.lock:
                    leader_diketahui = self.leader_id is not None

                if not leader_diketahui:
                    print(
                        f"[Node {self.node_id}] Belum menerima "
                        "COORDINATOR; mencoba election ulang"
                    )
                    threading.Thread(
                        target=self.start_election,
                        daemon=True,
                    ).start()

            else:
                # Jangan mengumumkan diri jika leader baru sudah diterima.
                with self.lock:
                    leader_berubah = (
                        self.leader_id != previous_leader
                        and self.leader_id is not None
                    )

                if not leader_berubah:
                    self.declare_leader()

        finally:
            self.election_lock.release()

    def declare_leader(self):
        """Menetapkan diri sebagai leader dan memberi tahu semua node."""

        with self.lock:
            self.leader_id = self.node_id

        print(f"[Node {self.node_id}] Saya menjadi leader")

        for peer_id, peer_port in self.peers.items():
            berhasil = self.send_message(
                peer_port,
                "COORDINATOR",
            )

            if berhasil:
                print(
                    f"[Node {self.node_id}] Mengirim COORDINATOR "
                    f"ke node {peer_id}"
                )
            else:
                print(
                    f"[Node {self.node_id}] Node {peer_id} "
                    "tidak merespons COORDINATOR"
                )

    def monitor_leader(self):
        """Memantau leader dan memulai election jika leader mati."""

        while True:
            time.sleep(MONITOR_INTERVAL)

            with self.lock:
                current_leader = self.leader_id

            if current_leader is None:
                continue

            if current_leader == self.node_id:
                continue

            leader_port = self.peers.get(current_leader)

            if leader_port is None:
                continue

            leader_alive = self.send_message(
                leader_port,
                "PING",
            )

            if not leader_alive:
                print(
                    f"[Node {self.node_id}] Leader node "
                    f"{current_leader} tidak merespons"
                )

                with self.lock:
                    if self.leader_id == current_leader:
                        self.leader_id = None
                        mulai_election = True
                    else:
                        mulai_election = False

                if mulai_election:
                    self.start_election()


