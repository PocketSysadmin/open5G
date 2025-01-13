import socket
import time
from threading import Thread

# Configuración del cliente
HOST = '10.18.0.2'
PORT = 65432

# Definir colores ANSI
COLOR_AZUL = '\033[94m'  # Azul
COLOR_RESET = '\033[0m'  # Restablecer al color normal

# Hilo para recibir mensajes del servidor
def recibir_mensajes(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            print('Disconnected from the server.')
            break
        # Imprimir respuesta del servidor en azul
        print(f"{COLOR_AZUL}{data}{COLOR_RESET}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Conectar al servidor
    client_socket.connect((HOST, PORT))
    # Mensaje de bienvenida del servidor en azul
    print(f"{COLOR_AZUL}{client_socket.recv(1024).decode()}{COLOR_RESET}")

    # Crear hilo para recibir mensajes del servidor
    thread = Thread(target=recibir_mensajes, args=(client_socket,))
    thread.start()

    while True:
        print("Enter the command to execute:")
        comando = input()
        client_socket.sendall(comando.encode())
