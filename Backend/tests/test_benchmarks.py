"""
Performance Benchmarks para Análisis de Algoritmos
==================================================

Benchmarks de rendimiento para los algoritmos principales del proyecto.

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
University: Universidad del Quindío - Análisis de Algoritmos
"""

import pytest
from app.services.ml_analysis.similarity import (
    LevenshteinSimilarity,
    TFIDFCosineSimilarity,
    JaccardSimilarity,
    NGramSimilarity,
    SentenceBERTSimilarity
)
from app.services.ml_analysis.frequency import ConceptAnalyzer, ExtractionMethod
from app.services.ml_analysis.clustering import HierarchicalClustering, LinkageMethod


# ============================================================================
# DATOS DE PRUEBA
# ============================================================================

# Texto corto (100 caracteres)
SHORT_TEXT_1 = "Machine learning is a subset of artificial intelligence that enables systems to learn from data."
SHORT_TEXT_2 = "Machine learning allows computers to learn and improve from experience without being explicitly programmed."

# Texto medio (500 caracteres)
MEDIUM_TEXT_1 = """
Generative AI represents a significant advancement in artificial intelligence technology.
It can create new content including text, images, music, and code based on patterns learned 
from training data. Large language models like GPT and Claude demonstrate remarkable 
capabilities in understanding context and generating human-like responses. These models 
are trained on massive datasets and use transformer architectures to process information 
efficiently. The applications of generative AI span across education, healthcare, 
entertainment, and software development.
"""

MEDIUM_TEXT_2 = """
Artificial intelligence has evolved dramatically with the introduction of generative models.
These systems can produce original content such as articles, artwork, melodies, and programs
by learning from extensive training datasets. Modern language models exhibit impressive
abilities in contextual understanding and natural language generation. They leverage
transformer-based neural networks and are trained on billions of parameters. Generative AI
finds applications in diverse fields including teaching, medicine, creative arts, and
programming assistance.
"""

# Texto largo (1000+ caracteres)
LONG_TEXT_1 = """
The field of machine learning has revolutionized how we approach problem-solving in computer science.
At its core, machine learning enables computers to learn patterns from data without being explicitly
programmed for every scenario. This paradigm shift has led to breakthrough applications across 
numerous domains including natural language processing, computer vision, and predictive analytics.

Deep learning, a subset of machine learning, uses artificial neural networks with multiple layers
to progressively extract higher-level features from raw input. These networks are inspired by the
structure of the human brain and have proven exceptionally effective at tasks such as image
recognition, speech processing, and game playing. The availability of large datasets and powerful
GPU computing has accelerated progress in this area dramatically.

Supervised learning remains one of the most widely used approaches, where models learn from labeled
training data to make predictions on unseen examples. Common algorithms include decision trees,
support vector machines, and neural networks. Unsupervised learning, on the other hand, discovers
hidden patterns in unlabeled data through techniques like clustering and dimensionality reduction.
"""

LONG_TEXT_2 = """
Machine learning has fundamentally transformed computational problem-solving methodologies.
The technology allows computer systems to identify patterns within data without requiring
explicit programming for each specific case. This revolutionary approach has enabled significant
advances in areas such as language understanding, visual recognition, and forecasting models.

Neural networks with deep architectures, known as deep learning systems, extract increasingly
abstract features from input data through multiple processing layers. These computational models
draw inspiration from biological neural structures and excel at complex tasks including visual
classification, audio analysis, and strategic game decisions. The combination of massive datasets
and advanced graphics processing units has greatly accelerated development in this field.

In supervised learning scenarios, models are trained on labeled datasets to generate accurate
predictions for new data points. Popular techniques include tree-based methods, kernel machines,
and multilayer perceptrons. Conversely, unsupervised methods uncover latent structures in
unlabeled datasets using approaches like grouping algorithms and feature space compression.
"""

# Lista de abstracts para clustering
TEST_ABSTRACTS = [
    "Machine learning enables computers to learn from data and improve their performance over time.",
    "Deep learning uses neural networks with multiple layers to extract features from raw data.",
    "Natural language processing allows computers to understand and generate human language.",
    "Computer vision enables machines to interpret and understand visual information from images.",
    "Reinforcement learning teaches agents to make decisions through trial and error.",
    "Supervised learning trains models on labeled data to make predictions on new examples.",
    "Unsupervised learning discovers patterns in unlabeled data through clustering and dimensionality reduction.",
    "Transfer learning leverages knowledge from one task to improve performance on another related task."
]


# ============================================================================
# BENCHMARKS DE SIMILITUD
# ============================================================================

class TestSimilarityBenchmarks:
    """Benchmarks para algoritmos de similitud."""
    
    def test_benchmark_levenshtein_short(self, benchmark):
        """Benchmark: Levenshtein con textos cortos (100 chars)."""
        algo = LevenshteinSimilarity()
        result = benchmark(algo.calculate_similarity, SHORT_TEXT_1, SHORT_TEXT_2)
        assert 0 <= result <= 1
    
    def test_benchmark_levenshtein_medium(self, benchmark):
        """Benchmark: Levenshtein con textos medios (500 chars)."""
        algo = LevenshteinSimilarity()
        result = benchmark(algo.calculate_similarity, MEDIUM_TEXT_1, MEDIUM_TEXT_2)
        assert 0 <= result <= 1
    
    def test_benchmark_tfidf_short(self, benchmark):
        """Benchmark: TF-IDF con textos cortos."""
        algo = TFIDFCosineSimilarity()
        result = benchmark(algo.calculate_similarity, SHORT_TEXT_1, SHORT_TEXT_2)
        assert 0 <= result <= 1
    
    def test_benchmark_tfidf_medium(self, benchmark):
        """Benchmark: TF-IDF con textos medios."""
        algo = TFIDFCosineSimilarity()
        result = benchmark(algo.calculate_similarity, MEDIUM_TEXT_1, MEDIUM_TEXT_2)
        assert 0 <= result <= 1
    
    def test_benchmark_tfidf_long(self, benchmark):
        """Benchmark: TF-IDF con textos largos (1000+ chars)."""
        algo = TFIDFCosineSimilarity()
        result = benchmark(algo.calculate_similarity, LONG_TEXT_1, LONG_TEXT_2)
        assert 0 <= result <= 1
    
    def test_benchmark_jaccard_medium(self, benchmark):
        """Benchmark: Jaccard con textos medios."""
        algo = JaccardSimilarity()
        result = benchmark(algo.calculate_similarity, MEDIUM_TEXT_1, MEDIUM_TEXT_2)
        assert 0 <= result <= 1
    
    def test_benchmark_ngram_char(self, benchmark):
        """Benchmark: N-grams de caracteres (n=3)."""
        algo = NGramSimilarity(n=3, ngram_type='char')
        result = benchmark(algo.calculate_similarity, MEDIUM_TEXT_1, MEDIUM_TEXT_2)
        assert 0 <= result <= 1
    
    def test_benchmark_ngram_word(self, benchmark):
        """Benchmark: N-grams de palabras (n=2)."""
        algo = NGramSimilarity(n=2, ngram_type='word')
        result = benchmark(algo.calculate_similarity, MEDIUM_TEXT_1, MEDIUM_TEXT_2)
        assert 0 <= result <= 1
    
    def test_benchmark_sentence_bert_medium(self, benchmark):
        """Benchmark: Sentence-BERT con textos medios."""
        algo = SentenceBERTSimilarity()
        result = benchmark(algo.calculate_similarity, MEDIUM_TEXT_1, MEDIUM_TEXT_2)
        assert 0 <= result <= 1


# ============================================================================
# BENCHMARKS DE FRECUENCIA
# ============================================================================

class TestFrequencyBenchmarks:
    """Benchmarks para análisis de frecuencias."""
    
    def test_benchmark_concept_analysis_predefined(self, benchmark):
        """Benchmark: Análisis de conceptos predefinidos."""
        analyzer = ConceptAnalyzer()
        
        # Conceptos predefinidos simples
        concepts = ["machine learning", "artificial intelligence", "deep learning"]
        
        result = benchmark(
            analyzer.analyze_predefined_concepts,
            TEST_ABSTRACTS,
            concepts
        )
        assert len(result) > 0
    
    def test_benchmark_tfidf_extraction(self, benchmark):
        """Benchmark: Extracción de keywords con TF-IDF."""
        analyzer = ConceptAnalyzer()
        result = benchmark(
            analyzer.extract_keywords_tfidf,
            TEST_ABSTRACTS,
            max_keywords=15
        )
        assert len(result) > 0
    
    def test_benchmark_frequency_extraction(self, benchmark):
        """Benchmark: Extracción de keywords por frecuencia."""
        analyzer = ConceptAnalyzer()
        result = benchmark(
            analyzer.extract_keywords_frequency,
            TEST_ABSTRACTS,
            max_keywords=15
        )
        assert len(result) > 0


# ============================================================================
# BENCHMARKS DE CLUSTERING
# ============================================================================

class TestClusteringBenchmarks:
    """Benchmarks para clustering jerárquico."""
    
    def test_benchmark_ward_clustering_small(self, benchmark):
        """Benchmark: Ward linkage con dataset pequeño (8 docs)."""
        clusterer = HierarchicalClustering()
        result = benchmark(
            clusterer.cluster_texts,
            TEST_ABSTRACTS,
            method=LinkageMethod.WARD,
            num_clusters=3,
            generate_plot=False
        )
        assert result.num_documents == len(TEST_ABSTRACTS)
    
    def test_benchmark_average_clustering(self, benchmark):
        """Benchmark: Average linkage con dataset pequeño."""
        clusterer = HierarchicalClustering()
        result = benchmark(
            clusterer.cluster_texts,
            TEST_ABSTRACTS,
            method=LinkageMethod.AVERAGE,
            num_clusters=3,
            generate_plot=False
        )
        assert result.num_documents == len(TEST_ABSTRACTS)
    
    def test_benchmark_complete_clustering(self, benchmark):
        """Benchmark: Complete linkage con dataset pequeño."""
        clusterer = HierarchicalClustering()
        result = benchmark(
            clusterer.cluster_texts,
            TEST_ABSTRACTS,
            method=LinkageMethod.COMPLETE,
            num_clusters=3,
            generate_plot=False
        )
        assert result.num_documents == len(TEST_ABSTRACTS)
    
    def test_benchmark_ward_with_dendrogram(self, benchmark):
        """Benchmark: Ward linkage con generación de dendrograma."""
        clusterer = HierarchicalClustering()
        result = benchmark(
            clusterer.cluster_texts,
            TEST_ABSTRACTS,
            method=LinkageMethod.WARD,
            num_clusters=3,
            generate_plot=True
        )
        assert result.dendrogram_data is not None


# ============================================================================
# BENCHMARKS COMPARATIVOS
# ============================================================================

class TestComparativeBenchmarks:
    """Benchmarks comparativos entre diferentes algoritmos."""
    
    def test_benchmark_all_similarity_algorithms(self, benchmark):
        """Benchmark: Comparar todos los algoritmos de similitud."""
        algorithms = [
            LevenshteinSimilarity(),
            TFIDFCosineSimilarity(),
            JaccardSimilarity(),
            NGramSimilarity(n=3, ngram_type='char'),
            SentenceBERTSimilarity()
        ]
        
        def run_all():
            results = []
            for algo in algorithms:
                score = algo.calculate_similarity(MEDIUM_TEXT_1, MEDIUM_TEXT_2)
                results.append(score)
            return results
        
        results = benchmark(run_all)
        assert len(results) == 5
        assert all(0 <= score <= 1 for score in results)
    
    def test_benchmark_all_linkage_methods(self, benchmark):
        """Benchmark: Comparar todos los métodos de linkage."""
        clusterer = HierarchicalClustering()
        methods = [LinkageMethod.WARD, LinkageMethod.AVERAGE, LinkageMethod.COMPLETE]
        
        def run_all():
            results = []
            for method in methods:
                result = clusterer.cluster_texts(
                    TEST_ABSTRACTS,
                    method=method,
                    num_clusters=3,
                    generate_plot=False
                )
                results.append(result)
            return results
        
        results = benchmark(run_all)
        assert len(results) == 3
        assert all(r.num_documents == len(TEST_ABSTRACTS) for r in results)
