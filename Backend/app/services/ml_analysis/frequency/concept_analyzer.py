"""
Analizador de Frecuencias de Conceptos para Análisis Bibliométrico
===================================================================

Este módulo implementa el análisis de frecuencias de conceptos predefinidos
y la extracción automática de palabras clave desde abstracts científicos.

Requerimiento 3: Análisis de Frecuencias de Conceptos

Funcionalidades principales:
1. Análisis de frecuencias de conceptos predefinidos
2. Extracción automática de keywords usando múltiples algoritmos
3. Cálculo de métricas de precisión y relevancia
4. Análisis de co-ocurrencias y contextos

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
University: Universidad del Quindío - Análisis de Algoritmos
"""

import re
import logging
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import Counter, defaultdict
from dataclasses import dataclass, field
import numpy as np
from enum import Enum

# NLP libraries
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    from nltk.util import ngrams as nltk_ngrams
except ImportError:
    nltk = None

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    TfidfVectorizer = None


# Configurar logging
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS Y DATACLASSES
# ============================================================================

class ExtractionMethod(str, Enum):
    """Métodos de extracción de keywords."""
    TFIDF = "tfidf"
    FREQUENCY = "frequency"
    NGRAMS = "ngrams"
    COMBINED = "combined"


@dataclass
class ConceptFrequency:
    """Representa la frecuencia de un concepto en el corpus."""
    concept: str
    total_occurrences: int
    document_frequency: int  # En cuántos documentos aparece
    relative_frequency: float  # Porcentaje del total de palabras
    documents_with_concept: List[int] = field(default_factory=list)
    contexts: List[str] = field(default_factory=list)  # Contextos donde aparece
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return {
            "concept": self.concept,
            "total_occurrences": self.total_occurrences,
            "document_frequency": self.document_frequency,
            "relative_frequency": round(self.relative_frequency, 4),
            "documents_with_concept": self.documents_with_concept[:10],  # Primeros 10
            "example_contexts": self.contexts[:3]  # Primeros 3 contextos
        }


@dataclass
class KeywordScore:
    """Representa un keyword extraído con su score."""
    keyword: str
    score: float
    method: str
    frequency: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario."""
        return {
            "keyword": self.keyword,
            "score": round(self.score, 4),
            "method": self.method,
            "frequency": self.frequency
        }


# ============================================================================
# CLASE PRINCIPAL: CONCEPT ANALYZER
# ============================================================================

class ConceptAnalyzer:
    """
    Analizador de conceptos y extractor de keywords para análisis bibliométrico.
    
    Funcionalidades:
    1. Análisis de frecuencias de conceptos predefinidos
    2. Extracción automática de keywords usando TF-IDF
    3. Extracción de n-gramas relevantes
    4. Cálculo de métricas de precisión
    5. Análisis de contextos y co-ocurrencias
    
    Algoritmos implementados:
    - TF-IDF (Term Frequency-Inverse Document Frequency)
    - Frequency-based ranking
    - N-gram extraction
    - Stopwords filtering
    - Stemming/Lemmatization
    
    Ejemplo de uso:
    ```python
    analyzer = ConceptAnalyzer(language='english')
    
    # Analizar conceptos predefinidos
    predefined = ["machine learning", "deep learning", "neural networks"]
    abstracts = ["Machine learning is...", "Deep learning uses..."]
    results = analyzer.analyze_predefined_concepts(abstracts, predefined)
    
    # Extraer keywords automáticamente
    keywords = analyzer.extract_keywords(abstracts, max_keywords=15)
    
    # Calcular precisión
    precision = analyzer.calculate_precision(keywords, predefined)
    ```
    """
    
    def __init__(
        self,
        language: str = 'english',
        use_stemming: bool = False,
        use_lemmatization: bool = True,
        min_word_length: int = 3,
        max_ngram_size: int = 3
    ):
        """
        Inicializa el analizador de conceptos.
        
        Args:
            language: Idioma para stopwords ('english', 'spanish')
            use_stemming: Usar stemming (Porter Stemmer)
            use_lemmatization: Usar lemmatization (WordNet)
            min_word_length: Longitud mínima de palabras a considerar
            max_ngram_size: Tamaño máximo de n-gramas (1=unigrams, 2=bigrams, etc.)
        """
        self.language = language
        self.use_stemming = use_stemming
        self.use_lemmatization = use_lemmatization
        self.min_word_length = min_word_length
        self.max_ngram_size = max_ngram_size
        
        # Inicializar componentes NLP
        self._initialize_nlp_components()
        
        logger.info(f"ConceptAnalyzer inicializado con idioma={language}, "
                   f"stemming={use_stemming}, lemmatization={use_lemmatization}")
    
    def _initialize_nlp_components(self):
        """Inicializa componentes de NLTK."""
        if nltk is None:
            logger.warning("NLTK no está instalado. Funcionalidad limitada.")
            self.stopwords = set()
            self.stemmer = None
            self.lemmatizer = None
            return
        
        try:
            # Descargar recursos necesarios si no existen
            required_resources = [
                'stopwords',
                'punkt',
                'wordnet',
                'averaged_perceptron_tagger'
            ]
            
            for resource in required_resources:
                try:
                    nltk.data.find(f'corpora/{resource}' if resource in ['stopwords', 'wordnet'] 
                                  else f'tokenizers/{resource}')
                except LookupError:
                    logger.info(f"Descargando recurso NLTK: {resource}")
                    nltk.download(resource, quiet=True)
            
            # Cargar stopwords
            self.stopwords = set(stopwords.words(self.language))
            
            # Agregar stopwords personalizadas comunes en textos científicos
            custom_stopwords = {
                'abstract', 'introduction', 'conclusion', 'results', 'methods',
                'discussion', 'paper', 'study', 'research', 'analysis', 'approach',
                'using', 'based', 'proposed', 'novel', 'present', 'show', 'et', 'al',
                'also', 'however', 'therefore', 'thus', 'furthermore', 'moreover'
            }
            self.stopwords.update(custom_stopwords)
            
            # Inicializar stemmer y lemmatizer
            self.stemmer = PorterStemmer() if self.use_stemming else None
            self.lemmatizer = WordNetLemmatizer() if self.use_lemmatization else None
            
            logger.info(f"Componentes NLP inicializados. Stopwords: {len(self.stopwords)}")
            
        except Exception as e:
            logger.error(f"Error inicializando componentes NLP: {str(e)}")
            self.stopwords = set()
            self.stemmer = None
            self.lemmatizer = None
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocesa un texto para análisis.
        
        Pasos:
        1. Convertir a minúsculas
        2. Eliminar caracteres especiales (excepto espacios y guiones)
        3. Normalizar espacios
        
        Args:
            text: Texto a preprocesar
        
        Returns:
            Texto preprocesado
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Reemplazar guiones por espacios (para frases como "machine-learning")
        text = text.replace('-', ' ')
        
        # Eliminar caracteres especiales, mantener solo letras, números y espacios
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        
        # Normalizar espacios múltiples
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text: str, remove_stopwords: bool = True) -> List[str]:
        """
        Tokeniza un texto en palabras.
        
        Args:
            text: Texto a tokenizar
            remove_stopwords: Si eliminar stopwords
        
        Returns:
            Lista de tokens
        """
        if not text:
            return []
        
        # Preprocesar
        text = self.preprocess_text(text)
        
        # Tokenizar
        if nltk:
            tokens = word_tokenize(text)
        else:
            # Fallback simple
            tokens = text.split()
        
        # Filtrar por longitud mínima
        tokens = [t for t in tokens if len(t) >= self.min_word_length]
        
        # Eliminar stopwords
        if remove_stopwords and self.stopwords:
            tokens = [t for t in tokens if t not in self.stopwords]
        
        # Aplicar stemming o lemmatization
        if self.use_stemming and self.stemmer:
            tokens = [self.stemmer.stem(t) for t in tokens]
        elif self.use_lemmatization and self.lemmatizer:
            tokens = [self.lemmatizer.lemmatize(t) for t in tokens]
        
        return tokens
    
    def extract_ngrams(
        self,
        text: str,
        n: int = 2,
        remove_stopwords: bool = True
    ) -> List[str]:
        """
        Extrae n-gramas de un texto.
        
        Args:
            text: Texto fuente
            n: Tamaño de n-gramas (2=bigrams, 3=trigrams)
            remove_stopwords: Si eliminar stopwords
        
        Returns:
            Lista de n-gramas como strings
        """
        tokens = self.tokenize(text, remove_stopwords=remove_stopwords)
        
        if len(tokens) < n:
            return []
        
        # Generar n-gramas
        ngrams_list = list(nltk_ngrams(tokens, n)) if nltk else []
        
        # Convertir tuplas a strings
        ngrams_strings = [' '.join(ngram) for ngram in ngrams_list]
        
        return ngrams_strings
    
    def find_concept_in_text(
        self,
        text: str,
        concept: str,
        context_window: int = 50
    ) -> Tuple[int, List[str]]:
        """
        Busca un concepto en un texto y extrae contextos.
        
        El concepto puede ser una palabra simple o una frase multi-palabra.
        La búsqueda es case-insensitive.
        
        Args:
            text: Texto donde buscar
            concept: Concepto a buscar (ej: "machine learning")
            context_window: Caracteres de contexto antes/después
        
        Returns:
            Tupla (count, contexts) donde:
            - count: Número de ocurrencias
            - contexts: Lista de fragmentos de contexto
        """
        if not text or not concept:
            return 0, []
        
        # Preprocesar concepto y texto
        concept_lower = concept.lower()
        text_lower = text.lower()
        
        # Contar ocurrencias
        count = text_lower.count(concept_lower)
        
        if count == 0:
            return 0, []
        
        # Extraer contextos
        contexts = []
        start = 0
        
        while True:
            # Encontrar siguiente ocurrencia
            pos = text_lower.find(concept_lower, start)
            
            if pos == -1:
                break
            
            # Extraer contexto
            context_start = max(0, pos - context_window)
            context_end = min(len(text), pos + len(concept) + context_window)
            
            context = text[context_start:context_end].strip()
            
            # Agregar elipsis si el contexto está truncado
            if context_start > 0:
                context = "..." + context
            if context_end < len(text):
                context = context + "..."
            
            contexts.append(context)
            
            # Continuar búsqueda después de esta ocurrencia
            start = pos + len(concept)
        
        return count, contexts
    
    def analyze_predefined_concepts(
        self,
        abstracts: List[str],
        concepts: List[str]
    ) -> Dict[str, ConceptFrequency]:
        """
        Analiza la frecuencia de conceptos predefinidos en un corpus de abstracts.
        
        Para cada concepto calcula:
        - Frecuencia total (total de ocurrencias)
        - Frecuencia documental (en cuántos documentos aparece)
        - Frecuencia relativa (porcentaje)
        - Documentos donde aparece
        - Contextos de aparición
        
        Args:
            abstracts: Lista de abstracts a analizar
            concepts: Lista de conceptos predefinidos a buscar
        
        Returns:
            Diccionario {concepto: ConceptFrequency}
        
        Ejemplo:
        ```python
        abstracts = [
            "Machine learning is a subset of artificial intelligence...",
            "Deep learning uses neural networks..."
        ]
        concepts = ["machine learning", "deep learning", "neural networks"]
        results = analyzer.analyze_predefined_concepts(abstracts, concepts)
        
        for concept, freq in results.items():
            print(f"{concept}: {freq.total_occurrences} occurrences")
        ```
        """
        logger.info(f"Analizando {len(concepts)} conceptos en {len(abstracts)} abstracts")
        
        results = {}
        
        # Contar total de palabras en el corpus (para frecuencia relativa)
        total_words = sum(len(self.tokenize(abstract)) for abstract in abstracts)
        
        for concept in concepts:
            total_occurrences = 0
            documents_with_concept = []
            all_contexts = []
            
            # Buscar en cada abstract
            for doc_idx, abstract in enumerate(abstracts):
                count, contexts = self.find_concept_in_text(abstract, concept)
                
                if count > 0:
                    total_occurrences += count
                    documents_with_concept.append(doc_idx)
                    all_contexts.extend(contexts)
            
            # Calcular frecuencia relativa
            relative_freq = (total_occurrences / total_words) if total_words > 0 else 0.0
            
            # Crear objeto ConceptFrequency
            freq_obj = ConceptFrequency(
                concept=concept,
                total_occurrences=total_occurrences,
                document_frequency=len(documents_with_concept),
                relative_frequency=relative_freq,
                documents_with_concept=documents_with_concept,
                contexts=all_contexts[:10]  # Guardar máximo 10 contextos
            )
            
            results[concept] = freq_obj
            
            logger.debug(f"Concepto '{concept}': {total_occurrences} ocurrencias "
                        f"en {len(documents_with_concept)} documentos")
        
        return results
    
    def extract_keywords_tfidf(
        self,
        abstracts: List[str],
        max_keywords: int = 15,
        max_features: int = 1000,
        ngram_range: Tuple[int, int] = (1, 3)
    ) -> List[KeywordScore]:
        """
        Extrae keywords usando TF-IDF (Term Frequency-Inverse Document Frequency).
        
        TF-IDF es un método estadístico que evalúa la importancia de una palabra
        en un documento relativo a un corpus de documentos.
        
        Fórmula:
        - TF (Term Frequency) = (Frecuencia del término en el documento) / (Total de términos en el documento)
        - IDF (Inverse Document Frequency) = log(Total de documentos / Documentos que contienen el término)
        - TF-IDF = TF * IDF
        
        Args:
            abstracts: Lista de abstracts
            max_keywords: Número máximo de keywords a extraer
            max_features: Tamaño máximo del vocabulario
            ngram_range: Rango de n-gramas (1,1)=solo palabras, (1,2)=palabras y bigramas
        
        Returns:
            Lista de KeywordScore ordenada por score descendente
        """
        if not TfidfVectorizer:
            logger.error("scikit-learn no está instalado")
            return []
        
        if not abstracts:
            return []
        
        logger.info(f"Extrayendo keywords con TF-IDF (max={max_keywords}, "
                   f"features={max_features}, ngrams={ngram_range})")
        
        try:
            # Crear vectorizador TF-IDF
            vectorizer = TfidfVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                stop_words=list(self.stopwords) if self.stopwords else None,
                min_df=1,  # Mínimo 1 documento
                max_df=0.8,  # Máximo 80% de documentos (para evitar términos muy comunes)
                sublinear_tf=True,  # Aplicar escala logarítmica a TF
                lowercase=True
            )
            
            # Calcular matriz TF-IDF
            tfidf_matrix = vectorizer.fit_transform(abstracts)
            
            # Obtener nombres de features
            feature_names = vectorizer.get_feature_names_out()
            
            # Calcular score promedio de cada término en todo el corpus
            avg_tfidf_scores = np.asarray(tfidf_matrix.mean(axis=0)).flatten()
            
            # Crear lista de (término, score)
            term_scores = list(zip(feature_names, avg_tfidf_scores))
            
            # Ordenar por score descendente
            term_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Tomar top max_keywords
            top_terms = term_scores[:max_keywords]
            
            # Crear objetos KeywordScore
            keywords = []
            for term, score in top_terms:
                # Contar frecuencia total del término
                freq = sum(abstract.lower().count(term.lower()) for abstract in abstracts)
                
                keywords.append(KeywordScore(
                    keyword=term,
                    score=float(score),
                    method="tfidf",
                    frequency=freq
                ))
            
            logger.info(f"Extraídos {len(keywords)} keywords con TF-IDF")
            
            return keywords
            
        except Exception as e:
            logger.error(f"Error en extracción TF-IDF: {str(e)}")
            return []
    
    def extract_keywords_frequency(
        self,
        abstracts: List[str],
        max_keywords: int = 15,
        include_ngrams: bool = True
    ) -> List[KeywordScore]:
        """
        Extrae keywords basándose en frecuencia simple.
        
        Este método cuenta la frecuencia de palabras y n-gramas en el corpus
        y retorna los más frecuentes, excluyendo stopwords.
        
        Args:
            abstracts: Lista de abstracts
            max_keywords: Número máximo de keywords
            include_ngrams: Si incluir bigramas y trigramas
        
        Returns:
            Lista de KeywordScore ordenada por frecuencia
        """
        logger.info(f"Extrayendo keywords por frecuencia (max={max_keywords})")
        
        all_terms = []
        
        for abstract in abstracts:
            # Agregar unigrams (palabras individuales)
            tokens = self.tokenize(abstract, remove_stopwords=True)
            all_terms.extend(tokens)
            
            # Agregar n-gramas si está habilitado
            if include_ngrams:
                for n in range(2, self.max_ngram_size + 1):
                    ngrams = self.extract_ngrams(abstract, n=n)
                    all_terms.extend(ngrams)
        
        # Contar frecuencias
        term_counts = Counter(all_terms)
        
        # Obtener los más comunes
        most_common = term_counts.most_common(max_keywords)
        
        # Crear objetos KeywordScore
        keywords = [
            KeywordScore(
                keyword=term,
                score=float(count),
                method="frequency",
                frequency=count
            )
            for term, count in most_common
        ]
        
        logger.info(f"Extraídos {len(keywords)} keywords por frecuencia")
        
        return keywords
    
    def extract_keywords(
        self,
        abstracts: List[str],
        max_keywords: int = 15,
        method: ExtractionMethod = ExtractionMethod.TFIDF
    ) -> List[KeywordScore]:
        """
        Extrae keywords usando el método especificado.
        
        Args:
            abstracts: Lista de abstracts
            max_keywords: Número máximo de keywords
            method: Método de extracción
        
        Returns:
            Lista de KeywordScore
        """
        if method == ExtractionMethod.TFIDF:
            return self.extract_keywords_tfidf(abstracts, max_keywords)
        
        elif method == ExtractionMethod.FREQUENCY:
            return self.extract_keywords_frequency(abstracts, max_keywords)
        
        elif method == ExtractionMethod.COMBINED:
            # Combinar TF-IDF y frecuencia
            tfidf_keywords = self.extract_keywords_tfidf(abstracts, max_keywords)
            freq_keywords = self.extract_keywords_frequency(abstracts, max_keywords)
            
            # Combinar y eliminar duplicados
            combined = {}
            for kw in tfidf_keywords + freq_keywords:
                if kw.keyword in combined:
                    # Promediar scores
                    combined[kw.keyword].score = (combined[kw.keyword].score + kw.score) / 2
                else:
                    combined[kw.keyword] = kw
            
            # Ordenar por score y tomar top max_keywords
            sorted_keywords = sorted(
                combined.values(),
                key=lambda x: x.score,
                reverse=True
            )[:max_keywords]
            
            for kw in sorted_keywords:
                kw.method = "combined"
            
            return sorted_keywords
        
        else:
            logger.error(f"Método de extracción no soportado: {method}")
            return []
    
    def calculate_precision(
        self,
        extracted_keywords: List[KeywordScore],
        predefined_concepts: List[str],
        threshold: float = 0.8
    ) -> Dict[str, Any]:
        """
        Calcula la precisión de los keywords extraídos comparándolos con conceptos predefinidos.
        
        Métricas calculadas:
        - Precision: (Keywords extraídos que coinciden con predefinidos) / (Total keywords extraídos)
        - Recall: (Conceptos predefinidos encontrados) / (Total conceptos predefinidos)
        - F1-Score: Media armónica de Precision y Recall
        - Coincidencias exactas
        - Coincidencias parciales (similitud > threshold)
        
        Args:
            extracted_keywords: Keywords extraídos automáticamente
            predefined_concepts: Conceptos predefinidos
            threshold: Umbral de similitud para coincidencias parciales
        
        Returns:
            Diccionario con métricas de precisión
        """
        logger.info(f"Calculando precisión: {len(extracted_keywords)} extraídos vs "
                   f"{len(predefined_concepts)} predefinidos")
        
        if not extracted_keywords or not predefined_concepts:
            return {
                "precision": 0.0,
                "recall": 0.0,
                "f1_score": 0.0,
                "exact_matches": [],
                "partial_matches": [],
                "total_extracted": len(extracted_keywords),
                "total_predefined": len(predefined_concepts)
            }
        
        # Convertir a minúsculas para comparación
        extracted_set = {kw.keyword.lower() for kw in extracted_keywords}
        predefined_set = {concept.lower() for concept in predefined_concepts}
        
        # Coincidencias exactas
        exact_matches = list(extracted_set.intersection(predefined_set))
        
        # Coincidencias parciales (usando similitud de Jaccard simple)
        partial_matches = []
        
        for extracted in extracted_set:
            if extracted in exact_matches:
                continue
            
            for predefined in predefined_set:
                # Similitud basada en palabras en común
                extracted_words = set(extracted.split())
                predefined_words = set(predefined.split())
                
                if not extracted_words or not predefined_words:
                    continue
                
                intersection = len(extracted_words.intersection(predefined_words))
                union = len(extracted_words.union(predefined_words))
                
                similarity = intersection / union if union > 0 else 0.0
                
                if similarity >= threshold:
                    partial_matches.append({
                        "extracted": extracted,
                        "predefined": predefined,
                        "similarity": round(similarity, 3)
                    })
                    break
        
        # Calcular métricas
        num_exact = len(exact_matches)
        num_partial = len(partial_matches)
        num_total_matches = num_exact + num_partial
        
        precision = num_total_matches / len(extracted_keywords) if extracted_keywords else 0.0
        recall = num_total_matches / len(predefined_concepts) if predefined_concepts else 0.0
        f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        results = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1_score, 4),
            "exact_matches": exact_matches,
            "partial_matches": partial_matches,
            "total_extracted": len(extracted_keywords),
            "total_predefined": len(predefined_concepts),
            "num_exact_matches": num_exact,
            "num_partial_matches": num_partial,
            "num_no_match": len(extracted_keywords) - num_total_matches
        }
        
        logger.info(f"Precisión: {precision:.2%}, Recall: {recall:.2%}, F1: {f1_score:.2%}")
        
        return results
    
    def generate_frequency_report(
        self,
        abstracts: List[str],
        predefined_concepts: List[str],
        max_keywords: int = 15
    ) -> Dict[str, Any]:
        """
        Genera un reporte completo de análisis de frecuencias.
        
        Incluye:
        - Análisis de conceptos predefinidos
        - Extracción automática de keywords
        - Cálculo de precisión
        - Estadísticas del corpus
        
        Args:
            abstracts: Lista de abstracts
            predefined_concepts: Conceptos predefinidos
            max_keywords: Máximo de keywords a extraer
        
        Returns:
            Diccionario con reporte completo
        """
        logger.info(f"Generando reporte de frecuencias para {len(abstracts)} abstracts")
        
        # Análisis de conceptos predefinidos
        predefined_results = self.analyze_predefined_concepts(abstracts, predefined_concepts)
        
        # Extracción de keywords
        extracted_keywords = self.extract_keywords(
            abstracts,
            max_keywords=max_keywords,
            method=ExtractionMethod.TFIDF
        )
        
        # Cálculo de precisión
        precision_metrics = self.calculate_precision(
            extracted_keywords,
            predefined_concepts
        )
        
        # Estadísticas del corpus
        total_words = sum(len(self.tokenize(abstract)) for abstract in abstracts)
        avg_abstract_length = total_words / len(abstracts) if abstracts else 0
        
        # Construir reporte
        report = {
            "corpus_statistics": {
                "total_abstracts": len(abstracts),
                "total_words": total_words,
                "average_abstract_length": round(avg_abstract_length, 2),
                "unique_words": len(set(
                    word for abstract in abstracts 
                    for word in self.tokenize(abstract)
                ))
            },
            "predefined_concepts": {
                concept: freq.to_dict()
                for concept, freq in predefined_results.items()
            },
            "extracted_keywords": [kw.to_dict() for kw in extracted_keywords],
            "precision_metrics": precision_metrics
        }
        
        logger.info("Reporte de frecuencias generado exitosamente")
        
        return report
