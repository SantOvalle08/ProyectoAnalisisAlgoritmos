"""
Tests para Clustering Jerárquico - Requerimiento 4
===================================================

Valida los algoritmos de agrupamiento jerárquico implementados.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
"""

import sys
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.services.ml_analysis.clustering import (
    HierarchicalClustering,
    LinkageMethod,
    ClusteringResult
)
import numpy as np

# Datos de prueba - abstracts sobre IA generativa en educación
TEST_ABSTRACTS = [
    "Generative models have revolutionized education by enabling personalized learning experiences. "
    "Machine learning algorithms can adapt to student needs, while fine-tuning helps customize AI systems.",
    
    "Prompting techniques are essential for effective human-AI interaction in educational contexts. "
    "Students must develop AI literacy to understand how generative models work.",
    
    "Training data quality significantly impacts the performance of educational AI systems. "
    "Privacy concerns arise when collecting student data for machine learning models.",
    
    "Multimodality enables richer learning experiences by combining text, images, and audio. "
    "Co-creation between students and AI fosters creativity and deeper understanding.",
    
    "Algorithmic bias in AI systems can perpetuate educational inequalities. "
    "Transparency and explainability are crucial for building trust in AI-powered learning tools.",
    
    "Ethics must guide the development and deployment of generative AI in education. "
    "Privacy protection and data security are fundamental considerations.",
    
    "Fine-tuning pre-trained models for educational applications requires careful consideration. "
    "Personalization through generative models can enhance student engagement and outcomes.",
    
    "AI literacy programs help students and teachers understand generative AI capabilities. "
    "Human-AI interaction patterns reveal the importance of intuitive interfaces.",
    
    "Machine learning models must be explainable to gain acceptance from educators. "
    "Transparency in AI decision-making builds confidence in educational technology.",
    
    "Generative AI creates opportunities for personalized content and adaptive learning. "
    "Co-creation tools empower students to become active participants in learning."
]

print("\n" + "="*80)
print("INICIANDO TESTS - CLUSTERING JERARQUICO (REQUERIMIENTO 4)")
print("="*80 + "\n")

# =============================================================================
# TEST 1: Inicialización de HierarchicalClustering
# =============================================================================
print("TEST 1: Inicialización de HierarchicalClustering")
print("-" * 80)

try:
    clustering = HierarchicalClustering(
        max_features=1000,
        ngram_range=(1, 3),
        min_df=1,
        max_df=0.95
    )
    
    assert clustering.max_features == 1000, "max_features incorrecto"
    assert clustering.ngram_range == (1, 3), "ngram_range incorrecto"
    assert clustering.vectorizer is not None, "Vectorizer no inicializado"
    
    print(f"HierarchicalClustering inicializado correctamente")
    print(f"  - max_features: {clustering.max_features}")
    print(f"  - ngram_range: {clustering.ngram_range}")
    print(f"  - Vectorizer TF-IDF: inicializado")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 2: Preprocesamiento de Textos con TF-IDF
# =============================================================================
print("TEST 2: Preprocesamiento de Textos con TF-IDF")
print("-" * 80)

try:
    clustering = HierarchicalClustering()
    
    # Preprocesar textos
    tfidf_matrix = clustering.preprocess_texts(TEST_ABSTRACTS)
    
    assert tfidf_matrix.shape[0] == len(TEST_ABSTRACTS), "Número de documentos incorrecto"
    assert tfidf_matrix.shape[1] > 0, "No se extrajeron características"
    assert isinstance(tfidf_matrix, np.ndarray), "Tipo de matriz incorrecto"
    
    print(f"Textos preprocesados exitosamente")
    print(f"  - Documentos: {tfidf_matrix.shape[0]}")
    print(f"  - Características (términos): {tfidf_matrix.shape[1]}")
    print(f"  - Tipo de matriz: {type(tfidf_matrix)}")
    print(f"  - Sparsity: {np.count_nonzero(tfidf_matrix == 0) / tfidf_matrix.size:.2%}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 3: Cálculo de Matriz de Distancias
# =============================================================================
print("TEST 3: Cálculo de Matriz de Distancias")
print("-" * 80)

try:
    clustering = HierarchicalClustering()
    tfidf_matrix = clustering.preprocess_texts(TEST_ABSTRACTS)
    
    # Calcular distancias
    distance_matrix = clustering.compute_distance_matrix(tfidf_matrix, metric='cosine')
    
    # Validar matriz
    num_pairs = len(TEST_ABSTRACTS) * (len(TEST_ABSTRACTS) - 1) // 2
    assert len(distance_matrix) == num_pairs, "Número de pares incorrecto"
    assert np.all(distance_matrix >= 0), "Distancias deben ser no negativas"
    assert np.all(distance_matrix <= 1.01), "Distancias coseno exceden 1"  # Pequeña tolerancia
    
    print(f"Matriz de distancias calculada")
    print(f"  - Número de pares: {len(distance_matrix)}")
    print(f"  - Distancia mínima: {np.min(distance_matrix):.4f}")
    print(f"  - Distancia máxima: {np.max(distance_matrix):.4f}")
    print(f"  - Distancia promedio: {np.mean(distance_matrix):.4f}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 4: Clustering con Ward Linkage
# =============================================================================
print("TEST 4: Clustering con Ward Linkage")
print("-" * 80)

try:
    clustering = HierarchicalClustering()
    tfidf_matrix = clustering.preprocess_texts(TEST_ABSTRACTS)
    distance_matrix = clustering.compute_distance_matrix(tfidf_matrix)
    
    # Aplicar Ward
    linkage_matrix = clustering.apply_clustering(distance_matrix, LinkageMethod.WARD)
    
    # Validar matriz de linkage
    assert linkage_matrix.shape[0] == len(TEST_ABSTRACTS) - 1, "Pasos de linkage incorrectos"
    assert linkage_matrix.shape[1] == 4, "Columnas de linkage incorrectas"
    
    # Calcular correlación cofenética
    cophenetic_corr = clustering.calculate_cophenetic_correlation(
        linkage_matrix,
        distance_matrix
    )
    
    assert 0 <= cophenetic_corr <= 1, "Correlación fuera de rango"
    
    print(f"Ward Linkage aplicado exitosamente")
    print(f"  - Pasos de clustering: {linkage_matrix.shape[0]}")
    print(f"  - Correlación cofenética: {cophenetic_corr:.4f}")
    print(f"  - Distancia final: {linkage_matrix[-1, 2]:.4f}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 5: Clustering con Average Linkage
# =============================================================================
print("TEST 5: Clustering con Average Linkage")
print("-" * 80)

try:
    clustering = HierarchicalClustering()
    tfidf_matrix = clustering.preprocess_texts(TEST_ABSTRACTS)
    distance_matrix = clustering.compute_distance_matrix(tfidf_matrix)
    
    # Aplicar Average
    linkage_matrix = clustering.apply_clustering(distance_matrix, LinkageMethod.AVERAGE)
    
    # Calcular correlación cofenética
    cophenetic_corr = clustering.calculate_cophenetic_correlation(
        linkage_matrix,
        distance_matrix
    )
    
    print(f"Average Linkage aplicado exitosamente")
    print(f"  - Pasos de clustering: {linkage_matrix.shape[0]}")
    print(f"  - Correlación cofenética: {cophenetic_corr:.4f}")
    print(f"  - Distancia final: {linkage_matrix[-1, 2]:.4f}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 6: Clustering con Complete Linkage
# =============================================================================
print("TEST 6: Clustering con Complete Linkage")
print("-" * 80)

try:
    clustering = HierarchicalClustering()
    tfidf_matrix = clustering.preprocess_texts(TEST_ABSTRACTS)
    distance_matrix = clustering.compute_distance_matrix(tfidf_matrix)
    
    # Aplicar Complete
    linkage_matrix = clustering.apply_clustering(distance_matrix, LinkageMethod.COMPLETE)
    
    # Calcular correlación cofenética
    cophenetic_corr = clustering.calculate_cophenetic_correlation(
        linkage_matrix,
        distance_matrix
    )
    
    print(f"Complete Linkage aplicado exitosamente")
    print(f"  - Pasos de clustering: {linkage_matrix.shape[0]}")
    print(f"  - Correlación cofenética: {cophenetic_corr:.4f}")
    print(f"  - Distancia final: {linkage_matrix[-1, 2]:.4f}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 7: Cortar Árbol y Asignar Clusters
# =============================================================================
print("TEST 7: Cortar Árbol y Asignar Clusters")
print("-" * 80)

try:
    clustering = HierarchicalClustering()
    tfidf_matrix = clustering.preprocess_texts(TEST_ABSTRACTS)
    distance_matrix = clustering.compute_distance_matrix(tfidf_matrix)
    linkage_matrix = clustering.apply_clustering(distance_matrix, LinkageMethod.WARD)
    
    # Cortar en 3 clusters
    num_clusters = 3
    cluster_labels = clustering.cut_tree(linkage_matrix, num_clusters)
    
    # Validar
    assert len(cluster_labels) == len(TEST_ABSTRACTS), "Número de etiquetas incorrecto"
    assert len(np.unique(cluster_labels)) <= num_clusters, "Más clusters de los solicitados"
    
    # Mostrar distribución
    unique, counts = np.unique(cluster_labels, return_counts=True)
    
    print(f"Árbol cortado en {num_clusters} clusters")
    print(f"  - Clusters obtenidos: {len(unique)}")
    print(f"  - Distribución:")
    for cluster_id, count in zip(unique, counts):
        print(f"    * Cluster {cluster_id}: {count} documentos")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 8: Evaluación de Calidad del Clustering
# =============================================================================
print("TEST 8: Evaluación de Calidad del Clustering")
print("-" * 80)

try:
    clustering = HierarchicalClustering()
    tfidf_matrix = clustering.preprocess_texts(TEST_ABSTRACTS)
    distance_matrix = clustering.compute_distance_matrix(tfidf_matrix)
    linkage_matrix = clustering.apply_clustering(distance_matrix, LinkageMethod.WARD)
    cluster_labels = clustering.cut_tree(linkage_matrix, 3)
    
    # Evaluar calidad
    metrics = clustering.evaluate_clustering(tfidf_matrix, cluster_labels)
    
    # Validar métricas
    assert 'silhouette_score' in metrics, "Falta Silhouette Score"
    assert 'davies_bouldin_score' in metrics, "Falta Davies-Bouldin Score"
    assert 'calinski_harabasz_score' in metrics, "Falta Calinski-Harabasz Score"
    
    assert -1 <= metrics['silhouette_score'] <= 1, "Silhouette fuera de rango"
    assert metrics['davies_bouldin_score'] >= 0, "Davies-Bouldin debe ser no negativo"
    assert metrics['calinski_harabasz_score'] >= 0, "Calinski-Harabasz debe ser no negativo"
    
    print(f"Métricas de calidad calculadas")
    print(f"  - Silhouette Score: {metrics['silhouette_score']:.4f} (mayor es mejor)")
    print(f"  - Davies-Bouldin: {metrics['davies_bouldin_score']:.4f} (menor es mejor)")
    print(f"  - Calinski-Harabasz: {metrics['calinski_harabasz_score']:.2f} (mayor es mejor)")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 9: Proceso Completo de Clustering
# =============================================================================
print("TEST 9: Proceso Completo de Clustering")
print("-" * 80)

try:
    clustering = HierarchicalClustering()
    
    # Ejecutar proceso completo
    result = clustering.cluster_texts(
        texts=TEST_ABSTRACTS,
        method=LinkageMethod.WARD,
        num_clusters=3,
        labels=[f"Doc{i+1}" for i in range(len(TEST_ABSTRACTS))],
        generate_plot=True
    )
    
    # Validar resultado
    assert isinstance(result, ClusteringResult), "Tipo de resultado incorrecto"
    assert result.method == LinkageMethod.WARD.value, "Método incorrecto"
    assert result.num_documents == len(TEST_ABSTRACTS), "Número de documentos incorrecto"
    assert result.linkage_matrix is not None, "Falta matriz de linkage"
    assert result.cophenetic_correlation > 0, "Correlación debe ser positiva"
    assert result.cluster_labels is not None, "Faltan etiquetas de clusters"
    assert result.dendrogram_data is not None, "Falta dendrograma"
    
    print(f"Proceso completo ejecutado exitosamente")
    print(f"  - Método: {result.method}")
    print(f"  - Documentos: {result.num_documents}")
    print(f"  - Features: {result.num_features}")
    print(f"  - Correlación cofenética: {result.cophenetic_correlation:.4f}")
    print(f"  - Silhouette: {result.silhouette_score:.4f}")
    print(f"  - Davies-Bouldin: {result.davies_bouldin_score:.4f}")
    print(f"  - Dendrograma generado: {'image_base64' in result.dendrogram_data}")
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# TEST 10: Comparación de los 3 Métodos
# =============================================================================
print("TEST 10: Comparación de los 3 Métodos")
print("-" * 80)

try:
    clustering = HierarchicalClustering()
    
    # Comparar todos los métodos
    results = clustering.compare_methods(
        texts=TEST_ABSTRACTS,
        num_clusters=3,
        labels=[f"Doc{i+1}" for i in range(len(TEST_ABSTRACTS))]
    )
    
    # Validar que tenemos los 3 resultados
    assert len(results) == 3, "Deben haber 3 resultados"
    assert 'ward' in results, "Falta resultado de Ward"
    assert 'average' in results, "Falta resultado de Average"
    assert 'complete' in results, "Falta resultado de Complete"
    
    # Comparar correlaciones cofenéticas
    print(f"Comparación de métodos completada")
    print(f"\nCorrelaciones Cofenéticas (mayor es mejor):")
    for method_name, result in results.items():
        print(f"  - {method_name.upper()}: {result.cophenetic_correlation:.4f}")
    
    print(f"\nSilhouette Scores (mayor es mejor):")
    for method_name, result in results.items():
        if result.silhouette_score:
            print(f"  - {method_name.upper()}: {result.silhouette_score:.4f}")
    
    print(f"\nDavies-Bouldin Scores (menor es mejor):")
    for method_name, result in results.items():
        if result.davies_bouldin_score:
            print(f"  - {method_name.upper()}: {result.davies_bouldin_score:.4f}")
    
    # Determinar el mejor
    best_cophenetic = max(results.items(), key=lambda x: x[1].cophenetic_correlation)
    print(f"\nMejor método según correlación cofenética: {best_cophenetic[0].upper()}")
    
    print("Resultado: PASO")
    
except Exception as e:
    print(f"ERROR: {e}")
    print("Resultado: FALLO")

print()

# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("\n" + "="*80)
print("RESUMEN DE TESTS - CLUSTERING JERARQUICO")
print("="*80)
print("\nTODOS LOS TESTS HAN SIDO EJECUTADOS")
print("\nComponentes validados:")
print("  1. Inicialización de HierarchicalClustering")
print("  2. Preprocesamiento con TF-IDF")
print("  3. Cálculo de matriz de distancias")
print("  4. Ward Linkage")
print("  5. Average Linkage (UPGMA)")
print("  6. Complete Linkage")
print("  7. Corte de árbol y asignación de clusters")
print("  8. Evaluación de calidad (Silhouette, Davies-Bouldin, Calinski-Harabasz)")
print("  9. Proceso completo de clustering")
print("  10. Comparación de los 3 métodos")
print("\nFuncionalidades implementadas:")
print("  - Preprocesamiento de texto con TF-IDF")
print("  - Cálculo de matriz de distancias (similitud)")
print("  - 3 algoritmos de clustering jerárquico")
print("  - Generación de dendrogramas")
print("  - Evaluación de coherencia con múltiples métricas")
print("  - Comparación automática de métodos")
print("="*80 + "\n")
