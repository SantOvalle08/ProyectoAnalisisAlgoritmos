"""
Tests para la API de Frequency Analysis (Requerimiento 3)
Verifica todos los endpoints de frequency analysis
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# Cliente de prueba
client = TestClient(app)

# Datos de prueba - abstracts simulados sobre IA generativa en educacion
TEST_ABSTRACTS = [
    "Generative models have revolutionized education by enabling personalized learning experiences. "
    "Machine learning algorithms can adapt to student needs, while fine-tuning helps customize AI systems. "
    "However, algorithmic bias remains a concern in educational AI applications.",
    
    "Prompting techniques are essential for effective human-AI interaction in educational contexts. "
    "Students must develop AI literacy to understand how generative models work. "
    "Transparency and explainability are crucial for building trust in AI-powered learning tools.",
    
    "Training data quality significantly impacts the performance of educational AI systems. "
    "Privacy concerns arise when collecting student data for machine learning models. "
    "Ethics must guide the development and deployment of generative AI in education.",
    
    "Multimodality enables richer learning experiences by combining text, images, and audio. "
    "Co-creation between students and AI fosters creativity and deeper understanding. "
    "Personalization through generative models can enhance student engagement and outcomes.",
    
    "Fine-tuning pre-trained models for educational applications requires careful consideration. "
    "AI literacy programs help students and teachers understand generative AI capabilities. "
    "Transparency in AI decision-making builds confidence in educational technology."
]

# Datos de prueba - abstracts adicionales para precision analysis
EXTENDED_ABSTRACTS = TEST_ABSTRACTS + [
    "The integration of generative AI in educational settings demands careful attention to ethics and privacy. "
    "Machine learning models must be explainable to gain acceptance from educators and students.",
    
    "Human-AI interaction patterns in education reveal the importance of intuitive interfaces. "
    "Prompting strategies can significantly improve student outcomes when using generative models.",
]


# =============================================================================
# TESTS
# =============================================================================

def test_01_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/frequency/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "analyzer_initialized" in data
    assert data["analyzer_initialized"] == True


def test_02_get_predefined_concepts():
    """Test getting predefined concepts"""
    response = client.get("/api/v1/frequency/predefined-concepts")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "generative_ai_education" in data
    assert "education_related" in data
    assert "ai_technical" in data
    
    gen_ai_concepts = data["generative_ai_education"]
    assert "concepts" in gen_ai_concepts
    assert len(gen_ai_concepts["concepts"]) == 15


def test_03_get_extraction_methods():
    """Test getting available extraction methods"""
    response = client.get("/api/v1/frequency/extraction-methods")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    
    method_names = [m["method"] for m in data]
    assert "tfidf" in method_names
    assert "frequency" in method_names
    assert "combined" in method_names


def test_04_analyze_concepts_basic():
    """Test basic concept analysis with predefined concepts"""
    request_data = {
        "abstracts": TEST_ABSTRACTS[:3],
        "concepts": None
    }
    
    response = client.post("/api/v1/frequency/analyze-concepts", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_05_analyze_concepts_custom():
    """Test concept analysis with custom concepts"""
    request_data = {
        "abstracts": TEST_ABSTRACTS,
        "concepts": ["neural networks", "deep learning", "natural language processing"]
    }
    
    response = client.post("/api/v1/frequency/analyze-concepts", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) >= 3


def test_06_extract_keywords_tfidf():
    """Test keyword extraction using TF-IDF method"""
    request_data = {
        "abstracts": TEST_ABSTRACTS,
        "method": "tfidf",
        "max_keywords": 15
    }
    
    response = client.post("/api/v1/frequency/extract-keywords", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 15
    
    for keyword in data[:3]:
        assert "keyword" in keyword
        assert "score" in keyword
        assert keyword["score"] > 0


def test_07_extract_keywords_frequency():
    """Test keyword extraction using frequency method"""
    request_data = {
        "abstracts": TEST_ABSTRACTS,
        "method": "frequency",
        "max_keywords": 10
    }
    
    response = client.post("/api/v1/frequency/extract-keywords", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10


def test_08_extract_keywords_combined():
    """Test keyword extraction using combined method"""
    request_data = {
        "abstracts": TEST_ABSTRACTS,
        "method": "combined",
        "max_keywords": 20
    }
    
    response = client.post("/api/v1/frequency/extract-keywords", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 20


def test_09_precision_analysis():
    """Test precision analysis of extracted keywords"""
    request_data = {
        "abstracts": EXTENDED_ABSTRACTS,
        "predefined_concepts": None,
        "max_keywords": 20,
        "extraction_method": "tfidf",
        "precision_threshold": 0.7
    }
    
    response = client.post("/api/v1/frequency/precision-analysis", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "precision" in data
    assert "recall" in data
    assert "f1_score" in data
    assert "exact_matches" in data
    assert "total_extracted" in data
    assert "total_predefined" in data
    
    assert 0 <= data["precision"] <= 1
    assert 0 <= data["recall"] <= 1
    assert 0 <= data["f1_score"] <= 1


def test_10_full_report():
    """Test full frequency analysis report generation"""
    request_data = {
        "abstracts": EXTENDED_ABSTRACTS,
        "predefined_concepts": None,
        "max_keywords": 15
    }
    
    response = client.post("/api/v1/frequency/full-report", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    
    assert "corpus_statistics" in data
    assert "predefined_concepts" in data
    assert "extracted_keywords" in data
    assert "precision_metrics" in data
    
    corpus_stats = data["corpus_statistics"]
    assert "total_abstracts" in corpus_stats
    assert corpus_stats["total_abstracts"] == len(EXTENDED_ABSTRACTS)
    assert "total_words" in corpus_stats
    assert "unique_words" in corpus_stats
    
    predefined_concepts = data["predefined_concepts"]
    assert len(predefined_concepts) > 0
    
    extracted_keywords = data["extracted_keywords"]
    assert len(extracted_keywords) == 15
    
    precision_metrics = data["precision_metrics"]
    assert "precision" in precision_metrics
    assert "recall" in precision_metrics
    assert "f1_score" in precision_metrics


def test_11_error_empty_abstracts():
    """Test error handling for empty abstracts"""
    request_data = {
        "abstracts": [],
        "concepts": None
    }
    
    response = client.post("/api/v1/frequency/analyze-concepts", json=request_data)
    assert response.status_code == 422


def test_12_error_invalid_method():
    """Test error handling for invalid extraction method"""
    request_data = {
        "abstracts": TEST_ABSTRACTS,
        "method": "invalid_method",
        "max_keywords": 10
    }
    
    response = client.post("/api/v1/frequency/extract-keywords", json=request_data)
    assert response.status_code == 422
