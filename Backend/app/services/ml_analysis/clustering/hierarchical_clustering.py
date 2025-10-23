"""
Hierarchical Clustering - Algoritmos de Agrupamiento Jerárquico
================================================================

Implementación de algoritmos de clustering jerárquico para agrupar
abstracts científicos basados en su similitud semántica.

Requerimiento 4: Agrupamiento Jerárquico

Algoritmos implementados:
1. Ward Linkage: Minimiza la varianza dentro de clusters
2. Average Linkage (UPGMA): Promedio de distancias entre todos los pares
3. Complete Linkage: Máxima distancia entre elementos de clusters

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
University: Universidad del Quindío - Análisis de Algoritmos
"""

import numpy as np
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist, squareform
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI para generar imágenes
import io
import base64

# Configurar logging
logger = logging.getLogger(__name__)


class LinkageMethod(str, Enum):
    """Métodos de linkage disponibles para clustering jerárquico."""
    WARD = "ward"
    AVERAGE = "average"
    COMPLETE = "complete"


@dataclass
class ClusteringResult:
    """
    Resultado del clustering jerárquico.
    
    Attributes:
        method: Método de linkage utilizado
        linkage_matrix: Matriz de linkage de scipy
        num_documents: Número de documentos agrupados
        num_features: Número de características (términos TF-IDF)
        cophenetic_correlation: Correlación cofenética (coherencia)
        dendrogram_data: Datos del dendrograma
        cluster_labels: Etiquetas de cluster para cada documento (si se corta)
        silhouette_score: Score de silueta (calidad de clustering)
        davies_bouldin_score: Score Davies-Bouldin (menor es mejor)
        calinski_harabasz_score: Score Calinski-Harabasz (mayor es mejor)
    """
    method: str
    linkage_matrix: np.ndarray
    num_documents: int
    num_features: int
    cophenetic_correlation: float
    dendrogram_data: Optional[Dict[str, Any]] = None
    cluster_labels: Optional[np.ndarray] = None
    silhouette_score: Optional[float] = None
    davies_bouldin_score: Optional[float] = None
    calinski_harabasz_score: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el resultado a diccionario."""
        return {
            "method": self.method,
            "num_documents": self.num_documents,
            "num_features": self.num_features,
            "cophenetic_correlation": round(self.cophenetic_correlation, 4),
            "cluster_labels": self.cluster_labels.tolist() if self.cluster_labels is not None else None,
            "silhouette_score": round(self.silhouette_score, 4) if self.silhouette_score else None,
            "davies_bouldin_score": round(self.davies_bouldin_score, 4) if self.davies_bouldin_score else None,
            "calinski_harabasz_score": round(self.calinski_harabasz_score, 4) if self.calinski_harabasz_score else None,
            "dendrogram_available": self.dendrogram_data is not None
        }


class HierarchicalClustering:
    """
    Clase principal para clustering jerárquico de abstracts científicos.
    
    Implementa tres métodos de linkage:
    - Ward: Minimiza la varianza intra-cluster
    - Average (UPGMA): Promedio de distancias entre todos los pares
    - Complete: Máxima distancia entre elementos
    
    El proceso completo incluye:
    1. Preprocesamiento de texto con TF-IDF
    2. Cálculo de matriz de distancias
    3. Aplicación de clustering jerárquico
    4. Generación de dendrogramas
    5. Evaluación de coherencia
    """
    
    def __init__(
        self,
        max_features: int = 1000,
        ngram_range: Tuple[int, int] = (1, 3),
        min_df: int = 1,
        max_df: float = 0.95,
        use_idf: bool = True
    ):
        """
        Inicializa el sistema de clustering.
        
        Args:
            max_features: Número máximo de características TF-IDF
            ngram_range: Rango de n-gramas (min, max)
            min_df: Mínima frecuencia documental
            max_df: Máxima frecuencia documental (proporción)
            use_idf: Usar pesos IDF
        """
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.max_df = max_df
        self.use_idf = use_idf
        
        # Inicializar vectorizador TF-IDF
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df,
            use_idf=use_idf,
            lowercase=True,
            stop_words='english',
            sublinear_tf=True  # Escala logarítmica para TF
        )
        
        logger.info(
            f"HierarchicalClustering inicializado: "
            f"max_features={max_features}, ngram_range={ngram_range}"
        )
    
    def preprocess_texts(self, texts: List[str]) -> np.ndarray:
        """
        Preprocesa textos y convierte a vectores TF-IDF.
        
        Este es el paso 1 del requerimiento: transformar los abstracts.
        Utiliza TF-IDF para crear representaciones vectoriales que
        capturen la importancia de cada término en cada documento.
        
        Args:
            texts: Lista de abstracts a procesar
        
        Returns:
            Matriz TF-IDF (num_docs x num_features)
        """
        logger.info(f"Preprocesando {len(texts)} textos con TF-IDF")
        
        # Validar entrada
        if not texts or len(texts) < 2:
            raise ValueError("Se requieren al menos 2 textos para clustering")
        
        # Vectorizar textos
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        
        logger.info(
            f"Textos vectorizados: shape={tfidf_matrix.shape}, "
            f"features={len(self.vectorizer.get_feature_names_out())}"
        )
        
        return tfidf_matrix.toarray()
    
    def compute_distance_matrix(
        self,
        tfidf_matrix: np.ndarray,
        metric: str = 'cosine'
    ) -> np.ndarray:
        """
        Calcula matriz de distancias entre documentos.
        
        Este es el paso 2 del requerimiento: cálculo de similitud.
        
        Args:
            tfidf_matrix: Matriz TF-IDF
            metric: Métrica de distancia ('cosine', 'euclidean', 'correlation')
        
        Returns:
            Matriz de distancias condensada
        """
        logger.info(f"Calculando matriz de distancias con métrica: {metric}")
        
        # Calcular distancias por pares
        distances = pdist(tfidf_matrix, metric=metric)
        
        logger.info(f"Matriz de distancias calculada: {len(distances)} pares")
        
        return distances
    
    def apply_clustering(
        self,
        distance_matrix: np.ndarray,
        method: LinkageMethod = LinkageMethod.WARD
    ) -> np.ndarray:
        """
        Aplica clustering jerárquico con el método especificado.
        
        Este es el paso 3 del requerimiento: aplicación de clustering.
        
        EXPLICACIÓN MATEMÁTICA DE LOS MÉTODOS:
        
        1. WARD LINKAGE:
           - Minimiza la suma de cuadrados dentro de clusters
           - Distancia entre clusters A y B:
             d(A,B) = sqrt(|A||B| / (|A| + |B|)) * ||mean(A) - mean(B)||
           - Objetivo: min Σ Σ ||x - μ_k||²
           - Ventaja: Produce clusters balanceados y compactos
        
        2. AVERAGE LINKAGE (UPGMA):
           - Promedio de todas las distancias entre pares
           - Distancia entre clusters A y B:
             d(A,B) = (1 / |A||B|) * Σ Σ d(a,b) para a∈A, b∈B
           - Ventaja: Menos sensible a outliers que complete
        
        3. COMPLETE LINKAGE:
           - Máxima distancia entre cualquier par de elementos
           - Distancia entre clusters A y B:
             d(A,B) = max{d(a,b) : a∈A, b∈B}
           - Ventaja: Evita cadenas largas, produce clusters compactos
        
        Args:
            distance_matrix: Matriz de distancias condensada
            method: Método de linkage a utilizar
        
        Returns:
            Matriz de linkage de scipy
        """
        logger.info(f"Aplicando clustering jerárquico: método={method.value}")
        
        # Aplicar clustering según el método
        linkage_matrix = sch.linkage(
            distance_matrix,
            method=method.value,
            metric='euclidean' if method == LinkageMethod.WARD else None
        )
        
        logger.info(
            f"Clustering completado: "
            f"steps={len(linkage_matrix)}, "
            f"método={method.value}"
        )
        
        return linkage_matrix
    
    def calculate_cophenetic_correlation(
        self,
        linkage_matrix: np.ndarray,
        distance_matrix: np.ndarray
    ) -> float:
        """
        Calcula la correlación cofenética.
        
        La correlación cofenética mide qué tan fielmente el dendrograma
        preserva las distancias originales entre pares de documentos.
        
        Valores cercanos a 1.0 indican alta coherencia.
        
        FÓRMULA:
        c = corr(d_original, d_cophenetic)
        
        donde d_cophenetic es la distancia en el dendrograma
        
        Args:
            linkage_matrix: Matriz de linkage
            distance_matrix: Matriz de distancias original
        
        Returns:
            Coeficiente de correlación cofenética (0 a 1)
        """
        logger.info("Calculando correlación cofenética")
        
        # Calcular distancias cofenéticas
        cophenetic_distances = sch.cophenet(linkage_matrix, distance_matrix)
        
        correlation = cophenetic_distances[0]
        
        logger.info(f"Correlación cofenética: {correlation:.4f}")
        
        return correlation
    
    def cut_tree(
        self,
        linkage_matrix: np.ndarray,
        num_clusters: int
    ) -> np.ndarray:
        """
        Corta el dendrograma para obtener un número específico de clusters.
        
        Args:
            linkage_matrix: Matriz de linkage
            num_clusters: Número de clusters deseado
        
        Returns:
            Array con etiquetas de cluster para cada documento
        """
        logger.info(f"Cortando árbol en {num_clusters} clusters")
        
        labels = sch.fcluster(
            linkage_matrix,
            num_clusters,
            criterion='maxclust'
        )
        
        logger.info(f"Clusters asignados: {np.unique(labels)}")
        
        return labels
    
    def evaluate_clustering(
        self,
        tfidf_matrix: np.ndarray,
        cluster_labels: np.ndarray
    ) -> Dict[str, float]:
        """
        Evalúa la calidad del clustering usando múltiples métricas.
        
        MÉTRICAS IMPLEMENTADAS:
        
        1. Silhouette Score:
           - Mide qué tan similar es un objeto a su cluster vs otros
           - Rango: [-1, 1], mayor es mejor
           - s(i) = (b(i) - a(i)) / max(a(i), b(i))
        
        2. Davies-Bouldin Index:
           - Mide la separación entre clusters
           - Menor es mejor (0 es óptimo)
           - DB = (1/k) Σ max_j≠i (σ_i + σ_j) / d(c_i, c_j)
        
        3. Calinski-Harabasz Index:
           - Ratio de dispersión entre/dentro clusters
           - Mayor es mejor
           - CH = (tr(B_k) / tr(W_k)) * ((n-k) / (k-1))
        
        Args:
            tfidf_matrix: Matriz TF-IDF
            cluster_labels: Etiquetas de clusters
        
        Returns:
            Diccionario con las métricas
        """
        logger.info("Evaluando calidad del clustering")
        
        metrics = {}
        
        # Validar que hay múltiples clusters
        unique_labels = np.unique(cluster_labels)
        if len(unique_labels) < 2:
            logger.warning("Solo hay 1 cluster, no se pueden calcular métricas")
            return metrics
        
        try:
            # Silhouette Score
            silhouette = silhouette_score(tfidf_matrix, cluster_labels)
            metrics['silhouette_score'] = silhouette
            logger.info(f"Silhouette Score: {silhouette:.4f}")
        except Exception as e:
            logger.warning(f"Error calculando Silhouette: {e}")
        
        try:
            # Davies-Bouldin Index
            davies_bouldin = davies_bouldin_score(tfidf_matrix, cluster_labels)
            metrics['davies_bouldin_score'] = davies_bouldin
            logger.info(f"Davies-Bouldin Score: {davies_bouldin:.4f}")
        except Exception as e:
            logger.warning(f"Error calculando Davies-Bouldin: {e}")
        
        try:
            # Calinski-Harabasz Index
            calinski_harabasz = calinski_harabasz_score(tfidf_matrix, cluster_labels)
            metrics['calinski_harabasz_score'] = calinski_harabasz
            logger.info(f"Calinski-Harabasz Score: {calinski_harabasz:.4f}")
        except Exception as e:
            logger.warning(f"Error calculando Calinski-Harabasz: {e}")
        
        return metrics
    
    def generate_dendrogram(
        self,
        linkage_matrix: np.ndarray,
        labels: Optional[List[str]] = None,
        method: str = "ward",
        max_labels: int = 30,
        figsize: Tuple[int, int] = (12, 8),
        truncate_mode: Optional[str] = None,
        p: int = 30
    ) -> Dict[str, Any]:
        """
        Genera un dendrograma visual del clustering.
        
        Este es el paso 4 del requerimiento: representación mediante dendrograma.
        
        Args:
            linkage_matrix: Matriz de linkage
            labels: Etiquetas opcionales para los documentos
            method: Método de linkage usado
            max_labels: Máximo número de etiquetas a mostrar
            figsize: Tamaño de la figura
            truncate_mode: Modo de truncado ('lastp', 'level', None)
            p: Parámetro para truncado
        
        Returns:
            Diccionario con datos del dendrograma e imagen base64
        """
        logger.info("Generando dendrograma")
        
        # Crear figura
        plt.figure(figsize=figsize)
        
        # Configurar parámetros del dendrograma
        dendrogram_params = {
            'Z': linkage_matrix,
            'orientation': 'top',
            'distance_sort': 'ascending',
            'show_leaf_counts': True,
            'color_threshold': None,
            'above_threshold_color': 'gray'
        }
        
        # Agregar etiquetas si hay pocas
        if labels and len(labels) <= max_labels:
            dendrogram_params['labels'] = labels
        
        # Truncar si hay muchos documentos
        if truncate_mode:
            dendrogram_params['truncate_mode'] = truncate_mode
            dendrogram_params['p'] = p
        
        # Generar dendrograma
        dendrogram_data = sch.dendrogram(**dendrogram_params)
        
        # Configurar título y ejes
        plt.title(
            f'Dendrograma - Clustering Jerárquico ({method.upper()})',
            fontsize=14,
            fontweight='bold'
        )
        plt.xlabel('Índice de Documento o Cluster', fontsize=12)
        plt.ylabel('Distancia', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Rotar etiquetas si existen
        if labels and len(labels) <= max_labels:
            plt.xticks(rotation=90)
        
        plt.tight_layout()
        
        # Convertir a imagen base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
        
        logger.info("Dendrograma generado exitosamente")
        
        return {
            'dendrogram_data': dendrogram_data,
            'image_base64': image_base64
        }
    
    def cluster_texts(
        self,
        texts: List[str],
        method: LinkageMethod = LinkageMethod.WARD,
        num_clusters: Optional[int] = None,
        labels: Optional[List[str]] = None,
        generate_plot: bool = True
    ) -> ClusteringResult:
        """
        Ejecuta el proceso completo de clustering jerárquico.
        
        PROCESO COMPLETO (4 PASOS DEL REQUERIMIENTO):
        1. Preprocesamiento: Convierte textos a vectores TF-IDF
        2. Cálculo de similitud: Matriz de distancias coseno
        3. Clustering: Aplica algoritmo jerárquico seleccionado
        4. Dendrograma: Genera visualización del árbol
        
        Args:
            texts: Lista de abstracts científicos
            method: Método de linkage (ward, average, complete)
            num_clusters: Número de clusters (opcional, para cortar árbol)
            labels: Etiquetas para documentos (opcional)
            generate_plot: Generar dendrograma visual
        
        Returns:
            ClusteringResult con todos los datos y métricas
        """
        logger.info(
            f"Iniciando clustering de {len(texts)} textos con método {method.value}"
        )
        
        # Paso 1: Preprocesamiento
        tfidf_matrix = self.preprocess_texts(texts)
        
        # Paso 2: Cálculo de similitud
        distance_matrix = self.compute_distance_matrix(tfidf_matrix)
        
        # Paso 3: Aplicación de clustering
        linkage_matrix = self.apply_clustering(distance_matrix, method)
        
        # Calcular correlación cofenética (coherencia)
        cophenetic_corr = self.calculate_cophenetic_correlation(
            linkage_matrix,
            distance_matrix
        )
        
        # Crear resultado base
        result = ClusteringResult(
            method=method.value,
            linkage_matrix=linkage_matrix,
            num_documents=len(texts),
            num_features=tfidf_matrix.shape[1],
            cophenetic_correlation=cophenetic_corr
        )
        
        # Cortar árbol si se especifica número de clusters
        if num_clusters and num_clusters > 1:
            cluster_labels = self.cut_tree(linkage_matrix, num_clusters)
            result.cluster_labels = cluster_labels
            
            # Evaluar calidad del clustering
            metrics = self.evaluate_clustering(tfidf_matrix, cluster_labels)
            result.silhouette_score = metrics.get('silhouette_score')
            result.davies_bouldin_score = metrics.get('davies_bouldin_score')
            result.calinski_harabasz_score = metrics.get('calinski_harabasz_score')
        
        # Paso 4: Generar dendrograma
        if generate_plot:
            dendrogram_result = self.generate_dendrogram(
                linkage_matrix,
                labels=labels,
                method=method.value,
                truncate_mode='lastp' if len(texts) > 30 else None,
                p=30
            )
            result.dendrogram_data = dendrogram_result
        
        logger.info(
            f"Clustering completado: "
            f"correlación={cophenetic_corr:.4f}, "
            f"features={result.num_features}"
        )
        
        return result
    
    def compare_methods(
        self,
        texts: List[str],
        num_clusters: Optional[int] = None,
        labels: Optional[List[str]] = None
    ) -> Dict[str, ClusteringResult]:
        """
        Compara los 3 métodos de linkage para determinar cuál produce
        agrupamientos más coherentes.
        
        Este es el paso 5 del requerimiento: determinar el algoritmo
        con agrupamientos más coherentes.
        
        CRITERIOS DE COMPARACIÓN:
        1. Correlación cofenética (mayor es mejor)
        2. Silhouette Score (mayor es mejor)
        3. Davies-Bouldin Index (menor es mejor)
        4. Calinski-Harabasz Index (mayor es mejor)
        
        Args:
            texts: Lista de abstracts
            num_clusters: Número de clusters para evaluación
            labels: Etiquetas opcionales
        
        Returns:
            Diccionario con resultados de cada método
        """
        logger.info("Comparando los 3 métodos de linkage")
        
        results = {}
        
        for method in [LinkageMethod.WARD, LinkageMethod.AVERAGE, LinkageMethod.COMPLETE]:
            logger.info(f"Procesando método: {method.value}")
            
            result = self.cluster_texts(
                texts=texts,
                method=method,
                num_clusters=num_clusters,
                labels=labels,
                generate_plot=True
            )
            
            results[method.value] = result
        
        # Determinar el mejor método
        best_method = self._determine_best_method(results)
        logger.info(f"Mejor método según métricas: {best_method}")
        
        return results
    
    def _determine_best_method(
        self,
        results: Dict[str, ClusteringResult]
    ) -> str:
        """
        Determina el mejor método basado en las métricas.
        
        Args:
            results: Resultados de todos los métodos
        
        Returns:
            Nombre del mejor método
        """
        scores = {}
        
        for method_name, result in results.items():
            score = 0
            
            # Correlación cofenética (peso: 0.4)
            score += result.cophenetic_correlation * 0.4
            
            # Silhouette (peso: 0.3)
            if result.silhouette_score:
                score += result.silhouette_score * 0.3
            
            # Davies-Bouldin invertido (peso: 0.15)
            if result.davies_bouldin_score:
                score += (1 / (1 + result.davies_bouldin_score)) * 0.15
            
            # Calinski-Harabasz normalizado (peso: 0.15)
            if result.calinski_harabasz_score:
                score += min(result.calinski_harabasz_score / 1000, 1) * 0.15
            
            scores[method_name] = score
        
        best_method = max(scores, key=scores.get)
        
        logger.info(f"Scores finales: {scores}")
        
        return best_method
