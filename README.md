# Odoo 18 con Docker Compose

Proyecto de Odoo 18 con PostgreSQL 15 usando Docker Compose para un entorno de desarrollo y producción estable.

## 📋 Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) instalado (versión 20.10 o superior)
- [Docker Compose](https://docs.docker.com/compose/install/) instalado (versión 2.0 o superior)
- Al menos 4GB de RAM disponible
- Puerto 8069 libre en tu máquina

## 🚀 Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/ValkoinenKissa/SGE-odoo.git
cd SGE-odoo
```

### 2. Levantar el proyecto

```bash
docker compose up -d
```

Los volúmenes de datos se crean automáticamente gestionados por Docker. No es necesario crear directorios manualmente.

## 📁 Estructura del proyecto

```
.
├── .devcontainer/
│   ├── devcontainer.json       # Configuración del Dev Container
│   └── docker-compose.yml      # Override de Docker Compose para desarrollo
├── addons/                     # Tus módulos personalizados de Odoo
├── scripts/
│   └── init-db.sh              # Script de inicialización de la base de datos
├── docker-compose.yml          # Configuración de Docker Compose
├── odoo.conf                   # Configuración de Odoo
├── .gitignore
├── LICENSE
└── README.md
```

> Los datos de PostgreSQL y el filestore de Odoo se almacenan en **named volumes** gestionados por Docker (`sge-odoo_db-data` y `sge-odoo_web-data`). No aparecen como carpetas en el proyecto y no deben versionarse.

## ⚙️ Configuración

### `odoo.conf`

```ini
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
admin_passwd = admin123
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
workers = 0
```

> ⚠️ `admin_passwd` es la contraseña **maestra** para gestión de bases de datos desde `/web/database/manager`, no la contraseña del usuario `admin` de Odoo.

> ℹ️ `db_name` no está definido intencionalmente, lo que permite trabajar con múltiples bases de datos desde la interfaz web.

## 🌐 Acceder a Odoo

Una vez levantado, accede a Odoo desde tu navegador en:

```
http://localhost:8069
```

Las credenciales por defecto son:

- **Usuario**: `admin`
- **Contraseña**: `admin`

## 🛠️ Comandos útiles

### Ver el estado de los contenedores

```bash
docker compose ps
```

### Ver logs

```bash
# Todos los servicios
docker compose logs -f

# Solo Odoo
docker compose logs -f web

# Solo PostgreSQL
docker compose logs -f db
```

### Detener los contenedores (mantiene los datos)

```bash
docker compose down
```

### Reiniciar solo Odoo

```bash
docker compose restart web
```

### Detener y eliminar todo, incluidos los datos ⚠️

```bash
docker compose down -v
```

### Acceder a la consola del contenedor de Odoo

```bash
docker compose exec web bash
```

### Acceder a PostgreSQL

```bash
docker compose exec db psql -U odoo -d postgres
```

### Ver los volúmenes de Docker

```bash
docker volume ls | grep sge-odoo
```

## 📦 Añadir módulos personalizados

1. Coloca tus módulos en la carpeta `addons/`:

```
addons/
└── mi_modulo/
    ├── __init__.py
    ├── __manifest__.py
    └── ...
```

2. Reinicia Odoo:

```bash
docker compose restart web
```

3. En Odoo ve a **Aplicaciones** → **Actualizar lista de aplicaciones** e instala tu módulo.

Para actualizar un módulo existente:

```bash
docker compose exec web odoo --config /etc/odoo/odoo.conf -d odoo_SGE --update=nombre_modulo --stop-after-init
```

## 🧑‍💻 Desarrollo con Dev Containers (VS Code)

Este proyecto incluye configuración para [Dev Containers](https://containers.dev/), lo que te permite desarrollar directamente dentro del contenedor de Odoo usando VS Code.

### Requisitos

- [Visual Studio Code](https://code.visualstudio.com/)
- Extensión [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Docker en ejecución

### Cómo funciona

La configuración en `.devcontainer/` extiende el `docker-compose.yml` principal:

- **`devcontainer.json`** apunta al servicio `web` como contenedor de trabajo, reenvía el puerto 8069, y ejecuta `scripts/init-db.sh` automáticamente la primera vez mediante `postCreateCommand`.
- **`.devcontainer/docker-compose.yml`** sobreescribe el comando del contenedor con `odoo ... & sleep infinity` para mantenerlo activo mientras VS Code está conectado.

### `scripts/init-db.sh`

Este script se ejecuta una sola vez al crear el devcontainer. Se encarga de:

1. Esperar a que PostgreSQL esté listo.
2. Crear la base de datos `odoo_SGE` (si no existe).
3. Inicializar Odoo con el módulo `base`.

```bash
#!/bin/bash
set -e

while ! pg_isready -h db -U odoo; do sleep 2; done

PGPASSWORD=odoo psql -h db -U odoo -d postgres -c 'CREATE DATABASE "odoo_SGE" OWNER odoo;' 2>/dev/null || true

odoo --config /etc/odoo/odoo.conf -d odoo_SGE -i base --stop-after-init
```

> El `|| true` al final del `psql` hace que si la BD ya existe el script no falle y continúe normalmente.

### Pasos para usarlo

1. Abre el proyecto en VS Code.
2. Abre la paleta de comandos (`Ctrl+Shift+P`) y ejecuta:

```
Dev Containers: Reopen in Container
```

3. VS Code construirá el entorno e inicializará automáticamente la base de datos `odoo_SGE` la primera vez.
4. Accede a Odoo en `http://localhost:8069` con:
   - **Usuario**: `admin`
   - **Contraseña**: `admin`

### Notas importantes

- Los cambios en `addons/` se reflejan en tiempo real gracias al volumen montado.
- La base de datos solo se inicializa la primera vez. En reinicios posteriores del devcontainer los datos persisten en los named volumes.
- Si necesitas reinicializar desde cero, elimina los volúmenes y vuelve a abrir el devcontainer:

```bash
docker compose down -v
# Dev Containers: Rebuild and Reopen in Container
```

## 🔐 Seguridad para producción

Si vas a usar esto en producción:

1. **Cambia todas las contraseñas** en `docker-compose.yml` y `odoo.conf`.
2. **Usa variables de entorno** en lugar de contraseñas hardcodeadas.
3. **Configura un proxy reverso** (nginx) con SSL/TLS.
4. **Limita el acceso** al puerto 8069 usando firewall.
5. **Haz backups regulares** de los volúmenes Docker.
6. **Actualiza regularmente** las imágenes de Docker.

Para hacer backup de los volúmenes:

```bash
docker run --rm -v sge-odoo_db-data:/data -v $(pwd):/backup alpine tar czf /backup/db-backup.tar.gz /data
docker run --rm -v sge-odoo_web-data:/data -v $(pwd):/backup alpine tar czf /backup/web-backup.tar.gz /data
```

## 📚 Recursos adicionales

- [Documentación oficial de Odoo](https://www.odoo.com/documentation/18.0/)
- [Odoo en Docker Hub](https://hub.docker.com/_/odoo)
- [PostgreSQL en Docker Hub](https://hub.docker.com/_/postgres)