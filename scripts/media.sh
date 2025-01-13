#!/bin/bash

# Verificar si se proporciona un parámetro de tiempo
if [ -z "$1" ]; then
    echo "Use: $0 <time in seconds>"
    exit 1
fi

TIME=$1

# Contenedores y puertos correspondientes
CONTAINERS=("ueransim-ue-0" "ueransim-ue-1" "ueransim-ue-2")
PORTS=("8080" "8082" "8083")

# Endender el servidor de streaming
echo "Starting streaming server..."
adjusted_time=$((TIME + 3))
docker exec ffmpeg sh -c "timeout $adjusted_time ./streaming.sh" &

#esperan 1 segon
sleep 1
# Bucle para ejecutar el comando en cada contenedor y puerto con límite de tiempo
for i in "${!CONTAINERS[@]}"; do
    CONTAINER=${CONTAINERS[$i]}
    PORT=${PORTS[$i]}
    
    echo "Executing in container $CONTAINER with port $PORT for $TIME seconds..."
    docker exec "$CONTAINER" sh -c "timeout $TIME ffmpeg -i http://10.18.0.2:$PORT -c copy -f null /dev/null" &

done

# Mostrar procesos en segundo plano
echo "Running processes:"
jobs

# Esperar a que terminen los procesos en segundo plano
wait

echo "All processes finished."