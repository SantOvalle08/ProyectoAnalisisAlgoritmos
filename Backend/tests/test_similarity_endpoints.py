"""
Tests para Endpoints de API de Similitud
=========================================

Tests completos para todos los endpoints de similitud textual.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestCompareEndpoint:
    """Tests para /similarity/compare"""
    
    def test_compare_with_levenshtein(self):
        """Test básico de comparación con Levenshtein"""
        response = client.post("/api/v1/similarity/compare", json={
            "text1": "Generative AI in education",
            "text2": "Generative artificial intelligence in education",
            "algorithm": "levenshtein"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "similarity" in data
        assert "algorithm" in data
        assert "similarity_percentage" in data
        assert 0.0 <= data["similarity"] <= 1.0
        assert "Levenshtein" in data["algorithm"]
    
    def test_compare_with_tfidf(self):
        """Test de comparación con TF-IDF + Coseno"""
        response = client.post("/api/v1/similarity/compare", json={
            "text1": "Machine learning is a subset of artificial intelligence",
            "text2": "AI includes machine learning as a subdomain",
            "algorithm": "tfidf_cosine"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["similarity"] > 0.1  # TF-IDF puede dar valores más bajos con textos cortos
    
    def test_compare_with_jaccard(self):
        """Test de comparación con Jaccard"""
        response = client.post("/api/v1/similarity/compare", json={
            "text1": "apple orange banana",
            "text2": "apple orange grape",
            "algorithm": "jaccard"
        })
        
        assert response.status_code == 200
        data = response.json()
        # Jaccard = intersección/unión = 2/4 = 0.5
        assert 0.4 < data["similarity"] < 0.6
    
    def test_compare_with_ngram(self):
        """Test de comparación con N-gramas"""
        response = client.post("/api/v1/similarity/compare", json={
            "text1": "hello world",
            "text2": "hello world!",
            "algorithm": "ngram",
            "ngram_n": 3,
            "ngram_type": "char"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["similarity"] > 0.8  # Muy similares
    
    def test_compare_identical_texts(self):
        """Test con textos idénticos"""
        text = "This is a test text for similarity comparison"
        response = client.post("/api/v1/similarity/compare", json={
            "text1": text,
            "text2": text,
            "algorithm": "tfidf_cosine"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["similarity"] > 0.99  # Casi 1.0 para textos idénticos
    
    def test_compare_completely_different_texts(self):
        """Test con textos completamente diferentes"""
        response = client.post("/api/v1/similarity/compare", json={
            "text1": "apple banana cherry",
            "text2": "computer network database",
            "algorithm": "jaccard"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["similarity"] < 0.2  # Muy bajos para textos diferentes
    
    def test_compare_with_empty_text_fails(self):
        """Test que debe fallar con texto vacío"""
        response = client.post("/api/v1/similarity/compare", json={
            "text1": "",
            "text2": "some text",
            "algorithm": "levenshtein"
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_compare_with_invalid_algorithm_fails(self):
        """Test con algoritmo inválido"""
        response = client.post("/api/v1/similarity/compare", json={
            "text1": "text one",
            "text2": "text two",
            "algorithm": "invalid_algorithm"
        })
        
        assert response.status_code == 422  # Validation error


class TestCompareAllEndpoint:
    """Tests para /similarity/compare-all"""
    
    def test_compare_all_algorithms(self):
        """Test de comparación con todos los algoritmos"""
        response = client.post(
            "/api/v1/similarity/compare-all",
            json={
                "text1": "Generative AI transforms education",
                "text2": "Artificial intelligence changes learning"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verificar que retorna resultados para algoritmos clásicos
        assert "levenshtein" in data
        assert "tfidf_cosine" in data
        assert "jaccard" in data
        assert "ngram" in data
        
        # Verificar estructura de cada resultado
        for algo_result in data.values():
            if isinstance(algo_result, dict) and "similarity" in algo_result:
                assert 0.0 <= algo_result["similarity"] <= 1.0
                assert "algorithm" in algo_result
    
    def test_compare_all_with_identical_texts(self):
        """Test comparación con todos usando textos idénticos"""
        text = "Machine learning is amazing"
        response = client.post(
            "/api/v1/similarity/compare-all",
            json={"text1": text, "text2": text}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Todos los algoritmos deberían dar similitud muy alta
        for algo_name, algo_result in data.items():
            if isinstance(algo_result, dict) and "similarity" in algo_result:
                assert algo_result["similarity"] > 0.95


class TestAnalyzeEndpoint:
    """Tests para /similarity/analyze"""
    
    def test_analyze_with_levenshtein(self):
        """Test de análisis detallado con Levenshtein"""
        response = client.post("/api/v1/similarity/analyze", json={
            "text1": "hello",
            "text2": "hallo",
            "algorithm": "levenshtein"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "algorithm" in data
        # analyze_step_by_step returns nested structure with results
        assert "results" in data
        assert "similarity" in data["results"]
        assert "explanation" in data
    
    def test_analyze_with_tfidf(self):
        """Test de análisis detallado con TF-IDF"""
        response = client.post("/api/v1/similarity/analyze", json={
            "text1": "machine learning artificial intelligence",
            "text2": "AI and ML are related fields",
            "algorithm": "tfidf_cosine"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert "algorithm" in data
        assert "vectors" in data or "similarity" in data
    
    def test_analyze_fails_with_all_algorithm(self):
        """Test que debe fallar al usar 'all' en análisis"""
        response = client.post("/api/v1/similarity/analyze", json={
            "text1": "text one",
            "text2": "text two",
            "algorithm": "all"
        })
        
        assert response.status_code == 422  # Validation error


class TestBatchEndpoint:
    """Tests para /similarity/batch"""
    
    def test_batch_compare_multiple_pairs(self):
        """Test de comparación por lotes"""
        response = client.post("/api/v1/similarity/batch", json={
            "pairs": [
                {"text1": "hello world", "text2": "hello earth"},
                {"text1": "apple fruit", "text2": "orange fruit"},
                {"text1": "car vehicle", "text2": "automobile transportation"}
            ],
            "algorithm": "jaccard"
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 3
        for result in data:
            if isinstance(result, dict) and "similarity" in result:
                assert 0.0 <= result["similarity"] <= 1.0
    
    def test_batch_with_single_pair(self):
        """Test de batch con un solo par"""
        response = client.post("/api/v1/similarity/batch", json={
            "pairs": [
                {"text1": "test", "text2": "test"}
            ],
            "algorithm": "levenshtein"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["similarity"] > 0.99
    
    def test_batch_with_invalid_pair_format_fails(self):
        """Test que debe fallar con formato de par inválido"""
        response = client.post("/api/v1/similarity/batch", json={
            "pairs": [
                {"text1": "hello"}  # Falta text2
            ],
            "algorithm": "jaccard"
        })
        
        assert response.status_code == 422  # Validation error


class TestAlgorithmsEndpoint:
    """Tests para /similarity/algorithms"""
    
    def test_list_algorithms(self):
        """Test para listar algoritmos disponibles"""
        response = client.get("/api/v1/similarity/algorithms")
        
        assert response.status_code == 200
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) == 6  # 6 algoritmos
        
        # Verificar estructura de cada algoritmo
        algorithm_ids = set()
        for algo in data:
            assert "id" in algo
            assert "name" in algo
            assert "type" in algo
            assert "description" in algo
            assert "complexity" in algo
            assert "best_use_cases" in algo
            algorithm_ids.add(algo["id"])
        
        # Verificar que todos los algoritmos esperados están presentes
        expected_ids = {
            "levenshtein", "tfidf_cosine", "jaccard",
            "ngram", "bert", "sentence_bert"
        }
        assert expected_ids == algorithm_ids


class TestHealthEndpoint:
    """Tests para /similarity/health"""
    
    def test_health_check(self):
        """Test del health check"""
        response = client.get("/api/v1/similarity/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert "service" in data
        assert "algorithms_available" in data
        assert data["algorithms_available"] == 6


class TestParameterValidation:
    """Tests de validación de parámetros"""
    
    def test_ngram_with_custom_n(self):
        """Test con parámetro n personalizado para n-gramas"""
        response = client.post("/api/v1/similarity/compare", json={
            "text1": "testing ngrams",
            "text2": "testing bigrams",
            "algorithm": "ngram",
            "ngram_n": 2,
            "ngram_type": "word"
        })
        
        assert response.status_code == 200
    
    def test_tfidf_with_custom_max_features(self):
        """Test con max_features personalizado para TF-IDF"""
        response = client.post("/api/v1/similarity/compare", json={
            "text1": "machine learning deep learning neural networks",
            "text2": "artificial intelligence machine learning",
            "algorithm": "tfidf_cosine",
            "tfidf_max_features": 1000
        })
        
        assert response.status_code == 200
    
    def test_invalid_ngram_n_fails(self):
        """Test con n inválido para n-gramas"""
        response = client.post("/api/v1/similarity/compare", json={
            "text1": "test",
            "text2": "test",
            "algorithm": "ngram",
            "ngram_n": 0  # Inválido, debe ser >= 1
        })
        
        assert response.status_code == 422


# Tests de rendimiento básicos
class TestPerformance:
    """Tests básicos de rendimiento"""
    
    def test_compare_performance_is_reasonable(self):
        """Verificar que las comparaciones se completen en tiempo razonable"""
        import time
        
        text1 = "This is a longer text for performance testing " * 10
        text2 = "This is another longer text for testing performance " * 10
        
        start = time.time()
        response = client.post("/api/v1/similarity/compare", json={
            "text1": text1,
            "text2": text2,
            "algorithm": "tfidf_cosine"
        })
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 5.0  # Debería completarse en menos de 5 segundos
    
    def test_batch_performance(self):
        """Test de rendimiento de batch"""
        import time
        
        pairs = [
            {"text1": f"text number {i}", "text2": f"text number {i+1}"}
            for i in range(10)
        ]
        
        start = time.time()
        response = client.post("/api/v1/similarity/batch", json={
            "pairs": pairs,
            "algorithm": "jaccard"
        })
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 10.0  # 10 pares en menos de 10 segundos


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
