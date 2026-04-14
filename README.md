# Odoo 18 + Docker Compose

Entorno de desarrollo para Odoo 18 con PostgreSQL 15 y un módulo personalizado de newsletter.

## Objetivo del repositorio

- Levantar Odoo de forma reproducible con Docker Compose.
- Desarrollar módulos en local usando `addons/` montado en el contenedor.
- Probar e instalar el módulo `newsletter_module`.

## Requisitos

- Docker 20.10+
- Docker Compose 2.x
- Puerto `8069` libre
- 4 GB de RAM recomendados

## Inicio rápido

1. Clonar el repositorio:

```bash
git clone https://github.com/ValkoinenKissa/SGE-odoo.git
cd SGE-odoo
```

2. Levantar servicios:

```bash
docker compose up -d
```

3. Abrir Odoo en:

`http://localhost:8069`

4. Crear la base de datos manualmente desde la pantalla inicial de Odoo.

> Este proyecto **no** crea bases de datos automáticamente al arrancar contenedores.

---

## Estructura del proyecto

```text
.
├── .devcontainer/
├── addons/
│   └── newsletter_module/
├── docker-compose.yml
├── odoo.conf
├── LICENSE
└── README.md
```

## Configuración actual

### `docker-compose.yml`

- **db**
  - Imagen: `postgres:15`
  - Credenciales: `odoo/odoo`
  - Base inicial: `postgres`
  - Volumen persistente: `db-data`
  - Healthcheck con `pg_isready`

- **web**
  - Imagen: `odoo:18`
  - Puerto expuesto: `8069`
  - Montajes:
    - `./addons -> /mnt/extra-addons`
    - `./odoo.conf -> /etc/odoo/odoo.conf`
    - `web-data -> /var/lib/odoo`
  - Dependencia de `db` con condición `service_healthy`

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

**Importante:** `admin_passwd` es la contraseña maestra para gestión de bases de datos (no la del usuario `admin` de Odoo).

---

## Módulo incluido: `newsletter_module`

### Resumen

Módulo de gestión de suscripciones newsletter con categorías, validación de email, historial (chatter) y acciones para activar/desactivar suscriptores.

### Dependencias

- `base`
- `mail`

### Modelos

1. `newsletter.subscription`
   - Campos: `name`, `email`, `is_active`, `subscription_date`, `category_id`, `source`
   - Restricciones:
     - SQL: `email` único
     - Python: validación de email por regex
   - Métodos:
     - `action_activate`
     - `action_deactivate`

2. `newsletter.category`
   - Campos: `name`, `code`, `subscription_ids`
   - Campo calculado: `subscriber_count`

### Seguridad

Permisos en `security/ir.model.access.csv` para `base.group_user`:

- Lectura, creación y escritura
- Sin borrado

### Vistas y menús

- Vista lista y formulario para `newsletter.subscription`
- Vista lista y formulario para `newsletter.category`
- Menú raíz **Newsletter**
- Menú **Subscriptions** enlazado a la acción principal

---

## Instalar y actualizar el módulo

### Desde interfaz Odoo

1. Activar modo desarrollador
2. Ir a **Aplicaciones**
3. Actualizar lista de aplicaciones
4. Buscar `Custom Newsletter` o `newsletter_module`
5. Instalar

### Desde consola

Ejemplo con base `odoo_SGE`:

```bash
docker compose exec web odoo --config /etc/odoo/odoo.conf -d odoo_SGE -i newsletter_module --stop-after-init
```

Actualizar módulo:

```bash
docker compose exec web odoo --config /etc/odoo/odoo.conf -d odoo_SGE -u newsletter_module --stop-after-init
docker compose restart web
```

---

## Flujo recomendado de desarrollo

1. Editar código en `addons/newsletter_module`
2. Actualizar módulo con `-u newsletter_module`
3. Revisar logs:

```bash
docker compose logs -f web
```

4. Validar en `http://localhost:8069`

---

## Comandos útiles

```bash
# Estado
docker compose ps

# Logs
docker compose logs -f
docker compose logs -f web
docker compose logs -f db

# Shell en Odoo
docker compose exec web bash

# Consola PostgreSQL
docker compose exec db psql -U odoo -d postgres

# Parar (manteniendo datos)
docker compose down

# Parar y borrar datos
docker compose down -v
```

---

## Dev Container (VS Code)

La carpeta `.devcontainer` permite abrir el proyecto en contenedor desde VS Code.

Pasos:

1. Abrir proyecto en VS Code
2. Ejecutar **Dev Containers: Reopen in Container**
3. Esperar inicialización

Notas:

- La base de datos se crea **manual** desde Odoo.
- No hay scripts automáticos de inicialización de BD.
- Puedes usar `docker compose exec web bash` para administración.

---

## Solución de problemas

1. **No abre `localhost:8069`**
   - Revisar `docker compose ps`
   - Revisar `docker compose logs -f web`

2. **El módulo no aparece**
   - Confirmar `addons/newsletter_module/__manifest__.py`
   - Actualizar lista de aplicaciones
   - Revisar logs de Odoo (XML/permisos)

3. **Error de base de datos**
   - Verificar `odoo.conf` y `docker-compose.yml`
   - Revisar logs de DB: `docker compose logs -f db`

---

## Seguridad y producción

Antes de producción:

1. Cambiar contraseñas por secretos reales
2. Evitar credenciales hardcodeadas (usar variables de entorno)
3. Publicar Odoo detrás de proxy inverso con TLS
4. Restringir acceso de red al puerto `8069`
5. Configurar backups periódicos

---

## Referencias

- Odoo 18: https://www.odoo.com/documentation/18.0/
- Imagen Odoo: https://hub.docker.com/_/odoo
- Imagen PostgreSQL: https://hub.docker.com/_/postgres