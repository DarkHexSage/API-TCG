# 🐳 TCG API + Frontend - Docker Setup

Deployment completo y listo para producción con Docker Compose.

## 🚀 Quick Start

### 1. Preparar la estructura

Asegúrate que tienes:
```
~/API TCG/
├── db_standardizer/
│   └── tcg_unified.db
├── TCG-API/
│   ├── main.py
│   ├── requirements.txt
│   └── index.html
└── tcg_docker/
    ├── docker-compose.yml
    ├── api.Dockerfile
    ├── frontend.Dockerfile
    ├── nginx.conf
    ├── manage.sh
    └── README.md
```

### 2. Hacer el script ejecutable

```bash
cd ~/API\ TCG/tcg_docker/
chmod +x manage.sh
```

### 3. Levantar todo

```bash
./manage.sh start
```

### 4. Verificar que funciona

```bash
./manage.sh test
```

Deberías ver:
```
Probando API health... ✅
Probando API games... ✅
Probando Frontend... ✅
```

---

## 📊 URLs disponibles

| Servicio | URL | Puerto |
|----------|-----|--------|
| Frontend | http://localhost:8080 | 8080 |
| API | http://localhost:8005 | 8005 |
| API Docs | http://localhost:8005/docs | 8005 |

---

## 🛠️ Comandos útiles

### Ver estado de servicios
```bash
./manage.sh status
```

### Ver logs
```bash
# Todos los logs
./manage.sh logs

# Solo API
./manage.sh logs api

# Solo Frontend
./manage.sh logs frontend

# Último log en vivo
./manage.sh logs api -f
```

### Detener servicios
```bash
./manage.sh stop
```

### Reiniciar
```bash
./manage.sh restart
```

### Entrar a shell del API
```bash
./manage.sh shell-api
```

### Compilar imágenes nuevamente
```bash
./manage.sh build
```

### Limpiar todo
```bash
./manage.sh clean
```

---

## 🔧 Personalizar configuración

### Cambiar puertos

Editar `docker-compose.yml`:

```yaml
services:
  api:
    ports:
      - "3000:8000"  # API en puerto 3000

  frontend:
    ports:
      - "3001:80"    # Frontend en puerto 3001
```

### Cambiar URL del API (si usas dominio)

En el `docker-compose.yml`, reemplazar en las variables de ambiente:

```yaml
services:
  frontend:
    environment:
      - API_URL=https://tudominio.com/api
```

---

## 📈 Deployment en Producción

### Opción 1: Oracle Linux con Docker

```bash
# Transferir archivos
scp -r ~/API\ TCG opc@TU_IP_ORACLE:~/

# Conectar
ssh opc@TU_IP_ORACLE

# Levantar
cd ~/API\ TCG/tcg_docker/
./manage.sh start
```

### Opción 2: Con Nginx reverse proxy

```nginx
server {
    listen 80;
    server_name tudominio.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Opción 3: Con SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot certonly --standalone -d tudominio.com

# Usar en Nginx config
server {
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/tudominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tudominio.com/privkey.pem;
    # ... resto de config
}
```

---

## 🐛 Troubleshooting

### "Port already in use"

```bash
# Ver qué está usando el puerto
lsof -i :8080
lsof -i :8005

# Cambiar puertos en docker-compose.yml o:
./manage.sh stop
# Esperar 30 segundos
./manage.sh start
```

### API retorna error 500

```bash
# Ver logs
./manage.sh logs api

# Verificar que la DB existe
./manage.sh shell-api
ls -la tcg_unified.db
sqlite3 tcg_unified.db "SELECT COUNT(*) FROM cards;"
```

### Frontend en blanco

```bash
# Verificar que index.html está
./manage.sh shell-frontend
ls -la /usr/share/nginx/html/

# Ver errores de nginx
./manage.sh logs frontend
```

### Contenedores se detienen

```bash
# Ver por qué
docker ps -a

# Reconstruir
./manage.sh clean
./manage.sh build
./manage.sh start
```

---

## 📊 Monitoring

### Ver consumo de recursos

```bash
docker stats
```

### Ver logs en tiempo real

```bash
./manage.sh logs -f
```

### Health check

```bash
curl http://localhost:8005/health
curl http://localhost:8080/health
```

---

## 🚀 Performance Tips

1. **Usar volumen para DB**:
   - Ya está configurado como read-only
   - Mejora performance del API

2. **Nginx caching**:
   - Ya está configurado (1 año para assets)

3. **Health checks**:
   - Ayudan a detectar problemas
   - Ya configurado en docker-compose

4. **Restart policy**:
   - `unless-stopped` reinicia automáticamente
   - Perfecto para producción

---

## 📦 Desarrollo

Para hacer cambios:

```bash
# 1. Editar archivos locales
nano TCG-API/index.html
nano TCG-API/main.py

# 2. Recompilar
./manage.sh build

# 3. Reiniciar
./manage.sh restart

# 4. Ver cambios
curl http://localhost:8080
```

---

## 🔐 Seguridad

**⚠️ Para producción:**

- [ ] Cambiar puertos (no usar 8080, 8005)
- [ ] Usar HTTPS/SSL
- [ ] Usar variables de ambiente para URLs
- [ ] Limitar acceso a IPs específicas
- [ ] Usar autenticación en la API
- [ ] Monitorear logs regularmente

```bash
# Ejemplo con variables de ambiente
export API_PORT=3000
export FRONTEND_PORT=3001
docker-compose -f docker-compose.yml up -d
```

---

## 📞 Support

Si hay problemas:

```bash
# Verificar todo
./manage.sh test

# Ver logs
./manage.sh logs

# Contactar con la info de:
docker --version
docker-compose --version
./manage.sh status
```

---

**Happy deploying! 🚀**
