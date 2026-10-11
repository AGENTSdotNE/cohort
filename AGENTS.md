# Guide for AI coding assistants

This is a training project. The people building on it range from students to working developers, and many
are new to these tools. Write code they can read, learn from and change without you.

## Stack

- Backend: Django 5.2 and Django REST Framework in `backend/`, Postgres, managed with `uv`.
- Frontend: React 19, Vite, TypeScript, Tailwind 4 and shadcn/ui in `frontend/`.
- Data fetching with TanStack Query, forms with react-hook-form and zod.

## Commands

- `make test` runs the same checks as CI: ruff, the migration check, the Django tests, ESLint, Prettier,
  the TypeScript check and the frontend build. It must pass before any change is finished.
- `make format` fixes formatting in both halves.
- After changing a Django model, run `uv run python manage.py makemigrations` in `backend/`.

## Follow the existing patterns

- A new feature follows `docs/adding-a-feature.md` exactly: a Django app with `models.py`,
  `serializers.py`, `views.py` (a `ModelViewSet`), `urls.py` and `tests/`, and a folder under
  `frontend/src/` with `api.ts`, a `use-*.ts` hook file, and one component per file.
- Every viewset's `get_queryset` must limit rows to what `request.user` may see.
- All HTTP calls go through `apiRequest` in `frontend/src/lib/api-client.ts`, never `fetch`.
- Forms use react-hook-form, a zod schema, `FormField`, and `useApiForm` for server errors.
- UI comes from `frontend/src/components/ui` (shadcn). Add components with
  `npx shadcn@latest add <name>`. If it writes `from "cn"`, change it to `from '@/lib/utils'` and run
  `npm uninstall cn`.
- Read the signed-in user with `useSession()` where it is needed. Do not pass it through props.
- Pages that need sign-in go inside the `RequireAuth` routes in `frontend/src/app/router.tsx`, and get a
  link in `frontend/src/app/layout/app-nav.tsx`.

## Style

- Keep it simple. No abstractions for needs that do not exist yet.
- Small files with one job. One component per file.
- Clear, full names. Comments only for a non-obvious reason why, on one line.
- Add or update tests for every backend change.

## Do not

- Put API keys or secrets in frontend code. Call third-party APIs from Django.
- Change `accounts/` or `frontend/src/auth/` unless the task is about sign-in, accounts or user roles.
- Add new libraries without saying why. Use what is already installed first.
- Commit or push unless asked. When asked, work on a branch and open a pull request. Never commit or push
  to `main`.
- Edit `backend/.env`.
