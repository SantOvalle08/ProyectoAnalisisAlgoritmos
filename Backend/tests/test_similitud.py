"""
Script de Prueba Rápida - Algoritmos de Similitud
=================================================

Prueba los algoritmos de similitud implementados con textos de ejemplo.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

import sys
import os

# Agregar el directorio Backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.ml_analysis.similarity import (
    LevenshteinSimilarity,
    TFIDFCosineSimilarity,
    JaccardSimilarity,
    NGramSimilarity
)


def test_levenshtein():
    """Prueba el algoritmo de Levenshtein."""
    print("\n" + "="*80)
    print("PRUEBA: Distancia de Levenshtein")
    print("="*80 + "\n")
    
    text1 = "Generative artificial intelligence in education"
    text2 = "Generative AI in educational contexts"
    
    algo = LevenshteinSimilarity()
    
    # Prueba simple
    similarity = algo.calculate_similarity(text1, text2)
    print(f"📊 Similitud entre textos: {similarity:.4f} ({similarity*100:.2f}%)")
    print(f"   Texto 1: '{text1}'")
    print(f"   Texto 2: '{text2}'")
    print()
    
    # Análisis detallado
    print("🔍 Análisis detallado:")
    analysis = algo.analyze_step_by_step(text1, text2)
    
    print(f"   - Distancia: {analysis['results']['distance']}")
    print(f"   - Similitud: {analysis['results']['similarity_percentage']}")
    print(f"   - Operaciones totales: {analysis['operations']['total_edits']}")
    print(f"   - Inserciones: {analysis['operations']['counts']['insert']}")
    print(f"   - Eliminaciones: {analysis['operations']['counts']['delete']}")
    print(f"   - Sustituciones: {analysis['operations']['counts']['substitute']}")
    print(f"   - Coincidencias: {analysis['operations']['counts']['match']}")
    
    return True


def test_tfidf_cosine():
    """Prueba el algoritmo TF-IDF + Coseno."""
    print("\n" + "="*80)
    print("PRUEBA: TF-IDF + Similitud del Coseno")
    print("="*80 + "\n")
    
    text1 = """
    Generative artificial intelligence has revolutionized education by providing
    personalized learning experiences. Machine learning algorithms analyze student
    performance and adapt content accordingly. This technology enables teachers
    to focus on individual student needs while AI handles routine tasks.
    """
    
    text2 = """
    The impact of AI in educational settings is significant. Generative models
    create customized learning materials for students. Teachers can leverage
    these AI tools to enhance their teaching methods and improve student outcomes.
    """
    
    algo = TFIDFCosineSimilarity(max_features=100, ngram_range=(1, 2))
    
    # Prueba simple
    similarity = algo.calculate_similarity(text1, text2)
    print(f"📊 Similitud entre textos: {similarity:.4f} ({similarity*100:.2f}%)")
    print()
    
    # Análisis detallado
    print("🔍 Análisis detallado:")
    analysis = algo.analyze_step_by_step(text1, text2)
    
    print(f"   - Similitud del coseno: {analysis['results']['similarity_percentage']}")
    print(f"   - Ángulo entre vectores: {analysis['results']['angle_degrees']:.2f}°")
    print(f"   - Tamaño del vocabulario: {analysis['vectorization']['vocabulary_size']}")
    print(f"   - Términos comunes: {analysis['vocabulary_stats']['common_terms_count']}")
    
    print("\n   📝 Top 5 términos en Texto 1:")
    for term in analysis['vectorization']['top_terms_text1'][:5]:
        print(f"      - '{term['term']}': {term['tfidf_weight']:.4f}")
    
    print("\n   📝 Top 5 términos en Texto 2:")
    for term in analysis['vectorization']['top_terms_text2'][:5]:
        print(f"      - '{term['term']}': {term['tfidf_weight']:.4f}")
    
    return True


def test_jaccard():
    """Prueba el algoritmo de Jaccard."""
    print("\n" + "="*80)
    print("PRUEBA: Coeficiente de Jaccard")
    print("="*80 + "\n")
    
    text1 = "Generative artificial intelligence in education and learning"
    text2 = "Artificial intelligence for education and teaching"
    
    # Prueba con tokens de palabras
    algo = JaccardSimilarity(use_char_ngrams=False, remove_stopwords=True)
    
    similarity = algo.calculate_similarity(text1, text2)
    print(f"📊 Similitud entre textos (palabras): {similarity:.4f} ({similarity*100:.2f}%)")
    print(f"   Texto 1: '{text1}'")
    print(f"   Texto 2: '{text2}'")
    print()
    
    # Análisis detallado
    print("🔍 Análisis detallado:")
    analysis = algo.analyze_step_by_step(text1, text2)
    
    print(f"   - Coeficiente de Jaccard: {analysis['results']['jaccard_percentage']}")
    print(f"   - Tokens en Texto 1: {analysis['tokenization']['total_tokens_text1']}")
    print(f"   - Tokens en Texto 2: {analysis['tokenization']['total_tokens_text2']}")
    print(f"   - Tokens comunes: {analysis['set_operations']['intersection_size']}")
    print(f"   - Tokens únicos totales: {analysis['set_operations']['union_size']}")
    
    return True


def test_ngrams():
    """Prueba el algoritmo de N-gramas."""
    print("\n" + "="*80)
    print("PRUEBA: Similitud por N-gramas")
    print("="*80 + "\n")
    
    text1 = "Machine learning algorithms"
    text2 = "Machine learning models"
    
    # Prueba con trigramas de caracteres
    algo = NGramSimilarity(n=3, ngram_type='char', similarity_metric='dice')
    
    similarity = algo.calculate_similarity(text1, text2)
    print(f"📊 Similitud entre textos (3-gramas): {similarity:.4f} ({similarity*100:.2f}%)")
    print(f"   Texto 1: '{text1}'")
    print(f"   Texto 2: '{text2}'")
    print()
    
    # Análisis detallado
    print("🔍 Análisis detallado:")
    analysis = algo.analyze_step_by_step(text1, text2)
    
    print(f"   - Similitud de Dice: {analysis['results']['all_metrics']['dice']:.4f}")
    print(f"   - Similitud de Jaccard: {analysis['results']['all_metrics']['jaccard']:.4f}")
    print(f"   - Similitud del Coseno: {analysis['results']['all_metrics']['cosine']:.4f}")
    print(f"   - Total 3-gramas Texto 1: {analysis['ngrams']['total_ngrams_text1']}")
    print(f"   - Total 3-gramas Texto 2: {analysis['ngrams']['total_ngrams_text2']}")
    print(f"   - 3-gramas comunes: {analysis['set_operations']['intersection_size']}")
    
    return True


def main():
    """Función principal de pruebas."""
    print("\n" + "="*80)
    print("🧪 PRUEBAS DE ALGORITMOS DE SIMILITUD - REQUERIMIENTO 2")
    print("Proyecto de Análisis Bibliométrico")
    print("Universidad del Quindío - 2025-2")
    print("="*80)
    
    results = []
    
    try:
        # Prueba 1: Levenshtein
        result1 = test_levenshtein()
        results.append(("Levenshtein", result1))
    except Exception as e:
        print(f"❌ ERROR en Levenshtein: {str(e)}")
        results.append(("Levenshtein", False))
    
    try:
        # Prueba 2: TF-IDF + Coseno
        result2 = test_tfidf_cosine()
        results.append(("TF-IDF + Coseno", result2))
    except Exception as e:
        print(f"❌ ERROR en TF-IDF + Coseno: {str(e)}")
        results.append(("TF-IDF + Coseno", False))
    
    try:
        # Prueba 3: Jaccard
        result3 = test_jaccard()
        results.append(("Jaccard", result3))
    except Exception as e:
        print(f"❌ ERROR en Jaccard: {str(e)}")
        results.append(("Jaccard", False))
    
    try:
        # Prueba 4: N-gramas
        result4 = test_ngrams()
        results.append(("N-gramas", result4))
    except Exception as e:
        print(f"❌ ERROR en N-gramas: {str(e)}")
        results.append(("N-gramas", False))
    
    # Resumen de resultados
    print("\n" + "="*80)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*80 + "\n")
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"   {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    else:
        print("⚠️ ALGUNAS PRUEBAS FALLARON")
    print("="*80 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
