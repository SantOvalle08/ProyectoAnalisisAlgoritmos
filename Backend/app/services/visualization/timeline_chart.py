"""
Generador de Líneas Temporales
===============================

Crea visualizaciones de líneas temporales mostrando la evolución de
publicaciones científicas a lo largo del tiempo.

Características:
- Agrupación por año
- Agrupación por revista
- Gráficos interactivos con plotly
- Múltiples series de datos
- Tooltips informativos

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña
Date: Octubre 2025
"""

from typing import List, Dict, Optional, Tuple
from collections import defaultdict, Counter
from datetime import datetime

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class TimelineChart:
    """
    Generador de gráficos de línea temporal para análisis bibliométrico.
    
    Procesa información temporal de publicaciones para crear visualizaciones
    de tendencias y distribuciones a lo largo del tiempo.
    """
    
    def __init__(self, colorscale: str = 'Set2'):
        """
        Inicializa el generador de líneas temporales.
        
        Args:
            colorscale: Escala de colores de plotly
        """
        self.colorscale = colorscale
    
    def extract_year(self, publication: Dict) -> Optional[int]:
        """
        Extrae el año de publicación.
        
        Args:
            publication: Diccionario con información de la publicación
        
        Returns:
            Año como entero o None si no se encuentra
        """
        # Intentar campo 'year'
        if 'year' in publication and publication['year']:
            try:
                return int(publication['year'])
            except (ValueError, TypeError):
                pass
        
        # Intentar campo 'published_date'
        if 'published_date' in publication and publication['published_date']:
            try:
                date_str = publication['published_date']
                # Intentar parsear fecha
                if isinstance(date_str, str):
                    # Formato ISO
                    if '-' in date_str:
                        year = int(date_str.split('-')[0])
                        return year
                    # Solo año
                    elif len(date_str) == 4:
                        return int(date_str)
            except (ValueError, TypeError, IndexError):
                pass
        
        # Intentar campo 'publication_date'
        if 'publication_date' in publication and publication['publication_date']:
            try:
                date_str = publication['publication_date']
                if isinstance(date_str, str) and '-' in date_str:
                    year = int(date_str.split('-')[0])
                    return year
            except (ValueError, TypeError, IndexError):
                pass
        
        return None
    
    def extract_journal(self, publication: Dict) -> Optional[str]:
        """
        Extrae el nombre de la revista/conferencia.
        
        Args:
            publication: Diccionario con información de la publicación
        
        Returns:
            Nombre de la revista o None
        """
        # Intentar varios campos posibles
        for field in ['journal', 'venue', 'container_title', 'publication_venue']:
            if field in publication and publication[field]:
                return str(publication[field])
        
        return 'Unknown'
    
    def aggregate_by_year(
        self,
        publications: List[Dict]
    ) -> Dict[int, int]:
        """
        Agrupa publicaciones por año.
        
        Args:
            publications: Lista de publicaciones
        
        Returns:
            Diccionario {año: cantidad}
        """
        year_counts = Counter()
        
        for pub in publications:
            year = self.extract_year(pub)
            if year and 1900 <= year <= datetime.now().year + 1:
                year_counts[year] += 1
        
        return dict(sorted(year_counts.items()))
    
    def aggregate_by_year_and_journal(
        self,
        publications: List[Dict],
        top_n_journals: int = 10
    ) -> Tuple[Dict[int, Dict[str, int]], List[str]]:
        """
        Agrupa publicaciones por año y revista.
        
        Args:
            publications: Lista de publicaciones
            top_n_journals: Número de revistas principales a considerar
        
        Returns:
            Tupla (datos_agrupados, lista_revistas_principales)
            - datos_agrupados: {año: {revista: cantidad}}
            - lista_revistas_principales: Top N revistas
        """
        # Primero, contar publicaciones por revista
        journal_counts = Counter()
        for pub in publications:
            journal = self.extract_journal(pub)
            journal_counts[journal] += 1
        
        # Obtener top N revistas
        top_journals = [
            journal for journal, _ in journal_counts.most_common(top_n_journals)
        ]
        
        # Agrupar por año y revista
        year_journal_data = defaultdict(lambda: defaultdict(int))
        
        for pub in publications:
            year = self.extract_year(pub)
            journal = self.extract_journal(pub)
            
            if year and 1900 <= year <= datetime.now().year + 1:
                if journal in top_journals:
                    year_journal_data[year][journal] += 1
                else:
                    year_journal_data[year]['Others'] += 1
        
        # Incluir 'Others' en la lista de revistas si hay datos
        if any('Others' in journals for journals in year_journal_data.values()):
            if 'Others' not in top_journals:
                top_journals.append('Others')
        
        return dict(year_journal_data), top_journals
    
    def generate_timeline_simple(
        self,
        year_counts: Dict[int, int],
        title: Optional[str] = None
    ) -> str:
        """
        Genera línea temporal simple (total por año).
        
        Args:
            year_counts: Diccionario {año: cantidad}
            title: Título del gráfico
        
        Returns:
            HTML interactivo del gráfico
        """
        if not year_counts:
            raise ValueError("No hay datos para generar la línea temporal")
        
        years = list(year_counts.keys())
        counts = list(year_counts.values())
        
        # Crear gráfico de línea
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=years,
            y=counts,
            mode='lines+markers',
            name='Publicaciones',
            line=dict(color='rgb(49, 130, 189)', width=3),
            marker=dict(size=8, color='rgb(49, 130, 189)'),
            text=[f"Año {year}: {count} publicaciones" for year, count in zip(years, counts)],
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
        
        # Configurar layout
        fig.update_layout(
            title_text=title or 'Evolución Temporal de Publicaciones',
            title_x=0.5,
            title_font_size=18,
            xaxis_title='Año',
            yaxis_title='Número de Publicaciones',
            hovermode='x unified',
            height=500,
            width=1200,
            showlegend=True,
            template='plotly_white'
        )
        
        # Configurar ejes
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        
        # Convertir a HTML
        html_string = fig.to_html(include_plotlyjs='cdn')
        
        return html_string
    
    def generate_timeline_by_journal(
        self,
        year_journal_data: Dict[int, Dict[str, int]],
        journals: List[str],
        title: Optional[str] = None
    ) -> str:
        """
        Genera línea temporal con series por revista.
        
        Args:
            year_journal_data: {año: {revista: cantidad}}
            journals: Lista de revistas a graficar
            title: Título del gráfico
        
        Returns:
            HTML interactivo del gráfico
        """
        if not year_journal_data:
            raise ValueError("No hay datos para generar la línea temporal")
        
        # Obtener todos los años
        all_years = sorted(year_journal_data.keys())
        
        # Crear figura
        fig = go.Figure()
        
        # Color palette
        colors = px.colors.qualitative.Set2 + px.colors.qualitative.Pastel
        
        # Agregar traza para cada revista
        for idx, journal in enumerate(journals):
            # Obtener datos para esta revista
            counts = [year_journal_data[year].get(journal, 0) for year in all_years]
            
            # Solo agregar si tiene datos
            if sum(counts) > 0:
                fig.add_trace(go.Scatter(
                    x=all_years,
                    y=counts,
                    mode='lines+markers',
                    name=journal,
                    line=dict(width=2),
                    marker=dict(size=6),
                    hovertemplate=f'<b>{journal}</b><br>Año: %{{x}}<br>Publicaciones: %{{y}}<extra></extra>'
                ))
        
        # Configurar layout
        fig.update_layout(
            title_text=title or 'Evolución Temporal por Revista/Conferencia',
            title_x=0.5,
            title_font_size=18,
            xaxis_title='Año',
            yaxis_title='Número de Publicaciones',
            hovermode='x unified',
            height=600,
            width=1200,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1.0,
                xanchor="left",
                x=1.02
            ),
            template='plotly_white'
        )
        
        # Configurar ejes
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        
        # Convertir a HTML
        html_string = fig.to_html(include_plotlyjs='cdn')
        
        return html_string
    
    def generate_from_publications(
        self,
        publications: List[Dict],
        group_by_journal: bool = True,
        top_n_journals: int = 10,
        title: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Genera visualización temporal desde publicaciones.
        
        Args:
            publications: Lista de publicaciones
            group_by_journal: Si True, agrupa por revista; si False, solo por año
            top_n_journals: Número de revistas principales a mostrar
            title: Título opcional
        
        Returns:
            Diccionario con:
                - html: HTML interactivo
                - yearly_distribution: Distribución por año
                - num_publications: Total de publicaciones
                - year_range: Rango de años
        """
        if group_by_journal:
            # Agrupar por año y revista
            year_journal_data, top_journals = self.aggregate_by_year_and_journal(
                publications,
                top_n_journals=top_n_journals
            )
            
            html = self.generate_timeline_by_journal(
                year_journal_data,
                top_journals,
                title=title
            )
            
            # Calcular total por año
            yearly_totals = {
                year: sum(journals.values())
                for year, journals in year_journal_data.items()
            }
        else:
            # Solo por año
            yearly_totals = self.aggregate_by_year(publications)
            
            html = self.generate_timeline_simple(
                yearly_totals,
                title=title
            )
        
        # Preparar distribución
        distribution = [
            {'year': year, 'count': count}
            for year, count in sorted(yearly_totals.items())
        ]
        
        # Rango de años
        years = list(yearly_totals.keys())
        year_range = {
            'min': min(years) if years else None,
            'max': max(years) if years else None
        }
        
        return {
            'html': html,
            'yearly_distribution': distribution,
            'num_publications': len(publications),
            'year_range': year_range
        }
