import threading
import traceback
import socket
import pickle
from main import HuffmanCode

class Service:
    def __init__(self, client_socket, client_address):
        self.client_socket = client_socket
        self.client_address = client_address

    def handle_client(self):
        print(f"Client connected from {self.client_address}")

        try:
            # Recevoir le fichier compressé et la table de codage
            data_received = pickle.loads(self.client_socket.recv(4096))
            file_name = data_received["file_name"]
            file_data = data_received["file_data"]
            huffman = HuffmanCode()
            huffman.compress(file_name, file_data)

        except Exception as e:
            print(f"Error handling client: {e}")
            traceback.print_exc()
        finally:
            self.client_socket.close()
            print(f"Client disconnected from {self.client_address}")

# Exemple d'utilisation
if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()
        service = Service(client_socket)
        client_thread = threading.Thread(target=service.handle_client)
        client_thread.start()
