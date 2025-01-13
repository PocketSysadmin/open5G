# Usa una imagen base que tenga ffmpeg instalado
FROM jrottenberg/ffmpeg:4.4-ubuntu

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /video

# Copia todos los archivos del directorio actual al contenedor
COPY . /video

# Da permisos de ejecución al script
RUN chmod +x /video/streaming.sh

# Establece ffmpeg como servicio principal para interactuar
ENTRYPOINT ["/bin/bash"]
