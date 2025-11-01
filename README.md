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
