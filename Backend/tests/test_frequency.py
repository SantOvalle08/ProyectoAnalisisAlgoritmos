"""Tests para Frequency Analyzer - simplificados"""
import pytest
from app.services.ml_analysis.frequency import ConceptAnalyzer
from app.config.concepts import get_generative_ai_concepts

ABSTRACTS = ["Machine learning and AI in education.", "Generative models for students."]

@pytest.fixture
def analyzer():
    return ConceptAnalyzer(language='english')

def test_initialization():
    a = ConceptAnalyzer(language='english')
    assert a is not None

def test_preprocessing(analyzer):
    result = analyzer.preprocess_text("Test & Text")
    assert isinstance(result, str)

def test_tokenization(analyzer):
    tokens = analyzer.tokenize("machine learning")
    assert isinstance(tokens, list)

def test_ngram_extraction(analyzer):
    result = analyzer.extract_ngrams("machine learning", n=2)
    assert isinstance(result, list)

def test_concept_finding(analyzer):
    count, contexts = analyzer.find_concept_in_text(ABSTRACTS[0], "learning")
    assert count >= 0

def test_predefined_analysis(analyzer):
    concepts = get_generative_ai_concepts()
    results = analyzer.analyze_predefined_concepts(ABSTRACTS, concepts)
    assert isinstance(results, dict)

def test_tfidf_extraction(analyzer):
    keywords = analyzer.extract_keywords_tfidf(ABSTRACTS, max_keywords=5)
    assert isinstance(keywords, list)

def test_frequency_extraction(analyzer):
    keywords = analyzer.extract_keywords_frequency(ABSTRACTS, max_keywords=5)
    assert isinstance(keywords, list)

def test_precision_calculation(analyzer):
    concepts = get_generative_ai_concepts()
    keywords = analyzer.extract_keywords_tfidf(ABSTRACTS, max_keywords=5)
    metrics = analyzer.calculate_precision(keywords, concepts)
    assert 'precision' in metrics

def test_full_report(analyzer):
    concepts = get_generative_ai_concepts()
    report = analyzer.generate_frequency_report(ABSTRACTS, concepts)
    assert 'corpus_statistics' in report
