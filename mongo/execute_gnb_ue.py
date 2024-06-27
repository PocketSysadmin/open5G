import subprocess

def get_container_id_by_name(name):
    # Ejecuta `docker ps` y captura la salida
    result = subprocess.run(['docker', 'ps'], stdout=subprocess.PIPE)
    lines = result.stdout.decode('utf-8').splitlines()
    
    # Filtra las líneas que contienen el nombre especificado y extrae el ID del contenedor
    container_ids = []
    for line in lines:
        if name in line:
            container_id = line.split()[0]  # El ID del contenedor es la primera columna
            container_ids.append(container_id)
    
    return container_ids

def execute_command_in_container(container_id, command, detach=False):
    # Ejecuta el comando `docker exec -it ID_CONTENEDOR command`
    exec_command = ['docker', 'exec']
    if detach:
        exec_command.append('-d')
    exec_command += ['-it', container_id] + command
    subprocess.run(exec_command)

def main():
    # Obtén el ID del contenedor gnb
    gnb_container_ids = get_container_id_by_name('gnb')
    
    if gnb_container_ids:
        # Ejecuta el comando en el contenedor gnb en segundo plano
        for gnb_container_id in gnb_container_ids:
            execute_command_in_container(gnb_container_id, ['./nr-gnb', '-c', 'oai-gnb.yaml'], detach=True)
    else:
        print("No se encontró el contenedor gnb")
        return
    
    # Obtén los IDs de los contenedores ue-
    ue_container_ids = get_container_id_by_name('ue-')
    
    if ue_container_ids:
        # Ejecuta el comando en cada contenedor ue- en segundo plano
        for ue_container_id in ue_container_ids:
            execute_command_in_container(ue_container_id, ['./nr-ue', '-c', 'oai-ue.yaml'], detach=True)
    else:
        print("No se encontraron contenedores ue-")

if __name__ == "__main__":
    main()
