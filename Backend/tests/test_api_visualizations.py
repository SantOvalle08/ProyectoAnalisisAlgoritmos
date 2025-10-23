"""
Tests de API para endpoints de visualización.
Prueba todos los endpoints del módulo de visualizaciones.
"""

import requests
import json
import base64
from pathlib import Path

# URL base del servidor
BASE_URL = "http://localhost:8000/api/v1/visualizations"

# Datos de prueba
SAMPLE_PUBLICATIONS = [
    {
        "title": "Machine Learning Applications in Healthcare",
        "abstract": "This paper explores machine learning algorithms for medical diagnosis. Deep learning models show promising results in image classification and patient outcome prediction. Neural networks are applied to medical imaging data.",
        "keywords": ["machine learning", "healthcare", "deep learning", "diagnosis", "neural networks"],
        "authors": [
            {"name": "John Smith", "affiliation": "Stanford University, USA"},
            {"name": "Jane Doe", "affiliation": "MIT, Cambridge, USA"}
        ],
        "year": "2023",
        "journal": "Journal of Medical AI"
    },
    {
        "title": "Natural Language Processing for Scientific Text Mining",
        "abstract": "We present a comprehensive study of NLP techniques for extracting knowledge from scientific publications. Text mining and information extraction are key components. We use transformer models for semantic analysis.",
        "keywords": ["NLP", "text mining", "information extraction", "scientific publications", "transformers"],
        "authors": [
            {"name": "Carlos García", "affiliation": "Universidad Nacional de Colombia, Bogotá"},
            {"name": "María López", "affiliation": "Universidad de los Andes, Colombia"}
        ],
        "year": "2022",
        "journal": "Computational Linguistics"
    },
    {
        "title": "Advances in Computer Vision",
        "abstract": "Recent advances in convolutional neural networks have revolutionized computer vision. Object detection and image segmentation achieve state-of-the-art performance. Deep learning methods outperform traditional approaches.",
        "keywords": ["computer vision", "CNN", "object detection", "image segmentation", "deep learning"],
        "authors": [
            {"name": "Wei Zhang", "affiliation": "Tsinghua University, Beijing, China"},
            {"name": "Li Wang", "affiliation": "Peking University, China"}
        ],
        "year": "2023",
        "journal": "IEEE Transactions on Pattern Analysis"
    },
    {
        "title": "Reinforcement Learning in Robotics",
        "abstract": "This work investigates reinforcement learning approaches for robotic control. Model-free methods demonstrate superior performance in complex navigation tasks. Deep Q-learning is applied to autonomous systems.",
        "keywords": ["reinforcement learning", "robotics", "control", "navigation", "Q-learning"],
        "authors": [
            {"name": "Hans Mueller", "affiliation": "Technical University of Munich, Germany"},
            {"name": "Anna Schmidt", "affiliation": "University of Heidelberg, Germany"}
        ],
        "year": "2022",
        "journal": "Robotics and Autonomous Systems"
    },
    {
        "title": "Blockchain Technology for Secure Data Sharing",
        "abstract": "We propose a blockchain-based framework for secure and transparent data sharing in healthcare. Smart contracts enable automated data access control. Distributed ledger technology ensures data integrity.",
        "keywords": ["blockchain", "data sharing", "security", "smart contracts", "distributed systems"],
        "authors": [
            {"name": "Sophie Martin", "affiliation": "University of Oxford, United Kingdom"},
            {"name": "James Wilson", "affiliation": "Imperial College London, UK"}
        ],
        "year": "2023",
        "journal": "Journal of Cybersecurity"
    },
    {
        "title": "Quantum Computing for Optimization Problems",
        "abstract": "Quantum algorithms offer exponential speedup for certain optimization problems. We evaluate quantum annealing on logistics and scheduling tasks. Quantum computing shows promise for NP-hard problems.",
        "keywords": ["quantum computing", "optimization", "quantum algorithms", "logistics", "NP-hard"],
        "authors": [
            {"name": "Pierre Dubois", "affiliation": "École Polytechnique, Paris, France"},
            {"name": "Marie Lefevre", "affiliation": "Sorbonne University, France"}
        ],
        "year": "2021",
        "journal": "Quantum Information Processing"
    },
    {
        "title": "Federated Learning for Privacy-Preserving AI",
        "abstract": "Federated learning enables collaborative model training without sharing raw data. Privacy-preserving machine learning techniques protect sensitive information. Distributed training improves model generalization.",
        "keywords": ["federated learning", "privacy", "machine learning", "distributed training", "security"],
        "authors": [
            {"name": "Emma Brown", "affiliation": "Google Research, USA"},
            {"name": "David Lee", "affiliation": "Stanford University, USA"}
        ],
        "year": "2023",
        "journal": "Journal of Privacy and Security"
    },
    {
        "title": "Graph Neural Networks for Social Network Analysis",
        "abstract": "Graph neural networks provide powerful tools for analyzing social networks. Node classification and link prediction tasks benefit from graph-based deep learning. Network embedding techniques capture structural information.",
        "keywords": ["graph neural networks", "social networks", "node classification", "link prediction", "embeddings"],
        "authors": [
            {"name": "Yuki Tanaka", "affiliation": "University of Tokyo, Japan"},
            {"name": "Hiroshi Sato", "affiliation": "Kyoto University, Japan"}
        ],
        "year": "2022",
        "journal": "Social Network Analysis and Mining"
    }
]


def test_health_check():
    """Prueba endpoint de health check."""
    print("\n" + "="*80)
    print("TEST 1: Health Check")
    print("="*80)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Verificaciones
            assert data["status"] == "healthy", "Estado debe ser 'healthy'"
            assert "wordcloud" in data["modules"], "Debe incluir módulo wordcloud"
            assert "heatmap" in data["modules"], "Debe incluir módulo heatmap"
            assert "timeline" in data["modules"], "Debe incluir módulo timeline"
            assert "pdf_export" in data["modules"], "Debe incluir módulo pdf_export"
            
            print("✓ Health check pasado correctamente")
            return True
        else:
            print(f"✗ Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error en health check: {e}")
        return False


def test_wordcloud_generation():
    """Prueba generación de word cloud."""
    print("\n" + "="*80)
    print("TEST 2: Word Cloud Generation")
    print("="*80)
    
    try:
        payload = {
            "publications": SAMPLE_PUBLICATIONS,
            "max_words": 30,
            "use_tfidf": True,
            "include_keywords": True
        }
        
        print(f"Enviando {len(SAMPLE_PUBLICATIONS)} publicaciones...")
        response = requests.post(f"{BASE_URL}/wordcloud", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificaciones
            assert "image_base64" in data, "Debe incluir imagen en base64"
            assert "top_terms" in data, "Debe incluir términos principales"
            assert "num_publications" in data, "Debe incluir número de publicaciones"
            assert "total_terms" in data, "Debe incluir total de términos"
            
            print(f"\nEstadísticas:")
            print(f"  - Total publicaciones: {data['num_publications']}")
            print(f"  - Total términos: {data['total_terms']}")
            
            print(f"\nTop 10 términos:")
            for i, term_obj in enumerate(data['top_terms'][:10], 1):
                print(f"  {i}. {term_obj['term']}: {term_obj['weight']:.4f}")
            
            # Verificar que la imagen base64 es válida
            image_len = len(data['image_base64'])
            print(f"\nTamaño imagen base64: {image_len} caracteres")
            assert image_len > 1000, "Imagen debe tener contenido significativo"
            
            # Guardar imagen para inspección visual (opcional)
            try:
                image_data = base64.b64decode(data['image_base64'])
                output_path = Path("test_wordcloud.png")
                output_path.write_bytes(image_data)
                print(f"✓ Imagen guardada en: {output_path.absolute()}")
            except Exception as e:
                print(f"⚠ No se pudo guardar imagen: {e}")
            
            print("✓ Word cloud generado correctamente")
            return True
        else:
            print(f"✗ Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error en word cloud: {e}")
        return False


def test_heatmap_choropleth():
    """Prueba generación de mapa coroplético."""
    print("\n" + "="*80)
    print("TEST 3: Geographic Heatmap - Choropleth")
    print("="*80)
    
    try:
        payload = {
            "publications": SAMPLE_PUBLICATIONS,
            "map_type": "choropleth",
            "title": "Distribución Geográfica de Publicaciones - Test"
        }
        
        print(f"Enviando {len(SAMPLE_PUBLICATIONS)} publicaciones...")
        response = requests.post(f"{BASE_URL}/heatmap", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            html_content = response.text
            
            # Verificaciones
            assert "plotly" in html_content.lower(), "HTML debe contener plotly"
            assert len(html_content) > 1000, "HTML debe tener contenido significativo"
            
            # Guardar HTML para inspección visual
            output_path = Path("test_heatmap_choropleth.html")
            output_path.write_text(html_content, encoding='utf-8')
            print(f"✓ Mapa coroplético guardado en: {output_path.absolute()}")
            print(f"  Tamaño HTML: {len(html_content)} caracteres")
            
            print("✓ Mapa coroplético generado correctamente")
            return True
        else:
            print(f"✗ Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error en mapa coroplético: {e}")
        return False


def test_heatmap_bar():
    """Prueba generación de gráfico de barras."""
    print("\n" + "="*80)
    print("TEST 4: Geographic Heatmap - Bar Chart")
    print("="*80)
    
    try:
        payload = {
            "publications": SAMPLE_PUBLICATIONS,
            "map_type": "bar",
            "title": "Top Países por Publicaciones - Test",
            "top_n": 5
        }
        
        print(f"Enviando {len(SAMPLE_PUBLICATIONS)} publicaciones...")
        response = requests.post(f"{BASE_URL}/heatmap", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            html_content = response.text
            
            # Verificaciones
            assert "plotly" in html_content.lower(), "HTML debe contener plotly"
            assert len(html_content) > 1000, "HTML debe tener contenido significativo"
            
            # Guardar HTML para inspección visual
            output_path = Path("test_heatmap_bar.html")
            output_path.write_text(html_content, encoding='utf-8')
            print(f"✓ Gráfico de barras guardado en: {output_path.absolute()}")
            print(f"  Tamaño HTML: {len(html_content)} caracteres")
            
            print("✓ Gráfico de barras generado correctamente")
            return True
        else:
            print(f"✗ Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error en gráfico de barras: {e}")
        return False


def test_timeline_simple():
    """Prueba generación de línea temporal simple."""
    print("\n" + "="*80)
    print("TEST 5: Timeline Chart - Simple")
    print("="*80)
    
    try:
        payload = {
            "publications": SAMPLE_PUBLICATIONS,
            "group_by_journal": False,
            "title": "Evolución Temporal de Publicaciones - Test"
        }
        
        print(f"Enviando {len(SAMPLE_PUBLICATIONS)} publicaciones...")
        response = requests.post(f"{BASE_URL}/timeline", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            html_content = response.text
            
            # Verificaciones
            assert "plotly" in html_content.lower(), "HTML debe contener plotly"
            assert len(html_content) > 1000, "HTML debe tener contenido significativo"
            
            # Guardar HTML para inspección visual
            output_path = Path("test_timeline_simple.html")
            output_path.write_text(html_content, encoding='utf-8')
            print(f"✓ Timeline simple guardado en: {output_path.absolute()}")
            print(f"  Tamaño HTML: {len(html_content)} caracteres")
            
            print("✓ Timeline simple generado correctamente")
            return True
        else:
            print(f"✗ Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error en timeline simple: {e}")
        return False


def test_timeline_by_journal():
    """Prueba generación de línea temporal por revista."""
    print("\n" + "="*80)
    print("TEST 6: Timeline Chart - By Journal")
    print("="*80)
    
    try:
        payload = {
            "publications": SAMPLE_PUBLICATIONS,
            "group_by_journal": True,
            "top_n_journals": 5,
            "title": "Evolución por Revista - Test"
        }
        
        print(f"Enviando {len(SAMPLE_PUBLICATIONS)} publicaciones...")
        response = requests.post(f"{BASE_URL}/timeline", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            html_content = response.text
            
            # Verificaciones
            assert "plotly" in html_content.lower(), "HTML debe contener plotly"
            assert len(html_content) > 1000, "HTML debe tener contenido significativo"
            
            # Guardar HTML para inspección visual
            output_path = Path("test_timeline_journal.html")
            output_path.write_text(html_content, encoding='utf-8')
            print(f"✓ Timeline por revista guardado en: {output_path.absolute()}")
            print(f"  Tamaño HTML: {len(html_content)} caracteres")
            
            print("✓ Timeline por revista generado correctamente")
            return True
        else:
            print(f"✗ Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error en timeline por revista: {e}")
        return False


def test_pdf_export():
    """Prueba exportación a PDF."""
    print("\n" + "="*80)
    print("TEST 7: PDF Export")
    print("="*80)
    
    try:
        payload = {
            "publications": SAMPLE_PUBLICATIONS,
            "include_wordcloud": True,
            "include_heatmap": False,  # No soportado aún
            "include_timeline": False,  # No soportado aún
            "title": "Reporte de Análisis Científico - Test"
        }
        
        print(f"Enviando {len(SAMPLE_PUBLICATIONS)} publicaciones...")
        print("⚠ Nota: Solo WordCloud soportado actualmente en PDF")
        response = requests.post(f"{BASE_URL}/export-pdf", json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Verificar que es un PDF
            assert response.headers.get('content-type') == 'application/pdf', "Content-type debe ser application/pdf"
            
            pdf_content = response.content
            assert pdf_content.startswith(b'%PDF'), "Debe ser un PDF válido"
            
            # Guardar PDF
            output_path = Path("test_export.pdf")
            output_path.write_bytes(pdf_content)
            print(f"✓ PDF guardado en: {output_path.absolute()}")
            print(f"  Tamaño PDF: {len(pdf_content)} bytes")
            
            print("✓ PDF exportado correctamente")
            return True
        else:
            print(f"✗ Error: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error en exportación PDF: {e}")
        return False


def run_all_tests():
    """Ejecuta todas las pruebas."""
    print("\n" + "="*80)
    print("INICIANDO PRUEBAS DE API DE VISUALIZACIONES")
    print("="*80)
    print(f"URL Base: {BASE_URL}")
    print(f"Total publicaciones de prueba: {len(SAMPLE_PUBLICATIONS)}")
    
    results = {
        "Health Check": test_health_check(),
        "Word Cloud": test_wordcloud_generation(),
        "Heatmap Choropleth": test_heatmap_choropleth(),
        "Heatmap Bar": test_heatmap_bar(),
        "Timeline Simple": test_timeline_simple(),
        "Timeline by Journal": test_timeline_by_journal(),
        "PDF Export": test_pdf_export()
    }
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE PRUEBAS")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASÓ" if result else "✗ FALLÓ"
        print(f"{test_name:25s} {status}")
    
    print(f"\n{passed}/{total} pruebas pasadas ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        return True
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron")
        return False


if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nPruebas interrumpidas por el usuario")
        exit(1)
    except Exception as e:
        print(f"\n\nError fatal: {e}")
        exit(1)
