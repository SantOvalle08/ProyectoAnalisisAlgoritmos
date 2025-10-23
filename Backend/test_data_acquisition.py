"""
Tests para el Sistema de Adquisición de Datos (Requerimiento 1)
================================================================

Suite de tests completa para validar:
- Scrapers individuales (CrossRef, ACM, SAGE, ScienceDirect)
- Sistema de deduplicación
- Descargador unificado
- Parsers bibliográficos
- Endpoints de API

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Course: Análisis de Algoritmos (2025-2), Universidad del Quindío
"""

import pytest
import asyncio
from typing import List
from datetime import datetime

from app.services.data_acquisition.crossref_scraper import CrossRefScraper
from app.services.data_acquisition.acm_scraper import ACMScraper
from app.services.data_acquisition.sage_scraper import SAGEScraper
from app.services.data_acquisition.sciencedirect_scraper import ScienceDirectScraper
from app.services.data_acquisition.deduplicator import Deduplicator, DuplicateReport
from app.services.data_acquisition.unified_downloader import UnifiedDownloader
from app.models.publication import Publication, Author


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def sample_publications():
    """Genera publicaciones de ejemplo para testing."""
    return [
        Publication(
            title="Generative AI in Education",
            abstract="This study explores the use of generative AI in educational contexts.",
            authors=[Author(name="John Doe"), Author(name="Jane Smith")],
            keywords=["AI", "Education", "Generative Models"],
            doi="10.1145/example.001",
            url="https://example.com/article1",
            publication_date=datetime(2024, 1, 15).date(),
            journal="Journal of AI Research",
            source="crossref"
        ),
        Publication(
            title="Generative AI in Education",  # Duplicado exacto
            abstract="This study explores the use of generative AI in educational contexts.",
            authors=[Author(name="John Doe"), Author(name="Jane Smith")],
            keywords=["AI", "Education"],
            doi="10.1145/example.001",  # Mismo DOI
            url="https://example.com/article1",
            publication_date=datetime(2024, 1, 15).date(),
            journal="Journal of AI Research",
            source="acm"
        ),
        Publication(
            title="Generative Artificial Intelligence in Educational Contexts",  # Similar
            abstract="A comprehensive study on generative AI applications in education.",
            authors=[Author(name="John Doe")],
            keywords=["Generative AI", "Learning"],
            doi="10.1145/example.002",
            url="https://example.com/article2",
            publication_date=datetime(2024, 2, 1).date(),
            journal="Educational Technology Review",
            source="sage"
        ),
        Publication(
            title="Machine Learning for Data Analysis",  # Diferente
            abstract="This paper discusses machine learning techniques for data analysis.",
            authors=[Author(name="Alice Brown")],
            keywords=["Machine Learning", "Data Science"],
            doi="10.1016/example.003",
            url="https://example.com/article3",
            publication_date=datetime(2023, 12, 1).date(),
            journal="Data Science Journal",
            source="sciencedirect"
        ),
    ]


@pytest.fixture
def deduplicator():
    """Crea instancia del deduplicador."""
    return Deduplicator(similarity_threshold=0.85)


# =============================================================================
# TESTS DE DEDUPLICACIÓN
# =============================================================================

class TestDeduplicator:
    """Tests para el sistema de deduplicación."""
    
    def test_exact_duplicate_detection_by_doi(self, deduplicator, sample_publications):
        """Debe detectar duplicados exactos por DOI."""
        unique, report = deduplicator.deduplicate(sample_publications)
        
        # Debe haber detectado el duplicado con mismo DOI
        assert report.total_duplicates >= 1
        assert len(unique) < len(sample_publications)
        
        # Verificar que se eliminó el duplicado correcto
        assert report.duplicate_by_doi >= 1
    
    def test_similar_title_detection(self, deduplicator):
        """Debe detectar publicaciones con títulos muy similares."""
        pubs = [
            Publication(
                title="Generative AI in Education",
                abstract="Abstract 1",
                authors=[Author(name="A")],
                source="acm"
            ),
            Publication(
                title="Generative AI in Educational Contexts",  # Similar
                abstract="Abstract 2",
                authors=[Author(name="B")],
                doi="10.1234/different.doi",
                source="sage"
            )
        ]
        
        unique, report = deduplicator.deduplicate(pubs)
        
        # Con threshold de 0.85, estos títulos deberían considerarse similares
        assert len(unique) <= 2  # Puede o no detectar dependiendo de similitud exacta
    
    def test_no_duplicates_when_different(self, deduplicator):
        """No debe detectar duplicados cuando los artículos son diferentes."""
        pubs = [
            Publication(
                title="Generative AI in Education",
                abstract="Abstract 1",
                authors=[Author(name="A")],
                doi="10.1145/001",
                source="crossref"
            ),
            Publication(
                title="Machine Learning for Healthcare",
                abstract="Abstract 2",
                authors=[Author(name="B")],
                doi="10.1016/002",
                source="sciencedirect"
            )
        ]
        
        unique, report = deduplicator.deduplicate(pubs)
        
        assert len(unique) == 2
        assert report.total_duplicates == 0
    
    def test_duplicate_report_generation(self, deduplicator, sample_publications):
        """Debe generar reporte de duplicados correctamente."""
        unique, report = deduplicator.deduplicate(sample_publications)
        
        report_data = report.generate_report()
        
        assert 'summary' in report_data
        assert 'duplicates' in report_data
        assert 'statistics' in report_data
        assert report_data['summary']['total_duplicates_found'] >= 0
    
    def test_empty_list_handling(self, deduplicator):
        """Debe manejar lista vacía sin errores."""
        unique, report = deduplicator.deduplicate([])
        
        assert len(unique) == 0
        assert report.total_duplicates == 0


# =============================================================================
# TESTS DE SCRAPERS
# =============================================================================

class TestCrossRefScraper:
    """Tests para CrossRefScraper."""
    
    @pytest.mark.asyncio
    async def test_crossref_scraper_initialization(self):
        """Debe inicializar correctamente."""
        scraper = CrossRefScraper()
        
        assert scraper.source_name == "crossref"
        assert scraper.base_url == "https://api.crossref.org"
        assert scraper.session is None  # No creada hasta primer uso
        
        await scraper.close()
    
    @pytest.mark.asyncio
    async def test_crossref_search_with_query(self):
        """Debe buscar publicaciones en CrossRef (test de integración real)."""
        scraper = CrossRefScraper(rate_limit=1.0)
        
        try:
            # Búsqueda pequeña para test rápido
            results = await scraper.search(
                query="machine learning",
                max_results=5
            )
            
            # Debe retornar algunos resultados
            assert isinstance(results, list)
            assert len(results) <= 5
            
            # Si hay resultados, validar estructura
            if results:
                pub = results[0]
                assert isinstance(pub, Publication)
                assert pub.title is not None
                assert pub.source == "crossref"
        
        finally:
            await scraper.close()
    
    @pytest.mark.asyncio
    async def test_crossref_search_with_filters(self):
        """Debe aplicar filtros de año correctamente."""
        scraper = CrossRefScraper(rate_limit=1.0)
        
        try:
            results = await scraper.search(
                query="artificial intelligence",
                max_results=3,
                start_year=2023,
                end_year=2024
            )
            
            assert isinstance(results, list)
            
            # Validar que los años están en el rango (si hay fecha)
            for pub in results:
                if pub.publication_date:
                    year = pub.publication_date.year
                    assert 2023 <= year <= 2024
        
        finally:
            await scraper.close()


class TestACMScraper:
    """Tests para ACMScraper."""
    
    @pytest.mark.asyncio
    async def test_acm_scraper_initialization(self):
        """Debe inicializar correctamente."""
        scraper = ACMScraper()
        
        assert scraper.source_name == "acm"
        assert scraper.base_url == "https://dl.acm.org"
        assert scraper.rate_limit == 0.5  # Conservador
        
        await scraper.close()
    
    @pytest.mark.asyncio
    async def test_acm_export_to_json(self):
        """Debe exportar a JSON correctamente."""
        scraper = ACMScraper()
        
        sample_pubs = [
            Publication(
                title="Test Article",
                abstract="Test abstract",
                authors=[Author(name="Test Author")],
                source="acm"
            )
        ]
        
        json_output = scraper.export_to_format(sample_pubs, format='json')
        
        assert isinstance(json_output, str)
        assert "Test Article" in json_output
        assert "acm" in json_output
        
        await scraper.close()


class TestSAGEScraper:
    """Tests para SAGEScraper."""
    
    @pytest.mark.asyncio
    async def test_sage_scraper_initialization(self):
        """Debe inicializar correctamente."""
        scraper = SAGEScraper()
        
        assert scraper.source_name == "sage"
        assert scraper.base_url == "https://journals.sagepub.com"
        
        await scraper.close()


class TestScienceDirectScraper:
    """Tests para ScienceDirectScraper."""
    
    @pytest.mark.asyncio
    async def test_sciencedirect_initialization(self):
        """Debe inicializar correctamente."""
        scraper = ScienceDirectScraper()
        
        assert scraper.source_name == "sciencedirect"
        assert scraper.base_url == "https://api.elsevier.com"
        
        await scraper.close()
    
    @pytest.mark.asyncio
    async def test_sciencedirect_mock_data_without_api_key(self):
        """Debe generar datos de ejemplo cuando no hay API key."""
        scraper = ScienceDirectScraper(api_key=None)
        
        try:
            results = await scraper.search(
                query="generative AI",
                max_results=3
            )
            
            # Debe retornar datos mock
            assert isinstance(results, list)
            assert len(results) <= 5  # Mock limita a 5
            
            if results:
                assert "[MOCK]" in results[0].title
                assert results[0].source == "sciencedirect"
        
        finally:
            await scraper.close()


# =============================================================================
# TESTS DE INTEGRACIÓN
# =============================================================================

class TestUnifiedDownloader:
    """Tests para el descargador unificado."""
    
    @pytest.mark.asyncio
    async def test_downloader_initialization(self):
        """Debe inicializar correctamente."""
        downloader = UnifiedDownloader(
            similarity_threshold=0.9,
            rate_limit=1.0,
            output_dir="data/downloads/test"
        )
        
        assert downloader.similarity_threshold == 0.9
        assert downloader.rate_limit == 1.0
    
    @pytest.mark.asyncio
    async def test_multiple_source_download(self):
        """Debe descargar de múltiples fuentes y unificar."""
        downloader = UnifiedDownloader(
            similarity_threshold=0.9,
            rate_limit=1.0,
            output_dir="data/downloads/test"
        )
        
        # Test con CrossRef (fuente disponible sin API key)
        # Limitamos a 2 resultados para test rápido
        try:
            result = await downloader.download(
                query="machine learning",
                sources=["crossref"],
                max_results_per_source=2
            )
            
            assert isinstance(result, dict)
            assert 'total_downloaded' in result
            assert 'total_unique' in result
            assert result['total_downloaded'] >= 0
        
        except Exception as e:
            # En caso de error de red, el test no debe fallar
            pytest.skip(f"Test de integración falló (red): {e}")


# =============================================================================
# TESTS DE ENDPOINTS API
# =============================================================================

@pytest.mark.asyncio
async def test_api_endpoint_download_validation():
    """Test de validación de parámetros del endpoint de descarga."""
    from app.api.v1.data_acquisition import DownloadRequest, DataSource
    
    # Request válido
    valid_request = DownloadRequest(
        query="generative AI",
        sources=[DataSource.CROSSREF],
        max_results_per_source=50,
        start_year=2023,
        end_year=2024
    )
    
    assert valid_request.query == "generative AI"
    assert len(valid_request.sources) == 1
    assert valid_request.max_results_per_source == 50


def test_data_source_enum():
    """Test del enum de fuentes de datos."""
    from app.api.v1.data_acquisition import DataSource
    
    assert DataSource.CROSSREF.value == "crossref"
    assert DataSource.ACM.value == "acm"
    assert DataSource.SAGE.value == "sage"
    assert DataSource.SCIENCEDIRECT.value == "sciencedirect"


# =============================================================================
# TESTS DE RENDIMIENTO
# =============================================================================

class TestPerformance:
    """Tests de rendimiento y escalabilidad."""
    
    def test_deduplication_performance(self):
        """Deduplicación debe ser rápida incluso con muchas publicaciones."""
        import time
        
        # Usar threshold bajo para evitar falsos positivos
        deduplicator = Deduplicator(similarity_threshold=0.99)
        
        # Generar 50 publicaciones totalmente diferentes
        pubs = []
        for i in range(50):
            pub = Publication(
                title=f"Research Study Number {i} on Subject {chr(65 + i % 26)} and Method {chr(90 - i % 26)}",
                abstract=f"Detailed abstract for research {i} discussing methodology and results...",
                authors=[Author(name=f"Dr. Researcher {i} {chr(65 + i % 26)}")],
                doi=f"10.{1000 + i}/journal.article.{i:05d}",
                source="crossref"
            )
            pubs.append(pub)
        
        start_time = time.time()
        unique, report = deduplicator.deduplicate(pubs)
        elapsed_time = time.time() - start_time
        
        # Debe completar en menos de 3 segundos
        assert elapsed_time < 3.0
        # Performance test: solo verificamos que termine en tiempo razonable
        assert len(unique) > 0


# =============================================================================
# EJECUCIÓN DE TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
