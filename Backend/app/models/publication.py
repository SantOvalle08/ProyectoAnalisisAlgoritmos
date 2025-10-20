"""
Modelo de Publicación Científica
=================================

Define la estructura de datos unificada para publicaciones científicas
provenientes de diferentes fuentes (ACM, SAGE, ScienceDirect).

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
"""

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List, Optional
from datetime import date, datetime
import re


class Author(BaseModel):
    """
    Modelo para representar un autor de una publicación científica.
    
    Attributes:
        name: Nombre completo del autor
        affiliation: Institución de afiliación
        email: Correo electrónico (opcional)
        country: País de procedencia
        orcid: ID ORCID del autor (opcional)
    """
    name: str = Field(
        ...,
        description="Nombre completo del autor",
        min_length=1,
        max_length=200
    )
    affiliation: Optional[str] = Field(
        None,
        description="Institución de afiliación",
        max_length=300
    )
    email: Optional[str] = Field(
        None,
        description="Correo electrónico del autor"
    )
    country: Optional[str] = Field(
        None,
        description="País de procedencia",
        max_length=100
    )
    orcid: Optional[str] = Field(
        None,
        description="ID ORCID del autor",
        pattern=r"^\d{4}-\d{4}-\d{4}-\d{3}[0-9X]$"
    )
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Valida el formato del email."""
        if v is not None and v.strip():
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, v):
                raise ValueError(f"Email inválido: {v}")
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Dr. John Smith",
                "affiliation": "Massachusetts Institute of Technology",
                "email": "john.smith@mit.edu",
                "country": "United States",
                "orcid": "0000-0002-1825-0097"
            }
        }
    )


class Publication(BaseModel):
    """
    Modelo unificado de publicación científica.
    
    Este modelo representa una publicación científica con todos sus metadatos,
    independientemente de la fuente de origen (ACM, SAGE, ScienceDirect).
    
    Attributes:
        id: Identificador único generado automáticamente
        title: Título de la publicación
        abstract: Resumen o abstract
        authors: Lista de autores
        keywords: Palabras clave asociadas
        doi: Digital Object Identifier
        publication_date: Fecha de publicación
        publication_year: Año de publicación
        journal: Nombre de la revista o conferencia
        volume: Volumen de la publicación
        issue: Número o issue
        pages: Rango de páginas
        publisher: Editorial
        source: Fuente de datos (acm, sage, sciencedirect)
        source_id: ID original en la fuente
        url: URL de acceso al artículo
        pdf_url: URL del PDF (si está disponible)
        citation_count: Número de citas
        publication_type: Tipo de publicación (article, conference, book_chapter, etc.)
        language: Idioma de la publicación
        isbn: ISBN (para libros/capítulos)
        issn: ISSN (para revistas)
        created_at: Timestamp de creación del registro
        updated_at: Timestamp de última actualización
    """
    
    # Identificadores
    id: Optional[str] = Field(
        None,
        description="ID único generado automáticamente"
    )
    source_id: Optional[str] = Field(
        None,
        description="ID original en la fuente de datos"
    )
    doi: Optional[str] = Field(
        None,
        description="Digital Object Identifier",
        pattern=r"^10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+$"
    )
    
    # Información básica
    title: str = Field(
        ...,
        description="Título de la publicación",
        min_length=1,
        max_length=1000
    )
    abstract: str = Field(
        ...,
        description="Resumen o abstract de la publicación",
        min_length=1
    )
    
    # Autores y palabras clave
    authors: List[Author] = Field(
        default=[],
        description="Lista de autores de la publicación"
    )
    keywords: List[str] = Field(
        default=[],
        description="Palabras clave asociadas"
    )
    
    # Metadatos de publicación
    publication_date: Optional[date] = Field(
        None,
        description="Fecha completa de publicación"
    )
    publication_year: Optional[int] = Field(
        None,
        description="Año de publicación",
        ge=1900,
        le=2100
    )
    journal: Optional[str] = Field(
        None,
        description="Nombre de la revista o conferencia",
        max_length=500
    )
    volume: Optional[str] = Field(
        None,
        description="Volumen de la publicación",
        max_length=50
    )
    issue: Optional[str] = Field(
        None,
        description="Número o issue",
        max_length=50
    )
    pages: Optional[str] = Field(
        None,
        description="Rango de páginas (ej: 123-145)",
        max_length=50
    )
    publisher: Optional[str] = Field(
        None,
        description="Editorial",
        max_length=300
    )
    
    # Fuente y acceso
    source: str = Field(
        ...,
        description="Fuente de datos (acm, sage, sciencedirect, crossref)",
        pattern=r"^(acm|sage|sciencedirect|crossref|ieee|springer)$"
    )
    url: Optional[str] = Field(
        None,
        description="URL de acceso al artículo"
    )
    pdf_url: Optional[str] = Field(
        None,
        description="URL del PDF"
    )
    
    # Métricas
    citation_count: int = Field(
        default=0,
        description="Número de citas",
        ge=0
    )
    
    # Clasificación
    publication_type: Optional[str] = Field(
        default="article",
        description="Tipo de publicación",
        pattern=r"^(article|conference|book_chapter|review|editorial|letter)$"
    )
    language: Optional[str] = Field(
        default="en",
        description="Idioma de la publicación (código ISO 639-1)",
        max_length=5
    )
    
    # Identificadores adicionales
    isbn: Optional[str] = Field(
        None,
        description="ISBN para libros o capítulos"
    )
    issn: Optional[str] = Field(
        None,
        description="ISSN para revistas"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp de creación del registro"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp de última actualización"
    )
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Valida y limpia el título."""
        if not v or not v.strip():
            raise ValueError("El título no puede estar vacío")
        return v.strip()
    
    @field_validator('abstract')
    @classmethod
    def validate_abstract(cls, v: str) -> str:
        """Valida y limpia el abstract."""
        if not v or not v.strip():
            raise ValueError("El abstract no puede estar vacío")
        # Cambiado de 50 a 10 caracteres mínimos para abstracts cortos
        if len(v.strip()) < 10:
            raise ValueError("El abstract debe tener al menos 10 caracteres")
        return v.strip()
    
    @field_validator('keywords')
    @classmethod
    def validate_keywords(cls, v: List[str]) -> List[str]:
        """Limpia y normaliza las palabras clave."""
        return [kw.strip().lower() for kw in v if kw.strip()]
    
    @field_validator('publication_year')
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        """Valida que el año de publicación sea razonable."""
        if v is not None:
            current_year = datetime.now().year
            if v < 1900 or v > current_year + 1:
                raise ValueError(f"Año de publicación inválido: {v}")
        return v
    
    def generate_id(self) -> str:
        """
        Genera un ID único basado en DOI o combinación de título y año.
        
        Returns:
            ID único para la publicación
        """
        import hashlib
        
        if self.doi:
            # Usar DOI como base si está disponible
            return f"pub_{hashlib.md5(self.doi.encode()).hexdigest()[:12]}"
        else:
            # Generar ID basado en título y año
            identifier = f"{self.title}_{self.publication_year or 'unknown'}"
            return f"pub_{hashlib.md5(identifier.encode()).hexdigest()[:12]}"
    
    def to_bibtex(self) -> str:
        """
        Convierte la publicación a formato BibTeX.
        
        Returns:
            Representación en formato BibTeX
        """
        pub_type = "article" if self.publication_type == "article" else "inproceedings"
        entry_key = self.id or self.generate_id()
        
        bibtex = f"@{pub_type}{{{entry_key},\n"
        bibtex += f"  title = {{{self.title}}},\n"
        
        if self.authors:
            authors_str = " and ".join([author.name for author in self.authors])
            bibtex += f"  author = {{{authors_str}}},\n"
        
        if self.journal:
            bibtex += f"  journal = {{{self.journal}}},\n"
        
        if self.publication_year:
            bibtex += f"  year = {{{self.publication_year}}},\n"
        
        if self.volume:
            bibtex += f"  volume = {{{self.volume}}},\n"
        
        if self.issue:
            bibtex += f"  number = {{{self.issue}}},\n"
        
        if self.pages:
            bibtex += f"  pages = {{{self.pages}}},\n"
        
        if self.doi:
            bibtex += f"  doi = {{{self.doi}}},\n"
        
        if self.url:
            bibtex += f"  url = {{{self.url}}},\n"
        
        bibtex += "}\n"
        return bibtex
    
    def get_first_author_country(self) -> Optional[str]:
        """
        Obtiene el país del primer autor.
        
        Returns:
            País del primer autor o None si no está disponible
        """
        if self.authors and len(self.authors) > 0:
            return self.authors[0].country
        return None
    
    def get_author_names(self) -> List[str]:
        """
        Obtiene una lista con los nombres de todos los autores.
        
        Returns:
            Lista de nombres de autores
        """
        return [author.name for author in self.authors]
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "pub_abc123def456",
                "title": "Generative AI in Educational Contexts: A Systematic Review",
                "abstract": "This study presents a comprehensive systematic review of the application of generative artificial intelligence in educational settings. We analyze 150 publications from major scientific databases...",
                "authors": [
                    {
                        "name": "Dr. Emily Johnson",
                        "affiliation": "Stanford University",
                        "country": "United States",
                        "orcid": "0000-0002-1825-0097"
                    },
                    {
                        "name": "Prof. Michael Chen",
                        "affiliation": "MIT",
                        "country": "United States"
                    }
                ],
                "keywords": [
                    "generative ai",
                    "education",
                    "machine learning",
                    "systematic review"
                ],
                "doi": "10.1145/3544548.3580958",
                "publication_date": "2024-04-23",
                "publication_year": 2024,
                "journal": "ACM Transactions on Computer-Human Interaction",
                "volume": "31",
                "issue": "2",
                "pages": "1-42",
                "publisher": "ACM",
                "source": "acm",
                "url": "https://dl.acm.org/doi/10.1145/3544548.3580958",
                "citation_count": 15,
                "publication_type": "article",
                "language": "en"
            }
        }
    )
