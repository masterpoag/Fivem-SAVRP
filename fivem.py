import socket
import threading
import time
from typing import Dict
import queue

class ConnectionManager:
    """Python equivalent of the C# ConnectionManager with queued message sending."""

    def __init__(self):
        self._clients: Dict[str, socket.socket] = {}
        self._lock = threading.Lock()
        self._connect_timeout = 2.0
        self._header = bytes(int(x, 16) for x in "43:4d:4e:44:00:d2:00:00".split(':'))

        # Queue system
        self._message_queue = queue.Queue()
        self._running = True
        self._sender_thread = threading.Thread(target=self._process_queue, daemon=True)
        self._sender_thread.start()

    def stop(self):
        """Stop the background sender thread."""
        self._running = False
        self._message_queue.put(None)  # unblock queue

    def _process_queue(self):
        while self._running:
            item = self._message_queue.get()
            if item is None:
                break
            message, ip, port, can_retry = item
            try:
                self._send_message_direct(message, ip, port, can_retry)
            except Exception as e:
                print(f"Failed to send queued message to {ip}:{port}: {e}")
            self._message_queue.task_done()
            time.sleep(0.05)  # small delay to prevent flooding

    def send_message(self, message: str, ip: str = "127.0.0.1", port: int = 29200, can_retry: bool = True):
        """Queue a message for sending."""
        print(f"Sending command: {message}")
        if message is None:
            return
        self._message_queue.put((message, ip, port, can_retry))

    def _send_message_direct(self, message: str, ip: str, port: int, can_retry: bool):
        """Internal method to actually send a message immediately."""
        cmd_bytes = (message + "\n").encode("utf-8")
        length_val = len(message) + 13
        length_bytes = length_val.to_bytes(4, byteorder='big')
        padding = b'\x00\x00'
        terminator = b'\x00'
        data = b''.join((self._header, length_bytes, padding, cmd_bytes, terminator))

        key = self._client_key(ip, port)
        try_count = 0
        while True:
            try_count += 1
            try:
                sock = self._connect_if_needed(ip, port)
                sock.sendall(data)
                return
            except Exception as ex:
                with self._lock:
                    try:
                        existing = self._clients.get(key)
                        if existing:
                            try:
                                existing.close()
                            except Exception:
                                pass
                        self._clients[key] = self._make_socket()
                    except Exception:
                        pass
                if can_retry and try_count == 1:
                    time.sleep(0.1)
                    continue
                raise ex

    def _client_key(self, ip: str, port: int) -> str:
        return f"{ip}::{port}"

    def _make_socket(self) -> socket.socket:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self._connect_timeout)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        return s

    def _connect_if_needed(self, ip: str, port: int) -> socket.socket:
        key = self._client_key(ip, port)
        with self._lock:
            sock = self._clients.get(key)
            if sock is None or sock.fileno() < 0:
                try:
                    if sock:
                        sock.close()
                except Exception:
                    pass
                sock = self._make_socket()
                self._clients[key] = sock

            try:
                sock.getpeername()
            except OSError:
                try:
                    sock.settimeout(self._connect_timeout)
                    sock.connect((ip, port))
                    sock.settimeout(None)
                except Exception:
                    try:
                        sock.close()
                    except Exception:
                        pass
                    sock = self._make_socket()
                    self._clients[key] = sock
                    raise
            return sock

    def initialize_clients(self):
        with self._lock:
            for s in self._clients.values():
                try:
                    s.close()
                except Exception:
                    pass
            self._clients = {}

    def dispose(self):
        self.stop()
        with self._lock:
            for s in self._clients.values():
                try:
                    s.shutdown(socket.SHUT_RDWR)
                    s.close()
                except Exception:
                    pass
            self._clients.clear()


# Example usage
if __name__ == "__main__":
    cm = ConnectionManager()
    try:
        # Queue multiple commands for sending
        for i in range(10):
            cm.send_message(f"me test {i}", ip="127.0.0.1", port=29200)
        print("Queued commands for sending.")
        # Wait for queue to finish
        cm._message_queue.join()
    finally:
        cm.dispose()
