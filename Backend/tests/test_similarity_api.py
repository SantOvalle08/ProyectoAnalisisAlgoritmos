"""
Tests para la API de Similitud (tests antiguos actualizados)
"""
import pytest
import sys
from pathlib import Path

# Ensure Backend folder is on sys.path so 'app' package is importable
backend_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_similarity_tfidf():
    """Test de similitud con TF-IDF usando nuevo endpoint"""
    payload = {
        "text1": "Generative AI in education",
        "text2": "Generative artificial intelligence applied to education",
        "algorithm": "tfidf_cosine"
    }

    r = client.post("/api/v1/similarity/compare", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert 'similarity' in body
    assert 0.0 <= body['similarity'] <= 1.0


def test_similarity_levenshtein():
    """Test de similitud con Levenshtein usando nuevo endpoint"""
    payload = {
        "text1": "abc",
        "text2": "abcd",
        "algorithm": "levenshtein"
    }
    r = client.post("/api/v1/similarity/compare", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "Levenshtein" in body['algorithm']
    assert 0.0 <= body['similarity'] <= 1.0


def test_similarity_sentence_bert_fallback():
    """Test de similitud con Sentence-BERT"""
    payload = {
        "text1": "Hello world",
        "text2": "Hello",
        "algorithm": "sentence_bert"
    }
    r = client.post("/api/v1/similarity/compare", json=payload)

    # Should return 200 with valid similarity
    assert r.status_code == 200
    body = r.json()
    assert 'similarity' in body
    assert 0.0 <= body['similarity'] <= 1.0
