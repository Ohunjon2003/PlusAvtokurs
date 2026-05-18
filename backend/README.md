# PlusAvto.Uz Backend (Django + PostgreSQL)

## Setup

### 1. Requirements
- Python 3.10+
- PostgreSQL
- pip

### 2. Installation

```bash
# Clone repo
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy .env file
copy .env.example .env
# Edit .env with your database credentials
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb plusavto_db

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (for Django admin)
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata initial_data.json
```

### 4. Run Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Access:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

### 5. API Endpoints

#### Users
- `POST /api/users/login/` - Login
- `POST /api/users/register/` - Register
- `POST /api/users/reset_password/` - Reset password
- `GET /api/users/` - Get all users

#### Questions
- `GET /api/questions/` - Get all questions
- `GET /api/questions/by_category/?category=qoidalar` - Get questions by category

#### Test Results
- `GET /api/test-results/` - Get all results
- `GET /api/test-results/by_user/?userId=user_123` - Get user results
- `POST /api/test-results/` - Save test result

#### Categories
- `GET /api/categories/` - Get all categories

#### Other endpoints
- `/api/activity-logs/`
- `/api/chat-messages/`
- `/api/goals/`
- `/api/bookmarks/`
- `/api/study-materials/`
- `/api/notifications/`

## DigitalOcean Deployment

See DEPLOY_DIGITALOCEAN.md for production setup.
