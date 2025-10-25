#!/bin/bash

echo "🔨 Building BiblioAnalysis Project..."

# Backend
echo "📦 Building Backend..."
cd Backend
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

# Run backend tests
echo "🧪 Running Backend Tests..."
pytest tests/ -v
if [ $? -ne 0 ]; then
    echo "❌ Backend tests failed!"
    exit 1
fi

cd ..

# Frontend
echo "📦 Building Frontend..."
cd Frontend
npm ci
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed!"
    exit 1
fi

cd ..

echo "✅ Build completed successfully!"
