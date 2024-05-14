# If not working, first do: sudo rm -rf /tmp/.docker.xauth
# It still not working, try running the script as root.
## Build the image first
### docker build -t r2_path_planning .
## then run this script

# Para dar permisos al fichero: "sudo chmod +x Nombre_archivo.bash"
# Para lanzarlo ./Nombre_archivo.bash

docker build -t python_flask . 

docker run -it \
    --name python_flask \
    --gpus all \
    --volume /home/enzo/containers/python_flask:/home/enzo \
    --ipc=host \
    --user $(id -u):$(id -g) \
    python_flask \
    bash

