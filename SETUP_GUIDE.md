# PlusAvto.Uz - Complete Setup Guide

Loyihani Postgres + Django + React orqali o'z serveriga o'tkazishning to'liq qo'llanmasi.

## 📋 Loyiha Struktura

```
PlusAvtoKurs/
├── backend/              # Django API Server
│   ├── config/          # Django settings
│   ├── api/             # API app
│   ├── manage.py
│   └── requirements.txt
├── PlusAvto.Uz/         # React Frontend
│   ├── src/
│   ├── api/
│   │   ├── api.ts       # Django API integration
│   │   └── bot.js
│   ├── .env.example
│   └── package.json
└── docker-compose.yml   # Local dev setup
```

## 🚀 Option 1: Local Setup (Windows/Mac/Linux)

### Step 1: PostgreSQL Installation

**Windows:**
- Download: https://www.postgresql.org/download/windows/
- Install with pgAdmin4 ✅
- Remember password

**Mac:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux:**
```bash
sudo apt install postgresql postgresql-contrib
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env with database credentials
# DB_NAME=plusavto_db
# DB_USER=postgres
# DB_PASSWORD=your_password
```

### Step 3: Database Setup

```bash
# Enter PostgreSQL
psql -U postgres

# Run these commands:
CREATE DATABASE plusavto_db;
CREATE USER plusavto_user WITH PASSWORD 'your_password';
ALTER ROLE plusavto_user SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE plusavto_db TO plusavto_user;
\q

# Back to terminal - Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Username: admin
# Password: (set any password)
# Email: admin@admin.com
```

### Step 4: Run Backend

```bash
python manage.py runserver 0.0.0.0:8000
```

Access:
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/ (login with superuser)

### Step 5: Frontend Setup

```bash
cd PlusAvto.Uz

# Copy .env
copy .env.example .env

# Install dependencies
npm install

# Run frontend
npm run dev
```

Access: http://localhost:5173

---

## 🐳 Option 2: Docker Setup (Recommended for DigitalOcean)

### Prerequisites
- Install Docker: https://www.docker.com/
- Install Docker Compose

### Run Everything

```bash
# From root directory (PlusAvtoKurs/)
docker-compose up

# First time setup (in another terminal)
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- pgAdmin: http://localhost:5050/ (admin@admin.com / admin)

### Stop everything
```bash
docker-compose down
```

---

## 🌐 DigitalOcean Deployment

See `backend/DEPLOY_DIGITALOCEAN.md` for production setup.

### Quick Overview
1. Create Ubuntu 22.04 Droplet
2. Install Python, PostgreSQL, Nginx
3. Clone repo and setup Django
4. Configure Gunicorn + Nginx
5. Setup SSL with Let's Encrypt
6. Deploy React frontend to Vercel or same server

---

## 📝 Database Schema

### Main Tables
- **custom_users** - User accounts
- **categories** - Question categories
- **questions** - Quiz questions
- **test_results** - User test scores
- **activity_logs** - User actions
- **chat_messages** - Chat data
- **user_goals** - User goals
- **bookmarks** - Saved questions
- **study_materials** - Learning materials
- **notifications** - User notifications

### pgAdmin Access
- URL: http://localhost:5050
- Email: admin@admin.com
- Password: admin

Add new server in pgAdmin:
- Hostname: postgres (or localhost)
- Port: 5432
- Username: postgres
- Password: postgres

---

## 🔌 API Integration

Frontend uses new `api/api.ts` file instead of localStorage.

### Example Usage in React

```typescript
import { usersApi, questionsApi, testResultsApi } from './api/api';

// Login
const loginUser = async () => {
  const result = await usersApi.login('username', 'password');
  if (result.data) {
    console.log('Logged in:', result.data);
  }
};

// Get questions
const getQuestions = async () => {
  const result = await questionsApi.getByCategory('qoidalar');
  console.log('Questions:', result.data);
};

// Save test result
const saveResult = async () => {
  const result = await testResultsApi.create({
    userId: 'user_123',
    testDate: new Date().toISOString(),
    score: 85,
    totalQuestions: 100,
    category: 'qoidalar',
    answers: { q1: 'A', q2: 'B' }
  });
};
```

---

## 🔒 Environment Variables

### Backend (.env)

```env
SECRET_KEY=django-insecure-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=plusavto_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### Production (.env)

```env
SECRET_KEY=very-long-random-string-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DB_NAME=plusavto_db
DB_USER=plusavto_user
DB_PASSWORD=very-strong-password
DB_HOST=db-server-ip
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

---

## 🐛 Common Issues

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error
```bash
# Check PostgreSQL is running
# Windows: Services.msc → PostgreSQL → start
# Mac: brew services start postgresql@15
# Linux: sudo systemctl start postgresql
```

### CORS Error
- Check `CORS_ALLOWED_ORIGINS` in backend .env
- Restart backend after changing .env

### Migration Errors
```bash
# Reset database (development only)
python manage.py flush
python manage.py migrate
```

---

## 📊 Admin Panel Features

Access: http://localhost:8000/admin/

- Manage users
- Add/edit questions
- View test results
- See activity logs
- Manage categories
- Create notifications

---

## 🔄 Data Migration from localStorage

When switching from localhost to backend:

```python
# In Django shell: python manage.py shell

from api.models import Question, Category, CustomUser

# Import old data from localStorage export
# Then create models in Django

# Example:
cat = Category.objects.create(
    id='qoidalar',
    nameUz='Harakatlanish Qoidalari',
    emoji='📖',
    color='from-cyan-400 to-violet-600',
    order=2
)
```

---

## 📞 Support

For issues:
1. Check logs: `docker-compose logs backend`
2. Check database: Use pgAdmin
3. Check API: Use Postman or curl
4. Check network: Browser DevTools → Network tab

---

## Next Steps

✅ Local testing complete?
1. Deploy to DigitalOcean (see DEPLOY_DIGITALOCEAN.md)
2. Setup domain + SSL
3. Configure pgAdmin backup script
4. Deploy React to Vercel/Netlify or same server
5. Monitor logs and performance
