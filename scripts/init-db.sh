#!/bin/bash
set -e

while ! pg_isready -h db -U odoo; do sleep 2; done

PGPASSWORD=odoo psql -h db -U odoo -d postgres -c 'DROP DATABASE IF EXISTS "odoo_SGE";'
PGPASSWORD=odoo psql -h db -U odoo -d postgres -c 'CREATE DATABASE "odoo_SGE" OWNER odoo;'

odoo --config /etc/odoo/odoo.conf -d odoo_SGE -i base --stop-after-init