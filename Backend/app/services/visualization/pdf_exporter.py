"""
Exportador a PDF de Visualizaciones
====================================

Combina múltiples visualizaciones bibliométricas en un documento PDF
profesional y bien estructurado.

Características:
- Combinación de mapas, wordclouds y líneas temporales
- Layout profesional con ReportLab
- Imágenes en alta calidad
- Metadatos del documento
- Tabla de contenidos

Authors: Santiago Ovalle Cortés, Juan Sebastián Noreña  
Date: Octubre 2025
"""

import base64
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Optional
import tempfile
import os

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, 
    PageBreak, Table, TableStyle
)
from reportlab.pdfgen import canvas


class PDFExporter:
    """
    Exportador de visualizaciones bibliométricas a PDF.
    
    Combina mapas geográficos, nubes de palabras y líneas temporales
    en un documento PDF profesional.
    """
    
    def __init__(
        self,
        page_size=A4,
        margin: float = 0.75 * inch,
        title: str = "Análisis Bibliométrico",
        author: str = "Universidad del Quindío"
    ):
        """
        Inicializa el exportador PDF.
        
        Args:
            page_size: Tamaño de página (A4, letter, etc.)
            margin: Margen de página en puntos
            title: Título del documento
            author: Autor del documento
        """
        self.page_size = page_size
        self.margin = margin
        self.title = title
        self.author = author
        
        # Estilos
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Crea estilos personalizados para el documento."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
        
        # Caption
        self.styles.add(ParagraphStyle(
            name='Caption',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER,
            spaceAfter=12
        ))
    
    def _decode_base64_image(self, base64_string: str) -> BytesIO:
        """
        Decodifica imagen base64 a BytesIO.
        
        Args:
            base64_string: String base64 de la imagen
        
        Returns:
            BytesIO con datos de la imagen
        """
        image_data = base64.b64decode(base64_string)
        return BytesIO(image_data)
    
    def _add_cover_page(self, story: List, metadata: Dict):
        """
        Agrega página de portada.
        
        Args:
            story: Lista de elementos del documento
            metadata: Metadatos del análisis
        """
        # Espaciador inicial
        story.append(Spacer(1, 2 * inch))
        
        # Título principal
        title = Paragraph(self.title, self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.3 * inch))
        
        # Subtítulo
        subtitle = Paragraph(
            "Informe de Análisis de Producción Científica",
            self.styles['CustomHeading']
        )
        story.append(subtitle)
        story.append(Spacer(1, 0.5 * inch))
        
        # Información del análisis
        info_data = [
            ["Número de publicaciones:", str(metadata.get('num_publications', 'N/A'))],
            ["Rango temporal:", f"{metadata.get('year_min', 'N/A')} - {metadata.get('year_max', 'N/A')}"],
            ["Países analizados:", str(metadata.get('num_countries', 'N/A'))],
            ["Fecha de generación:", datetime.now().strftime("%d/%m/%Y %H:%M")]
        ]
        
        info_table = Table(info_data, colWidths=[3*inch, 2*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.5 * inch))
        
        # Autor
        author_text = Paragraph(
            f"<b>Generado por:</b> {self.author}",
            self.styles['CustomBody']
        )
        story.append(author_text)
        
        # Nueva página
        story.append(PageBreak())
    
    def _add_visualization(
        self,
        story: List,
        title: str,
        image_base64: str,
        description: str,
        width: float = 6 * inch,
        height: float = 4 * inch
    ):
        """
        Agrega una visualización al documento.
        
        Args:
            story: Lista de elementos del documento
            title: Título de la visualización
            image_base64: Imagen en base64
            description: Descripción textual
            width: Ancho de la imagen
            height: Alto de la imagen
        """
        # Título de la visualización
        viz_title = Paragraph(title, self.styles['CustomHeading'])
        story.append(viz_title)
        story.append(Spacer(1, 0.2 * inch))
        
        # Imagen
        try:
            image_buffer = self._decode_base64_image(image_base64)
            img = Image(image_buffer, width=width, height=height)
            story.append(img)
            story.append(Spacer(1, 0.1 * inch))
        except Exception as e:
            error_text = Paragraph(
                f"<i>Error cargando imagen: {str(e)}</i>",
                self.styles['Caption']
            )
            story.append(error_text)
        
        # Descripción
        if description:
            desc_paragraph = Paragraph(description, self.styles['CustomBody'])
            story.append(desc_paragraph)
        
        story.append(Spacer(1, 0.3 * inch))
    
    def generate_pdf(
        self,
        wordcloud_data: Optional[Dict] = None,
        heatmap_data: Optional[Dict] = None,
        timeline_data: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
        output_path: Optional[str] = None
    ) -> bytes:
        """
        Genera documento PDF con visualizaciones.
        
        Args:
            wordcloud_data: Datos de nube de palabras
            heatmap_data: Datos de mapa de calor (NO SOPORTADO - requiere conversión HTML a imagen)
            timeline_data: Datos de línea temporal (NO SOPORTADO - requiere conversión HTML a imagen)
            metadata: Metadatos del análisis
            output_path: Ruta de salida (opcional)
        
        Returns:
            Bytes del PDF generado
        """
        # Buffer para PDF
        if output_path:
            pdf_buffer = output_path
        else:
            pdf_buffer = BytesIO()
        
        # Crear documento
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=self.page_size,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin,
            title=self.title,
            author=self.author
        )
        
        # Story (contenido)
        story = []
        
        # Metadatos por defecto
        if metadata is None:
            metadata = {}
        
        # Portada
        self._add_cover_page(story, metadata)
        
        # Nube de palabras
        if wordcloud_data and 'image_base64' in wordcloud_data:
            self._add_visualization(
                story=story,
                title="1. Nube de Palabras",
                image_base64=wordcloud_data['image_base64'],
                description=f"Términos más frecuentes extraídos de {wordcloud_data.get('num_publications', 'N/A')} publicaciones. "
                           f"Total de términos únicos: {wordcloud_data.get('total_terms', 'N/A')}.",
                width=6.5 * inch,
                height=3.5 * inch
            )
            
            # Top términos
            if 'top_terms' in wordcloud_data:
                story.append(Paragraph("Términos Principales:", self.styles['CustomHeading']))
                
                top_terms = wordcloud_data['top_terms'][:10]
                terms_text = ", ".join([
                    f"<b>{term['term']}</b> ({term['weight']:.2f})"
                    for term in top_terms
                ])
                
                terms_paragraph = Paragraph(terms_text, self.styles['CustomBody'])
                story.append(terms_paragraph)
                story.append(Spacer(1, 0.3 * inch))
            
            story.append(PageBreak())
        
        # Nota sobre mapa de calor y timeline
        # (Requieren conversión de HTML interactivo a imagen estática)
        if heatmap_data or timeline_data:
            note = Paragraph(
                "<b>Nota:</b> Los mapas de calor geográficos y líneas temporales se generan como "
                "visualizaciones interactivas HTML. Para incluirlos en el PDF, se requiere conversión "
                "a imagen estática mediante herramientas adicionales (selenium, playwright, etc.).",
                self.styles['CustomBody']
            )
            story.append(note)
        
        # Generar PDF
        doc.build(story)
        
        # Retornar bytes
        if isinstance(pdf_buffer, BytesIO):
            pdf_bytes = pdf_buffer.getvalue()
            pdf_buffer.close()
            return pdf_bytes
        else:
            # Si es ruta de archivo, leer y retornar bytes
            with open(pdf_buffer, 'rb') as f:
                return f.read()
    
    def export_visualizations(
        self,
        visualizations: Dict[str, Dict],
        metadata: Optional[Dict] = None
    ) -> bytes:
        """
        Exporta múltiples visualizaciones a PDF.
        
        Args:
            visualizations: Diccionario con visualizaciones:
                - 'wordcloud': Datos de nube de palabras
                - 'heatmap': Datos de mapa de calor
                - 'timeline': Datos de línea temporal
            metadata: Metadatos del análisis
        
        Returns:
            Bytes del PDF generado
        """
        return self.generate_pdf(
            wordcloud_data=visualizations.get('wordcloud'),
            heatmap_data=visualizations.get('heatmap'),
            timeline_data=visualizations.get('timeline'),
            metadata=metadata
        )
