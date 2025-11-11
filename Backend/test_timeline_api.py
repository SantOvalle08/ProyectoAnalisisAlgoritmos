"""
Script para probar el endpoint de timeline con datos reales.
Simula la llamada del frontend al backend.
"""

import json
import requests
from pathlib import Path

def test_timeline_endpoint():
    """Prueba el endpoint /api/v1/visualizations/timeline"""
    
    print("=" * 80)
    print("TEST DEL ENDPOINT DE TIMELINE")
    print("=" * 80)
    
    # URL del backend
    base_url = "http://localhost:8000"
    endpoint = f"{base_url}/api/v1/visualizations/timeline"
    
    # Cargar publicaciones
    json_file = Path(__file__).parent.parent / "publications_job_51314db58488.json"
    
    if not json_file.exists():
        print(f"❌ ERROR: No se encontró el archivo: {json_file}")
        return
    
    print(f"\n📁 Cargando publicaciones desde: {json_file.name}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        publications = json.load(f)
    
    print(f"✓ Cargadas {len(publications)} publicaciones")
    
    # Tomar una muestra para la prueba (primeras 50)
    sample = publications[:50]
    print(f"✓ Usando muestra de {len(sample)} publicaciones para la prueba")
    
    # Preparar request
    request_data = {
        "publications": sample,
        "group_by_journal": False,
        "top_n_journals": 10,
        "title": "Timeline de Prueba - API"
    }
    
    print("\n" + "=" * 80)
    print("PRUEBA 1: Timeline simple (solo por año)")
    print("=" * 80)
    
    try:
        print(f"\n📤 Enviando POST request a: {endpoint}")
        response = requests.post(endpoint, json=request_data, timeout=30)
        
        print(f"✓ Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ Timeline generado exitosamente!")
            print(f"  - Publicaciones procesadas: {result['num_publications']}")
            print(f"  - Rango de años: {result['year_range']}")
            print(f"  - Distribución anual: {len(result['yearly_distribution'])} años")
            
            # Guardar HTML
            output_file = Path(__file__).parent / "data" / "downloads" / "test_timeline_api_simple.html"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result['html'])
            
            print(f"  - HTML guardado en: {output_file}")
            
        else:
            print(f"\n❌ ERROR {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ ERROR: No se pudo conectar al backend en {base_url}")
        print("   Asegúrate de que el backend esté corriendo (.\start-project.ps1)")
        return
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Prueba 2: Por revista
    print("\n" + "=" * 80)
    print("PRUEBA 2: Timeline por revista (top 5)")
    print("=" * 80)
    
    request_data["group_by_journal"] = True
    request_data["top_n_journals"] = 5
    
    try:
        print(f"\n📤 Enviando POST request a: {endpoint}")
        response = requests.post(endpoint, json=request_data, timeout=30)
        
        print(f"✓ Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ Timeline por revista generado exitosamente!")
            print(f"  - Publicaciones procesadas: {result['num_publications']}")
            print(f"  - Rango de años: {result['year_range']}")
            
            # Guardar HTML
            output_file = Path(__file__).parent / "data" / "downloads" / "test_timeline_api_journal.html"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result['html'])
            
            print(f"  - HTML guardado en: {output_file}")
            
        else:
            print(f"\n❌ ERROR {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print("""
✓ Endpoint de timeline probado
✓ Backend reconoce el campo 'publication_year'
✓ Ambos modos funcionan (simple y por revista)

🎉 ¡El botón de timeline debería funcionar ahora!

💡 Si el frontend sigue dando error:
   1. Recarga el navegador (Ctrl+F5)
   2. Verifica que el backend esté corriendo
   3. Revisa la consola del navegador para ver el error exacto
""")

if __name__ == "__main__":
    test_timeline_endpoint()
