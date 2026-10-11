# Staging

Each team has a staging copy of the app on [Railway](https://railway.com), so people outside the team can
try the journey without installing anything. Its link is at the top of the README.

## What works differently there

- **No email.** As on your machine, signing up signs you straight in.
- **Forgotten passwords.** Ask a facilitator, who sets a new one in Django admin.
- **Anyone with the link can sign up.** Use fictional data only, as you do locally.
- **It runs `main`.** Every merge to `main` deploys once its CI checks pass, and migrations run as the app
  starts. If CI fails, staging keeps the last version that passed.
- **Its data is its own.** Accounts and records on your machine do not exist on staging, and the reverse.
  Groups your feature relies on (see [sharing data](sharing-data.md)) must be created in staging's admin too.

## Things that pass locally and fail on staging

- **A new setting with no default.** The Docker build loads the settings before Railway's variables exist,
  so `env('MY_KEY')` with no default fails the build. Always give `env()` a default, and set the real value
  on the Railway service.
- **A changed dependency without its lock file.** The build installs exactly what `uv.lock` and
  `package-lock.json` say. Commit them whenever `pyproject.toml` or `package.json` changes.
- **Server errors.** Staging shows "The server had a problem". The traceback is in the service's
  **Deploy Logs** on Railway.

## Setting up a team's staging (facilitators)

One Railway project per team, each with its own Postgres, so one team's migrations never touch another's
data. Each team's repository is a fork of the base repository, such as `AGENTSdotNE/cohort-1a`.

1. Create a project from the team's fork. Railway builds the root `Dockerfile` and deploys on
   every push to `main`. In the service's **Settings**, under **Source**, turn on **Wait for CI**, so a
   push only deploys after the GitHub Actions checks pass.
2. Add a Postgres database to the project.
3. Add a volume to the app service, mounted at `/app/media`, so profile pictures survive a redeploy.
4. Set these variables on the app service:

   | Variable | Value |
   | --- | --- |
   | `DEBUG` | `false` |
   | `SECRET_KEY` | A long random string. Set it once; changing it signs everyone out. |
   | `ALLOWED_HOSTS` | The app's domain, such as `cohort-1a.up.railway.app`. Comma separated, no spaces. |
   | `CSRF_TRUSTED_ORIGINS` | The same domain with `https://`, such as `https://cohort-1a.up.railway.app` |
   | `FRONTEND_URL` | The same as `CSRF_TRUSTED_ORIGINS` |
   | `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` |
   | `SITE_NAME` | The team's app name |

   Email stays off unless you set `EMAIL_ENABLED=true`, and with `DEBUG` off the app refuses to start
   without `SECRET_KEY`.
5. Generate a domain under the service's **Networking** settings, and put it at the top of the team's
   README.
6. Create your admin account from a shell on the service (`railway ssh`), then run
   `uv run --no-sync python manage.py createsuperuser`.

To turn email on later, set the SMTP variables from `backend/.env.example` and `EMAIL_ENABLED=true`.
Accounts created while it was off are already confirmed, so nobody is locked out.

## Bringing base-app fixes to the teams (facilitators)

Fix the base repository first, merge it into its `main`, then sync each team's fork:

```bash
gh repo sync AGENTSdotNE/cohort-1a
```

This only fast-forwards, so it works until a team has merged its own work. After that, open a pull request
on the team's fork from the base repository's `main` into the fork's `main`, so CI runs and the team can
review the merge. Never add `--force`, and never choose **Discard commits** under GitHub's **Sync fork**:
both replace the team's `main` with the base repository's and throw their work away. Each sync deploys to
that team's staging like any other merge.
