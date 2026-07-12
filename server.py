# server.py
import socket
import threading
import sqlite3

HOST = '0.0.0.0'
PORT = 55555

def db_init():
    conn = sqlite3.connect("kullanicilar.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data: break
            parts = data.split(":")
            komut = parts[0]
            
            if komut == "REGISTER":
                user, pasw = parts[1], parts[2]
                conn = sqlite3.connect("kullanicilar.db")
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pasw))
                    conn.commit()
                    client_socket.send("REG_OK".encode('utf-8'))
                except sqlite3.IntegrityError:
                    client_socket.send("REG_ERR_TAKEN".encode('utf-8'))
                conn.close()
                
            elif komut == "LOGIN":
                user, pasw = parts[1], parts[2]
                conn = sqlite3.connect("kullanicilar.db")
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pasw))
                if cursor.fetchone():
                    client_socket.send("AUTH_OK".encode('utf-8'))
                else:
                    client_socket.send("AUTH_ERR".encode('utf-8'))
                conn.close()
        except: break
    client_socket.close()

def start_server():
    db_init()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("🚀 Veritabanlı Güvenli Sunucu Aktif...")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start_server()