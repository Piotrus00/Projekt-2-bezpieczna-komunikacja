import socket
import ssl

HOST = "127.0.0.1"
PORT = 8443
CA_FILE = "server.crt"


def main() -> None:
    context = ssl.create_default_context(cafile=CA_FILE)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    context.check_hostname = True #sprawdza czy certyfikat jest wystawiony dla hosta, z którym się łączymy

    with socket.create_connection((HOST, PORT)) as sock: #laczenie bez TLS
        with context.wrap_socket(sock, server_hostname="localhost") as tls_sock: #laczenie z TLS, sprawdza certyfikat + handshake
            tls_sock.sendall(b"hello from client")
            data = tls_sock.recv(4096)
            print(data.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
