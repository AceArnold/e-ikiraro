# E-ikiraro

E-ikiraro is a web application built with Django.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
*   [Python 3](https://www.python.org/downloads/) (version 3.8 or newer recommended)
*   [Git](https://git-scm.com/downloads/)

## Setup and Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/e-ikiraro.git
cd e-ikiraro
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

**On Windows:**

```bash
# Create the virtual environment
py -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```

**On macOS and Linux:**

```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

With your virtual environment activated, install the required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Database Migration

Once the dependencies are installed, apply the database migrations:

```bash
cd django_backend
python manage.py makemigrations
python manage.py migrate
```

## Running the Application

To run the development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Creating a Superuser

To access the Django admin panel, you'll need a superuser account:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a username, email, and password. You can then log in to the admin panel at `http://127.0.0.1:8000/admin`.

## Environment variables & secrets

Secrets (SECRET_KEY, SMTP credentials, OAuth client IDs/secrets) must not be committed to the repository. We provide a template you should copy and fill locally.

1. Copy the template to create a local `.env` file (DO NOT commit `.env`):

```bash
cp django_backend/.env.example django_backend/.env
# open and fill values (SECRET_KEY, EMAIL_HOST_PASSWORD, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, etc.)
```

2. The repository already ignores local secret files (`.env` and `client_secret_*.json`). Do NOT add secrets to git. If a secret was accidentally committed, rotate it immediately.

3. The project loads environment variables from your local `.env` (settings use `python-decouple` / `decouple.config`) so the app reads credentials at runtime.

## Google social login (allauth)

We support signing in with Google using `django-allauth`. To avoid committing the client secret to the repo, follow one of these approaches.

A) Create the SocialApp from environment variables (recommended for local/dev):

1. Add `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to `django_backend/.env`.
2. Run migrations and then run the helper management command which reads the env vars and creates/updates the SocialApp in the DB:

```bash
source venv/bin/activate
cd django_backend
python manage.py migrate
python manage.py create_socialapp
```

This command will attach the SocialApp to site id 1.

B) Or create the SocialApp via Django admin:

1. Start the server and log in to the admin at `/admin/`.
2. Under Social Accounts → Social applications, add a new app for provider `google`, paste the client id and secret, and attach the site.

Notes:
- Make sure the OAuth redirect URI registered in Google Cloud matches your dev server (e.g. `http://127.0.0.1:8000/accounts/google/login/callback/`).
- Keep client secrets out of source control. If a secret was pushed to a remote, rotate it immediately in the Google Cloud Console.

## Troubleshooting

- If email sending fails in development, you can use the console email backend by setting `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` in your local `.env`.
- If `create_socialapp` reports the env vars are missing, ensure you exported them or placed them in `django_backend/.env` and that your virtualenv is active.
