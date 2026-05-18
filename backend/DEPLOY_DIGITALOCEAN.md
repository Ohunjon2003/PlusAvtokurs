# DigitalOcean Deployment Guide

## Step 1: Create DigitalOcean Droplet

1. Create a new Ubuntu 22.04 LTS droplet (minimum $6/month)
2. SSH into your droplet

## Step 2: Install Dependencies

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Step 3: Setup PostgreSQL

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE plusavto_db;
CREATE USER plusavto_user WITH PASSWORD 'your_secure_password';
ALTER ROLE plusavto_user SET client_encoding TO 'utf8';
ALTER ROLE plusavto_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE plusavto_user SET default_transaction_deferrable TO on;
ALTER ROLE plusavto_user SET default_transaction_level TO 'read committed';
ALTER ROLE plusavto_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE plusavto_db TO plusavto_user;
\q
```

## Step 4: Setup Django Application

```bash
cd /home/your_user

# Clone repository (or upload your code)
git clone <your_repo_url> plusavto-backend
cd plusavto-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
SECRET_KEY=your_secure_secret_key_here
DEBUG=False
ALLOWED_HOSTS=your_domain.com,www.your_domain.com,your_droplet_ip
DB_NAME=plusavto_db
DB_USER=plusavto_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://your_domain.com,https://www.your_domain.com
EOF

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Step 5: Setup Gunicorn

```bash
pip install gunicorn

# Create systemd service
sudo cat > /etc/systemd/system/plusavto.service << EOF
[Unit]
Description=PlusAvto Django Application
After=network.target

[Service]
User=your_user
WorkingDirectory=/home/your_user/plusavto-backend
ExecStart=/home/your_user/plusavto-backend/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Enable service
sudo systemctl enable plusavto
sudo systemctl start plusavto
```

## Step 6: Setup Nginx

```bash
# Create Nginx config
sudo cat > /etc/nginx/sites-available/plusavto << 'EOF'
upstream plusavto {
    server unix:/run/gunicorn.sock;
}

server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

    location /static/ {
        alias /home/your_user/plusavto-backend/staticfiles/;
    }

    location /media/ {
        alias /home/your_user/plusavto-backend/media/;
    }

    location / {
        proxy_pass http://plusavto;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/plusavto /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## Step 7: SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d your_domain.com -d www.your_domain.com

# Update Nginx config (auto-handled by certbot)
sudo certbot --nginx -d your_domain.com -d www.your_domain.com
```

## Step 8: Setup pgAdmin (Optional)

```bash
# pgAdmin installation on DigitalOcean
pip install pgadmin4

# Access at: http://your_domain.com:5050
# Create account on first login
```

## Step 9: Database Backups

```bash
# Create backup script
cat > /home/your_user/backup_db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/your_user/backups"
mkdir -p $BACKUP_DIR
pg_dump -U plusavto_user -d plusavto_db > $BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql
EOF

chmod +x /home/your_user/backup_db.sh

# Add to crontab for daily backups
crontab -e
# Add line: 0 2 * * * /home/your_user/backup_db.sh
```

## Step 10: Firewall Setup (Optional)

```bash
# Enable UFW
sudo ufw enable

# Allow SSH, HTTP, HTTPS
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
```

## Monitoring

Check service status:
```bash
sudo systemctl status plusavto
sudo systemctl status nginx

# View logs
sudo journalctl -u plusavto -f
sudo tail -f /var/log/nginx/error.log
```

## API Access

- Backend API: https://your_domain.com/api/
- Admin Panel: https://your_domain.com/admin/
- pgAdmin: https://your_domain.com:5050/ (if configured)

## Troubleshooting

If port 8000 is busy:
```bash
sudo fuser -k 8000/tcp
```

Restart all services:
```bash
sudo systemctl restart postgresql
sudo systemctl restart plusavto
sudo systemctl restart nginx
```
