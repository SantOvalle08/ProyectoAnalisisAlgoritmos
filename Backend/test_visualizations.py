"""
Tests para los servicios de visualización.
Prueba unitaria de WordCloud, Heatmap, Timeline y PDF Exporter.
"""

import pytest
from app.services.visualization.wordcloud_generator import WordCloudGenerator
from app.services.visualization.geographic_heatmap import GeographicHeatmap
from app.services.visualization.timeline_chart import TimelineChart
from app.services.visualization.pdf_exporter import PDFExporter
import base64
from io import BytesIO


@pytest.fixture
def sample_publications():
    """Publicaciones de ejemplo para testing."""
    return [
        {
            "title": "Machine Learning Applications in Healthcare",
            "abstract": "This paper explores machine learning algorithms for medical diagnosis. Deep learning models show promising results in image classification and patient outcome prediction.",
            "keywords": ["machine learning", "healthcare", "deep learning", "diagnosis"],
            "authors": [
                {"name": "John Smith", "affiliation": "Stanford University, USA"},
                {"name": "Jane Doe", "affiliation": "MIT, Cambridge, USA"}
            ],
            "year": "2023",
            "journal": "Journal of Medical AI"
        },
        {
            "title": "Natural Language Processing for Scientific Text Mining",
            "abstract": "We present a comprehensive study of NLP techniques for extracting knowledge from scientific publications. Text mining and information extraction are key components.",
            "keywords": ["NLP", "text mining", "information extraction", "scientific publications"],
            "authors": [
                {"name": "Carlos García", "affiliation": "Universidad Nacional de Colombia, Bogotá"},
                {"name": "María López", "affiliation": "Universidad de los Andes, Colombia"}
            ],
            "year": "2022",
            "journal": "Computational Linguistics"
        },
        {
            "title": "Advances in Computer Vision",
            "abstract": "Recent advances in convolutional neural networks have revolutionized computer vision. Object detection and image segmentation achieve state-of-the-art performance.",
            "keywords": ["computer vision", "CNN", "object detection", "image segmentation"],
            "authors": [
                {"name": "Wei Zhang", "affiliation": "Tsinghua University, Beijing, China"},
                {"name": "Li Wang", "affiliation": "Peking University, China"}
            ],
            "year": "2023",
            "journal": "IEEE Transactions on Pattern Analysis"
        },
        {
            "title": "Reinforcement Learning in Robotics",
            "abstract": "This work investigates reinforcement learning approaches for robotic control. Model-free methods demonstrate superior performance in complex navigation tasks.",
            "keywords": ["reinforcement learning", "robotics", "control", "navigation"],
            "authors": [
                {"name": "Hans Mueller", "affiliation": "Technical University of Munich, Germany"},
                {"name": "Anna Schmidt", "affiliation": "University of Heidelberg, Germany"}
            ],
            "year": "2022",
            "journal": "Robotics and Autonomous Systems"
        },
        {
            "title": "Blockchain Technology for Secure Data Sharing",
            "abstract": "We propose a blockchain-based framework for secure and transparent data sharing in healthcare. Smart contracts enable automated data access control.",
            "keywords": ["blockchain", "data sharing", "security", "smart contracts"],
            "authors": [
                {"name": "Sophie Martin", "affiliation": "University of Oxford, United Kingdom"},
                {"name": "James Wilson", "affiliation": "Imperial College London, UK"}
            ],
            "year": "2023",
            "journal": "Journal of Cybersecurity"
        },
        {
            "title": "Quantum Computing for Optimization Problems",
            "abstract": "Quantum algorithms offer exponential speedup for certain optimization problems. We evaluate quantum annealing on logistics and scheduling tasks.",
            "keywords": ["quantum computing", "optimization", "quantum algorithms", "logistics"],
            "authors": [
                {"name": "Pierre Dubois", "affiliation": "École Polytechnique, Paris, France"},
                {"name": "Marie Lefevre", "affiliation": "Sorbonne University, France"}
            ],
            "year": "2021",
            "journal": "Quantum Information Processing"
        }
    ]


class TestWordCloudGenerator:
    """Tests para WordCloudGenerator."""

    def test_initialization(self):
        """Verifica inicialización correcta."""
        generator = WordCloudGenerator()
        assert generator.width == 1200
        assert generator.height == 600
        assert generator.max_words == 100
        assert generator.colormap == "viridis"

    def test_preprocess_text(self):
        """Verifica limpieza de texto."""
        generator = WordCloudGenerator()
        text = "This is a test! Email: test@example.com. URL: https://example.com. Numbers: 12345."
        processed = generator.preprocess_text(text)
        
        # No debe contener URLs, emails, números
        assert "test@example.com" not in processed
        assert "https://example.com" not in processed
        assert "12345" not in processed
        # Debe estar en minúsculas
        assert processed.islower()

    def test_extract_terms_frequency(self, sample_publications):
        """Verifica extracción de términos por frecuencia."""
        generator = WordCloudGenerator()
        terms = generator.extract_terms(sample_publications, use_tfidf=False, max_terms=10)
        
        assert isinstance(terms, dict)
        assert len(terms) <= 10
        # Términos técnicos frecuentes deben aparecer
        assert any(term in ["learning", "machine", "data", "algorithms"] for term in terms.keys())

    def test_extract_terms_tfidf(self, sample_publications):
        """Verifica extracción de términos con TF-IDF."""
        generator = WordCloudGenerator()
        terms = generator.extract_terms(sample_publications, use_tfidf=True, max_terms=10)
        
        assert isinstance(terms, dict)
        assert len(terms) <= 10
        # Todos los pesos deben ser positivos
        assert all(weight > 0 for weight in terms.values())

    def test_generate_wordcloud(self, sample_publications):
        """Verifica generación de word cloud."""
        generator = WordCloudGenerator()
        result = generator.generate_from_publications(
            sample_publications,
            max_words=20,
            use_tfidf=True,
            include_keywords=True
        )
        
        assert "image_base64" in result
        assert "top_terms" in result
        assert "statistics" in result
        
        # Verificar imagen base64 válida
        image_data = result["image_base64"]
        assert isinstance(image_data, str)
        assert len(image_data) > 0
        
        # Verificar top terms
        assert len(result["top_terms"]) > 0
        assert len(result["top_terms"]) <= 20
        
        # Verificar estadísticas
        stats = result["statistics"]
        assert stats["total_publications"] == 6
        assert stats["total_terms"] > 0


class TestGeographicHeatmap:
    """Tests para GeographicHeatmap."""

    def test_initialization(self):
        """Verifica inicialización correcta."""
        heatmap = GeographicHeatmap()
        assert heatmap.colorscale == "Viridis"

    def test_extract_country(self):
        """Verifica extracción de países."""
        heatmap = GeographicHeatmap()
        
        # Casos de prueba
        assert heatmap.extract_country("Stanford University, USA") == "USA"
        assert heatmap.extract_country("Universidad Nacional de Colombia, Bogotá") == "COL"
        assert heatmap.extract_country("Tsinghua University, Beijing, China") == "CHN"
        assert heatmap.extract_country("Technical University of Munich, Germany") == "DEU"
        assert heatmap.extract_country("University of Oxford, United Kingdom") == "GBR"
        assert heatmap.extract_country("École Polytechnique, Paris, France") == "FRA"
        assert heatmap.extract_country("Unknown Location") is None

    def test_extract_countries_from_publications(self, sample_publications):
        """Verifica extracción de países desde publicaciones."""
        heatmap = GeographicHeatmap()
        country_counts = heatmap.extract_countries_from_publications(sample_publications)
        
        assert isinstance(country_counts, dict)
        assert len(country_counts) > 0
        
        # Debe detectar USA (2 publicaciones), Colombia (1), China (1), etc.
        assert "USA" in country_counts
        assert country_counts["USA"] == 2
        assert "COL" in country_counts
        assert country_counts["COL"] == 1

    def test_generate_choropleth(self, sample_publications):
        """Verifica generación de mapa coroplético."""
        heatmap = GeographicHeatmap()
        result = heatmap.generate_from_publications(
            sample_publications,
            map_type="choropleth",
            title="Test Geographic Distribution"
        )
        
        assert "html" in result
        assert "country_distribution" in result
        assert "statistics" in result
        
        # HTML debe contener plotly
        assert "plotly" in result["html"].lower()
        
        # Verificar distribución
        assert len(result["country_distribution"]) > 0
        
        # Verificar estadísticas
        stats = result["statistics"]
        assert stats["total_publications"] == 6
        assert stats["countries_identified"] > 0

    def test_generate_bar_chart(self, sample_publications):
        """Verifica generación de gráfico de barras."""
        heatmap = GeographicHeatmap()
        result = heatmap.generate_from_publications(
            sample_publications,
            map_type="bar",
            title="Test Country Distribution",
            top_n=5
        )
        
        assert "html" in result
        assert "country_distribution" in result
        
        # HTML debe contener plotly
        assert "plotly" in result["html"].lower()


class TestTimelineChart:
    """Tests para TimelineChart."""

    def test_initialization(self):
        """Verifica inicialización correcta."""
        timeline = TimelineChart()
        assert timeline is not None

    def test_extract_year(self):
        """Verifica extracción de años."""
        timeline = TimelineChart()
        
        # Casos de prueba
        pub1 = {"year": "2023"}
        assert timeline.extract_year(pub1) == 2023
        
        pub2 = {"published_date": "2022-05-15"}
        assert timeline.extract_year(pub2) == 2022
        
        pub3 = {"publication_date": "2021"}
        assert timeline.extract_year(pub3) == 2021
        
        pub4 = {}
        assert timeline.extract_year(pub4) is None

    def test_extract_journal(self):
        """Verifica extracción de revistas."""
        timeline = TimelineChart()
        
        pub1 = {"journal": "Nature"}
        assert timeline.extract_journal(pub1) == "Nature"
        
        pub2 = {"venue": "Science"}
        assert timeline.extract_journal(pub2) == "Science"
        
        pub3 = {}
        assert timeline.extract_journal(pub3) == "Unknown"

    def test_aggregate_by_year(self, sample_publications):
        """Verifica agregación por año."""
        timeline = TimelineChart()
        yearly_data = timeline.aggregate_by_year(sample_publications)
        
        assert isinstance(yearly_data, dict)
        assert len(yearly_data) > 0
        
        # Debe haber datos para 2021, 2022, 2023
        assert 2021 in yearly_data
        assert 2022 in yearly_data
        assert 2023 in yearly_data
        
        # Verificar conteos
        assert yearly_data[2023] == 3  # 3 publicaciones en 2023
        assert yearly_data[2022] == 2  # 2 publicaciones en 2022
        assert yearly_data[2021] == 1  # 1 publicación en 2021

    def test_generate_timeline_simple(self, sample_publications):
        """Verifica generación de línea temporal simple."""
        timeline = TimelineChart()
        result = timeline.generate_from_publications(
            sample_publications,
            group_by_journal=False,
            title="Test Publication Timeline"
        )
        
        assert "html" in result
        assert "yearly_distribution" in result
        assert "statistics" in result
        
        # HTML debe contener plotly
        assert "plotly" in result["html"].lower()
        
        # Verificar estadísticas
        stats = result["statistics"]
        assert stats["total_publications"] == 6
        assert stats["year_range"]["start"] == 2021
        assert stats["year_range"]["end"] == 2023

    def test_generate_timeline_by_journal(self, sample_publications):
        """Verifica generación de línea temporal por revista."""
        timeline = TimelineChart()
        result = timeline.generate_from_publications(
            sample_publications,
            group_by_journal=True,
            top_n_journals=3,
            title="Test Timeline by Journal"
        )
        
        assert "html" in result
        assert "yearly_distribution" in result
        
        # HTML debe contener plotly
        assert "plotly" in result["html"].lower()


class TestPDFExporter:
    """Tests para PDFExporter."""

    def test_initialization(self):
        """Verifica inicialización correcta."""
        exporter = PDFExporter(title="Test Report")
        assert exporter.title == "Test Report"
        assert exporter.author == "Scientific Literature Analysis System"

    def test_decode_base64_image(self):
        """Verifica decodificación de imágenes base64."""
        exporter = PDFExporter()
        
        # Crear una imagen base64 simple (1x1 pixel PNG)
        base64_img = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        
        img_buffer = exporter._decode_base64_image(base64_img)
        assert isinstance(img_buffer, BytesIO)
        assert img_buffer.getvalue() is not None

    def test_export_visualizations(self, sample_publications):
        """Verifica exportación a PDF."""
        # Generar word cloud primero
        wc_generator = WordCloudGenerator()
        wc_result = wc_generator.generate_from_publications(sample_publications, max_words=30)
        
        # Exportar a PDF
        exporter = PDFExporter(title="Test Visualization Report")
        pdf_buffer = exporter.export_visualizations(
            publications=sample_publications,
            wordcloud_image=wc_result["image_base64"],
            include_wordcloud=True,
            include_heatmap=False,
            include_timeline=False
        )
        
        assert isinstance(pdf_buffer, BytesIO)
        assert len(pdf_buffer.getvalue()) > 0
        
        # Verificar que es un PDF válido (comienza con %PDF)
        pdf_content = pdf_buffer.getvalue()
        assert pdf_content.startswith(b'%PDF')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
