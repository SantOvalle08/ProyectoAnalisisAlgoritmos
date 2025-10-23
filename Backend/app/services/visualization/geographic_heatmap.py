"""
Generador de Mapas de Calor Geográficos
========================================

Crea visualizaciones de mapas de calor mostrando la distribución geográfica
de publicaciones científicas según el país del primer autor.

Características:
- Extracción automática de países de afiliaciones
- Mapa interactivo con plotly
- Gradiente de colores por frecuencia
- Tooltips informativos
- Exportación a imagen base64

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
"""

import base64
from io import BytesIO
from typing import List, Dict, Optional, Tuple
from collections import Counter
import re

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class GeographicHeatmap:
    """
    Generador de mapas de calor geográficos para análisis bibliométrico.
    
    Procesa afiliaciones de autores para crear visualizaciones de
    distribución geográfica de publicaciones científicas.
    """
    
    # Mapeo de nombres de países a códigos ISO
    COUNTRY_CODES = {
        'united states': 'USA', 'usa': 'USA', 'us': 'USA', 'united states of america': 'USA',
        'china': 'CHN', 'people\'s republic of china': 'CHN', 'prc': 'CHN',
        'united kingdom': 'GBR', 'uk': 'GBR', 'great britain': 'GBR', 'england': 'GBR',
        'germany': 'DEU', 'deutschland': 'DEU',
        'france': 'FRA', 'república francesa': 'FRA',
        'spain': 'ESP', 'españa': 'ESP',
        'italy': 'ITA', 'italia': 'ITA',
        'canada': 'CAN',
        'australia': 'AUS',
        'japan': 'JPN', 'nippon': 'JPN',
        'south korea': 'KOR', 'korea': 'KOR', 'republic of korea': 'KOR',
        'india': 'IND',
        'brazil': 'BRA', 'brasil': 'BRA',
        'netherlands': 'NLD', 'holland': 'NLD',
        'switzerland': 'CHE', 'suiza': 'CHE',
        'sweden': 'SWE', 'suecia': 'SWE',
        'norway': 'NOR', 'noruega': 'NOR',
        'denmark': 'DNK', 'dinamarca': 'DNK',
        'finland': 'FIN', 'finlandia': 'FIN',
        'poland': 'POL', 'polonia': 'POL',
        'russia': 'RUS', 'russian federation': 'RUS',
        'mexico': 'MEX', 'méxico': 'MEX',
        'argentina': 'ARG',
        'chile': 'CHL',
        'colombia': 'COL',
        'peru': 'PER', 'perú': 'PER',
        'venezuela': 'VEN',
        'portugal': 'PRT',
        'belgium': 'BEL', 'bélgica': 'BEL',
        'austria': 'AUT',
        'greece': 'GRC', 'grecia': 'GRC',
        'turkey': 'TUR', 'türkiye': 'TUR',
        'israel': 'ISR',
        'south africa': 'ZAF', 'sudáfrica': 'ZAF',
        'egypt': 'EGY', 'egipto': 'EGY',
        'saudi arabia': 'SAU', 'arabia saudita': 'SAU',
        'united arab emirates': 'ARE', 'uae': 'ARE',
        'singapore': 'SGP', 'singapur': 'SGP',
        'hong kong': 'HKG',
        'taiwan': 'TWN',
        'thailand': 'THA', 'tailandia': 'THA',
        'malaysia': 'MYS', 'malasia': 'MYS',
        'indonesia': 'IDN',
        'philippines': 'PHL', 'filipinas': 'PHL',
        'vietnam': 'VNM',
        'pakistan': 'PAK', 'paquistán': 'PAK',
        'bangladesh': 'BGD',
        'iran': 'IRN', 'irán': 'IRN',
        'iraq': 'IRQ',
        'new zealand': 'NZL', 'nueva zelanda': 'NZL',
        'ireland': 'IRL', 'irlanda': 'IRL',
        'czech republic': 'CZE', 'república checa': 'CZE',
        'hungary': 'HUN', 'hungría': 'HUN',
        'romania': 'ROU', 'rumania': 'ROU',
        'ukraine': 'UKR', 'ucrania': 'UKR',
    }
    
    def __init__(self, colorscale: str = 'Viridis'):
        """
        Inicializa el generador de mapas de calor.
        
        Args:
            colorscale: Escala de colores de plotly
                       (Viridis, Blues, Reds, Greens, etc.)
        """
        self.colorscale = colorscale
    
    def extract_country(self, affiliation: str) -> Optional[str]:
        """
        Extrae el país de una afiliación de autor.
        
        Args:
            affiliation: Texto de afiliación del autor
        
        Returns:
            Código ISO del país o None si no se encuentra
        """
        if not affiliation:
            return None
        
        # Convertir a minúsculas
        affiliation_lower = affiliation.lower()
        
        # Buscar países conocidos
        for country_name, country_code in self.COUNTRY_CODES.items():
            if country_name in affiliation_lower:
                return country_code
        
        return None
    
    def extract_countries_from_publications(
        self,
        publications: List[Dict]
    ) -> Dict[str, int]:
        """
        Extrae conteo de países desde publicaciones.
        
        Args:
            publications: Lista de publicaciones con campo 'authors'
        
        Returns:
            Diccionario {código_país: cantidad}
        """
        country_counts = Counter()
        
        for pub in publications:
            # Extraer primer autor
            authors = pub.get('authors', [])
            if not authors:
                continue
            
            first_author = authors[0] if isinstance(authors, list) else None
            if not first_author:
                continue
            
            # Obtener afiliación
            affiliation = None
            if isinstance(first_author, dict):
                affiliation = first_author.get('affiliation')
            elif isinstance(first_author, str):
                # Si es string, asumir que contiene la afiliación
                affiliation = first_author
            
            # Extraer país
            if affiliation:
                country = self.extract_country(affiliation)
                if country:
                    country_counts[country] += 1
        
        return dict(country_counts)
    
    def generate_choropleth(
        self,
        country_counts: Dict[str, int],
        title: Optional[str] = None
    ) -> str:
        """
        Genera mapa coroplético (mapa de calor mundial).
        
        Args:
            country_counts: Diccionario {código_país: cantidad}
            title: Título del mapa
        
        Returns:
            HTML interactivo del mapa en formato string
        """
        if not country_counts:
            raise ValueError("No hay datos de países para generar el mapa")
        
        # Preparar datos
        countries = list(country_counts.keys())
        values = list(country_counts.values())
        
        # Crear mapa
        fig = go.Figure(data=go.Choropleth(
            locations=countries,
            z=values,
            text=[f"{country}: {count}" for country, count in country_counts.items()],
            colorscale=self.colorscale,
            autocolorscale=False,
            reversescale=False,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title="Publicaciones",
            colorbar=dict(
                title="Número de<br>Publicaciones",
                thickness=15,
                len=0.7,
                x=1.0,
                xanchor='left'
            )
        ))
        
        # Configurar layout
        fig.update_layout(
            title_text=title or 'Distribución Geográfica de Publicaciones',
            title_x=0.5,
            title_font_size=18,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='natural earth'
            ),
            height=600,
            width=1200
        )
        
        # Convertir a HTML
        html_string = fig.to_html(include_plotlyjs='cdn')
        
        return html_string
    
    def generate_bar_chart(
        self,
        country_counts: Dict[str, int],
        top_n: int = 15,
        title: Optional[str] = None
    ) -> str:
        """
        Genera gráfico de barras con los países principales.
        
        Args:
            country_counts: Diccionario {código_país: cantidad}
            top_n: Número de países principales a mostrar
            title: Título del gráfico
        
        Returns:
            HTML interactivo del gráfico en formato string
        """
        if not country_counts:
            raise ValueError("No hay datos de países para generar el gráfico")
        
        # Ordenar y tomar top N
        sorted_countries = sorted(
            country_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]
        
        countries = [item[0] for item in sorted_countries]
        values = [item[1] for item in sorted_countries]
        
        # Crear gráfico de barras
        fig = go.Figure(data=[
            go.Bar(
                x=values,
                y=countries,
                orientation='h',
                marker=dict(
                    color=values,
                    colorscale=self.colorscale,
                    showscale=True,
                    colorbar=dict(title="Publicaciones")
                ),
                text=values,
                textposition='auto'
            )
        ])
        
        # Configurar layout
        fig.update_layout(
            title_text=title or f'Top {top_n} Países por Número de Publicaciones',
            title_x=0.5,
            title_font_size=16,
            xaxis_title='Número de Publicaciones',
            yaxis_title='País',
            height=500,
            width=1000,
            showlegend=False
        )
        
        # Invertir orden del eje Y para que el mayor esté arriba
        fig.update_yaxes(autorange="reversed")
        
        # Convertir a HTML
        html_string = fig.to_html(include_plotlyjs='cdn')
        
        return html_string
    
    def generate_from_publications(
        self,
        publications: List[Dict],
        map_type: str = 'choropleth',
        title: Optional[str] = None,
        top_n: int = 15
    ) -> Dict[str, any]:
        """
        Genera visualización geográfica desde publicaciones.
        
        Args:
            publications: Lista de publicaciones
            map_type: Tipo de visualización ('choropleth' o 'bar')
            title: Título opcional
            top_n: Para gráfico de barras, número de países a mostrar
        
        Returns:
            Diccionario con:
                - html: HTML interactivo
                - country_distribution: Distribución por país
                - num_publications: Total de publicaciones
                - num_countries: Número de países únicos
        """
        # Extraer países
        country_counts = self.extract_countries_from_publications(publications)
        
        if not country_counts:
            raise ValueError("No se pudo extraer información geográfica")
        
        # Generar visualización según tipo
        if map_type == 'choropleth':
            html = self.generate_choropleth(country_counts, title=title)
        elif map_type == 'bar':
            html = self.generate_bar_chart(country_counts, top_n=top_n, title=title)
        else:
            raise ValueError(f"Tipo de mapa no válido: {map_type}")
        
        # Preparar distribución
        distribution = [
            {'country': country, 'count': count}
            for country, count in sorted(
                country_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )
        ]
        
        return {
            'html': html,
            'country_distribution': distribution,
            'num_publications': len(publications),
            'num_countries': len(country_counts)
        }
