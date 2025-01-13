#!/bin/bash

# Definimos los nombres de los videos y sus puertos correspondientes
VIDEOS=("JurassicCat.mp4" "Titanic3D.mp4" "TitanicCat.mp4")
PORTS=(8080 8083 8082)

# Función para iniciar una transmisión por cada video
start_streams() {
    for i in "${!VIDEOS[@]}"; do
        VIDEO=${VIDEOS[$i]}
        PORT=${PORTS[$i]}
        if [ -f "$VIDEO" ]; then
            echo "Iniciando transmisión de $VIDEO en el puerto $PORT..."
            ffmpeg -re -stream_loop -1 -i "$VIDEO" -f mpegts -listen 1 "http://0.0.0.0:$PORT" &
        else
            echo "El archivo $VIDEO no existe. Omisión."
        fi
    done
}

# Iniciar las transmisiones
start_streams

# Mostrar los procesos activos
echo "Transmisiones en marcha. Los procesos activos son:"
jobs

# Mantener el script en ejecución hasta que se termine manualmente
echo "Presiona Ctrl+C para detener las transmisiones."
wait
