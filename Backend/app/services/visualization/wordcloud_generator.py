"""
Generador de Nube de Palabras Dinámica
=======================================

Genera visualizaciones de nube de palabras a partir de abstracts y keywords
de publicaciones científicas.

Características:
- Extracción automática de términos frecuentes
- Filtrado de stopwords multiidioma
- Ponderación por frecuencia TF-IDF
- Generación de imágenes en base64
- Actualización dinámica con nuevas publicaciones

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
"""

import base64
from io import BytesIO
from typing import List, Dict, Optional, Tuple
from collections import Counter
import re

import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

# Descargar stopwords si no están disponibles
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords', quiet=True)


class WordCloudGenerator:
    """
    Generador de nubes de palabras dinámicas para análisis bibliométrico.
    
    Procesa abstracts y keywords de publicaciones científicas para generar
    visualizaciones de términos más frecuentes y relevantes.
    """
    
    def __init__(
        self,
        width: int = 1200,
        height: int = 600,
        background_color: str = 'white',
        colormap: str = 'viridis',
        max_words: int = 100,
        min_font_size: int = 10,
        max_font_size: int = 100,
        relative_scaling: float = 0.5
    ):
        """
        Inicializa el generador de nube de palabras.
        
        Args:
            width: Ancho de la imagen en píxeles
            height: Alto de la imagen en píxeles
            background_color: Color de fondo (nombre o hex)
            colormap: Mapa de colores de matplotlib
            max_words: Número máximo de palabras a mostrar
            min_font_size: Tamaño mínimo de fuente
            max_font_size: Tamaño máximo de fuente
            relative_scaling: Factor de escala relativa (0-1)
        """
        self.width = width
        self.height = height
        self.background_color = background_color
        self.colormap = colormap
        self.max_words = max_words
        self.min_font_size = min_font_size
        self.max_font_size = max_font_size
        self.relative_scaling = relative_scaling
        
        # Stopwords combinadas (inglés + español + técnicas)
        self.stopwords = self._build_stopwords()
    
    def _build_stopwords(self) -> set:
        """
        Construye conjunto de stopwords para filtrado.
        
        Returns:
            Conjunto de palabras a ignorar
        """
        stop_words = set()
        
        # Stopwords en inglés
        try:
            stop_words.update(stopwords.words('english'))
        except:
            pass
        
        # Stopwords en español
        try:
            stop_words.update(stopwords.words('spanish'))
        except:
            pass
        
        # Stopwords técnicas/comunes en papers
        technical_stops = {
            'study', 'research', 'paper', 'article', 'author', 'authors',
            'results', 'conclusion', 'introduction', 'method', 'methods',
            'discussion', 'abstract', 'keywords', 'et', 'al', 'however',
            'therefore', 'thus', 'moreover', 'furthermore', 'also',
            'using', 'used', 'use', 'based', 'propose', 'proposed',
            'approach', 'approaches', 'work', 'works', 'present',
            'presented', 'show', 'shows', 'shown', 'investigated',
            'investigated', 'analysis', 'analyzed', 'compared'
        }
        stop_words.update(technical_stops)
        
        return stop_words
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocesa texto para análisis.
        
        Args:
            text: Texto a preprocesar
        
        Returns:
            Texto limpio en minúsculas
        """
        # Convertir a minúsculas
        text = text.lower()
        
        # Eliminar URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Eliminar emails
        text = re.sub(r'\S+@\S+', '', text)
        
        # Eliminar números
        text = re.sub(r'\d+', '', text)
        
        # Eliminar puntuación excepto guiones internos
        text = re.sub(r'[^\w\s-]', ' ', text)
        
        # Eliminar espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_terms(
        self,
        texts: List[str],
        use_tfidf: bool = True,
        ngram_range: Tuple[int, int] = (1, 2)
    ) -> Dict[str, float]:
        """
        Extrae términos y sus pesos del corpus.
        
        Args:
            texts: Lista de textos (abstracts + keywords)
            use_tfidf: Si True, usa TF-IDF; si False, usa frecuencia simple
            ngram_range: Rango de n-gramas a considerar
        
        Returns:
            Diccionario {término: peso}
        """
        if not texts:
            return {}
        
        # Preprocesar textos
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        if use_tfidf:
            # TF-IDF para ponderar términos
            vectorizer = TfidfVectorizer(
                max_features=self.max_words * 3,
                stop_words=list(self.stopwords),
                ngram_range=ngram_range,
                min_df=2,
                max_df=0.85
            )
            
            try:
                tfidf_matrix = vectorizer.fit_transform(processed_texts)
                feature_names = vectorizer.get_feature_names_out()
                
                # Sumar scores TF-IDF para cada término
                term_scores = tfidf_matrix.sum(axis=0).A1
                term_weights = dict(zip(feature_names, term_scores))
                
            except ValueError:
                # Fallback a frecuencia simple si TF-IDF falla
                return self._extract_by_frequency(processed_texts)
        else:
            # Frecuencia simple
            term_weights = self._extract_by_frequency(processed_texts)
        
        # Filtrar términos muy cortos
        term_weights = {
            term: weight
            for term, weight in term_weights.items()
            if len(term) >= 3
        }
        
        # Ordenar por peso y tomar top max_words
        sorted_terms = sorted(
            term_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )[:self.max_words]
        
        return dict(sorted_terms)
    
    def _extract_by_frequency(self, texts: List[str]) -> Dict[str, float]:
        """
        Extrae términos por frecuencia simple.
        
        Args:
            texts: Textos preprocesados
        
        Returns:
            Diccionario {término: frecuencia}
        """
        # Tokenizar y contar
        all_words = []
        for text in texts:
            words = text.split()
            words = [
                word for word in words
                if word not in self.stopwords and len(word) >= 3
            ]
            all_words.extend(words)
        
        # Contar frecuencias
        word_counts = Counter(all_words)
        
        # Convertir a floats
        return {word: float(count) for word, count in word_counts.items()}
    
    def generate(
        self,
        term_weights: Dict[str, float],
        title: Optional[str] = None
    ) -> str:
        """
        Genera nube de palabras.
        
        Args:
            term_weights: Diccionario {término: peso}
            title: Título opcional para la visualización
        
        Returns:
            Imagen en formato base64 (PNG)
        """
        if not term_weights:
            raise ValueError("No hay términos para generar la nube de palabras")
        
        # Crear objeto WordCloud
        wordcloud = WordCloud(
            width=self.width,
            height=self.height,
            background_color=self.background_color,
            colormap=self.colormap,
            max_words=self.max_words,
            min_font_size=self.min_font_size,
            max_font_size=self.max_font_size,
            relative_scaling=self.relative_scaling,
            random_state=42,  # Reproducibilidad
            collocations=False  # Evitar bigramas duplicados
        )
        
        # Generar nube
        wordcloud.generate_from_frequencies(term_weights)
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
        
        # Mostrar nube
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        
        # Agregar título si se proporciona
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Ajustar layout
        plt.tight_layout()
        
        # Convertir a base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        # Limpiar
        plt.close(fig)
        buffer.close()
        
        return image_base64
    
    def generate_from_publications(
        self,
        publications: List[Dict],
        include_keywords: bool = True,
        use_tfidf: bool = True,
        title: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Genera nube de palabras desde publicaciones.
        
        Args:
            publications: Lista de diccionarios con 'abstract' y opcionalmente 'keywords'
            include_keywords: Si True, incluye keywords en el análisis
            use_tfidf: Si True, usa TF-IDF para ponderación
            title: Título opcional
        
        Returns:
            Diccionario con:
                - image_base64: Imagen en base64
                - top_terms: Lista de términos principales
                - num_publications: Número de publicaciones analizadas
                - total_terms: Total de términos únicos
        """
        # Recolectar textos
        texts = []
        
        for pub in publications:
            # Abstract
            if 'abstract' in pub and pub['abstract']:
                texts.append(pub['abstract'])
            
            # Keywords
            if include_keywords and 'keywords' in pub and pub['keywords']:
                if isinstance(pub['keywords'], list):
                    texts.append(' '.join(pub['keywords']))
                else:
                    texts.append(str(pub['keywords']))
        
        if not texts:
            raise ValueError("No hay textos para analizar en las publicaciones")
        
        # Extraer términos
        term_weights = self.extract_terms(texts, use_tfidf=use_tfidf)
        
        # Generar imagen
        image_base64 = self.generate(term_weights, title=title)
        
        # Top términos
        top_terms = sorted(
            term_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]
        
        return {
            'image_base64': image_base64,
            'top_terms': [{'term': term, 'weight': weight} for term, weight in top_terms],
            'num_publications': len(publications),
            'total_terms': len(term_weights)
        }
