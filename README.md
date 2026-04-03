# Prode WC26 - Django productivo

Base productiva para un **prode del Mundial** con:

- Django 5
- PostgreSQL
- Render Key Value (Redis-compatible)
- Celery worker
- cron jobs
- Django Admin
- grupos privados
- fixture
- pronósticos
- ranking
- auditoría básica

## Qué incluye

- auth completa con registro/login/logout
- grupos privados por código
- equipos, estadios, torneo, partidos y resultados
- pronósticos por usuario/partido
- cierre por horario (`lock_at`)
- recálculo de puntos y leaderboard
- tareas asíncronas para lock/recalc
- panel admin
- templates server-rendered + HTMX
- `render.yaml` listo para desplegar en Render Blueprint

## Importante

Esta base está lista para productivizar, pero **no trae el fixture oficial 2026 completo cargado**.
Sí trae:
- estructura de datos correcta
- comandos de carga
- demo data
- lugares exactos para importar tu fixture real

## Levantar con Docker

```bash
cp .env.example .env
docker compose up --build
```

Luego:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py load_demo_data
```

App:
- http://localhost:8000

Admin:
- http://localhost:8000/admin

## Comandos útiles

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py load_demo_data
docker compose exec web python manage.py rebuild_leaderboard
docker compose exec web python manage.py import_fixture_json data/fixture.sample.json
```

## Deploy en Render

Este repo ya trae un `render.yaml` para desplegar con **Blueprints**. Render soporta Blueprints con `render.yaml` en la raíz del repo, y el mismo blueprint puede definir un **web service**, **background worker**, **cron jobs**, **Render Key Value** y **Render Postgres**. citeturn891580search0turn891580search2

### Arquitectura que crea el blueprint

- `prode-wc26-web`: Django + Gunicorn
- `prode-wc26-worker`: Celery worker
- `prode-wc26-scheduler`: cron cada minuto para bloquear partidos y pasarlos a live
- `prode-wc26-rebuild-nightly`: cron nocturno para reconstruir leaderboards
- `prode-wc26-redis`: Render Key Value con `noeviction`
- `prode-wc26-db`: Render Postgres

Render documenta `type: web`, `worker`, `cron` y `keyvalue` en Blueprints, además de `fromDatabase` y `fromService` para inyectar `DATABASE_URL` y otras variables entre servicios. citeturn186999view0turn131505view3turn131505view4

### Pasos

1. Subí este repo a GitHub.
2. En Render, andá a **Blueprints** → **New Blueprint Instance**.
3. Conectá el repo.
4. Confirmá el `render.yaml`.
5. Deploy.

Render también tiene una guía oficial para desplegar Django y otra para Celery workers. La guía de Django recomienda un `build.sh` y usar Gunicorn para iniciar la app; la de Celery usa un **background worker** y una instancia **Key Value** como broker. citeturn891580search3turn891580search1

### Costos / planes a considerar

- Render permite `free` para algunos recursos, pero **background workers** y **cron jobs** no tienen plan free; el spec indica que esos servicios usan `starter` o superior. citeturn186999view0
- Render Postgres tiene plan `basic-256mb` por defecto en Blueprints, y el free tier de Postgres no es una base seria para producción prolongada. Render aclara que las instancias free de Postgres expiran tras 30 días. citeturn186999view0turn891580search3
- Para colas, Render recomienda **Key Value starter** con `noeviction` para no perder tareas cuando se llena la memoria. citeturn891580search1turn855142view2

### Variables más importantes

El `render.yaml` ya define:
- `DJANGO_SETTINGS_MODULE=config.settings.prod`
- `DATABASE_URL` desde Render Postgres
- `REDIS_URL` desde Render Key Value
- `SECRET_KEY` generado por Render
- `ALLOWED_HOSTS=.onrender.com`
- `CSRF_TRUSTED_ORIGINS=https://*.onrender.com`

### Después del primer deploy

Creá el admin desde el Shell de Render:

```bash
python manage.py createsuperuser
```

Luego podés cargar demo data:

```bash
python manage.py load_demo_data
```

O importar tu fixture real:

```bash
python manage.py import_fixture_json data/fixture.sample.json
```

## Observaciones

- Esta versión **sí** es adecuada para Render.
- **No** la desplegaría en Vercel como versión productiva completa, porque acá hay worker continuo + cron + broker + Postgres.
