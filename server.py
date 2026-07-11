# server.py  –  Run this on your own PC/server, NOT on Android.
# The Android APK connects to this server over the internet.
import socket
import threading
import sqlite3
import hashlib

HOST = '0.0.0.0'
PORT = 55555


def hash_password(password: str) -> str:
    """Simple SHA-256 hash so plain-text passwords are never stored."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def db_init():
    conn = sqlite3.connect("kullanicilar.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def handle_client(client_socket, addr):
    print(f"[+] Bağlantı: {addr}")
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            parts = data.split(":", 2)
            if len(parts) < 3:
                break
            komut, user, pasw = parts[0], parts[1], parts[2]
            hashed = hash_password(pasw)

            conn = sqlite3.connect("kullanicilar.db")
            cursor = conn.cursor()

            if komut == "REGISTER":
                try:
                    cursor.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)",
                        (user, hashed)
                    )
                    conn.commit()
                    client_socket.send("REG_OK".encode('utf-8'))
                except sqlite3.IntegrityError:
                    client_socket.send("REG_ERR_TAKEN".encode('utf-8'))

            elif komut == "LOGIN":
                cursor.execute(
                    "SELECT id FROM users WHERE username=? AND password=?",
                    (user, hashed)
                )
                if cursor.fetchone():
                    client_socket.send("AUTH_OK".encode('utf-8'))
                else:
                    client_socket.send("AUTH_ERR".encode('utf-8'))

            conn.close()

        except Exception as e:
            print(f"[-] Hata ({addr}): {e}")
            break

    client_socket.close()
    print(f"[-] Bağlantı kesildi: {addr}")


def start_server():
    db_init()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"🚀 Mahiru Chat Sunucusu aktif  →  {HOST}:{PORT}")
    while True:
        client, addr = server.accept()
        threading.Thread(
            target=handle_client, args=(client, addr), daemon=True
        ).start()


if __name__ == "__main__":
    start_server()
