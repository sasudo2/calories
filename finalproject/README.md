# Calorie Tracker

A simple Django app to log daily calorie entries and compute BMI, built as a small final project.

## Features

- User registration and login
- Log daily food/calorie entries
- View today's entries and historical records
- BMI calculator view

## Project structure

- `manage.py` — Django project management script
- `db.sqlite3` — SQLite database (included)
- `calories/` — Django app containing models, views, templates, and static files
  - `calories/templates/calories/` — HTML templates
  - `calories/static/calories/` — CSS and images

## Prerequisites

- Python 3.8 or newer
- pip

## Installation

1. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Before running the project, provide a secret key via environment variables. Copy the example and set your key:

```bash
cp .env.example .env
# edit .env and replace DJANGO_SECRET_KEY value
```

The project reads `DJANGO_SECRET_KEY` from the environment. `.env` is ignored by `.gitignore` (see `.env.example`).

3. Apply migrations (the repository includes `db.sqlite3`, but run migrations if you reset the DB):

```bash
python manage.py migrate
```

4. (Optional) Create a superuser:

```bash
python manage.py createsuperuser
```

## Running the app

Start the development server:

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. The main app pages are under the `calories` app templates, e.g., the index, login, register, today, record, and BMI pages.

## Useful files

- [manage.py](manage.py) — run server, migrations, and management commands
- [calories/models.py](calories/models.py) — data models for entries and user relations
- [calories/views.py](calories/views.py) — request handlers and view logic
- [calories/templates/calories/](calories/templates/calories/) — HTML templates

## Tests

Run tests with:

```bash
python manage.py test
```

## Notes

- The project uses SQLite (`db.sqlite3`) for ease of setup.
- Static CSS is under `calories/static/calories/styles.css`.

