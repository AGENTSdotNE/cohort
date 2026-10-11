# Troubleshooting

Problems people actually hit, and how to fix them. If you solve something that is not here, add it.

## `403 CSRF Failed: Origin checking failed`

Signing in works, but everything after it (saving, deleting, signing out) fails with a 403.

The frontend is running on a different address from the one Django trusts. Vite picks another port
if 5173 is busy, so check the address in your browser. Then set both values in `backend/.env` to match
and restart Django:

```
FRONTEND_URL=http://localhost:5174
CSRF_TRUSTED_ORIGINS=http://localhost:5174
```

## `TypeError: crypto.hash is not a function`, or `npm install` says "Unsupported engine"

Your Node is too old. Use the version in `frontend/.nvmrc`:

```bash
cd frontend
nvm install
nvm use
```

## `password authentication failed for user "cohort"`, or `connection refused` on port 5442

Django cannot reach the database.

- Is it running? `docker compose ps` should show `db` as healthy. If not, start `make dev`.
- Is something else using port 5442? `lsof -i :5442` shows what. Stop it, or change the port in
  `docker-compose.yml` and `DATABASE_URL` in `backend/.env` together.

## `relation "..." does not exist`

A migration has not been run. Run `make migrate`, or restart `make dev`, which applies migrations as it starts.
If you changed a model, run `uv run python manage.py makemigrations` in `backend/` first.

## Where are the confirmation and password reset emails?

Email is switched off, locally and on staging, so signing up signs you straight in and the sign-in page
hides "Forgotten your password?". If you forget a password, set a new one in Django admin, or run
`make seed` for accounts with a known password. To try the email flows, set `EMAIL_ENABLED=true` in
`backend/.env` and restart `make dev`: emails are then printed in its output, not sent.

## "The app can't load right now" or "The server had a problem"

Django is not running, or it crashed. Check that `make dev` is still running, then read the last
`backend-1` lines in its output: the traceback names the file and line that failed.

## "Could not reach the server"

The browser could not reach Vite at all. Check that `make dev` is still running, then reload.

## I keep getting sent back to the sign-in page

Your session ended: it expired, you changed your password on another device, or the database was reset.
Sign in again.

## `Bind for 0.0.0.0:8000 failed: port is already allocated`

Another program, often another project's Docker containers, is using a port this app needs (5173, 8000,
5442 or 6006). `docker ps` lists running containers and their ports. Stop the one using it, or close the
other program, then run `make dev` again.

## `make test` fails on formatting

Run `make format` to fix formatting in both the backend and the frontend, then run `make test` again.

## A shadcn component imports from `"cn"`

Newer versions of the shadcn CLI write `import { cn } from "cn"` and install a `cn` package. This
project uses its own helper, so change the import to `import { cn } from '@/lib/utils'` and run
`npm uninstall cn`.
