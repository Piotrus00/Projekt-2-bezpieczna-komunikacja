import socket
import ssl

HOST = "127.0.0.1"
PORT = 8445
CERT_FILE = "server.crt"
KEY_FILE = "server.key"
CA_FILE = "ca.crt"


def handle_client(conn: ssl.SSLSocket) -> None:
    try:
        peer_cert = conn.getpeercert() # pobieramy certyfikat klienta
        print(f"Client cert subject: {peer_cert.get('subject', [])}")
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
    context.load_verify_locations(cafile=CA_FILE)
    context.verify_mode = ssl.CERT_REQUIRED # wymuszamy certyfikat klienta

    with socket.create_server((HOST, PORT)) as server_sock:
        with context.wrap_socket(server_sock, server_side=True) as tls_sock:
            print(f"mTLS server listening on {HOST}:{PORT}")
            conn, addr = tls_sock.accept()
            print(f"Client connected: {addr}")
            handle_client(conn)


if __name__ == "__main__":
    main()
