"""
Tests de API REST para Clustering Jerárquico
============================================

Tests completos de los endpoints de clustering jerárquico.

Requerimiento 4: Clustering Jerárquico
API Testing

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
"""

import sys
import os
import requests
import json
from time import sleep
from typing import Dict, Any

# Configurar path para imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Configuración
BASE_URL = "http://127.0.0.1:8000"
API_PREFIX = "/api/v1/clustering"

# Datos de prueba: 10 abstracts sobre IA Generativa
TEST_ABSTRACTS = [
    "Generative AI models such as GPT-4 enable personalized learning experiences through adaptive content generation and real-time feedback mechanisms.",
    "Machine learning algorithms can analyze student performance data to create customized educational pathways that enhance engagement and retention.",
    "The integration of chatbots powered by large language models transforms traditional classroom interactions by providing 24/7 tutoring support.",
    "Natural language processing techniques allow automated essay grading with high accuracy, reducing teacher workload while maintaining educational standards.",
    "Educational technology platforms leverage generative models to produce interactive simulations that make complex concepts more accessible to learners.",
    "Privacy concerns arise when implementing AI systems in schools, requiring careful consideration of data protection and student consent policies.",
    "Automated content creation tools help educators develop diverse learning materials quickly, but quality control remains an important challenge.",
    "Bias detection algorithms are essential for ensuring fairness in AI-powered educational assessment systems across different student demographics.",
    "Virtual reality combined with generative AI creates immersive learning environments that simulate real-world scenarios for practical skill development.",
    "Teacher training programs must evolve to prepare educators for effective integration of AI tools while maintaining human-centered pedagogical approaches."
]


def print_separator(title: str = ""):
    """Imprime separador visual."""
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)


def print_test_header(test_num: int, test_name: str):
    """Imprime encabezado de test."""
    print(f"\nTEST {test_num}: {test_name}")
    print("-" * 80)


def print_result(passed: bool, message: str = ""):
    """Imprime resultado del test."""
    status = "PASO" if passed else "FALLO"
    symbol = "✓" if passed else "✗"
    print(f"Resultado: {symbol} {status}")
    if message:
        print(f"Detalle: {message}")


def validate_response_structure(response: Dict[str, Any], required_fields: list) -> bool:
    """
    Valida que la respuesta contenga los campos requeridos.
    
    Args:
        response: Respuesta a validar
        required_fields: Lista de campos requeridos
    
    Returns:
        True si todos los campos están presentes
    """
    missing = [field for field in required_fields if field not in response]
    if missing:
        print(f"Campos faltantes: {missing}")
        return False
    return True


# ============================================================================
# TESTS
# ============================================================================

def test_01_health_check():
    """Test 1: Health check del sistema de clustering."""
    print_test_header(1, "Health Check del Sistema de Clustering")
    
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/health")
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            print_result(False, f"Código esperado 200, recibido {response.status_code}")
            return False
        
        data = response.json()
        print(f"Respuesta: {json.dumps(data, indent=2)}")
        
        # Validar estructura
        required = ["status", "clustering_initialized"]
        if not validate_response_structure(data, required):
            print_result(False, "Estructura de respuesta inválida")
            return False
        
        # Validar estado
        if data["status"] != "healthy":
            print_result(False, f"Estado esperado 'healthy', recibido '{data['status']}'")
            return False
        
        if not data["clustering_initialized"]:
            print_result(False, "Clustering no inicializado")
            return False
        
        print_result(True, "Sistema de clustering operativo")
        return True
    
    except Exception as e:
        print_result(False, f"Excepción: {str(e)}")
        return False


def test_02_list_methods():
    """Test 2: Listar métodos de linkage disponibles."""
    print_test_header(2, "Listar Métodos de Linkage")
    
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/methods")
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            print_result(False, f"Código esperado 200, recibido {response.status_code}")
            return False
        
        data = response.json()
        print(f"Métodos disponibles: {len(data)}")
        
        # Debe haber exactamente 3 métodos
        if len(data) != 3:
            print_result(False, f"Esperados 3 métodos, recibidos {len(data)}")
            return False
        
        # Validar cada método
        expected_methods = {"ward", "average", "complete"}
        received_methods = {method["method"] for method in data}
        
        if received_methods != expected_methods:
            print_result(False, f"Métodos esperados {expected_methods}, recibidos {received_methods}")
            return False
        
        # Validar estructura de cada método
        for method in data:
            required = ["method", "name", "description", "formula", "use_case"]
            if not validate_response_structure(method, required):
                print_result(False, f"Estructura inválida para método {method.get('method')}")
                return False
            
            print(f"  - {method['method']}: {method['name']}")
        
        print_result(True, "3 métodos de linkage disponibles con documentación completa")
        return True
    
    except Exception as e:
        print_result(False, f"Excepción: {str(e)}")
        return False


def test_03_hierarchical_clustering_ward():
    """Test 3: Clustering jerárquico con Ward Linkage."""
    print_test_header(3, "Clustering Jerárquico - Ward Linkage")
    
    try:
        payload = {
            "abstracts": TEST_ABSTRACTS[:5],  # Usar solo 5 abstracts para test rápido
            "method": "ward",
            "num_clusters": 2,
            "generate_dendrogram": True
        }
        
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/hierarchical",
            json=payload
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            print_result(False, f"Código esperado 200, recibido {response.status_code}")
            print(f"Error: {response.text}")
            return False
        
        data = response.json()
        
        # Validar estructura
        required = [
            "method", "num_documents", "num_features",
            "cophenetic_correlation", "cluster_labels",
            "silhouette_score", "davies_bouldin_score",
            "calinski_harabasz_score", "dendrogram_base64"
        ]
        if not validate_response_structure(data, required):
            print_result(False, "Estructura de respuesta inválida")
            return False
        
        # Validar método
        if data["method"] != "ward":
            print_result(False, f"Método esperado 'ward', recibido '{data['method']}'")
            return False
        
        # Validar número de documentos
        if data["num_documents"] != 5:
            print_result(False, f"Documentos esperados 5, recibidos {data['num_documents']}")
            return False
        
        # Validar correlación cofenética (0-1)
        if not 0 <= data["cophenetic_correlation"] <= 1:
            print_result(False, f"Correlación cofenética inválida: {data['cophenetic_correlation']}")
            return False
        
        # Validar cluster labels (deben ser 5 etiquetas)
        if len(data["cluster_labels"]) != 5:
            print_result(False, f"Esperadas 5 etiquetas, recibidas {len(data['cluster_labels'])}")
            return False
        
        # Validar número de clusters (deben ser exactamente 2)
        unique_clusters = set(data["cluster_labels"])
        if len(unique_clusters) != 2:
            print_result(False, f"Esperados 2 clusters, encontrados {len(unique_clusters)}")
            return False
        
        # Validar silhouette score (-1 a 1)
        if data["silhouette_score"] is not None:
            if not -1 <= data["silhouette_score"] <= 1:
                print_result(False, f"Silhouette inválido: {data['silhouette_score']}")
                return False
        
        # Validar dendrograma
        if not data["dendrogram_base64"]:
            print_result(False, "Dendrograma no generado")
            return False
        
        print(f"Documentos: {data['num_documents']}")
        print(f"Features: {data['num_features']}")
        print(f"Correlación cofenética: {data['cophenetic_correlation']:.4f}")
        print(f"Silhouette Score: {data['silhouette_score']:.4f}")
        print(f"Davies-Bouldin: {data['davies_bouldin_score']:.4f}")
        print(f"Calinski-Harabasz: {data['calinski_harabasz_score']:.2f}")
        print(f"Clusters: {data['cluster_labels']}")
        print(f"Dendrograma generado: {len(data['dendrogram_base64'])} chars")
        
        print_result(True, "Clustering con Ward Linkage ejecutado correctamente")
        return True
    
    except Exception as e:
        print_result(False, f"Excepción: {str(e)}")
        return False


def test_04_hierarchical_clustering_average():
    """Test 4: Clustering jerárquico con Average Linkage."""
    print_test_header(4, "Clustering Jerárquico - Average Linkage")
    
    try:
        payload = {
            "abstracts": TEST_ABSTRACTS[:6],
            "method": "average",
            "num_clusters": 3,
            "generate_dendrogram": False  # Sin dendrograma para test más rápido
        }
        
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/hierarchical",
            json=payload
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            print_result(False, f"Código esperado 200, recibido {response.status_code}")
            return False
        
        data = response.json()
        
        # Validar método
        if data["method"] != "average":
            print_result(False, f"Método esperado 'average', recibido '{data['method']}'")
            return False
        
        # Validar número de clusters
        unique_clusters = set(data["cluster_labels"])
        if len(unique_clusters) != 3:
            print_result(False, f"Esperados 3 clusters, encontrados {len(unique_clusters)}")
            return False
        
        # Sin dendrograma
        if data["dendrogram_base64"] is not None:
            print_result(False, "No se esperaba dendrograma")
            return False
        
        print(f"Documentos: {data['num_documents']}")
        print(f"Correlación cofenética: {data['cophenetic_correlation']:.4f}")
        print(f"Clusters: {data['cluster_labels']}")
        
        print_result(True, "Clustering con Average Linkage ejecutado correctamente")
        return True
    
    except Exception as e:
        print_result(False, f"Excepción: {str(e)}")
        return False


def test_05_hierarchical_clustering_complete():
    """Test 5: Clustering jerárquico con Complete Linkage."""
    print_test_header(5, "Clustering Jerárquico - Complete Linkage")
    
    try:
        payload = {
            "abstracts": TEST_ABSTRACTS[:7],
            "method": "complete",
            "num_clusters": 2,
            "generate_dendrogram": True
        }
        
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/hierarchical",
            json=payload
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            print_result(False, f"Código esperado 200, recibido {response.status_code}")
            return False
        
        data = response.json()
        
        # Validar método
        if data["method"] != "complete":
            print_result(False, f"Método esperado 'complete', recibido '{data['method']}'")
            return False
        
        # Validar número de clusters
        unique_clusters = set(data["cluster_labels"])
        if len(unique_clusters) != 2:
            print_result(False, f"Esperados 2 clusters, encontrados {len(unique_clusters)}")
            return False
        
        print(f"Documentos: {data['num_documents']}")
        print(f"Correlación cofenética: {data['cophenetic_correlation']:.4f}")
        print(f"Silhouette Score: {data['silhouette_score']:.4f}")
        
        print_result(True, "Clustering con Complete Linkage ejecutado correctamente")
        return True
    
    except Exception as e:
        print_result(False, f"Excepción: {str(e)}")
        return False


def test_06_compare_methods():
    """Test 6: Comparar los 3 métodos de clustering."""
    print_test_header(6, "Comparar Métodos de Clustering")
    
    try:
        payload = {
            "abstracts": TEST_ABSTRACTS[:8],
            "num_clusters": 3
        }
        
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/compare-methods",
            json=payload
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            print_result(False, f"Código esperado 200, recibido {response.status_code}")
            print(f"Error: {response.text}")
            return False
        
        data = response.json()
        
        # Validar estructura
        required = ["methods", "best_method", "comparison_summary"]
        if not validate_response_structure(data, required):
            print_result(False, "Estructura de respuesta inválida")
            return False
        
        # Validar que hay 3 métodos
        if len(data["methods"]) != 3:
            print_result(False, f"Esperados 3 métodos, recibidos {len(data['methods'])}")
            return False
        
        # Validar métodos
        expected_methods = {"ward", "average", "complete"}
        if set(data["methods"].keys()) != expected_methods:
            print_result(False, f"Métodos incorrectos")
            return False
        
        # Validar que hay un mejor método
        if data["best_method"] not in expected_methods:
            print_result(False, f"Mejor método inválido: {data['best_method']}")
            return False
        
        # Validar comparison_summary
        summary = data["comparison_summary"]
        required_summary = ["cophenetic_correlations", "silhouette_scores", "davies_bouldin_scores"]
        if not validate_response_structure(summary, required_summary):
            print_result(False, "Estructura de comparison_summary inválida")
            return False
        
        print(f"\nComparación de Métodos:")
        print(f"  Mejor método: {data['best_method']}")
        
        print(f"\n  Correlaciones Cofenéticas:")
        for method, corr in summary["cophenetic_correlations"].items():
            print(f"    {method}: {corr:.4f}")
        
        print(f"\n  Silhouette Scores:")
        for method, score in summary["silhouette_scores"].items():
            print(f"    {method}: {score:.4f}")
        
        print(f"\n  Davies-Bouldin Scores:")
        for method, score in summary["davies_bouldin_scores"].items():
            print(f"    {method}: {score:.4f}")
        
        print_result(True, f"Comparación completada - Mejor método: {data['best_method']}")
        return True
    
    except Exception as e:
        print_result(False, f"Excepción: {str(e)}")
        return False


def test_07_error_handling_few_abstracts():
    """Test 7: Manejo de error - muy pocos abstracts."""
    print_test_header(7, "Error Handling - Abstracts Insuficientes")
    
    try:
        payload = {
            "abstracts": [TEST_ABSTRACTS[0]],  # Solo 1 abstract (mínimo es 2)
            "method": "ward"
        }
        
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/hierarchical",
            json=payload
        )
        
        print(f"Status code: {response.status_code}")
        
        # Debe retornar error 422 (Validation Error)
        if response.status_code != 422:
            print_result(False, f"Código esperado 422, recibido {response.status_code}")
            return False
        
        print_result(True, "Error de validación correctamente manejado")
        return True
    
    except Exception as e:
        print_result(False, f"Excepción: {str(e)}")
        return False


def test_08_error_handling_invalid_method():
    """Test 8: Manejo de error - método inválido."""
    print_test_header(8, "Error Handling - Método Inválido")
    
    try:
        payload = {
            "abstracts": TEST_ABSTRACTS[:5],
            "method": "invalid_method"  # Método que no existe
        }
        
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/hierarchical",
            json=payload
        )
        
        print(f"Status code: {response.status_code}")
        
        # Debe retornar error 422
        if response.status_code != 422:
            print_result(False, f"Código esperado 422, recibido {response.status_code}")
            return False
        
        print_result(True, "Método inválido correctamente rechazado")
        return True
    
    except Exception as e:
        print_result(False, f"Excepción: {str(e)}")
        return False


def test_09_clustering_with_labels():
    """Test 9: Clustering con etiquetas personalizadas."""
    print_test_header(9, "Clustering con Etiquetas Personalizadas")
    
    try:
        custom_labels = [f"Doc{i+1}" for i in range(5)]
        
        payload = {
            "abstracts": TEST_ABSTRACTS[:5],
            "method": "ward",
            "num_clusters": 2,
            "labels": custom_labels,
            "generate_dendrogram": True
        }
        
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/hierarchical",
            json=payload
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            print_result(False, f"Código esperado 200, recibido {response.status_code}")
            return False
        
        data = response.json()
        
        print(f"Etiquetas usadas: {custom_labels}")
        print(f"Clusters asignados: {data['cluster_labels']}")
        
        print_result(True, "Clustering con etiquetas ejecutado correctamente")
        return True
    
    except Exception as e:
        print_result(False, f"Excepción: {str(e)}")
        return False


def test_10_full_dataset_clustering():
    """Test 10: Clustering con dataset completo (10 abstracts)."""
    print_test_header(10, "Clustering con Dataset Completo")
    
    try:
        payload = {
            "abstracts": TEST_ABSTRACTS,  # Todos los 10 abstracts
            "method": "ward",
            "num_clusters": 4,
            "generate_dendrogram": True
        }
        
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/hierarchical",
            json=payload
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code != 200:
            print_result(False, f"Código esperado 200, recibido {response.status_code}")
            return False
        
        data = response.json()
        
        # Validar 4 clusters
        unique_clusters = set(data["cluster_labels"])
        if len(unique_clusters) != 4:
            print_result(False, f"Esperados 4 clusters, encontrados {len(unique_clusters)}")
            return False
        
        print(f"\nResultados del Clustering Completo:")
        print(f"  Documentos procesados: {data['num_documents']}")
        print(f"  Features extraídas: {data['num_features']}")
        print(f"  Clusters formados: {len(unique_clusters)}")
        print(f"  Correlación cofenética: {data['cophenetic_correlation']:.4f}")
        print(f"  Silhouette Score: {data['silhouette_score']:.4f}")
        print(f"  Davies-Bouldin Index: {data['davies_bouldin_score']:.4f}")
        print(f"  Calinski-Harabasz Index: {data['calinski_harabasz_score']:.2f}")
        
        print(f"\n  Distribución de clusters:")
        for i in range(len(unique_clusters)):
            count = data['cluster_labels'].count(i)
            print(f"    Cluster {i}: {count} documentos")
        
        print_result(True, "Dataset completo procesado exitosamente")
        return True
    
    except Exception as e:
        print_result(False, f"Excepción: {str(e)}")
        return False


# ============================================================================
# EJECUCIÓN DE TESTS
# ============================================================================

def main():
    """Ejecuta todos los tests de la API de clustering."""
    print_separator("TESTS DE API - CLUSTERING JERARQUICO (REQUERIMIENTO 4)")
    print("\nAutores: Santiago Ovalle Cortés, Juan Sebastián Noreña")
    print("Proyecto: Análisis de Algoritmos - Universidad del Quindío")
    print("\nNOTA: Asegúrese de que el servidor FastAPI esté corriendo en http://127.0.0.1:8000")
    print("      Ejecute: uvicorn main:app --reload")
    
    # Esperar a que el usuario confirme
    input("\nPresione ENTER para iniciar los tests...")
    
    # Lista de tests
    tests = [
        test_01_health_check,
        test_02_list_methods,
        test_03_hierarchical_clustering_ward,
        test_04_hierarchical_clustering_average,
        test_05_hierarchical_clustering_complete,
        test_06_compare_methods,
        test_07_error_handling_few_abstracts,
        test_08_error_handling_invalid_method,
        test_09_clustering_with_labels,
        test_10_full_dataset_clustering,
    ]
    
    # Ejecutar tests
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\nERROR CRÍTICO en {test.__name__}: {str(e)}")
            results.append(False)
        
        # Pequeña pausa entre tests
        sleep(0.5)
    
    # Resumen final
    print_separator("RESUMEN DE TESTS - CLUSTERING JERARQUICO")
    
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100
    
    print(f"\nTests ejecutados: {total}")
    print(f"Tests exitosos: {passed}")
    print(f"Tests fallidos: {total - passed}")
    print(f"Porcentaje de éxito: {percentage:.1f}%")
    
    if passed == total:
        print("\n🎉 TODOS LOS TESTS PASARON EXITOSAMENTE!")
    else:
        print(f"\n⚠️  {total - passed} test(s) fallaron")
    
    print("\n" + "=" * 80)
    
    return results


if __name__ == "__main__":
    main()
