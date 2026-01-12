#!/bin/bash

set -e

COMPOSE_FILE="docker-compose.yml"
COMPOSE_CMD="docker-compose -f $COMPOSE_FILE"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   TCG API + Frontend Docker Manager   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}\n"

# Verificar que estamos en el directorio correcto.
if [ ! -f "$COMPOSE_FILE" ]; then
    echo -e "${RED}❌ Error: docker-compose.yml no encontrado${NC}"
    echo "Ejecuta este script desde la carpeta que contiene docker-compose.yml"
    exit 1
fi

case "${1:-help}" in
    start)
        echo -e "${YELLOW}🚀 Iniciando servicios...${NC}\n"
        $COMPOSE_CMD up -d
        echo -e "${GREEN}✅ Servicios iniciados!${NC}\n"
        echo -e "${BLUE}URLs disponibles:${NC}"
        echo "  🎨 Frontend: http://localhost:8080"
        echo "  🚀 API: http://localhost:8005"
        echo "  📚 API Docs: http://localhost:8005/docs"
        ;;

    stop)
        echo -e "${YELLOW}⏹️  Deteniendo servicios...${NC}\n"
        $COMPOSE_CMD down
        echo -e "${GREEN}✅ Servicios detenidos${NC}"
        ;;

    restart)
        echo -e "${YELLOW}🔄 Reiniciando servicios...${NC}\n"
        $COMPOSE_CMD restart
        echo -e "${GREEN}✅ Servicios reiniciados${NC}"
        ;;

    logs)
        echo -e "${YELLOW}📋 Mostrando logs...${NC}\n"
        $COMPOSE_CMD logs -f ${2:-}
        ;;

    status)
        echo -e "${YELLOW}📊 Estado de servicios:${NC}\n"
        $COMPOSE_CMD ps
        ;;

    build)
        echo -e "${YELLOW}🔨 Compilando imágenes...${NC}\n"
        $COMPOSE_CMD build --no-cache
        echo -e "${GREEN}✅ Imágenes compiladas${NC}"
        ;;

    clean)
        echo -e "${YELLOW}🧹 Limpiando contenedores e imágenes...${NC}\n"
        $COMPOSE_CMD down -v --rmi all
        echo -e "${GREEN}✅ Limpieza completada${NC}"
        ;;

    shell-api)
        echo -e "${YELLOW}🔧 Entrando a contenedor API...${NC}\n"
        $COMPOSE_CMD exec api /bin/bash
        ;;

    shell-frontend)
        echo -e "${YELLOW}🔧 Entrando a contenedor Frontend...${NC}\n"
        $COMPOSE_CMD exec frontend /bin/sh
        ;;

    test)
        echo -e "${YELLOW}🧪 Testeando servicios...${NC}\n"
        
        echo -n "Probando API health... "
        if curl -s http://localhost:8005/health > /dev/null; then
            echo -e "${GREEN}✅${NC}"
        else
            echo -e "${RED}❌${NC}"
        fi
        
        echo -n "Probando API games... "
        if curl -s http://localhost:8005/api/games > /dev/null; then
            echo -e "${GREEN}✅${NC}"
        else
            echo -e "${RED}❌${NC}"
        fi
        
        echo -n "Probando Frontend... "
        if curl -s http://localhost:8080 > /dev/null; then
            echo -e "${GREEN}✅${NC}"
        else
            echo -e "${RED}❌${NC}"
        fi
        
        echo -e "\n${GREEN}✅ Todos los servicios funcionan correctamente${NC}"
        ;;

    help|*)
        echo -e "${BLUE}Comandos disponibles:${NC}\n"
        echo -e "${GREEN}  start${NC}           - Iniciar todos los servicios"
        echo -e "${GREEN}  stop${NC}            - Detener todos los servicios"
        echo -e "${GREEN}  restart${NC}         - Reiniciar servicios"
        echo -e "${GREEN}  logs${NC}            - Ver logs (usar: logs api|frontend)"
        echo -e "${GREEN}  status${NC}          - Ver estado de servicios"
        echo -e "${GREEN}  build${NC}           - Compilar imágenes Docker"
        echo -e "${GREEN}  clean${NC}           - Limpiar todo (contenedores e imágenes)"
        echo -e "${GREEN}  shell-api${NC}       - Entrar a shell del API"
        echo -e "${GREEN}  shell-frontend${NC}  - Entrar a shell del Frontend"
        echo -e "${GREEN}  test${NC}            - Testear que todo funciona"
        echo -e "${GREEN}  help${NC}            - Mostrar esta ayuda\n"
        
        echo -e "${BLUE}Ejemplos:${NC}"
        echo "  ./manage.sh start"
        echo "  ./manage.sh logs api"
        echo "  ./manage.sh status"
        echo "  ./manage.sh test"
        ;;
esac
