"""
Tests para el Analizador de Frecuencias de Conceptos
=====================================================

Prueba todas las funcionalidades del ConceptAnalyzer:
1. Preprocesamiento de texto
2. Tokenización
3. Extracción de n-gramas
4. Análisis de conceptos predefinidos
5. Extracción automática de keywords (TF-IDF y frecuencia)
6. Cálculo de precisión
7. Generación de reportes completos

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

import sys
import os
import time

# Agregar el directorio Backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.ml_analysis.frequency import (
    ConceptAnalyzer,
    ExtractionMethod
)
from app.config.concepts import (
    get_generative_ai_concepts,
    GENERATIVE_AI_EDUCATION_CONCEPTS
)


# Textos de prueba (abstracts simulados)
ABSTRACT1 = """
Generative artificial intelligence has revolutionized education by providing
personalized learning experiences. Machine learning algorithms analyze student
performance and adapt content accordingly. This technology enables teachers
to focus on individual student needs while AI handles routine tasks.
The prompting techniques allow students to interact with AI systems effectively.
Transparency and ethics are crucial considerations in educational AI applications.
"""

ABSTRACT2 = """
The impact of generative models in educational settings is significant.
These AI systems create customized learning materials for students through
advanced machine learning techniques. Teachers can leverage fine-tuning
to adapt AI tools to their specific teaching methods and improve student outcomes.
Privacy concerns and algorithmic bias must be addressed in AI literacy programs.
"""

ABSTRACT3 = """
Multimodality in AI education enables students to learn through different formats.
Training data quality is essential for developing effective generative models.
Human-AI interaction patterns in educational contexts require careful analysis.
Explainability of AI decisions helps students understand how the technology works.
Co-creation between humans and AI systems opens new pedagogical possibilities.
"""

ABSTRACT4 = """
Machine learning and deep learning are fundamental to generative AI in education.
Natural language processing enables AI to understand and generate educational content.
Personalization through AI helps address individual learning needs and preferences.
The ethics of using AI in education requires ongoing discussion and policy development.
"""

ABSTRACT5 = """
AI literacy is essential for students and teachers in the modern educational landscape.
Generative models can support co-creation of learning materials and assessments.
Fine-tuning pre-trained models allows customization for specific educational domains.
Transparency in AI decision-making builds trust in educational technology systems.
"""


def print_separator(title="", char="=", length=80):
    """Imprime separador visual."""
    if title:
        print("\n" + char*length)
        print(title)
        print(char*length + "\n")
    else:
        print(char*length)


def test_initialization():
    """Prueba la inicialización del analizador."""
    print_separator("TEST 1: Inicializacion del ConceptAnalyzer")
    
    try:
        analyzer = ConceptAnalyzer(
            language='english',
            use_stemming=False,
            use_lemmatization=True,
            min_word_length=3,
            max_ngram_size=3
        )
        
        print("ConceptAnalyzer inicializado correctamente")
        print(f"  - Idioma: {analyzer.language}")
        print(f"  - Stemming: {analyzer.use_stemming}")
        print(f"  - Lemmatization: {analyzer.use_lemmatization}")
        print(f"  - Longitud minima: {analyzer.min_word_length}")
        print(f"  - Stopwords cargadas: {len(analyzer.stopwords)}")
        
        return True, analyzer
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False, None


def test_preprocessing(analyzer):
    """Prueba el preprocesamiento de texto."""
    print_separator("TEST 2: Preprocesamiento de Texto")
    
    try:
        test_text = "Machine-Learning & Deep Learning: AI Systems!"
        processed = analyzer.preprocess_text(test_text)
        
        print(f"Texto original: '{test_text}'")
        print(f"Texto procesado: '{processed}'")
        
        assert "machine learning" in processed
        assert "deep learning" in processed
        assert "ai systems" in processed
        assert "&" not in processed
        assert ":" not in processed
        
        print("Preprocesamiento funcionando correctamente")
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_tokenization(analyzer):
    """Prueba la tokenización."""
    print_separator("TEST 3: Tokenizacion")
    
    try:
        text = "Machine learning enables personalized education for students"
        
        # Sin eliminar stopwords
        tokens_with_stop = analyzer.tokenize(text, remove_stopwords=False)
        print(f"Tokens (con stopwords): {tokens_with_stop}")
        
        # Eliminando stopwords
        tokens_no_stop = analyzer.tokenize(text, remove_stopwords=True)
        print(f"Tokens (sin stopwords): {tokens_no_stop}")
        
        assert len(tokens_no_stop) < len(tokens_with_stop)
        assert "machine" in tokens_no_stop or "learning" in tokens_no_stop
        
        print("Tokenizacion funcionando correctamente")
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_ngram_extraction(analyzer):
    """Prueba la extracción de n-gramas."""
    print_separator("TEST 4: Extraccion de N-gramas")
    
    try:
        text = "Machine learning enables personalized education"
        
        bigrams = analyzer.extract_ngrams(text, n=2)
        print(f"Bigrams extraidos: {bigrams[:5]}")
        
        trigrams = analyzer.extract_ngrams(text, n=3)
        print(f"Trigrams extraidos: {trigrams[:3]}")
        
        assert len(bigrams) > 0
        print(f"Total bigrams: {len(bigrams)}, Total trigrams: {len(trigrams)}")
        
        print("Extraccion de n-gramas funcionando correctamente")
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_concept_finding(analyzer):
    """Prueba la búsqueda de conceptos en texto."""
    print_separator("TEST 5: Busqueda de Conceptos")
    
    try:
        text = ABSTRACT1
        concept = "machine learning"
        
        count, contexts = analyzer.find_concept_in_text(text, concept, context_window=40)
        
        print(f"Concepto: '{concept}'")
        print(f"Ocurrencias: {count}")
        print(f"Contextos encontrados:")
        for i, ctx in enumerate(contexts[:2], 1):
            print(f"  {i}. {ctx}")
        
        assert count > 0
        assert len(contexts) == count
        
        print("Busqueda de conceptos funcionando correctamente")
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_predefined_analysis(analyzer):
    """Prueba el análisis de conceptos predefinidos."""
    print_separator("TEST 6: Analisis de Conceptos Predefinidos")
    
    try:
        abstracts = [ABSTRACT1, ABSTRACT2, ABSTRACT3, ABSTRACT4, ABSTRACT5]
        concepts = get_generative_ai_concepts()
        
        print(f"Analizando {len(concepts)} conceptos en {len(abstracts)} abstracts...")
        
        start_time = time.time()
        results = analyzer.analyze_predefined_concepts(abstracts, concepts)
        elapsed = time.time() - start_time
        
        print(f"Analisis completado en {elapsed:.2f} segundos\n")
        
        # Mostrar top 10 conceptos más frecuentes
        sorted_results = sorted(
            results.items(),
            key=lambda x: x[1].total_occurrences,
            reverse=True
        )
        
        print("Top 10 conceptos mas frecuentes:")
        for i, (concept, freq) in enumerate(sorted_results[:10], 1):
            print(f"{i:2}. {concept:25} - {freq.total_occurrences:3} ocurrencias "
                  f"en {freq.document_frequency} documentos "
                  f"({freq.relative_frequency*100:.2f}%)")
        
        # Verificar que se encontraron conceptos
        total_occurrences = sum(f.total_occurrences for f in results.values())
        assert total_occurrences > 0, "No se encontraron ocurrencias de conceptos"
        
        print(f"\nTotal de ocurrencias encontradas: {total_occurrences}")
        print("Analisis de conceptos predefinidos funcionando correctamente")
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_tfidf_extraction(analyzer):
    """Prueba la extracción de keywords con TF-IDF."""
    print_separator("TEST 7: Extraccion de Keywords con TF-IDF")
    
    try:
        abstracts = [ABSTRACT1, ABSTRACT2, ABSTRACT3, ABSTRACT4, ABSTRACT5]
        
        print(f"Extrayendo keywords de {len(abstracts)} abstracts...")
        
        start_time = time.time()
        keywords = analyzer.extract_keywords_tfidf(
            abstracts,
            max_keywords=15,
            ngram_range=(1, 2)
        )
        elapsed = time.time() - start_time
        
        print(f"Extraccion completada en {elapsed:.2f} segundos\n")
        
        print("Keywords extraidos con TF-IDF:")
        for i, kw in enumerate(keywords, 1):
            print(f"{i:2}. {kw.keyword:30} - Score: {kw.score:.4f}, Freq: {kw.frequency}")
        
        assert len(keywords) > 0
        assert len(keywords) <= 15
        
        print(f"\nTotal de keywords extraidos: {len(keywords)}")
        print("Extraccion TF-IDF funcionando correctamente")
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_frequency_extraction(analyzer):
    """Prueba la extracción de keywords por frecuencia."""
    print_separator("TEST 8: Extraccion de Keywords por Frecuencia")
    
    try:
        abstracts = [ABSTRACT1, ABSTRACT2, ABSTRACT3, ABSTRACT4, ABSTRACT5]
        
        print(f"Extrayendo keywords de {len(abstracts)} abstracts...")
        
        start_time = time.time()
        keywords = analyzer.extract_keywords_frequency(
            abstracts,
            max_keywords=15,
            include_ngrams=True
        )
        elapsed = time.time() - start_time
        
        print(f"Extraccion completada en {elapsed:.2f} segundos\n")
        
        print("Keywords extraidos por frecuencia:")
        for i, kw in enumerate(keywords, 1):
            print(f"{i:2}. {kw.keyword:30} - Frecuencia: {kw.frequency}")
        
        assert len(keywords) > 0
        assert len(keywords) <= 15
        
        print(f"\nTotal de keywords extraidos: {len(keywords)}")
        print("Extraccion por frecuencia funcionando correctamente")
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_precision_calculation(analyzer):
    """Prueba el cálculo de precisión."""
    print_separator("TEST 9: Calculo de Precision")
    
    try:
        abstracts = [ABSTRACT1, ABSTRACT2, ABSTRACT3, ABSTRACT4, ABSTRACT5]
        predefined_concepts = get_generative_ai_concepts()
        
        # Extraer keywords
        extracted_keywords = analyzer.extract_keywords(
            abstracts,
            max_keywords=15,
            method=ExtractionMethod.TFIDF
        )
        
        # Calcular precisión
        precision_metrics = analyzer.calculate_precision(
            extracted_keywords,
            predefined_concepts,
            threshold=0.7
        )
        
        print("Metricas de Precision:")
        print(f"  - Precision: {precision_metrics['precision']:.2%}")
        print(f"  - Recall: {precision_metrics['recall']:.2%}")
        print(f"  - F1-Score: {precision_metrics['f1_score']:.2%}")
        print(f"  - Coincidencias exactas: {precision_metrics['num_exact_matches']}")
        print(f"  - Coincidencias parciales: {precision_metrics['num_partial_matches']}")
        print(f"  - Sin coincidencia: {precision_metrics['num_no_match']}")
        
        if precision_metrics['exact_matches']:
            print(f"\nCoincidencias exactas:")
            for match in precision_metrics['exact_matches'][:5]:
                print(f"  - {match}")
        
        if precision_metrics['partial_matches']:
            print(f"\nCoincidencias parciales:")
            for match in precision_metrics['partial_matches'][:5]:
                print(f"  - '{match['extracted']}' ~ '{match['predefined']}' "
                      f"(similitud: {match['similarity']})")
        
        print("Calculo de precision funcionando correctamente")
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_full_report(analyzer):
    """Prueba la generación de reporte completo."""
    print_separator("TEST 10: Generacion de Reporte Completo")
    
    try:
        abstracts = [ABSTRACT1, ABSTRACT2, ABSTRACT3, ABSTRACT4, ABSTRACT5]
        predefined_concepts = get_generative_ai_concepts()
        
        print(f"Generando reporte completo...")
        
        start_time = time.time()
        report = analyzer.generate_frequency_report(
            abstracts,
            predefined_concepts,
            max_keywords=15
        )
        elapsed = time.time() - start_time
        
        print(f"Reporte generado en {elapsed:.2f} segundos\n")
        
        # Mostrar estadísticas del corpus
        stats = report['corpus_statistics']
        print("Estadisticas del Corpus:")
        print(f"  - Total de abstracts: {stats['total_abstracts']}")
        print(f"  - Total de palabras: {stats['total_words']}")
        print(f"  - Promedio palabras/abstract: {stats['average_abstract_length']:.1f}")
        print(f"  - Palabras unicas: {stats['unique_words']}")
        
        # Mostrar resumen de precisión
        precision = report['precision_metrics']
        print(f"\nResumen de Precision:")
        print(f"  - Precision: {precision['precision']:.2%}")
        print(f"  - Recall: {precision['recall']:.2%}")
        print(f"  - F1-Score: {precision['f1_score']:.2%}")
        
        # Verificar estructura del reporte
        assert 'corpus_statistics' in report
        assert 'predefined_concepts' in report
        assert 'extracted_keywords' in report
        assert 'precision_metrics' in report
        
        print("\nGeneracion de reporte funcionando correctamente")
        return True
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal de pruebas."""
    print("\n" + "="*80)
    print("PRUEBAS DEL ANALIZADOR DE FRECUENCIAS - REQUERIMIENTO 3")
    print("Proyecto de Analisis Bibliometrico")
    print("Universidad del Quindio - 2025-2")
    print("="*80)
    
    results = []
    total_start = time.time()
    
    # Test 1: Inicialización
    success, analyzer = test_initialization()
    results.append(("Inicializacion", success))
    
    if not success or not analyzer:
        print("\nERROR CRITICO: No se pudo inicializar el analizador")
        print("Verifica que NLTK y scikit-learn esten instalados")
        return 1
    
    # Tests restantes
    tests = [
        ("Preprocesamiento", lambda: test_preprocessing(analyzer)),
        ("Tokenizacion", lambda: test_tokenization(analyzer)),
        ("N-gramas", lambda: test_ngram_extraction(analyzer)),
        ("Busqueda de Conceptos", lambda: test_concept_finding(analyzer)),
        ("Analisis Predefinidos", lambda: test_predefined_analysis(analyzer)),
        ("TF-IDF Extraction", lambda: test_tfidf_extraction(analyzer)),
        ("Frequency Extraction", lambda: test_frequency_extraction(analyzer)),
        ("Calculo Precision", lambda: test_precision_calculation(analyzer)),
        ("Reporte Completo", lambda: test_full_report(analyzer))
    ]
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\nERROR en {name}: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Resumen
    total_time = time.time() - total_start
    
    print_separator("RESUMEN DE PRUEBAS")
    
    for name, result in results:
        status = "PASO" if result else "FALLO"
        symbol = "OK" if result else "X"
        print(f"   [{symbol}] {name:25} - {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} pruebas pasaron ({(passed/total)*100:.1f}%)")
    print(f"Tiempo total: {total_time:.2f}s")
    
    print("\n" + "="*80)
    if passed == total:
        print("TODAS LAS PRUEBAS PASARON - ANALIZADOR FUNCIONANDO CORRECTAMENTE")
    else:
        print(f"ATENCION: {total - passed} prueba(s) fallaron")
    print("="*80 + "\n")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
