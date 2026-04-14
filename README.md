# Odoo 18 + Docker Compose

Entorno de desarrollo para Odoo 18 con PostgreSQL 15 y un módulo personalizado de newsletter.

## Objetivo del repositorio

- Levantar Odoo de forma reproducible con Docker Compose.
- Desarrollar módulos en local usando la carpeta addons montada en el contenedor.
- Probar e instalar el módulo newsletter_module incluido en este proyecto.

## Requisitos

- Docker 20.10+.
- Docker Compose 2.x.
- Puerto 8069 libre.
- Al menos 4 GB de RAM recomendados.

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

```text
http://localhost:8069
```

4. Crear la base de datos desde el navegador en la pantalla inicial de Odoo.

Nota: el script scripts/init-db.sh está pensado para el flujo de Dev Container, donde sí está disponible dentro del entorno de trabajo.

## Estructura del proyecto

```text
.
├── .devcontainer/
├── addons/
│   └── newsletter_module/
├── scripts/
│   └── init-db.sh
├── docker-compose.yml
├── odoo.conf
├── LICENSE
└── README.md
```

## Configuración actual

### docker-compose.yml

- Servicio db:
  - Imagen postgres:15.
  - Usuario y contraseña: odoo/odoo.
  - Base inicial: postgres.
  - Volumen persistente: db-data.
  - Healthcheck con pg_isready.
- Servicio web:
  - Imagen odoo:18.
  - Puerto 8069 expuesto.
  - Montajes:
     - ./addons -> /mnt/extra-addons.
     - ./odoo.conf -> /etc/odoo/odoo.conf.
     - web-data -> /var/lib/odoo.

### odoo.conf

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

Importante: admin_passwd es la contraseña maestra de gestión de bases de datos, no la del usuario admin de Odoo.

## Módulo incluido: newsletter_module

### Resumen

Módulo de gestión de suscripciones newsletter con categorías, validación de email, historial (chatter) y acciones para activar o desactivar suscriptores.

### Dependencias del módulo

- base
- mail

### Modelos

1. newsletter.subscription
    - Campos principales: name, email, is_active, subscription_date, category_id, source.
    - Restricciones:
      - SQL: email único.
      - Python: validación de formato de email con regex.
    - Métodos:
      - action_activate.
      - action_deactivate.

2. newsletter.category
    - Campos principales: name, code, subscription_ids.
    - Campo calculado: subscriber_count.

### Seguridad

Permisos en security/ir.model.access.csv para usuarios internos (base.group_user):

- Lectura, escritura y creación en suscripciones y categorías.
- Sin permiso de borrado.

### Vistas y menús

- Vista lista y formulario para newsletter.subscription.
- Vista lista y formulario para newsletter.category.
- Menú raíz Newsletter.
- Menú Subscriptions enlazado a la acción principal.

## Instalar y actualizar el módulo

### Desde interfaz de Odoo

1. Activar modo desarrollador.
2. Ir a Aplicaciones.
3. Actualizar la lista de aplicaciones.
4. Buscar Custom Newsletter o newsletter_module.
5. Instalar.

### Desde consola

Usando la base odoo_SGE:

```bash
docker compose exec web odoo --config /etc/odoo/odoo.conf -d odoo_SGE -i newsletter_module --stop-after-init
```

Para actualizar cambios del módulo:

```bash
docker compose exec web odoo --config /etc/odoo/odoo.conf -d odoo_SGE -u newsletter_module --stop-after-init
docker compose restart web
```

## Flujo recomendado de desarrollo

1. Editar código en addons/newsletter_module.
2. Actualizar el módulo con -u newsletter_module.
3. Revisar logs:

```bash
docker compose logs -f web
```

4. Verificar interfaz en http://localhost:8069.

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

## Dev Container (VS Code)

La carpeta .devcontainer permite abrir el proyecto directamente en contenedor.

Pasos:

1. Abrir el proyecto en VS Code.
2. Ejecutar Dev Containers: Reopen in Container.
3. Esperar a que termine la inicialización.

Al levantar todo el stack desde Dev Container:

- Se crea automáticamente la base de datos odoo_SGE (si no existe).
- Las credenciales por defecto son:
  - Usuario: admin
  - Contraseña: admin

El script scripts/init-db.sh se encarga de:

- Esperar a PostgreSQL.
- Crear odoo_SGE si no existe.
- Instalar el módulo base.

## Solución de problemas

1. No abre localhost:8069.
    - Revisar docker compose ps y docker compose logs -f web.

2. El módulo no aparece en Aplicaciones.
    - Confirmar que existe addons/newsletter_module/__manifest__.py.
    - Actualizar lista de aplicaciones.
    - Revisar logs de Odoo por errores XML o permisos.

3. Error de base de datos.
    - Verificar credenciales en odoo.conf y docker-compose.yml.
    - Revisar estado de db con docker compose logs -f db.

## Seguridad y producción

Antes de pasar a producción:

1. Cambiar todas las contraseñas por secretos reales.
2. Evitar credenciales hardcodeadas, usar variables de entorno.
3. Publicar Odoo detrás de proxy inverso con TLS.
4. Restringir acceso de red al puerto 8069.
5. Configurar copias de seguridad periódicas.

## Referencias

- Documentación oficial de Odoo 18: https://www.odoo.com/documentation/18.0/
- Imagen Odoo: https://hub.docker.com/_/odoo
- Imagen PostgreSQL: https://hub.docker.com/_/postgres