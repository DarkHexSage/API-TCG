# 1. Descargar versión latest
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 2. Dar permisos de ejecución
sudo chmod +x /usr/local/bin/docker-compose

# 3. Verificar instalación
docker-compose --version
