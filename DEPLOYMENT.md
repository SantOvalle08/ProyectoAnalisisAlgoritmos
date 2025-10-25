# 🚀 Plan de Deployment - Análisis Bibliométrico

## Resumen de lo Implementado

### ✅ Completado hasta ahora:
- **Paso 2**: Integración Backend-Frontend ✅
  - Servicios del frontend conectados con APIs reales
  - Documentación de integración completa
  - Script de inicio automatizado

- **Paso 1**: Pruebas de Integración ✅
  - Tests de similitud: 3/3 pasando
  - Tests de clustering: 10/10 pasando
  - Tests de frecuencia: Pendiente pero API funcional
  - Total: 13+ tests pasando

## 📋 Paso 3: Deployment y Documentación

### 3.1 Dockerización

#### Backend Dockerfile
```dockerfile
# Backend/Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Descargar modelos de NLP si es necesario
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile
```dockerfile
# Frontend/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Copiar package files
COPY package*.json ./
RUN npm ci

# Copiar código fuente
COPY . .

# Build
ENV VITE_API_URL=http://localhost:8000
RUN npm run build

# Production stage
FROM nginx:alpine

# Copiar build
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuración nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: ./Backend
    container_name: analisis-backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=info
    volumes:
      - ./Backend/data:/app/data
      - ./Backend/logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./Frontend
    container_name: analisis-frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  backend_data:
  backend_logs:
```

### 3.2 Configuración de Nginx

```nginx
# Frontend/nginx.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript 
               application/x-javascript application/xml+rss 
               application/javascript application/json;

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Proxy API requests to backend
    location /api/ {
        proxy_pass http://backend:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3.3 Variables de Entorno

#### Producción
```env
# Backend/.env.production
ENVIRONMENT=production
LOG_LEVEL=warning
CORS_ORIGINS=https://your-domain.com
MAX_DOWNLOAD_SIZE=10000
CACHE_TTL=3600
```

```env
# Frontend/.env.production
VITE_API_URL=https://api.your-domain.com
VITE_ENV=production
```

### 3.4 Scripts de Deployment

#### build.sh
```bash
#!/bin/bash
# Build script for deployment

echo "🏗️  Building project..."

# Build backend
echo "📦 Building backend..."
cd Backend
pip install -r requirements.txt
python -m pytest tests/ -v
cd ..

# Build frontend
echo "🎨 Building frontend..."
cd Frontend
npm ci
npm run build
cd ..

echo "✅ Build complete!"
```

#### deploy.sh
```bash
#!/bin/bash
# Deployment script

echo "🚀 Deploying application..."

# Stop existing containers
docker-compose down

# Build and start new containers
docker-compose up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services..."
sleep 10

# Check health
curl -f http://localhost:8000/health || exit 1
curl -f http://localhost || exit 1

echo "✅ Deployment successful!"
echo "📌 Backend: http://localhost:8000"
echo "📌 Frontend: http://localhost"
echo "📌 API Docs: http://localhost:8000/docs"
```

### 3.5 CI/CD con GitHub Actions

```.github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      
      - name: Install dependencies
        run: |
          cd Backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd Backend
          pytest tests/ -v
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Build frontend
        run: |
          cd Frontend
          npm ci
          npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to server
        run: |
          # Add your deployment commands here
          echo "Deploying to production..."
```

### 3.6 Documentación Final

#### README.md Principal
```markdown
# Sistema de Análisis Bibliométrico

Sistema completo para análisis bibliométrico con descarga automatizada,
análisis de similitud, frecuencias, clustering y visualizaciones.

## 🚀 Quick Start

### Con Docker (Recomendado)
\`\`\`bash
docker-compose up -d
\`\`\`

### Manual
\`\`\`bash
# Backend
cd Backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd Frontend
npm install
npm run dev
\`\`\`

## 📚 Documentación
- [Guía de Integración](./INTEGRACION.md)
- [Plan de Pruebas](./PRUEBAS_INTEGRACION.md)
- [Estado del Proyecto](./ESTADO_ACTUAL_PROYECTO.md)
- [API Documentation](http://localhost:8000/docs)

## 🧪 Tests
\`\`\`bash
cd Backend
pytest tests/ -v
\`\`\`

## 📊 Características
- ✅ Descarga multi-fuente (CrossRef, ACM, IEEE, etc.)
- ✅ 6 Algoritmos de similitud textual
- ✅ Análisis de frecuencias con TF-IDF
- ✅ Clustering jerárquico (Ward, Average, Complete)
- ✅ Visualizaciones interactivas (Word clouds, mapas, timelines)
- ✅ API REST completa con FastAPI
- ✅ Frontend moderno con React + TypeScript
- ✅ Documentación automática con Swagger/OpenAPI

## 👥 Autores
- Santiago Ovalle Cortés
- Juan Sebastián Noreña

## 📄 Licencia
MIT License
\`\`\`

### 3.7 Optimización

#### Frontend
- [ ] Code splitting
- [ ] Lazy loading de rutas
- [ ] Tree shaking
- [ ] Compresión de assets
- [ ] Service Worker para PWA

#### Backend
- [ ] Caché de resultados
- [ ] Rate limiting
- [ ] Compresión de respuestas
- [ ] Optimización de queries
- [ ] Connection pooling

### 3.8 Monitoring y Logs

#### Configuración de Logs
```python
# Backend/app/config/logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    
    # Console handler
    ch = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
```

## ✅ Checklist de Deployment

### Pre-deployment
- [ ] Todos los tests pasando
- [ ] Documentación actualizada
- [ ] Variables de entorno configuradas
- [ ] Secrets configurados
- [ ] Base de datos lista (si aplica)

### Deployment
- [ ] Dockerfiles creados
- [ ] docker-compose.yml configurado
- [ ] nginx configurado
- [ ] Build exitoso
- [ ] Health checks funcionando

### Post-deployment
- [ ] Verificar URLs funcionando
- [ ] Verificar logs sin errores
- [ ] Pruebas de carga
- [ ] Monitoreo activo
- [ ] Backups configurados

## 🎯 Próximos Pasos

1. **Crear Dockerfiles** ✅ (Documentado)
2. **Configurar docker-compose** ✅ (Documentado)
3. **Crear scripts de deployment** ✅ (Documentado)
4. **Configurar CI/CD** ✅ (Documentado)
5. **Documentación final** ✅ (Documentado)
6. **Testing en producción** ⏳ Pendiente
7. **Monitoreo y alertas** ⏳ Pendiente
8. **Optimizaciones** ⏳ Pendiente

## 📝 Notas

- Backend probado y funcional con 13+ tests pasando
- Frontend completamente integrado con backend
- Documentación completa de integración disponible
- Listo para deployment con Docker
