#!/bin/bash

echo "🚀 Deploying BiblioAnalysis..."

# Stop existing containers
echo "⏹️  Stopping existing containers..."
docker-compose down

# Build and start
echo "🏗️  Building Docker images..."
docker-compose build --no-cache

echo "▶️  Starting containers..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check health
echo "🏥 Checking service health..."
docker-compose ps

# Test backend
echo "🧪 Testing backend..."
curl -f http://localhost:8000/health || echo "⚠️  Backend health check failed"

# Test frontend
echo "🧪 Testing frontend..."
curl -f http://localhost/ || echo "⚠️  Frontend health check failed"

# Show logs
echo "📋 Recent logs:"
docker-compose logs --tail=50

echo "✅ Deployment completed!"
echo "🌐 Frontend: http://localhost"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
