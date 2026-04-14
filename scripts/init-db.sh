#!/bin/bash
set -e

while ! pg_isready -h db -U odoo; do sleep 2; done

DB_EXISTS=$(PGPASSWORD=odoo psql -h db -U odoo -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='odoo_SGE';")

if [ "$DB_EXISTS" != "1" ]; then
    echo "Creando base de datos odoo_SGE..."
    PGPASSWORD=odoo psql -h db -U odoo -d postgres -c 'CREATE DATABASE "odoo_SGE" OWNER odoo;'
else
    echo "La base de datos odoo_SGE ya existe, omitiendo creación."
fi

odoo --config /etc/odoo/odoo.conf -d odoo_SGE -i base --stop-after-init