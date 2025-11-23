# E-ikiraro

**E-ikiraro** is a comprehensive web application for managing government document applications and services in Burundi. It streamlines the process for citizens to apply for passports, national IDs, and driver's licenses through an intuitive online platform with secure payment integration and real-time application tracking.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Database Migrations](#database-migrations)
- [Running the Application](#running-the-application)
- [Creating a Superuser](#creating-a-superuser)
- [Environment Configuration](#environment-configuration)
- [Authentication & Social Login](#authentication--social-login)
- [API Endpoints](#api-endpoints)
- [Application Workflows](#application-workflows)
- [File Upload & Storage](#file-upload--storage)
- [Development Tips](#development-tips)
- [Troubleshooting](#troubleshooting)

## 🎯 Features

### Core Features

- **Multi-Service Application System**
  - Passport applications with type selection (adult/child/diplomatic)
  - National ID card applications with parental information
  - Driver's License applications with medical/eye test requirements
  
- **User Authentication & Authorization**
  - Email/password registration and login
  - Google OAuth 2.0 integration via django-allauth
  - Email verification and account activation
  - Password reset functionality

- **Application Management**
  - Submit and track applications across multiple services
  - Real-time application status tracking (pending, reviewed, approved, rejected)
  - Detailed application view with submitted documents and payment status
  - Application history per user

- **Payment Processing**
  - Secure payment integration for application fees
  - Payment status tracking (pending, completed, failed)
  - Payment confirmation and receipts

- **Document Management**
  - Secure file uploads for required documents
  - Document type-specific storage (separate folders for passports, national IDs, licenses)
  - File size validation (5MB per file)
  - Support for various document formats (PDF, images)

- **Admin Dashboard**
  - Django admin interface for managing applications, payments, and services
  - Bulk operations and filtering
  - User management

### Frontend Features

- Responsive, mobile-first design
- Two-column form layouts with sidebar tips
- Real-time file preview for uploaded documents
- Client-side file size validation (5MB limit)
- Dynamic service listing from database
- Clean card-based UI for applications
- Bootstrap 5 styling with custom theme

## 📁 Project Structure

```
e-ikiraro/
├── django_backend/              # Django backend application
│   ├── manage.py               # Django management script
│   ├── db.sqlite3              # SQLite database (development)
│   ├── requirements.txt         # Backend dependencies
│   ├── .env.example            # Environment variables template
│   │
│   ├── django_backend/         # Main Django project settings
│   │   ├── settings.py         # Django configuration
│   │   ├── urls.py             # URL routing
│   │   ├── asgi.py             # ASGI configuration
│   │   └── wsgi.py             # WSGI configuration
│   │
│   ├── e_ikiraro/              # Main application (services & apps)
│   │   ├── models.py           # Data models (Service, Applications, Payment, Document)
│   │   ├── views.py            # View logic for home, services, admin
│   │   ├── urls.py             # URL patterns
│   │   ├── forms.py            # Django forms
│   │   ├── admin.py            # Django admin configuration
│   │   ├── api.py              # API endpoints
│   │   ├── templates/          # Templates for e_ikiraro app
│   │   └── static/             # Static files (CSS, JS, images)
│   │
│   ├── applications/           # Applications management app
│   │   ├── models.py           # (Empty - uses e_ikiraro models)
│   │   ├── views.py            # Application workflow views
│   │   ├── urls.py             # Application URLs
│   │   ├── forms.py            # Application forms (Passport, NID, DL)
│   │   ├── admin.py            # Admin config for applications
│   │   └── templates/          # Application templates
│   │       ├── my_applications.html
│   │       ├── application_detail.html
│   │       ├── passport_form.html
│   │       ├── nationalid_form.html
│   │       ├── drivers_license_form.html
│   │       └── service_start.html
│   │
│   ├── users/                  # User management app
│   │   ├── models.py           # Custom User model
│   │   ├── views.py            # Authentication views
│   │   ├── forms.py            # Registration/login forms
│   │   ├── admin.py            # User admin
│   │   ├── tokens.py           # Email verification tokens
│   │   └── templates/          # Auth templates (login, register, profile)
│   │
│   └── media/                  # User-uploaded files
│       └── documents/          # Application documents
│           ├── birth_certificates/
│           ├── passport_photos/
│           ├── national_ids/
│           ├── eye_test_certificates/
│           ├── medical_certificates/
│           └── license_photos/
│
├── front_end/                   # Static frontend files
│   ├── index.html              # Homepage
│   ├── pages/                  # Additional pages (login, register, docs, etc.)
│   ├── scripts/                # JavaScript files
│   ├── styles/                 # CSS stylesheets
│   ├── images/                 # Static images
│   └── assets/                 # Additional assets
│
└── requirements.txt            # Root-level dependencies
```

## ✅ Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.10 or newer** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads/))
- **pip** (usually included with Python)
- **virtualenv** (for virtual environment management)

## 🚀 Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AceArnold/e-ikiraro.git
cd e-ikiraro
```

### 2. Create and Activate a Virtual Environment

It is **highly recommended** to use a virtual environment to isolate project dependencies.

**On Windows:**

```bash
py -m venv venv
.\venv\Scripts\activate
```

**On macOS and Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

With your virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

**Key dependencies:**
- Django 5.2.7 – Web framework
- django-allauth 65.13.0 – User authentication with Google OAuth
- django-crispy-forms 2.4 & crispy-bootstrap5 2025.6 – Form rendering
- Pillow 12.0.0 – Image handling for file uploads
- python-decouple 3.8 – Environment variable management

### 4. Configure Environment Variables

1. Copy the template and create your local `.env` file:

```bash
cp django_backend/.env.example django_backend/.env
```

2. Open `django_backend/.env` and fill in the following values:

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True

# Email Configuration (for notifications and password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com          # or your email provider
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Google OAuth (Social Login)
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

**Important:** Never commit `.env` to version control. The `.gitignore` already excludes it.

## 🗄️ Database Migrations

### Initial Setup

After configuring the environment, navigate to the Django backend directory and apply migrations:

```bash
cd django_backend
python manage.py makemigrations
python manage.py migrate
```

### Available Models & Migrations

- **0001_initial** – Initial database schema (User, Service, Application models)
- **0002_alter_driverslicenseapplication_id_and_more** – ID field adjustments
- **0003_passportapplication_current_address_and_more** – Additional application fields
- **0004_alter_passportapplication_gender** – Gender field adjustments
- **0005_add_service_photo** – Service model photo field

### Creating Subsequent Migrations

When you modify models, create and apply new migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## ▶️ Running the Application

### Start the Development Server

```bash
cd django_backend
python manage.py runserver
```

The application will be available at:
- **Frontend:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### Check System Health

Verify everything is configured correctly:

```bash
python manage.py check
```

## 👨‍💼 Creating a Superuser

To access the Django admin panel and manage applications, create a superuser account:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter:
- Username
- Email address
- Password (twice for confirmation)

Then log in at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) with your credentials.

### Admin Capabilities

- **Manage Services:** Add, edit, or delete services (Passport, National ID, Driver's License)
- **Review Applications:** View submitted applications and update their status
- **Process Payments:** Track and manage payment records
- **User Management:** Manage user accounts and permissions
- **Document Management:** View and organize uploaded documents

## 🔐 Environment Configuration

All sensitive information should be stored in `django_backend/.env`. The project uses `python-decouple` to safely load environment variables at runtime.

**Environment Variables Reference:**

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Django secret key for security |
| `DEBUG` | Yes | Set to `True` for development, `False` for production |
| `EMAIL_HOST` | Yes | SMTP server for sending emails |
| `EMAIL_PORT` | Yes | SMTP port (usually 587 for TLS) |
| `EMAIL_HOST_USER` | Yes | Email account for sending notifications |
| `EMAIL_HOST_PASSWORD` | Yes | App-specific password or email password |
| `EMAIL_USE_TLS` | Yes | Enable TLS encryption for email |
| `DEFAULT_FROM_EMAIL` | Yes | Sender email address |
| `GOOGLE_CLIENT_ID` | No | For Google OAuth (optional) |
| `GOOGLE_CLIENT_SECRET` | No | For Google OAuth (optional) |

## 🔑 Authentication & Social Login

### Email/Password Registration

1. Navigate to the registration page
2. Fill in email, password, and confirm password
3. Submit the form
4. Verify your email using the link sent to your inbox
5. Log in with your credentials

### Google OAuth Login

1. Click "Sign in with Google" on the login page
2. Authenticate with your Google account
3. Authorize the application to access your profile and email
4. You will be logged in and redirected to your dashboard

**Note:** Google OAuth configuration requires setting `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`.

## 📡 API Endpoints

### Public Endpoints

- `GET /` – Homepage with service listings
- `POST /api/services/` – List available services

### Authenticated Endpoints

- `GET /my-applications/` – View user's applications
- `GET /applications/<id>/` – View application details
- `POST /passport/apply/` – Start passport application
- `POST /nationalid/apply/` – Start national ID application
- `POST /license/apply/` – Start driver's license application

## 📋 Application Workflows

### Passport Application Flow

1. **Start** – User clicks "Apply for Passport" → redirected to `service_start.html`
2. **Form Submission** – Fill form with personal info, emergency contact, and previous passport details
3. **Document Upload** – Upload passport photo, birth certificate, and national ID
4. **Payment** – Process payment for application fee
5. **Confirmation** – Receive confirmation email with application ID
6. **Tracking** – Check application status in "My Applications"

### National ID Application Flow

1. **Start** – Click "Apply for National ID" → view service start page
2. **Form** – Enter parental information and address
3. **Document** – Upload birth certificate
4. **Payment** – Pay application fee
5. **Confirmation** – Email confirmation with tracking ID
6. **Track** – Monitor status in dashboard

### Driver's License Application Flow

1. **Start** – Click "Apply for Driver's License"
2. **Form** – Select license type (motorcycle, car, etc.) and enter address
3. **Documents** – Upload photo, national ID, medical certificate, and eye test certificate
4. **Payment** – Complete payment
5. **Confirmation** – Receive email confirmation
6. **Track** – Follow progress in applications list

## 📁 File Upload & Storage

### Supported File Types

- PDF documents
- JPG/JPEG images
- PNG images
- Scans (PDF, JPG, PNG)

### File Size Limits

- **Maximum file size:** 5MB per document
- Client-side validation provides immediate feedback
- Server-side validation enforces the limit

### Storage Locations

All uploaded files are stored in `django_backend/media/documents/` organized by type:

```
media/documents/
├── passport_photos/        # Passport application photos
├── birth_certificates/     # Birth certificates (Passport & National ID)
├── national_ids/           # National ID scans
├── medical_certificates/   # Medical certificates (Driver's License)
├── eye_test_certificates/  # Eye test certificates (Driver's License)
├── license_photos/         # Driver's License application photos
└── service_photos/         # Service overview photos
```

### Security Considerations

- Files are scanned for malware on upload (optional - can be configured)
- User uploads are stored outside the web root
- File access is restricted to authenticated users
- File ownership is tied to the application record

## 🛠️ Development Tips

### Working with Forms

All application forms use Django's ModelForm and are styled with django-crispy-forms and Bootstrap 5:

```python
# Example form in applications/forms.py
from django import forms
from e_ikiraro.models import PassportApplication

class PassportApplicationForm(forms.ModelForm):
    class Meta:
        model = PassportApplication
        fields = ['passport_type', 'first_name', 'last_name', ...]
```

### Adding a New Service

To add a new service (e.g., Vehicle Registration):

1. **Create the model** in `e_ikiraro/models.py`
2. **Create the form** in `applications/forms.py`
3. **Add views** in `applications/views.py` (start, form, payment, confirmation)
4. **Create templates** in `applications/templates/applications/`
5. **Add URLs** to `applications/urls.py`
6. **Register in admin** in `applications/admin.py`
7. **Add service** to database via Django admin

### Client-Side Preview & Validation

File previews and validation are implemented in the form templates using vanilla JavaScript:

```javascript
// Example: File preview with size check
input.addEventListener('change', function() {
  const file = this.files[0];
  if (file.size > 5 * 1024 * 1024) {
    alert('File must be under 5MB');
    this.value = '';
    return;
  }
  // Create and display image preview
  const reader = new FileReader();
  reader.onload = function(e) {
    const img = document.createElement('img');
    img.src = e.target.result;
    previewContainer.appendChild(img);
  }
  reader.readAsDataURL(file);
});
```

### Email Templates

Email notifications use Django's template system:

- **Account activation:** `users/templates/template_activate_account.html`
- **Application confirmation:** `applications/templates/applications/application_confirmation_email.html`

Edit these to customize email content.

### Static Files

Collect static files for production:

```bash
python manage.py collectstatic
```

Static files (CSS, JavaScript, images) are served from:
- Development: `django_backend/e_ikiraro/static/`
- Production: `django_backend/static/` (after running collectstatic)

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. **ModuleNotFoundError: No module named 'decouple'**

**Solution:**
```bash
pip install python-decouple
```

#### 2. **ModuleNotFoundError: No module named 'PIL'**

**Solution:**
```bash
pip install Pillow
```

#### 3. **SECRET_KEY not found in environment**

**Issue:** `.env` file is missing or `SECRET_KEY` is not set.

**Solution:**
```bash
cp django_backend/.env.example django_backend/.env
# Edit .env and add your SECRET_KEY
```

Generate a secure SECRET_KEY:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### 4. **Database locked (sqlite3)**

**Issue:** Multiple processes trying to access the database.

**Solution:**
```bash
# Stop the development server and any other processes
# Then restart the server
python manage.py runserver
```

#### 5. **Email not sending**

**Issue:** Incorrect SMTP credentials or email configuration.

**Solution:**
- Verify `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD` in `.env`
- For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password
- Enable "Less secure app access" if not using App Passwords

#### 6. **Google OAuth not working**

**Issue:** `GOOGLE_CLIENT_ID` or `GOOGLE_CLIENT_SECRET` not set.

**Solution:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create an OAuth 2.0 credential (Web Application)
3. Add `http://localhost:8000/accounts/google/login/callback/` to Authorized redirect URIs
4. Copy Client ID and Client Secret to `.env`

#### 7. **Migrations not applying**

**Issue:** Migration conflicts or database schema issues.

**Solution:**
```bash
# Check migration status
python manage.py showmigrations

# Apply migrations
python manage.py migrate

# If there are conflicts, create a new migration
python manage.py makemigrations
python manage.py migrate
```

#### 8. **Static files not loading in development**

**Issue:** Static files configuration in `settings.py`.

**Solution:**
- Ensure `DEBUG = True` in `.env`
- Run `python manage.py collectstatic` if needed
- Check that static files URLs are configured in `urls.py`

### Getting Help

If you encounter issues:

1. Check Django documentation: https://docs.djangoproject.com/
2. Review django-allauth docs: https://django-allauth.readthedocs.io/
3. Check for error messages in the terminal or browser console
4. Review the GitHub issues page

## 📝 License

This project is open source. Please check the LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ✉️ Contact & Support

For questions or support:
- Email: support@e-ikiraro.bi
- Phone: +257 12 345 678

## 📚 Additional Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Pillow Image Processing](https://python-pillow.org/)

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
