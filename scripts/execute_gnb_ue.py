import subprocess
import time
import re

def get_container_id_and_name_by_partial_name(partial_name):
    # Ejecuta `docker ps` y captura la salida
    result = subprocess.run(['docker', 'ps', '--format', '{{.ID}} {{.Names}}'], stdout=subprocess.PIPE)
    lines = result.stdout.decode('utf-8').splitlines()
    
    # Filtra las líneas que contienen el nombre parcial especificado y extrae el ID y el nombre del contenedor
    containers = []
    for line in lines:
        if partial_name in line:
            container_id, container_name = line.split()[:2]  # El ID del contenedor es la primera columna y el nombre es la segunda
            containers.append((container_id, container_name))
    
    # Ordena los contenedores por nombre
    containers.sort(key=lambda x: x[1])
    
    return containers

def execute_command_in_container(container_id, commands, detach=False):
    for command in commands:
        exec_command = ['docker', 'exec']
        if detach:
            exec_command.append('-d')
        exec_command += ['-it', container_id] + command
        subprocess.run(exec_command)
        time.sleep(0.5)  # Espera 0.5 segundos entre comandos

def main():
    # Obtén el ID y el nombre del contenedor gnb
    gnb_containers = get_container_id_and_name_by_partial_name('gnb')
    
    if gnb_containers:
        # Ejecuta el comando en el contenedor gnb en segundo plano
        for gnb_container_id, gnb_container_name in gnb_containers:
            execute_command_in_container(gnb_container_id, [['./nr-gnb', '-c', 'oai-gnb.yaml']], detach=True)
    else:
        print("No se encontró el contenedor gnb")
        return
    
    # Obtén los IDs y nombres de los contenedores ue-
    ue_containers = get_container_id_and_name_by_partial_name('ue-')
    
    if ue_containers:
        # Ejecuta el comando en cada contenedor ue- en segundo plano
        for ue_container_id, ue_container_name in ue_containers:
            initial_command = ['./nr-ue', '-c', 'oai-ue.yaml']
            ip_command = ['ip', 'a']
            delete_route_command = ['ip', 'route', 'del', 'default']
            
            # Ejecuta el primer comando
            execute_command_in_container(ue_container_id, [initial_command], detach=True)
            
            # Espera 0.5 segundos antes de ejecutar los siguientes comandos
            time.sleep(0.5)
            
            # Obtén la IP de la interfaz y ajusta la ruta predeterminada
            ip_result = subprocess.run(['docker', 'exec', '-it', ue_container_id, 'ip', 'a'], stdout=subprocess.PIPE)
            ip_output = ip_result.stdout.decode('utf-8')
            ip_line = next(line for line in ip_output.splitlines() if 'uesimtun0' in line and 'inet' in line)
            ip_address = ip_line.split()[1].split('/')[0]
            
            add_route_command = ['ip', 'route', 'add', 'default', 'via', ip_address]
            
            # Ejecuta los comandos de red en el contenedor
            execute_command_in_container(ue_container_id, [delete_route_command, add_route_command])
    else:
        print("No se encontraron contenedores ue-")

if __name__ == "__main__":
    main()
