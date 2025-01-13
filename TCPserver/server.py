import socket
import threading
import subprocess
import time

HOST = '0.0.0.0'
PORT = 65432


def execute_traffigen_media(tim, client_socket):
    try:
        resultado = subprocess.check_output([f'../scripts/media.sh', tim], text=True)
        client_socket.sendall(f"Result:\n{resultado}\n".encode())
    except subprocess.CalledProcessError as e:
        client_socket.sendall(f"Error executing the script: media.sh: {e}\n".encode())

# Here you need to add the function to execute the web script
def execute_traffigen_web(tim, client_socket):
    pass

def manejar_cliente(client_socket, client_address):
    try:
        client_socket.sendall("Connected successfully.".encode())

        time.sleep(2)

        while True:

            data = client_socket.recv(1024).decode()
            if not data:
                print(f'Client {client_address} disconnected.')
                break
            
            partes = data.split()
            
            if len(partes) >= 3 and partes[0] == 'trafgen':
                script_type = partes[1]
                
                if script_type == 'media' and len(partes) == 3 and partes[2].isdigit():
                    tim = partes[2]

                    client_socket.sendall(f"Executing the script {script_type}.sh with time {tim}...".encode())

                    traffigen_media_thread = threading.Thread(target=execute_traffigen_media, args=(tim, client_socket))
                    traffigen_media_thread.start()

                elif script_type == 'web':  #Here you need to add the code to execute the web script
                   
                    pass

                else:
                    client_socket.sendall(f"Invalid command format for 'trafgen'. Check the help for valid options.\n".encode())

            else:
                # Here you need to add the help message for the client
                help_message = (
                    "Help:\n"
                    "trafgen media <time> - Execute the traffigen media script in ue-0, ue-1, ue-2\n"
                )
                client_socket.sendall(help_message.encode())
    finally:
        client_socket.close()

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f'Servidor escuchando en {HOST}:{PORT}...')

        while True:
            client_socket, client_address = server_socket.accept()
            print(f'Conexión establecida con {client_address}')
            cliente_hilo = threading.Thread(target=manejar_cliente, args=(client_socket, client_address))
            cliente_hilo.start()

if __name__ == '__main__':
    iniciar_servidor()
