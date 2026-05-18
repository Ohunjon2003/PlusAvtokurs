# ⚡ Quick Start

## 🚀 Fastest Way to Get Running (5 minutes)

### With Docker (Easiest)

```bash
# 1. Install Docker Desktop
# https://www.docker.com/products/docker-desktop

# 2. Start everything
docker-compose up

# 3. In new terminal - Setup database
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# 4. Access
# Frontend: http://localhost:5173
# API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
# Database UI: http://localhost:5050
```

### Without Docker (Local)

```bash
# 1. Install PostgreSQL
# Windows: https://www.postgresql.org/download/windows/
# Mac: brew install postgresql@15
# Linux: sudo apt install postgresql

# 2. Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows or source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env - set DB credentials
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# 3. Frontend (new terminal)
cd PlusAvto.Uz
npm install
npm run dev

# 4. Access
# http://localhost:5173 - Frontend
# http://localhost:8000/api/ - API
# http://localhost:8000/admin/ - Admin
```

## 🔗 API Endpoints

### Login
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"name":"admin","password":"admin"}'
```

### Get Questions
```bash
curl http://localhost:8000/api/questions/
```

### Get Questions by Category
```bash
curl "http://localhost:8000/api/questions/by_category/?category=qoidalar"
```

### Save Test Result
```bash
curl -X POST http://localhost:8000/api/test-results/ \
  -H "Content-Type: application/json" \
  -d '{
    "id": "result_123",
    "userId": "user_123",
    "testDate": "2024-01-01T10:00:00Z",
    "score": 85,
    "totalQuestions": 100,
    "category": "qoidalar",
    "answers": {"q1": "A", "q2": "B"}
  }'
```

## 📊 Admin Panel

- URL: http://localhost:8000/admin/
- Default: admin / admin (change after first login!)

## 🗄️ Database

### pgAdmin (if using Docker)
- URL: http://localhost:5050
- Email: admin@admin.com
- Password: admin

### Command Line
```bash
# Connect to database
psql -U postgres -d plusavto_db

# List tables
\dt

# Exit
\q
```

## 🐛 Troubleshooting

### Can't connect to database
```bash
# Check PostgreSQL is running
# Windows: Services → PostgreSQL
# Mac: brew services list
# Linux: sudo systemctl status postgresql
```

### Port 8000 is busy
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

### Dependencies issue
```bash
# Backend
pip install --upgrade -r requirements.txt

# Frontend
rm -rf node_modules package-lock.json
npm install
```

## 📝 Next Steps

1. ✅ Get it running locally
2. 📖 Read SETUP_GUIDE.md for detailed setup
3. 🌐 Read backend/DEPLOY_DIGITALOCEAN.md for production
4. 🔧 Customize data/questions
5. 🚀 Deploy to DigitalOcean

## 💡 Tips

- Use pgAdmin to manage database visually
- Use Django admin panel to add questions/categories
- Use Postman to test API endpoints
- Check console for errors: `docker-compose logs -f`
- Data persists in Docker volumes even after `docker-compose down`

---

Need help? Check error messages in logs or ask in the setup guide!
