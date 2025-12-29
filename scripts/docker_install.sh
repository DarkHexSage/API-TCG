# 1. Actualizar sistema
sudo apt update
sudo apt upgrade -y

# 2. Instalar dependencias
sudo apt install -y ca-certificates curl gnupg lsb-release

# 3. Agregar Docker GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Agregar Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Actualizar y instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 6. Agregar tu usuario a grupo docker (sin sudo)
sudo usermod -aG docker $USER

# 7. Aplicar cambios de grupo
newgrp docker

# 8. Verificar instalación
docker --version
docker run hello-world
