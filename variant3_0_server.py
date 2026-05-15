import socket
import ssl

HOST = "127.0.0.1"
PORT = 8443
CERT_FILE = "server.crt"
KEY_FILE = "server.key"


def handle_client(conn: ssl.SSLSocket) -> None:
    try:
        data = conn.recv(4096)
        if data:
            conn.sendall(b"echo: " + data)
    finally:
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()


def main() -> None:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    with socket.create_server((HOST, PORT)) as server_sock:
        with context.wrap_socket(server_sock, server_side=True) as tls_sock: # nasluchuje
            print(f"TLS server listening on {HOST}:{PORT}")
            conn, addr = tls_sock.accept() # akceptuje polaczenie, wykonuje handshake, sprawdza certyfikat
            print(f"Client connected: {addr}")
            handle_client(conn) # odbiera dane, wysyla odpowiedz, zamyka polaczenie


if __name__ == "__main__":
    main()
