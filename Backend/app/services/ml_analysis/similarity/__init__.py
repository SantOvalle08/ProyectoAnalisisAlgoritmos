"""
Módulo de Algoritmos de Similitud Textual
=========================================

Este módulo contiene implementaciones de 6 algoritmos de similitud textual:

ALGORITMOS CLÁSICOS (4):
1. Distancia de Levenshtein (Edit Distance)
2. TF-IDF + Similitud del Coseno
3. Coeficiente de Jaccard
4. Similitud por N-gramas

ALGORITMOS CON IA (2):
5. BERT Embeddings + Similitud del Coseno
6. Sentence-BERT

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

from .base_similarity import BaseSimilarity, SimilarityAlgorithmType
from .levenshtein import LevenshteinSimilarity
from .tfidf_cosine import TFIDFCosineSimilarity
from .jaccard import JaccardSimilarity
from .ngrams import NGramSimilarity
from .bert_embeddings import BERTEmbeddingsSimilarity
from .sentence_bert import SentenceBERTSimilarity

__all__ = [
    "BaseSimilarity",
    "SimilarityAlgorithmType",
    "LevenshteinSimilarity",
    "TFIDFCosineSimilarity",
    "JaccardSimilarity",
    "NGramSimilarity",
    "BERTEmbeddingsSimilarity",
    "SentenceBERTSimilarity",
]
