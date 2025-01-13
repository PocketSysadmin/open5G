#!/bin/bash

# Directorio donde se guardan los archivos
CAPTURE_DIR="/packet-capture"

# Comenzar captura con tcpdump
tcpdump -i any -G 60 -w "$CAPTURE_DIR/%Y_%m_%d-%H_%M.pcap" > /dev/null 2>&1 &

# Mientras tcpdump esté corriendo, elimina archivos antiguos cada minuto
while true; do
  # Encuentra y elimina archivos con más de 1 minuto de antigüedad
  find "$CAPTURE_DIR" -type f -name "*.pcap" -mmin +1 -exec rm -f {} \;

  # Esperar un minuto antes de la próxima limpieza
  sleep 60
done
