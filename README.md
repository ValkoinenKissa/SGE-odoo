# Odoo 18 con Docker Compose

Proyecto de Odoo 18 con PostgreSQL 15 usando Docker Compose para un entorno de desarrollo y producción estable.

## 📋 Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) instalado (versión 20.10 o superior)
- [Docker Compose](https://docs.docker.com/compose/install/) instalado (versión 2.0 o superior)
- Al menos 4GB de RAM disponible
- Puertos 8069 y 8072 libres en tu máquina

## 🚀 Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/ValkoinenKissa/SGE-odoo.git
cd SGE-odoo
```

### 2. Crear los directorios necesarios

Antes de levantar los contenedores, crea las carpetas donde se guardarán los datos:

```bash
mkdir -p addons postgresql odoo-web-data
```

**Descripción de los directorios:**
- `addons/` - Tus módulos personalizados de Odoo
- `postgresql/` - Datos de la base de datos PostgreSQL
- `odoo-web-data/` - Filestore de Odoo (archivos subidos, sesiones)

### 3. Crear el archivo de configuración de Odoo

Crea el archivo `odoo.conf` en la raíz del proyecto:

```bash
touch odoo.conf
```

Contenido recomendado para `odoo.conf`:

```ini
[options]
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
admin_passwd = CAMBIA_ESTA_PASSWORD_MAESTRA
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
workers = 2
max_cron_threads = 1
```

> ⚠️ **IMPORTANTE**: Cambia `admin_passwd` por una contraseña segura antes de usar en producción.

### 4. (Opcional) Configurar credenciales seguras

Para producción, edita el archivo `docker-compose.yml` y cambia las contraseñas:

```yaml
environment:
  - POSTGRES_PASSWORD=TU_PASSWORD_SEGURA  # Cambiar aquí
```

Y actualiza también en `odoo.conf`:
```ini
db_password = TU_PASSWORD_SEGURA
```

## 🏃 Levantar el proyecto

### Iniciar los contenedores

```bash
docker-compose up -d
```

Este comando:
- Descarga las imágenes de Odoo 18 y PostgreSQL 15 (solo la primera vez)
- Crea y levanta los contenedores en segundo plano
- Espera a que PostgreSQL esté completamente operativo antes de iniciar Odoo

### Verificar que todo está funcionando

```bash
docker-compose ps
```

Deberías ver algo como:

```
NAME                COMMAND                  SERVICE   STATUS          PORTS
project-db-1        "docker-entrypoint.s…"   db        Up (healthy)    5432/tcp
project-web-1       "/entrypoint.sh odoo"    web       Up              0.0.0.0:8069->8069/tcp, 0.0.0.0:8072->8072/tcp
```

### Ver los logs

```bash
# Ver todos los logs
docker-compose logs -f

# Ver solo logs de Odoo
docker-compose logs -f web

# Ver solo logs de PostgreSQL
docker-compose logs -f db
```

## 🌐 Acceder a Odoo

Una vez levantado, accede a Odoo desde tu navegador:

```
http://localhost:8069
```

En la primera ejecución:
1. Se mostrará la pantalla de creación de base de datos
2. Completa los siguientes campos:
   - **Master Password**: La que configuraste en `admin_passwd` del `odoo.conf`
   - **Database Name**: Nombre de tu base de datos (ej: `mi_empresa`)
   - **Email**: Tu email de administrador
   - **Password**: Contraseña para el usuario administrador
   - **Language**: Español (o el idioma que prefieras)
   - **Country**: España (o tu país)

## 🛠️ Comandos útiles

### Detener los contenedores

```bash
docker-compose down
```

### Reiniciar solo Odoo (sin afectar la base de datos)

```bash
docker-compose restart web
```

### Reiniciar todo

```bash
docker-compose restart
```

### Detener y eliminar contenedores (mantiene los datos)

```bash
docker-compose down
```

### Detener y eliminar todo (⚠️ BORRA LOS DATOS)

```bash
docker-compose down -v
rm -rf postgresql odoo-web-data
```

### Ver el uso de recursos

```bash
docker stats
```

### Acceder a la consola de Odoo

```bash
docker-compose exec web bash
```

### Acceder a PostgreSQL

```bash
docker-compose exec db psql -U odoo -d postgres
```

## 📦 Añadir módulos personalizados

1. Coloca tus módulos en la carpeta `addons/`:

```bash
addons/
├── mi_modulo/
│   ├── __init__.py
│   ├── __manifest__.py
│   └── ...
```

2. Reinicia Odoo:

```bash
docker-compose restart web
```

3. En Odoo, ve a **Aplicaciones** → **Actualizar lista de aplicaciones**
4. Busca e instala tu módulo

## 🔧 Solución de problemas

### Error de permisos en `odoo-web-data`

Si Odoo no puede escribir en el directorio:

```bash
sudo chown -R 101:101 odoo-web-data
```

### PostgreSQL no inicia correctamente

Verifica los logs:

```bash
docker-compose logs db
```

Si hay problemas de permisos:

```bash
sudo chown -R 999:999 postgresql
```

### Odoo no se conecta a la base de datos

1. Verifica que el healthcheck de PostgreSQL esté OK:
```bash
docker-compose ps
```

2. Comprueba que las credenciales en `docker-compose.yml` coincidan con `odoo.conf`

### Reiniciar completamente (borrar todo)

```bash
docker-compose down
sudo rm -rf postgresql odoo-web-data
mkdir -p addons postgresql odoo-web-data
docker-compose up -d
```

## 📁 Estructura del proyecto

```
.
├── docker-compose.yml      # Configuración de Docker Compose
├── odoo.conf              # Configuración de Odoo
├── .gitignore             # Archivos ignorados por Git
├── README.md              # Este archivo
├── addons/                # Tus módulos personalizados
├── postgresql/            # Datos de PostgreSQL (no versionar)
└── odoo-web-data/         # Filestore de Odoo (no versionar)
```

## 🔐 Seguridad para producción

Si vas a usar esto en producción:

1. **Cambia todas las contraseñas** en `docker-compose.yml` y `odoo.conf`
2. **Usa variables de entorno** en lugar de contraseñas hardcodeadas
3. **Configura un proxy reverso** (nginx) con SSL/TLS
4. **Limita el acceso** al puerto 8069 usando firewall
5. **Haz backups regulares** de `postgresql/` y `odoo-web-data/`
6. **Actualiza regularmente** las imágenes de Docker

## 📚 Recursos adicionales

- [Documentación oficial de Odoo](https://www.odoo.com/documentation/18.0/)
- [Odoo en Docker Hub](https://hub.docker.com/_/odoo)
- [PostgreSQL en Docker Hub](https://hub.docker.com/_/postgres)

