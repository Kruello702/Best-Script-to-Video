# Deployment Guide - Script to Video Generator

This guide provides step-by-step instructions for deploying the Script to Video Generator application in various environments.

## 🚀 Deployment Options

### 1. Local Development
Perfect for testing and development purposes.

### 2. Cloud Deployment
Production-ready deployment with scalability and reliability.

### 3. Docker Deployment
Containerized deployment for consistent environments.

## 📋 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / Windows 10+ / macOS 10.15+
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **Network**: Stable internet connection

### Software Dependencies
- **Python**: 3.11 or higher
- **Node.js**: 22.x or higher
- **pnpm**: Latest version
- **Git**: For version control

### Optional (for Azure features)
- **Azure Account**: With active subscription
- **Azure CLI**: For resource management

## 🔧 Local Development Setup

### Step 1: Clone and Setup Backend
```bash
# Navigate to backend directory
cd script-to-video-backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cat > .env << EOF
FLASK_ENV=development
FLASK_DEBUG=True
OPENAI_API_KEY=your_openai_key_here
EOF

# Start the backend server
python src/main.py
```

The backend will be available at: `http://localhost:5000`

### Step 2: Setup Frontend
```bash
# Navigate to frontend directory
cd script-to-video-frontend

# Install dependencies
pnpm install

# Start development server
pnpm run dev --host
```

The frontend will be available at: `http://localhost:5173`

### Step 3: Verify Installation
1. Open `http://localhost:5173` in your browser
2. Check that all three tabs load correctly
3. Test the interface components
4. Verify backend connectivity (may need troubleshooting)

## ☁️ Cloud Deployment

### Azure App Service Deployment

#### Backend Deployment
```bash
# Build the backend
cd script-to-video-backend

# Create deployment package
zip -r backend-deploy.zip . -x "venv/*" "__pycache__/*" "*.pyc"

# Deploy using Azure CLI
az webapp deploy --resource-group myResourceGroup \
                 --name myBackendApp \
                 --src-path backend-deploy.zip
```

#### Frontend Deployment
```bash
# Build the frontend
cd script-to-video-frontend
pnpm run build

# Deploy to Azure Static Web Apps
az staticwebapp deploy --name myFrontendApp \
                       --source-location ./dist \
                       --resource-group myResourceGroup
```

### AWS Deployment

#### Backend (Elastic Beanstalk)
```bash
# Install EB CLI
pip install awsebcli

# Initialize EB application
cd script-to-video-backend
eb init

# Create environment and deploy
eb create production
eb deploy
```

#### Frontend (S3 + CloudFront)
```bash
# Build the application
cd script-to-video-frontend
pnpm run build

# Deploy to S3
aws s3 sync ./dist s3://my-video-generator-bucket --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id ABCDEFGHIJK --paths "/*"
```

## 🐳 Docker Deployment

### Create Docker Files

#### Backend Dockerfile
```dockerfile
# script-to-video-backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY venv/ ./venv/

EXPOSE 5000

CMD ["python", "src/main.py"]
```

#### Frontend Dockerfile
```dockerfile
# script-to-video-frontend/Dockerfile
FROM node:22-alpine as builder

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

COPY . .
RUN pnpm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./script-to-video-backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data

  frontend:
    build: ./script-to-video-frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

### Deploy with Docker
```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Scale services
docker-compose up -d --scale backend=3
```

## 🔐 Production Configuration

### Environment Variables
```bash
# Backend (.env)
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Azure Configuration
AZURE_STORAGE_ACCOUNT_NAME=yourstorageaccount
AZURE_STORAGE_ACCOUNT_KEY=your-storage-key
AZURE_MEDIA_SERVICES_ACCOUNT=yourmediaaccount
AZURE_RESOURCE_GROUP=yourresourcegroup
AZURE_SUBSCRIPTION_ID=your-subscription-id

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=https://api.openai.com/v1
```

### Security Hardening
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Install SSL certificate (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### Performance Optimization
```bash
# Install and configure Nginx
sudo apt install nginx

# Configure reverse proxy
sudo nano /etc/nginx/sites-available/video-generator

# Enable site
sudo ln -s /etc/nginx/sites-available/video-generator /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

## 📊 Monitoring and Logging

### Application Monitoring
```bash
# Install monitoring tools
pip install prometheus-flask-exporter
npm install @sentry/react

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)
```

### Health Checks
```bash
# Backend health check
curl http://localhost:5000/health

# Frontend health check
curl http://localhost:3000/

# Database health check
curl http://localhost:5000/api/health/db
```

## 🔧 Troubleshooting

### Common Issues

#### Backend Not Starting
```bash
# Check Python version
python --version

# Check dependencies
pip list

# Check port availability
netstat -tulpn | grep :5000

# Check logs
tail -f /var/log/video-generator/backend.log
```

#### Frontend Build Errors
```bash
# Clear cache
pnpm store prune

# Reinstall dependencies
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Check Node version
node --version
```

#### Database Connection Issues
```bash
# Check database status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U username -d database_name

# Check connection string
echo $DATABASE_URL
```

### Performance Issues
```bash
# Monitor system resources
htop
iostat -x 1
free -h

# Check application metrics
curl http://localhost:5000/metrics

# Analyze logs
grep ERROR /var/log/video-generator/*.log
```

## 🔄 Maintenance

### Regular Updates
```bash
# Update backend dependencies
pip list --outdated
pip install -U package_name

# Update frontend dependencies
pnpm outdated
pnpm update

# Update system packages
sudo apt update && sudo apt upgrade
```

### Backup Strategy
```bash
# Database backup
pg_dump database_name > backup_$(date +%Y%m%d).sql

# Application backup
tar -czf app_backup_$(date +%Y%m%d).tar.gz /path/to/app

# Azure backup (if using Azure)
az storage blob upload-batch -d backups -s /local/backup/path
```

### Scaling Considerations
```bash
# Horizontal scaling with load balancer
# Add more backend instances
docker-compose up -d --scale backend=5

# Vertical scaling
# Increase server resources
# Optimize database queries
# Use caching (Redis)
```

## 📈 Performance Benchmarks

### Expected Performance
- **Video Generation**: 30-60 seconds for 10-second video
- **API Response Time**: < 200ms for most endpoints
- **Frontend Load Time**: < 3 seconds initial load
- **Concurrent Users**: 100+ with proper scaling

### Optimization Tips
1. **Use CDN** for static assets
2. **Enable gzip** compression
3. **Implement caching** for API responses
4. **Optimize images** and videos
5. **Use database indexing**
6. **Monitor and profile** regularly

## 🆘 Support and Maintenance

### Log Locations
- **Backend**: `/var/log/video-generator/backend.log`
- **Frontend**: Browser console and server logs
- **Nginx**: `/var/log/nginx/access.log`, `/var/log/nginx/error.log`
- **System**: `/var/log/syslog`

### Monitoring Endpoints
- **Health Check**: `GET /health`
- **Metrics**: `GET /metrics`
- **Status**: `GET /api/status`

### Emergency Procedures
1. **Service Down**: Restart services, check logs
2. **High Load**: Scale horizontally, check resources
3. **Database Issues**: Check connections, run diagnostics
4. **Security Incident**: Isolate, investigate, patch

---

**For additional support, please refer to the main README.md or contact the development team.**

