# PowerShell deployment script for Windows

Write-Host "🚀 Deploying BiblioAnalysis..." -ForegroundColor Green

# Stop existing containers
Write-Host "⏹️  Stopping existing containers..." -ForegroundColor Yellow
docker-compose down

# Build and start
Write-Host "🏗️  Building Docker images..." -ForegroundColor Cyan
docker-compose build --no-cache

Write-Host "▶️  Starting containers..." -ForegroundColor Cyan
docker-compose up -d

# Wait for services to be healthy
Write-Host "⏳ Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check health
Write-Host "🏥 Checking service health..." -ForegroundColor Cyan
docker-compose ps

# Test backend
Write-Host "🧪 Testing backend..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
    Write-Host "✅ Backend is healthy" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend health check failed" -ForegroundColor Red
}

# Test frontend
Write-Host "🧪 Testing frontend..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost/" -UseBasicParsing
    Write-Host "✅ Frontend is healthy" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Frontend health check failed" -ForegroundColor Red
}

# Show logs
Write-Host "📋 Recent logs:" -ForegroundColor Cyan
docker-compose logs --tail=50

Write-Host "`n✅ Deployment completed!" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
