"""
Tests para Parsers Bibliográficos
=================================

Tests unitarios para BibTeX, RIS, CSV y Unifier.
"""

import pytest
from pathlib import Path
from app.services.data_acquisition.parsers import (
    BibTeXParser,
    RISParser,
    CSVParser,
    PublicationUnifier
)


class TestBibTeXParser:
    """Tests para BibTeX Parser"""
    
    def test_parse_simple_article(self):
        """Test parseo de artículo simple"""
        bibtex = """
        @article{smith2024,
          author = {Smith, John and Doe, Jane},
          title = {Generative AI in Education},
          journal = {AI Journal},
          year = {2024},
          volume = {10},
          pages = {123--145},
          doi = {10.1234/example}
        }
        """
        
        parser = BibTeXParser()
        pubs = parser.parse_string(bibtex)
        
        assert len(pubs) == 1
        pub = pubs[0]
        
        assert pub.title == "Generative AI in Education"
        assert len(pub.authors) == 2
        assert pub.publication_year == 2024
        assert pub.doi == "10.1234/example"
        assert pub.journal == "AI Journal"
    
    def test_parse_multiple_entries(self):
        """Test múltiples entradas"""
        bibtex = """
        @article{ref1,
          title = {First Article},
          author = {Author One},
          year = {2023}
        }
        
        @inproceedings{ref2,
          title = {Conference Paper},
          author = {Author Two},
          year = {2024},
          booktitle = {AI Conference}
        }
        """
        
        parser = BibTeXParser()
        pubs = parser.parse_string(bibtex)
        
        assert len(pubs) == 2
        assert pubs[0].publication_type == 'article'
        assert pubs[1].publication_type == 'conference'


class TestRISParser:
    """Tests para RIS Parser"""
    
    def test_parse_simple_journal(self):
        """Test parseo de journal article"""
        ris = """
TY  - JOUR
TI  - Machine Learning Applications
AU  - Smith, John
AU  - Doe, Jane
JO  - ML Journal
PY  - 2024
VL  - 5
IS  - 2
SP  - 100
EP  - 120
DO  - 10.1234/ml
ER  -
        """
        
        parser = RISParser()
        pubs = parser.parse_string(ris)
        
        assert len(pubs) == 1
        pub = pubs[0]
        
        assert pub.title == "Machine Learning Applications"
        assert len(pub.authors) == 2
        assert pub.publication_year == 2024
        assert pub.journal == "ML Journal"
        assert pub.doi == "10.1234/ml"
        assert pub.pages == "100-120"
    
    def test_parse_multiple_records(self):
        """Test múltiples registros"""
        ris = """
TY  - JOUR
TI  - First Article
AU  - Author One
PY  - 2023
ER  -

TY  - CONF
TI  - Conference Paper
AU  - Author Two
PY  - 2024
ER  -
        """
        
        parser = RISParser()
        pubs = parser.parse_string(ris)
        
        assert len(pubs) == 2
        assert pubs[0].publication_type == 'article'
        assert pubs[1].publication_type == 'conference'


class TestCSVParser:
    """Tests para CSV Parser"""
    
    def test_parse_simple_csv(self):
        """Test parseo CSV simple"""
        csv_data = """title,authors,year,doi
"AI in Education","Smith, John; Doe, Jane",2024,10.1234/ex
"Machine Learning","Brown, Bob",2023,10.5678/ml
"""
        
        parser = CSVParser()
        pubs = parser.parse_string(csv_data)
        
        assert len(pubs) == 2
        assert pubs[0].title == "AI in Education"
        assert len(pubs[0].authors) == 2
        assert pubs[0].publication_year == 2024
    
    def test_parse_with_abstract(self):
        """Test CSV con abstract"""
        csv_data = """title,authors,year,abstract
"Test Article","Author",2024,"This is an abstract"
"""
        
        parser = CSVParser()
        pubs = parser.parse_string(csv_data)
        
        assert len(pubs) == 1
        assert pubs[0].abstract == "This is an abstract"


class TestPublicationUnifier:
    """Tests para Unifier"""
    
    def test_detect_format_json(self):
        """Test detección de formato JSON"""
        # Crear archivo temporal JSON
        import tempfile
        import json
        
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.json', 
            delete=False,
            encoding='utf-8'
        ) as f:
            data = [{
                "title": "Test",
                "authors": ["Author"],
                "publication_year": 2024,
                "abstract": "Test abstract",
                "keywords": [],
                "doi": None,
                "url": "",
                "source": "crossref",
                "publication_type": "article"
            }]
            json.dump(data, f)
            temp_path = f.name
        
        try:
            unifier = PublicationUnifier()
            pubs = unifier.parse_file(temp_path)
            
            assert len(pubs) == 1
            assert pubs[0].title == "Test"
        
        finally:
            Path(temp_path).unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
