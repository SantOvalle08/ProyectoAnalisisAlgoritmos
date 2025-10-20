"""
Sistema de Deduplicación Inteligente
=====================================

Implementa algoritmos avanzados para detectar y eliminar publicaciones duplicadas
basándose en múltiples criterios:
- Comparación de DOI
- Similitud de títulos (Levenshtein y fuzzy matching)
- Comparación de autores
- Análisis de metadatos

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

import hashlib
import logging
from typing import List, Tuple, Dict, Set, Optional
from difflib import SequenceMatcher
from collections import defaultdict
from datetime import datetime

from app.models.publication import Publication

logger = logging.getLogger(__name__)


class DuplicateReport:
    """
    Reporte de duplicados eliminados.
    
    Mantiene un registro detallado de todas las publicaciones duplicadas
    que fueron eliminadas durante el proceso de unificación.
    """
    
    def __init__(self):
        self.duplicates: List[Dict] = []
        self.duplicate_groups: List[List[Publication]] = []
        self.total_duplicates: int = 0
        self.duplicate_by_doi: int = 0
        self.duplicate_by_title: int = 0
        self.duplicate_by_hash: int = 0
        self.created_at: datetime = datetime.now()
    
    def add_duplicate(
        self,
        original: Publication,
        duplicate: Publication,
        reason: str,
        similarity_score: float = 1.0
    ):
        """Agrega un duplicado al reporte."""
        self.duplicates.append({
            'original_id': original.id or original.generate_id(),
            'original_title': original.title,
            'original_source': original.source,
            'duplicate_id': duplicate.id or duplicate.generate_id(),
            'duplicate_title': duplicate.title,
            'duplicate_source': duplicate.source,
            'reason': reason,
            'similarity_score': similarity_score,
            'timestamp': datetime.now().isoformat()
        })
        self.total_duplicates += 1
        
        # Actualizar contadores por tipo
        if 'doi' in reason.lower():
            self.duplicate_by_doi += 1
        elif 'title' in reason.lower():
            self.duplicate_by_title += 1
        elif 'hash' in reason.lower():
            self.duplicate_by_hash += 1
    
    def generate_report(self) -> Dict:
        """Genera un reporte completo en formato diccionario."""
        return {
            'summary': {
                'total_duplicates_found': self.total_duplicates,
                'duplicates_by_doi': self.duplicate_by_doi,
                'duplicates_by_title_similarity': self.duplicate_by_title,
                'duplicates_by_hash': self.duplicate_by_hash,
                'report_generated_at': self.created_at.isoformat()
            },
            'duplicates': self.duplicates,
            'statistics': {
                'duplicate_rate': f"{(self.total_duplicates / (self.total_duplicates + len(self.duplicate_groups)) * 100):.2f}%" if self.total_duplicates > 0 else "0%"
            }
        }
    
    def save_to_file(self, filepath: str = 'duplicates_report.json'):
        """Guarda el reporte en un archivo JSON."""
        import json
        
        report = self.generate_report()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Reporte de duplicados guardado en: {filepath}")


class Deduplicator:
    """
    Sistema inteligente de eliminación de duplicados.
    
    Implementa múltiples estrategias para detectar publicaciones duplicadas:
    
    1. **Comparación exacta por DOI**: Si dos publicaciones tienen el mismo DOI,
       son consideradas duplicadas con certeza 100%.
    
    2. **Hash de título normalizado**: Genera un hash MD5 del título normalizado
       (lowercase, sin espacios extras, sin puntuación) para detección rápida.
    
    3. **Similitud de título (Fuzzy Matching)**: Usa SequenceMatcher de difflib
       para calcular similitud entre títulos. Umbral configurable (default: 0.95).
    
    4. **Comparación de autores**: Verifica si los autores principales coinciden
       para reforzar la detección de duplicados.
    
    Algoritmo de programación dinámica O(n²) con optimizaciones:
    - Índice por DOI para búsqueda O(1)
    - Índice por hash de título para búsqueda O(1)
    - Similitud de título solo para candidatos potenciales
    
    Complejidad:
    - Mejor caso: O(n) cuando todos los duplicados tienen DOI
    - Caso promedio: O(n log n)
    - Peor caso: O(n²) cuando se requiere comparación exhaustiva de títulos
    """
    
    def __init__(
        self,
        similarity_threshold: float = 0.95,
        use_doi_comparison: bool = True,
        use_title_hash: bool = True,
        use_fuzzy_matching: bool = True,
        use_author_comparison: bool = False
    ):
        """
        Inicializa el deduplicador.
        
        Args:
            similarity_threshold: Umbral de similitud para títulos (0.0 a 1.0)
            use_doi_comparison: Habilitar comparación por DOI
            use_title_hash: Habilitar hash de título normalizado
            use_fuzzy_matching: Habilitar fuzzy matching de títulos
            use_author_comparison: Habilitar comparación de autores
        """
        self.similarity_threshold = similarity_threshold
        self.use_doi_comparison = use_doi_comparison
        self.use_title_hash = use_title_hash
        self.use_fuzzy_matching = use_fuzzy_matching
        self.use_author_comparison = use_author_comparison
        
        self.report = DuplicateReport()
        
        logger.info(f"Deduplicator inicializado con threshold={similarity_threshold}")
    
    def normalize_title(self, title: str) -> str:
        """
        Normaliza un título para comparación.
        
        Proceso:
        1. Convertir a minúsculas
        2. Eliminar puntuación
        3. Eliminar espacios extras
        4. Eliminar artículos comunes (a, an, the)
        
        Args:
            title: Título original
        
        Returns:
            Título normalizado
        """
        import re
        
        # Convertir a minúsculas
        normalized = title.lower()
        
        # Eliminar puntuación
        normalized = re.sub(r'[^\w\s]', '', normalized)
        
        # Eliminar artículos comunes al inicio
        normalized = re.sub(r'^(a|an|the)\s+', '', normalized)
        
        # Eliminar espacios extras
        normalized = ' '.join(normalized.split())
        
        return normalized
    
    def generate_title_hash(self, title: str) -> str:
        """
        Genera un hash MD5 del título normalizado.
        
        Args:
            title: Título de la publicación
        
        Returns:
            Hash MD5 hexadecimal
        """
        normalized = self.normalize_title(title)
        return hashlib.md5(normalized.encode('utf-8')).hexdigest()
    
    def calculate_title_similarity(self, title1: str, title2: str) -> float:
        """
        Calcula similitud entre dos títulos usando SequenceMatcher.
        
        Algoritmo de Gestalt Pattern Matching (Ratcliff/Obershelp):
        - Encuentra el bloque más largo común entre las dos cadenas
        - Recursivamente hace lo mismo con las subcadenas a izquierda y derecha
        - Similarity = 2 * matches / total_length
        
        Complejidad: O(n²) en el peor caso
        
        Args:
            title1: Primer título
            title2: Segundo título
        
        Returns:
            Ratio de similitud entre 0.0 y 1.0
        """
        # Normalizar ambos títulos
        norm_title1 = self.normalize_title(title1)
        norm_title2 = self.normalize_title(title2)
        
        # Calcular similitud
        similarity = SequenceMatcher(None, norm_title1, norm_title2).ratio()
        
        return similarity
    
    def are_authors_similar(
        self,
        authors1: List,
        authors2: List,
        min_overlap: float = 0.5
    ) -> bool:
        """
        Verifica si dos listas de autores son similares.
        
        Args:
            authors1: Lista de autores de la primera publicación
            authors2: Lista de autores de la segunda publicación
            min_overlap: Fracción mínima de autores que deben coincidir
        
        Returns:
            True si los autores son similares
        """
        if not authors1 or not authors2:
            return False
        
        # Extraer nombres de autores normalizados
        names1 = {self.normalize_title(author.name) for author in authors1}
        names2 = {self.normalize_title(author.name) for author in authors2}
        
        # Calcular intersección
        intersection = names1.intersection(names2)
        
        # Verificar overlap
        overlap_ratio = len(intersection) / min(len(names1), len(names2))
        
        return overlap_ratio >= min_overlap
    
    def is_duplicate(
        self,
        pub1: Publication,
        pub2: Publication
    ) -> Tuple[bool, str, float]:
        """
        Determina si dos publicaciones son duplicadas.
        
        Returns:
            Tupla (es_duplicado, razón, score_similitud)
        """
        # 1. Comparación por DOI (100% confiable)
        if self.use_doi_comparison:
            if pub1.doi and pub2.doi:
                if pub1.doi.lower() == pub2.doi.lower():
                    return True, "DOI idéntico", 1.0
        
        # 2. Comparación por hash de título
        if self.use_title_hash:
            hash1 = self.generate_title_hash(pub1.title)
            hash2 = self.generate_title_hash(pub2.title)
            
            if hash1 == hash2:
                return True, "Hash de título idéntico", 1.0
        
        # 3. Fuzzy matching de títulos
        if self.use_fuzzy_matching:
            similarity = self.calculate_title_similarity(pub1.title, pub2.title)
            
            if similarity >= self.similarity_threshold:
                # Verificar autores si está habilitado
                if self.use_author_comparison:
                    if self.are_authors_similar(pub1.authors, pub2.authors):
                        return True, f"Título similar ({similarity:.2%}) y autores coinciden", similarity
                else:
                    return True, f"Título altamente similar ({similarity:.2%})", similarity
        
        return False, "No es duplicado", 0.0
    
    def deduplicate(
        self,
        publications: List[Publication]
    ) -> Tuple[List[Publication], DuplicateReport]:
        """
        Elimina publicaciones duplicadas de una lista.
        
        Algoritmo:
        1. Crear índices por DOI y hash de título
        2. Para cada publicación:
           a. Verificar si ya existe en índices (O(1))
           b. Si no existe, comparar con publicaciones únicas usando fuzzy matching
           c. Si es duplicada, agregar a reporte
           d. Si no es duplicada, agregar a lista de únicos y actualizar índices
        
        Args:
            publications: Lista de publicaciones a procesar
        
        Returns:
            Tupla (publicaciones_únicas, reporte_de_duplicados)
        """
        logger.info(f"Iniciando deduplicación de {len(publications)} publicaciones...")
        
        unique_publications: List[Publication] = []
        doi_index: Dict[str, Publication] = {}
        hash_index: Dict[str, Publication] = {}
        
        duplicates_found = 0
        
        for i, pub in enumerate(publications):
            if i % 100 == 0 and i > 0:
                logger.info(f"Procesadas {i}/{len(publications)} publicaciones...")
            
            is_duplicate = False
            duplicate_of = None
            reason = ""
            similarity = 0.0
            
            # Verificar en índice de DOI
            if self.use_doi_comparison and pub.doi:
                doi_key = pub.doi.lower()
                if doi_key in doi_index:
                    is_duplicate = True
                    duplicate_of = doi_index[doi_key]
                    reason = "DOI idéntico"
                    similarity = 1.0
            
            # Verificar en índice de hash
            if not is_duplicate and self.use_title_hash:
                title_hash = self.generate_title_hash(pub.title)
                if title_hash in hash_index:
                    is_duplicate = True
                    duplicate_of = hash_index[title_hash]
                    reason = "Hash de título idéntico"
                    similarity = 1.0
            
            # Fuzzy matching con publicaciones únicas
            if not is_duplicate and self.use_fuzzy_matching:
                for unique_pub in unique_publications:
                    is_dup, dup_reason, sim_score = self.is_duplicate(pub, unique_pub)
                    if is_dup:
                        is_duplicate = True
                        duplicate_of = unique_pub
                        reason = dup_reason
                        similarity = sim_score
                        break
            
            # Procesar resultado
            if is_duplicate:
                duplicates_found += 1
                self.report.add_duplicate(
                    original=duplicate_of,
                    duplicate=pub,
                    reason=reason,
                    similarity_score=similarity
                )
                logger.debug(f"Duplicado encontrado: '{pub.title[:50]}...' - {reason}")
            else:
                # Agregar a publicaciones únicas
                unique_publications.append(pub)
                
                # Actualizar índices
                if pub.doi:
                    doi_index[pub.doi.lower()] = pub
                
                title_hash = self.generate_title_hash(pub.title)
                hash_index[title_hash] = pub
        
        logger.info(f"""
        Deduplicación completada:
        - Publicaciones originales: {len(publications)}
        - Publicaciones únicas: {len(unique_publications)}
        - Duplicados eliminados: {duplicates_found}
        - Tasa de duplicación: {(duplicates_found / len(publications) * 100):.2f}%
        """)
        
        return unique_publications, self.report
    
    def deduplicate_by_source(
        self,
        publications_by_source: Dict[str, List[Publication]]
    ) -> Tuple[List[Publication], DuplicateReport]:
        """
        Elimina duplicados entre múltiples fuentes de datos.
        
        Estrategia:
        1. Primero deduplica dentro de cada fuente
        2. Luego deduplica entre fuentes
        
        Args:
            publications_by_source: Diccionario {fuente: [publicaciones]}
        
        Returns:
            Tupla (publicaciones_únicas, reporte_de_duplicados)
        """
        logger.info("Deduplicando por fuente...")
        
        all_unique_pubs = []
        
        # Deduplicar dentro de cada fuente
        for source, pubs in publications_by_source.items():
            logger.info(f"Deduplicando fuente: {source} ({len(pubs)} publicaciones)")
            unique_pubs, _ = self.deduplicate(pubs)
            all_unique_pubs.extend(unique_pubs)
        
        # Deduplicar entre fuentes
        logger.info(f"Deduplicando entre fuentes ({len(all_unique_pubs)} publicaciones)")
        final_unique_pubs, final_report = self.deduplicate(all_unique_pubs)
        
        return final_unique_pubs, final_report


# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Crear datos de prueba
    from app.models.publication import Author
    
    test_publications = [
        Publication(
            title="Generative AI in Education",
            abstract="This study explores the use of generative AI in educational contexts...",
            authors=[Author(name="John Doe", country="USA")],
            doi="10.1145/123456",
            publication_year=2024,
            source="acm"
        ),
        Publication(
            title="Generative AI in Education",  # Duplicado exacto
            abstract="This study explores the use of generative AI in educational contexts...",
            authors=[Author(name="John Doe", country="USA")],
            doi="10.1145/123456",
            publication_year=2024,
            source="sage"
        ),
        Publication(
            title="Generative Artificial Intelligence in Educational Contexts",  # Similar
            abstract="A different abstract but similar topic...",
            authors=[Author(name="Jane Smith", country="UK")],
            publication_year=2024,
            source="sciencedirect"
        ),
        Publication(
            title="Machine Learning for Healthcare",  # Diferente
            abstract="Completely different topic about healthcare...",
            authors=[Author(name="Bob Johnson", country="Canada")],
            publication_year=2023,
            source="acm"
        )
    ]
    
    # Ejecutar deduplicación
    deduplicator = Deduplicator(similarity_threshold=0.90)
    unique_pubs, report = deduplicator.deduplicate(test_publications)
    
    print(f"\n{'='*60}")
    print(f"RESULTADOS DE DEDUPLICACIÓN")
    print(f"{'='*60}")
    print(f"Publicaciones originales: {len(test_publications)}")
    print(f"Publicaciones únicas: {len(unique_pubs)}")
    print(f"Duplicados eliminados: {report.total_duplicates}")
    print(f"{'='*60}\n")
    
    # Guardar reporte
    report.save_to_file('test_duplicates_report.json')
    print("Reporte guardado en: test_duplicates_report.json")
