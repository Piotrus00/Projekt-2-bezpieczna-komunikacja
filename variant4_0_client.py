import socket
import ssl

HOST = "127.0.0.1"
PORT = 8445
CA_FILE = "ca.crt"
CERT_FILE = "client.crt"
KEY_FILE = "client.key"


def main() -> None:
    context = ssl.create_default_context(cafile=CA_FILE)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    context.check_hostname = True
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE) # dodajemy certyfikat klienta

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname="localhost") as tls_sock:
            tls_sock.sendall(b"hello from client")
            data = tls_sock.recv(4096)
            print(data.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
