"""
Tests para la API de Frequency Analysis (Requerimiento 3)
Verifica todos los endpoints de frequency analysis
"""

import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

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

print("\n" + "="*80)
print("INICIANDO TESTS DE API - FREQUENCY ANALYSIS")
print("="*80 + "\n")

# =============================================================================
# TEST 1: Health Check Endpoint
# =============================================================================
print("TEST 1: Health Check Endpoint")
print("-" * 80)

try:
    response = client.get("/api/v1/frequency/health")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    assert data["status"] == "healthy", f"Expected status 'healthy', got {data['status']}"
    assert "analyzer_initialized" in data, "Missing analyzer_initialized field"
    assert data["analyzer_initialized"] == True, "Analyzer should be initialized"
    
    print(f"Response Status: {response.status_code}")
    print(f"Status: {data['status']}")
    print(f"Analyzer Initialized: {data['analyzer_initialized']}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 2: Get Predefined Concepts Endpoint
# =============================================================================
print("TEST 2: Get Predefined Concepts Endpoint")
print("-" * 80)

try:
    response = client.get("/api/v1/frequency/predefined-concepts")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    # El endpoint retorna un diccionario con 3 categorías
    assert isinstance(data, dict), f"Expected dict, got {type(data)}"
    assert "generative_ai_education" in data, "Missing generative_ai_education category"
    assert "education_related" in data, "Missing education_related category"
    assert "ai_technical" in data, "Missing ai_technical category"
    
    # Verificar que generative_ai_education tiene la estructura correcta
    gen_ai_concepts = data["generative_ai_education"]
    assert "concepts" in gen_ai_concepts, "Missing concepts field"
    assert len(gen_ai_concepts["concepts"]) == 15, f"Expected 15 concepts, got {len(gen_ai_concepts['concepts'])}"
    
    print(f"Response Status: {response.status_code}")
    print(f"Categories: {list(data.keys())}")
    print(f"Generative AI Education Concepts: {len(gen_ai_concepts['concepts'])}")
    print(f"First 3 Concepts: {gen_ai_concepts['concepts'][:3]}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 3: Get Extraction Methods Endpoint
# =============================================================================
print("TEST 3: Get Extraction Methods Endpoint")
print("-" * 80)

try:
    response = client.get("/api/v1/frequency/extraction-methods")
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    # El endpoint retorna una lista de metodos directamente
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    assert len(data) == 3, f"Expected 3 methods, got {len(data)}"
    
    # Verificar que todos los metodos esten presentes
    method_names = [m["method"] for m in data]
    assert "tfidf" in method_names, "Missing tfidf method"
    assert "frequency" in method_names, "Missing frequency method"
    assert "combined" in method_names, "Missing combined method"
    
    print(f"Response Status: {response.status_code}")
    print(f"Available Methods: {method_names}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 4: Analyze Concepts Endpoint - Basic Test
# =============================================================================
print("TEST 4: Analyze Concepts Endpoint - Basic Test")
print("-" * 80)

try:
    request_data = {
        "abstracts": TEST_ABSTRACTS[:3],  # Solo primeros 3 abstracts
        "concepts": None  # Usar solo predefinidos
    }
    
    response = client.post("/api/v1/frequency/analyze-concepts", json=request_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    # El endpoint retorna un dict donde keys=conceptos, values=frecuencia_info
    assert isinstance(data, dict), f"Expected dict, got {type(data)}"
    
    # Verificar que hay conceptos encontrados
    assert len(data) > 0, "No concepts found"
    
    # Convertir a lista y ordenar por frecuencia
    concepts_list = [
        {
            "concept": concept_name,
            "frequency": concept_data["total_occurrences"],
            "document_frequency": concept_data["document_frequency"]
        }
        for concept_name, concept_data in data.items()
    ]
    top_concepts = sorted(concepts_list, key=lambda x: x["frequency"], reverse=True)[:3]
    
    print(f"Response Status: {response.status_code}")
    print(f"Concepts Found: {len(data)}")
    print(f"Top 3 Concepts:")
    for concept in top_concepts:
        print(f"  - {concept['concept']}: {concept['frequency']} occurrences, "
              f"{concept['document_frequency']} documents")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 5: Analyze Concepts with Custom Concepts
# =============================================================================
print("TEST 5: Analyze Concepts with Custom Concepts")
print("-" * 80)

try:
    request_data = {
        "abstracts": TEST_ABSTRACTS,
        "concepts": ["neural networks", "deep learning", "natural language processing"]
    }
    
    response = client.post("/api/v1/frequency/analyze-concepts", json=request_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    assert len(data) >= 3, "Custom concepts should be included"
    
    print(f"Response Status: {response.status_code}")
    print(f"Total Concepts Analyzed: {len(data)}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 6: Extract Keywords - TF-IDF Method
# =============================================================================
print("TEST 6: Extract Keywords - TF-IDF Method")
print("-" * 80)

try:
    request_data = {
        "abstracts": TEST_ABSTRACTS,
        "method": "tfidf",
        "max_keywords": 15
    }
    
    response = client.post("/api/v1/frequency/extract-keywords", json=request_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    # El endpoint retorna una lista directamente
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    assert len(data) == 15, f"Expected 15 keywords, got {len(data)}"
    
    # Verificar estructura de keywords
    for keyword in data[:3]:
        assert "keyword" in keyword, "Missing keyword field"
        assert "score" in keyword, "Missing score field"
        assert keyword["score"] > 0, "Score should be positive"
    
    print(f"Response Status: {response.status_code}")
    print(f"Total Keywords: {len(data)}")
    print(f"Top 5 Keywords: {[k['keyword'] for k in data[:5]]}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 7: Extract Keywords - Frequency Method
# =============================================================================
print("TEST 7: Extract Keywords - Frequency Method")
print("-" * 80)

try:
    request_data = {
        "abstracts": TEST_ABSTRACTS,
        "method": "frequency",
        "max_keywords": 10
    }
    
    response = client.post("/api/v1/frequency/extract-keywords", json=request_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    assert len(data) == 10, f"Expected 10 keywords, got {len(data)}"
    
    print(f"Response Status: {response.status_code}")
    print(f"Total Keywords: {len(data)}")
    print(f"Top 5 Keywords: {[k['keyword'] for k in data[:5]]}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 8: Extract Keywords - Combined Method
# =============================================================================
print("TEST 8: Extract Keywords - Combined Method")
print("-" * 80)

try:
    request_data = {
        "abstracts": TEST_ABSTRACTS,
        "method": "combined",
        "max_keywords": 20
    }
    
    response = client.post("/api/v1/frequency/extract-keywords", json=request_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"
    assert len(data) == 20, f"Expected 20 keywords, got {len(data)}"
    
    print(f"Response Status: {response.status_code}")
    print(f"Total Keywords: {len(data)}")
    print(f"Top 5 Keywords: {[k['keyword'] for k in data[:5]]}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 9: Precision Analysis Endpoint
# =============================================================================
print("TEST 9: Precision Analysis Endpoint")
print("-" * 80)

try:
    request_data = {
        "abstracts": EXTENDED_ABSTRACTS,
        "predefined_concepts": None,
        "max_keywords": 20,
        "extraction_method": "tfidf",
        "precision_threshold": 0.7
    }
    
    response = client.post("/api/v1/frequency/precision-analysis", json=request_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    assert "precision" in data, "Missing precision field"
    assert "recall" in data, "Missing recall field"
    assert "f1_score" in data, "Missing f1_score field"
    assert "exact_matches" in data, "Missing exact_matches field"
    assert "total_extracted" in data, "Missing total_extracted field"
    assert "total_predefined" in data, "Missing total_predefined field"
    
    # Verificar que las metricas esten en rango valido
    assert 0 <= data["precision"] <= 1, f"Precision out of range: {data['precision']}"
    assert 0 <= data["recall"] <= 1, f"Recall out of range: {data['recall']}"
    assert 0 <= data["f1_score"] <= 1, f"F1 score out of range: {data['f1_score']}"
    
    print(f"Response Status: {response.status_code}")
    print(f"Precision: {data['precision']:.4f}")
    print(f"Recall: {data['recall']:.4f}")
    print(f"F1 Score: {data['f1_score']:.4f}")
    print(f"Exact Matches: {len(data['exact_matches'])}")
    print(f"Total Extracted: {data['total_extracted']}")
    print(f"Total Predefined: {data['total_predefined']}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 10: Full Report Endpoint
# =============================================================================
print("TEST 10: Full Report Endpoint")
print("-" * 80)

try:
    request_data = {
        "abstracts": EXTENDED_ABSTRACTS,
        "predefined_concepts": None,
        "max_keywords": 15
    }
    
    response = client.post("/api/v1/frequency/full-report", json=request_data)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    
    data = response.json()
    
    # Verificar estructura del reporte
    assert "corpus_statistics" in data, "Missing corpus_statistics section"
    assert "predefined_concepts" in data, "Missing predefined_concepts section"
    assert "extracted_keywords" in data, "Missing extracted_keywords section"
    assert "precision_metrics" in data, "Missing precision_metrics section"
    
    # Verificar corpus_statistics
    corpus_stats = data["corpus_statistics"]
    assert "total_abstracts" in corpus_stats, "Missing total_abstracts in corpus_statistics"
    assert corpus_stats["total_abstracts"] == len(EXTENDED_ABSTRACTS), "Incorrect abstract count"
    assert "total_words" in corpus_stats, "Missing total_words in corpus_statistics"
    assert "unique_words" in corpus_stats, "Missing unique_words in corpus_statistics"
    
    # Verificar predefined_concepts
    predefined_concepts = data["predefined_concepts"]
    assert len(predefined_concepts) > 0, "No predefined concepts found"
    
    # Verificar extracted_keywords
    extracted_keywords = data["extracted_keywords"]
    assert len(extracted_keywords) == 15, f"Expected 15 keywords, got {len(extracted_keywords)}"
    
    # Verificar precision_metrics
    precision_metrics = data["precision_metrics"]
    assert "precision" in precision_metrics, "Missing precision"
    assert "recall" in precision_metrics, "Missing recall"
    assert "f1_score" in precision_metrics, "Missing f1_score"
    
    print(f"Response Status: {response.status_code}")
    print(f"\nCorpus Statistics:")
    print(f"  - Abstracts: {corpus_stats['total_abstracts']}")
    print(f"  - Total Words: {corpus_stats['total_words']}")
    print(f"  - Unique Words: {corpus_stats['unique_words']}")
    print(f"\nPredefined Concepts:")
    print(f"  - Concepts Found: {len(predefined_concepts)}")
    print(f"\nExtracted Keywords:")
    print(f"  - Keywords: {len(extracted_keywords)}")
    print(f"\nPrecision Metrics:")
    print(f"  - Precision: {precision_metrics['precision']:.4f}")
    print(f"  - Recall: {precision_metrics['recall']:.4f}")
    print(f"  - F1 Score: {precision_metrics['f1_score']:.4f}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 11: Error Handling - Empty Abstracts
# =============================================================================
print("TEST 11: Error Handling - Empty Abstracts")
print("-" * 80)

try:
    request_data = {
        "abstracts": [],
        "concepts": None
    }
    
    response = client.post("/api/v1/frequency/analyze-concepts", json=request_data)
    assert response.status_code == 422, f"Expected status 422 for empty abstracts, got {response.status_code}"
    
    print(f"Response Status: {response.status_code}")
    print("Error correctly handled for empty abstracts")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 12: Error Handling - Invalid Extraction Method
# =============================================================================
print("TEST 12: Error Handling - Invalid Extraction Method")
print("-" * 80)

try:
    request_data = {
        "abstracts": TEST_ABSTRACTS,
        "method": "invalid_method",  # Metodo invalido
        "top_n": 10
    }
    
    response = client.post("/api/v1/frequency/extract-keywords", json=request_data)
    assert response.status_code == 422, f"Expected status 422 for invalid method, got {response.status_code}"
    
    print(f"Response Status: {response.status_code}")
    print("Error correctly handled for invalid extraction method")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("\n" + "="*80)
print("RESUMEN DE TESTS - API FREQUENCY ANALYSIS")
print("="*80)
print("\nTODOS LOS TESTS HAN SIDO EJECUTADOS")
print("\nEndpoints probados:")
print("  1. GET  /api/v1/frequency/health")
print("  2. GET  /api/v1/frequency/predefined-concepts")
print("  3. GET  /api/v1/frequency/extraction-methods")
print("  4. POST /api/v1/frequency/analyze-concepts")
print("  5. POST /api/v1/frequency/extract-keywords")
print("  6. POST /api/v1/frequency/precision-analysis")
print("  7. POST /api/v1/frequency/full-report")
print("\nFuncionalidades validadas:")
print("  - Analisis de conceptos predefinidos")
print("  - Analisis con conceptos personalizados")
print("  - Extraccion de keywords con TF-IDF")
print("  - Extraccion de keywords por frecuencia")
print("  - Extraccion combinada de keywords")
print("  - Calculo de metricas de precision")
print("  - Generacion de reportes completos")
print("  - Manejo de errores")
print("="*80 + "\n")
